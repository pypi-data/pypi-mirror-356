import os 
import re 
import warnings 
from typing import Optional 

import torch 
from ftfy import fix_text 
from loguru import logger 

from transformers import AutoConfig ,AutoModel ,AutoModelForCausalLM ,AutoTokenizer ,PretrainedConfig ,PreTrainedModel 
from transformers import VisionEncoderDecoderConfig ,VisionEncoderDecoderModel 
from transformers .models .vision_encoder_decoder .modeling_vision_encoder_decoder import logger as base_model_logger 

from .unimer_swin import UnimerSwinConfig ,UnimerSwinModel ,UnimerSwinImageProcessor 
from .unimer_mbart import UnimerMBartConfig ,UnimerMBartForCausalLM 

AutoConfig .register (UnimerSwinConfig .model_type ,UnimerSwinConfig )
AutoConfig .register (UnimerMBartConfig .model_type ,UnimerMBartConfig )
AutoModel .register (UnimerSwinConfig ,UnimerSwinModel )
AutoModelForCausalLM .register (UnimerMBartConfig ,UnimerMBartForCausalLM )


# TODO: rewrite tokenizer
class TokenizerWrapper :
    def __init__ (self ,tokenizer ):
        self .tokenizer =tokenizer 
        self .pad_token_id =self .tokenizer .pad_token_id 
        self .bos_token_id =self .tokenizer .bos_token_id 
        self .eos_token_id =self .tokenizer .eos_token_id 

    def __len__ (self ):
        return len (self .tokenizer )

    def tokenize (self ,text ,**kwargs ):
        return self .tokenizer (
        text ,
        return_token_type_ids =False ,
        return_tensors ="pt",
        padding ="longest",
        truncation =True ,
        **kwargs ,
        )

    def token2str (self ,tokens )->list :
        generated_text =self .tokenizer .batch_decode (tokens ,skip_special_tokens =True )
        generated_text =[fix_text (text )for text in generated_text ]
        return generated_text 

    def detokenize (self ,tokens ):
        toks =[self .tokenizer .convert_ids_to_tokens (tok )for tok in tokens ]
        for b in range (len (toks )):
            for i in reversed (range (len (toks [b ]))):
                if toks [b ][i ]is None :
                    toks [b ][i ]=''
                toks [b ][i ]=toks [b ][i ].replace ('Ġ',' ').strip ()
                if toks [b ][i ]in ([self .tokenizer .bos_token ,self .tokenizer .eos_token ,self .tokenizer .pad_token ]):
                    del toks [b ][i ]
        return toks 


LEFT_PATTERN =re .compile (r'(\\left)(\S*)')
RIGHT_PATTERN =re .compile (r'(\\right)(\S*)')
LEFT_COUNT_PATTERN =re .compile (r'\\left(?![a-zA-Z])')
RIGHT_COUNT_PATTERN =re .compile (r'\\right(?![a-zA-Z])')
LEFT_RIGHT_REMOVE_PATTERN =re .compile (r'\\left\.?|\\right\.?')

def fix_latex_left_right (s ):


    valid_delims_list =[r'(',r')',r'[',r']',r'{',r'}',r'/',r'|',
    r'\{',r'\}',r'\lceil',r'\rceil',r'\lfloor',
    r'\rfloor',r'\backslash',r'\uparrow',r'\downarrow',
    r'\Uparrow',r'\Downarrow',r'\|',r'\.']


    def fix_delim (match ,is_left =True ):
        cmd =match .group (1 )
        rest =match .group (2 )if len (match .groups ())>1 else ""
        if not rest or rest not in valid_delims_list :
            return cmd +"."
        return match .group (0 )




    s =LEFT_PATTERN .sub (lambda m :fix_delim (m ,True ),s )
    s =RIGHT_PATTERN .sub (lambda m :fix_delim (m ,False ),s )


    left_count =len (LEFT_COUNT_PATTERN .findall (s ))
    right_count =len (RIGHT_COUNT_PATTERN .findall (s ))

    if left_count ==right_count :

        return fix_left_right_pairs (s )
    else :

    # logger.debug(f"latex:{s}")
    # logger.warning(f"left_count: {left_count}, right_count: {right_count}")
        return LEFT_RIGHT_REMOVE_PATTERN .sub ('',s )


def fix_left_right_pairs (latex_formula ):


    brace_stack =[]

    left_stack =[]

    adjustments =[]

    i =0 
    while i <len (latex_formula ):

        if i >0 and latex_formula [i -1 ]=='\\':
            backslash_count =0 
            j =i -1 
            while j >=0 and latex_formula [j ]=='\\':
                backslash_count +=1 
                j -=1 

            if backslash_count %2 ==1 :
                i +=1 
                continue 


        if i +5 <len (latex_formula )and latex_formula [i :i +5 ]=="\\left"and i +5 <len (latex_formula ):
            delimiter =latex_formula [i +5 ]
            left_stack .append ((i ,len (brace_stack ),delimiter ))
            i +=6 
            continue 


        elif i +6 <len (latex_formula )and latex_formula [i :i +6 ]=="\\right"and i +6 <len (latex_formula ):
            delimiter =latex_formula [i +6 ]

            if left_stack :
                left_pos ,left_depth ,left_delim =left_stack .pop ()


                if left_depth !=len (brace_stack ):

                    target_pos =find_group_end (latex_formula ,left_pos ,left_depth )
                    if target_pos !=-1 :

                        adjustments .append ((i ,i +7 ,target_pos ))

            i +=7 
            continue 


        if latex_formula [i ]=='{':
            brace_stack .append (i )
        elif latex_formula [i ]=='}':
            if brace_stack :
                brace_stack .pop ()

        i +=1 


    if not adjustments :
        return latex_formula 

    result =list (latex_formula )
    adjustments .sort (reverse =True ,key =lambda x :x [0 ])

    for start ,end ,target in adjustments :

        right_part =result [start :end ]

        del result [start :end ]

        result .insert (target ,''.join (right_part ))

    return ''.join (result )


def find_group_end (text ,pos ,depth ):

    current_depth =depth 
    i =pos 

    while i <len (text ):
        if text [i ]=='{'and (i ==0 or not is_escaped (text ,i )):
            current_depth +=1 
        elif text [i ]=='}'and (i ==0 or not is_escaped (text ,i )):
            current_depth -=1 
            if current_depth <depth :
                return i 
        i +=1 

    return -1 


def is_escaped (text ,pos ):

    backslash_count =0 
    j =pos -1 
    while j >=0 and text [j ]=='\\':
        backslash_count +=1 
        j -=1 

    return backslash_count %2 ==1 


def fix_unbalanced_braces (latex_formula ):

    stack =[]
    unmatched =set ()
    i =0 

    while i <len (latex_formula ):

        if latex_formula [i ]in ['{','}']:

            backslash_count =0 
            j =i -1 
            while j >=0 and latex_formula [j ]=='\\':
                backslash_count +=1 
                j -=1 


            if backslash_count %2 ==1 :
                i +=1 
                continue 


            if latex_formula [i ]=='{':
                stack .append (i )
            else :# latex_formula[i] == '}'
                if stack :
                    stack .pop ()
                else :
                    unmatched .add (i )

        i +=1 


    unmatched .update (stack )


    return ''.join (char for i ,char in enumerate (latex_formula )if i not in unmatched )


def process_latex (input_string ):


    def replace_func (match ):

        next_char =match .group (1 )


        if next_char in "#$%&~_^|\\{} \t\n\r\v\f":
            return match .group (0 )


        if 'a'<=next_char <='z'or 'A'<=next_char <='Z':
            pos =match .start ()+2 
            if pos <len (input_string )and ('a'<=input_string [pos ]<='z'or 'A'<=input_string [pos ]<='Z'):

                return match .group (0 )


        return '\\'+' '+next_char 


    pattern =r'\\(.)'

    return re .sub (pattern ,replace_func ,input_string )


ENV_TYPES =['array','matrix','pmatrix','bmatrix','vmatrix',
'Bmatrix','Vmatrix','cases','aligned','gathered']
ENV_BEGIN_PATTERNS ={env :re .compile (r'\\begin\{'+env +r'\}')for env in ENV_TYPES }
ENV_END_PATTERNS ={env :re .compile (r'\\end\{'+env +r'\}')for env in ENV_TYPES }
ENV_FORMAT_PATTERNS ={env :re .compile (r'\\begin\{'+env +r'\}\{([^}]*)\}')for env in ENV_TYPES }

def fix_latex_environments (s ):

    for env in ENV_TYPES :
        begin_count =len (ENV_BEGIN_PATTERNS [env ].findall (s ))
        end_count =len (ENV_END_PATTERNS [env ].findall (s ))

        if begin_count !=end_count :
            if end_count >begin_count :
                format_match =ENV_FORMAT_PATTERNS [env ].search (s )
                default_format ='{c}'if env =='array'else ''
                format_str ='{'+format_match .group (1 )+'}'if format_match else default_format 

                missing_count =end_count -begin_count 
                begin_command ='\\begin{'+env +'}'+format_str +' '
                s =begin_command *missing_count +s 
            else :
                missing_count =begin_count -end_count 
                s =s +(' \\end{'+env +'}')*missing_count 

    return s 


UP_PATTERN =re .compile (r'\\up([a-zA-Z]+)')
COMMANDS_TO_REMOVE_PATTERN =re .compile (
r'\\(?:lefteqn|boldmath|ensuremath|centering|textsubscript|sides|textsl|textcent|emph|protect|null)')
REPLACEMENTS_PATTERNS ={
re .compile (r'\\underbar'):r'\\underline',
re .compile (r'\\Bar'):r'\\hat',
re .compile (r'\\Hat'):r'\\hat',
re .compile (r'\\Tilde'):r'\\tilde',
re .compile (r'\\slash'):r'/',
re .compile (r'\\textperthousand'):r'‰',
re .compile (r'\\sun'):r'☉',
re .compile (r'\\textunderscore'):r'\\_',
re .compile (r'\\fint'):r'⨏',
re .compile (r'\\up '):r'\\ ',
re .compile (r'\\vline = '):r'\\models ',
re .compile (r'\\vDash '):r'\\models ',
re .compile (r'\\sq \\sqcup '):r'\\square ',
}
QQUAD_PATTERN =re .compile (r'\\qquad(?!\s)')

def latex_rm_whitespace (s :str ):
    """Remove unnecessary whitespace from LaTeX code."""
    s =fix_unbalanced_braces (s )
    s =fix_latex_left_right (s )
    s =fix_latex_environments (s )


    s =UP_PATTERN .sub (
    lambda m :m .group (0 )if m .group (1 )in ["arrow","downarrow","lus","silon"]else f"\\{m .group (1 )}",s 
    )
    s =COMMANDS_TO_REMOVE_PATTERN .sub ('',s )


    for pattern ,replacement in REPLACEMENTS_PATTERNS .items ():
        s =pattern .sub (replacement ,s )


    s =process_latex (s )


    s =QQUAD_PATTERN .sub (r'\\qquad ',s )

    return s 


class UnimernetModel (VisionEncoderDecoderModel ):
    def __init__ (
    self ,
    config :Optional [PretrainedConfig ]=None ,
    encoder :Optional [PreTrainedModel ]=None ,
    decoder :Optional [PreTrainedModel ]=None ,
    ):
    # VisionEncoderDecoderModel's checking log has bug, disable for temp.
        base_model_logger .disabled =True 
        try :
            super ().__init__ (config ,encoder ,decoder )
        finally :
            base_model_logger .disabled =False 

        if not config or not hasattr (config ,"_name_or_path"):
            raise RuntimeError ("config._name_or_path is required by UnimernetModel.")

        model_path =config ._name_or_path 
        self .transform =UnimerSwinImageProcessor ()
        self .tokenizer =TokenizerWrapper (AutoTokenizer .from_pretrained (model_path ))
        self ._post_check ()

    def _post_check (self ):
        tokenizer =self .tokenizer 

        if tokenizer .tokenizer .model_max_length !=self .config .decoder .max_position_embeddings :
            warnings .warn (
            f"decoder.max_position_embeddings={self .config .decoder .max_position_embeddings },"+
            f" but tokenizer.model_max_length={tokenizer .tokenizer .model_max_length }, will set"+
            f" tokenizer.model_max_length to {self .config .decoder .max_position_embeddings }.")
            tokenizer .tokenizer .model_max_length =self .config .decoder .max_position_embeddings 

        assert self .config .decoder .vocab_size ==len (tokenizer )
        assert self .config .decoder_start_token_id ==tokenizer .bos_token_id 
        assert self .config .pad_token_id ==tokenizer .pad_token_id 

    @classmethod 
    def from_checkpoint (cls ,model_path :str ,model_filename :str ="pytorch_model.pth",state_dict_strip_prefix ="model.model."):
        config =VisionEncoderDecoderConfig .from_pretrained (model_path )
        config ._name_or_path =model_path 
        config .encoder =UnimerSwinConfig (**vars (config .encoder ))
        config .decoder =UnimerMBartConfig (**vars (config .decoder ))

        encoder =UnimerSwinModel (config .encoder )
        decoder =UnimerMBartForCausalLM (config .decoder )
        model =cls (config ,encoder ,decoder )

        # load model weights
        model_file_path =os .path .join (model_path ,model_filename )
        checkpoint =torch .load (model_file_path ,map_location ="cpu",weights_only =True )
        state_dict =checkpoint ["model"]if "model"in checkpoint else checkpoint 
        if not state_dict :
            raise RuntimeError ("state_dict is empty.")
        if state_dict_strip_prefix :
            state_dict ={
            k [len (state_dict_strip_prefix ):]if k .startswith (state_dict_strip_prefix )else k :v 
            for k ,v in state_dict .items ()
            }
        missing_keys ,unexpected_keys =model .load_state_dict (state_dict ,strict =False )
        if len (unexpected_keys )>0 :
            warnings .warn ("Unexpected key(s) in state_dict: {}.".format (", ".join (f'"{k }"'for k in unexpected_keys )))
        if len (missing_keys )>0 :
            raise RuntimeError ("Missing key(s) in state_dict: {}.".format (", ".join (f'"{k }"'for k in missing_keys )))
        return model 

    def forward_bak (self ,samples ):
        pixel_values ,text =samples ["image"],samples ["text_input"]

        text_inputs =self .tokenizer .tokenize (text ).to (pixel_values .device )
        decoder_input_ids ,decoder_attention_mask =text_inputs ["input_ids"],text_inputs ["attention_mask"]

        num_channels =pixel_values .shape [1 ]
        if num_channels ==1 :
            pixel_values =pixel_values .repeat (1 ,3 ,1 ,1 )

        labels =decoder_input_ids *1 
        labels =labels .masked_fill (labels ==self .tokenizer .pad_token_id ,-100 )

        loss =self .model (
        pixel_values =pixel_values ,
        decoder_input_ids =decoder_input_ids [:,:-1 ],
        decoder_attention_mask =decoder_attention_mask [:,:-1 ],
        labels =labels [:,1 :],
        ).loss 
        return {"loss":loss }

    def generate (self ,samples ,do_sample :bool =False ,temperature :float =0.2 ,top_p :float =0.95 ):
        pixel_values =samples ["image"]
        num_channels =pixel_values .shape [1 ]
        if num_channels ==1 :
            pixel_values =pixel_values .repeat (1 ,3 ,1 ,1 )

        kwargs ={}
        if do_sample :
            kwargs ["temperature"]=temperature 
            kwargs ["top_p"]=top_p 

        outputs =super ().generate (
        pixel_values =pixel_values ,
        max_new_tokens =self .tokenizer .tokenizer .model_max_length ,# required
        decoder_start_token_id =self .tokenizer .tokenizer .bos_token_id ,
        do_sample =do_sample ,
        **kwargs ,
        )

        outputs =outputs [:,1 :].cpu ().numpy ()
        pred_tokens =self .tokenizer .detokenize (outputs )
        pred_str =self .tokenizer .token2str (outputs )
        fixed_str =[latex_rm_whitespace (s )for s in pred_str ]
        return {"pred_ids":outputs ,"pred_tokens":pred_tokens ,"pred_str":pred_str ,"fixed_str":fixed_str }

