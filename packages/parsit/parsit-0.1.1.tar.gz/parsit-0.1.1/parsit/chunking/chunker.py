from __future__ import annotations 

import re 
import math 
import inspect 
import json 
from dataclasses import dataclass ,asdict 
from typing import Callable ,Sequence ,Tuple ,Dict ,List ,Optional ,Union ,Any ,TypedDict ,Literal ,TypeVar ,cast ,TYPE_CHECKING 
from itertools import accumulate ,chain 
from contextlib import suppress 
from functools import lru_cache ,partial 

import mpire 
from tqdm import tqdm 

if TYPE_CHECKING :
    import tiktoken 
    import tokenizers 
    import transformers 

T =TypeVar ('T')

class ContentBlock (TypedDict ,total =False ):

    type :str 
    text :str 
    text_level :Optional [int ]
    page_idx :Optional [int ]
    bbox :Optional [List [float ]]

class ChunkMetadata (TypedDict ,total =False ):

    block_types :List [str ]
    text_levels :List [int ]
    pages :List [int ]
    has_title :bool 
    bboxes :List [List [float ]]
    num_blocks :int 
    is_continuation :bool 
    is_subchunk :bool 

class StructuredChunk (TypedDict ):
    text :str 
    metadata :ChunkMetadata 

_memoized_token_counters ={}
_PROTECTED_PATTERNS =[
(r'\[TABLE_START\s+\{.*?\}\]','table_start'),
(r'\[TABLE_CAPTION\].*?\[/TABLE_CAPTION\]','table_caption'),
(r'\[TABLE_BODY\].*?\[/TABLE_BODY\]','table_body'),
(r'\[TABLE_FOOTNOTE\].*?\[/TABLE_FOOTNOTE\]','table_footnote'),
(r'\[TABLE_END\]','table_end'),
(r'<table[^>]*>.*?</table>','html_table'),
(r'\$\$.*?\$\$','display_math'),
(r'\$[^$]+\$','inline_math'),
(r'```.*?```','code_block'),
(r'\[\d+[,\s\-\]]+','citations'),
(r'\([A-Z][a-z]+(?:\s+et\s+al\.)?\s*,\s*\d{4}[a-z]?\)','citations'),
(r'[A-Z][a-z]+(?:\s+et\s+al\.)?\s*\(\d{4}[a-z]?\)','citations'),
(r'https?://[^\s<>"]+','url'),
(r'!\[.*?\]\([^)]+\)','images'),
(r'\b(?:Figure|Fig\.?|Table|Section|Eq\.?|Equation)\s+[0-9]+(?:\.[0-9]+)*\b','references'),
(r'\b(?:e\.g\.|i\.e\.|cf\.|et\s+al\.|vs\.|etc\.|Fig\.|Eq\.)\b','abbreviations'),
(r'<[a-z][a-z0-9]*[^>]*>.*?</[a-z][a-z0-9]*>','html_element'),
(r'<[a-z][a-z0-9]*(?:\\s+[a-z0-9-]+(?:\\s*=\\s*(?:"[^"]*"|'  "'[^']*'"  '|[^>\\s]+))?)*\\s*/?>','html_self_closing')
]

def _protect_content (text :str )->Tuple [str ,Dict [str ,str ]]:
    protected ={}
    placeholder_text =text 
    for i ,(pattern ,content_type )in enumerate (_PROTECTED_PATTERNS ):
        matches =list (re .finditer (pattern ,placeholder_text ,re .DOTALL ))
        for j ,match in enumerate (reversed (matches )):
            placeholder =f"__PROTECTED_{content_type .upper ()}_{i }_{j }__"
            protected [placeholder ]=match .group (0 )
            start ,end =match .span ()
            placeholder_text =placeholder_text [:start ]+placeholder +placeholder_text [end :]
    return placeholder_text ,protected 

def _restore_content (text :str ,protected :Dict [str ,str ])->str :
    for placeholder ,original in protected .items ():
        text =text .replace (placeholder ,original )
    return text 

_NON_WHITESPACE_SEMANTIC_SPLITTERS =(
".",
"?",
"!",
"*",
";",
",",
"(",
")",
"[",
"]",
"“",
"”",
"‘",
"’",
"'",
'"',
"`",
":",
"—",
"…",
"/",
"\\",
"–",
"&",
"-",
)

_REGEX_ESCAPED_NON_WHITESPACE_SEMANTIC_SPLITTERS =tuple (re .escape (splitter )for splitter in _NON_WHITESPACE_SEMANTIC_SPLITTERS )

def _split_text (text :str )->tuple [str ,bool ,list [str ]]:
    protected_text ,protected_map =_protect_content (text )
    splitter ,splitter_is_whitespace ,splits =_split_text_unprotected (protected_text )
    restored_splits =[_restore_content (split ,protected_map )for split in splits ]
    return splitter ,splitter_is_whitespace ,restored_splits 

def _split_text_unprotected (text :str )->tuple [str ,bool ,list [str ]]:
    splitter_is_whitespace =True 
    if "\n"in text or "\r"in text :
        splitter =max (re .findall (r"[\r\n]+",text ))
    elif "\t"in text :
        splitter =max (re .findall (r"\t+",text ))
    elif re .search (r"\s",text ):
        splitter =max (re .findall (r"\s+",text ))
        if len (splitter )==1 :
            for escaped_preceder in _REGEX_ESCAPED_NON_WHITESPACE_SEMANTIC_SPLITTERS :
                if re .search (rf'{escaped_preceder }(\s)',text ):
                    splitter =re .search (rf'{escaped_preceder }(\s)',text ).group (1 )
                    escaped_splitter =re .escape (splitter )
                    return splitter ,splitter_is_whitespace ,re .split (rf'(?<={escaped_preceder }){escaped_splitter }',text )
    else :
        for splitter in _NON_WHITESPACE_SEMANTIC_SPLITTERS :
            if splitter in text :
                splitter_is_whitespace =False 
                break 
        else :
            return "",splitter_is_whitespace ,list (text )
    return splitter ,splitter_is_whitespace ,text .split (splitter )

def bisect_left (sorted :list ,target :int ,low :int ,high :int )->int :
    while low <high :
        mid =(low +high )//2 
        if sorted [mid ]<target :
            low =mid +1 
        else :
            high =mid 
    return low 

def merge_splits (
splits :list [str ],cum_lens :list [int ],chunk_size :int ,splitter :str ,token_counter :Callable ,start :int ,high :int 
)->tuple [int ,str ]:
    average =0.2 
    low =start 
    offset =cum_lens [start ]
    target =offset +(chunk_size *average )
    while low <high :
        i =bisect_left (cum_lens ,target ,low =low ,high =high )
        midpoint =min (i ,high -1 )
        tokens =token_counter (splitter .join (splits [start :midpoint ]))
        local_cum =cum_lens [midpoint ]-offset 
        if local_cum and tokens >0 :
            average =local_cum /tokens 
            target =offset +(chunk_size *average )
        if tokens >chunk_size :
            high =midpoint 
        else :
            low =midpoint +1 
    end =low -1 
    return end ,splitter .join (splits [start :end ])

def _extract_block_text (block :ContentBlock )->str :
    text_parts =[]
    metadata ={}
    if block .get ('type')=='table':
        table_meta ={
        'type':'table',
        'has_caption':'table_caption'in block ,
        'has_footnote':'table_footnote'in block ,
        'page_idx':block .get ('page_idx')
        }
        text_parts .append (f"[TABLE_START {json .dumps (table_meta )}]")
        if 'table_caption'in block and block ['table_caption']:
            caption =' '.join (c .strip ()for c in block ['table_caption']if c .strip ())
            if caption :
                text_parts .append (f"[TABLE_CAPTION]{caption }[/TABLE_CAPTION]")
        table_html =''
        if 'table_body'in block and block ['table_body'].strip ():
            table_html =block ['table_body'].strip ()
            if table_html .startswith ("__PROTECTED_TABLE_BODY_"):
                protected_map =block .get ('protected_content',{})
                table_html =protected_map .get (table_html ,table_html )
            table_html =re .sub (r'^<html[^>]*>.*<body[^>]*>','',table_html ,flags =re .DOTALL )
            table_html =re .sub (r'</body>\s*</html>','',table_html ,flags =re .DOTALL )
            table_html =table_html .strip ()
            text_parts .append (f"[TABLE_BODY]{table_html }[/TABLE_BODY]")
        if 'table_footnote'in block and block ['table_footnote']:
            footnote =' '.join (f .strip ()for f in block ['table_footnote']if f .strip ())
            if footnote :
                text_parts .append (f"[TABLE_FOOTNOTE]{footnote }[/TABLE_FOOTNOTE]")
        text_parts .append ("[TABLE_END]")
        return '\n'.join (text_parts )
    if block .get ('type')=='image'and 'img_caption'in block :
        caption =' '.join (c .strip ()for c in block ['img_caption']if c .strip ())
        if caption :
            text_parts .append (f"[Image: {caption }]")
    elif block .get ('type')=='list'and 'text'in block :
        text_parts .append (block ['text'].strip ())
    elif 'text'in block and block ['text'].strip ():
        text_parts .append (block ['text'].strip ())
    return '\n'.join (text_parts )

def _process_structured_blocks (
blocks :List [ContentBlock ],
chunk_size :int ,
token_counter :Callable [[str ],int ],
overlap :int =20 ,
adjust_overlap :bool =True ,
ignore_headers_and_footers :bool =False ,
**kwargs 
)->List [Dict [str ,Any ]]:
    def get_hierarchy_level (block ):
        t =block .get ('type','')
        if t =='title':
            return 3 
        if t =='section_header':
            return 2 
        return 1 
    chunks =[]
    current_chunk =[]
    current_tokens =0 
    prev_hierarchy_level =1 
    i =0 
    while i <len (blocks ):
        block =blocks [i ]
        block_text =_extract_block_text (block )
        if not block_text .strip ():
            i +=1 
            continue 
        block ['text']=block_text 
        block_tokens =token_counter (block_text )
        block_type =block .get ('type','')
        if ignore_headers_and_footers and block_type in ('header','footer'):
            i +=1 
            continue 
        current_hierarchy_level =get_hierarchy_level (block )
        if current_hierarchy_level >prev_hierarchy_level and current_chunk :
            chunks .append (_create_structured_chunk (current_chunk ))
            current_chunk =[]
            current_tokens =0 
        if block_type =='table':
            if current_chunk :
                chunks .append (_create_structured_chunk (current_chunk ))
                current_chunk =[]
                current_tokens =0 
            table_caption =block .get ('table_caption',[])
            table_footnote =block .get ('table_footnote',[])
            table_body =block .get ('table_body','')
            table_meta ={
            'type':'table',
            'has_caption':bool (table_caption ),
            'has_footnote':bool (table_footnote ),
            'page_idx':block .get ('page_idx')
            }
            caption_text =''
            if table_caption :
                caption_text ='[TABLE_CAPTION]'+' '.join (c .strip ()for c in table_caption if c .strip ())+'[/TABLE_CAPTION]'
            footnote_text =''
            if table_footnote :
                footnote_text ='[TABLE_FOOTNOTE]'+' '.join (f .strip ()for f in table_footnote if f .strip ())+'[/TABLE_FOOTNOTE]'
            table_body_html =''
            if table_body and table_body .strip ():
                table_body_html =table_body .strip ()
                if table_body_html .startswith ("__PROTECTED_TABLE_BODY_"):
                    table_body_html =block .get ('protected_content',{}).get (table_body_html ,table_body_html )
                table_body_html =re .sub (r'^<html[^>]*>.*<body[^>]*>','',table_body_html ,flags =re .DOTALL )
                table_body_html =re .sub (r'</body>\s*</html>','',table_body_html ,flags =re .DOTALL )
                table_body_html =table_body_html .strip ()
            table_rows =re .findall (r'<tr>.*?</tr>',table_body_html ,flags =re .DOTALL )if table_body_html else []
            if not table_rows :
                table_rows =[table_body_html ]if table_body_html else []
            table_start =f"[TABLE_START {json .dumps (table_meta )}]"
            table_end ="[TABLE_END]"
            chunks_for_table =[]
            current_rows =[]
            def make_table_chunk (rows ):
                parts =[table_start ]
                if caption_text :
                    parts .append (caption_text )
                if rows :
                    parts .append ('[TABLE_BODY]'+''.join (rows )+'[/TABLE_BODY]')
                if footnote_text :
                    parts .append (footnote_text )
                parts .append (table_end )
                return '\n'.join (parts )
            for row in table_rows :
                row_tokens =token_counter (row )
                chunk_tokens =token_counter (make_table_chunk (current_rows +[row ]))
                if chunk_tokens >chunk_size and current_rows :
                    chunks_for_table .append (make_table_chunk (current_rows ))
                    current_rows =[row ]
                else :
                    current_rows .append (row )
            if current_rows :
                chunks_for_table .append (make_table_chunk (current_rows ))
            for table_chunk_text in chunks_for_table :
                table_block ={
                'type':'table',
                'text':table_chunk_text ,
                'table_caption':table_caption ,
                'table_footnote':table_footnote ,
                'table_body':'',
                'page_idx':block .get ('page_idx')
                }
                chunks .append (_create_structured_chunk ([table_block ]))
            i +=1 
            prev_hierarchy_level =current_hierarchy_level 
            continue 
        if block_type =='list':
            if current_chunk :
                chunks .append (_create_structured_chunk (current_chunk ))
                current_chunk =[]
                current_tokens =0 
            chunks .append (_create_structured_chunk ([block ]))
            i +=1 
            prev_hierarchy_level =current_hierarchy_level 
            continue 
        if block_type =='image':
            if current_chunk :
                chunks .append (_create_structured_chunk (current_chunk ))
                current_chunk =[]
                current_tokens =0 
            chunks .append (_create_structured_chunk ([block ]))
            i +=1 
            prev_hierarchy_level =current_hierarchy_level 
            continue 
        if block_type in ('section_header','title'):
            header_block =block 
            i +=1 
            if i <len (blocks ):
                next_block =blocks [i ]
                next_block_text =_extract_block_text (next_block )
                next_block ['text']=next_block_text 
                next_block_tokens =token_counter (next_block_text )
                if current_tokens +block_tokens +next_block_tokens >chunk_size and current_chunk :
                    chunks .append (_create_structured_chunk (current_chunk ))
                    current_chunk =[]
                    current_tokens =0 
                current_chunk .append (header_block )
                current_chunk .append (next_block )
                current_tokens +=block_tokens +next_block_tokens 
                i +=1 
                prev_hierarchy_level =get_hierarchy_level (next_block )
                continue 
            else :
                current_chunk .append (header_block )
                current_tokens +=block_tokens 
                prev_hierarchy_level =current_hierarchy_level 
                continue 
        if current_tokens +block_tokens >chunk_size and current_chunk :
            chunks .append (_create_structured_chunk (current_chunk ))
            current_chunk =[]
            current_tokens =0 
        current_chunk .append (block )
        current_tokens +=block_tokens 
        prev_hierarchy_level =current_hierarchy_level 
        i +=1 
    if current_chunk :
        chunks .append (_create_structured_chunk (current_chunk ))
    if not chunks :
        return []
    if token_counter is None :
        token_counter =len 
    merged_chunks =[]
    current_chunk =None 
    for chunk in chunks :
        block_types =chunk .get ('metadata',{}).get ('block_types',[])
        if 'table'in block_types or 'table_end'in block_types :
            if current_chunk is not None :
                current_chunk ['text']=current_chunk .pop ('_temp_text')
                merged_chunks .append (current_chunk )
                current_chunk =None 
            merged_chunks .append (chunk )
            continue 
        chunk_text =chunk ['text']
        chunk_tokens =token_counter (chunk_text )
        if current_chunk is None :
            current_chunk =chunk .copy ()
            current_chunk ['_temp_text']=chunk_text 
            current_chunk ['_temp_tokens']=chunk_tokens 
            continue 
        merged_text =current_chunk ['_temp_text'].rstrip ()+' '+chunk_text .lstrip ()
        merged_tokens =token_counter (merged_text )
        if merged_tokens >chunk_size or (current_chunk ['_temp_tokens']>=chunk_size //2 and chunk_tokens >=chunk_size //2 ):
            current_chunk ['text']=current_chunk ['_temp_text']
            merged_chunks .append (current_chunk )
            current_chunk =chunk .copy ()
            current_chunk ['_temp_text']=chunk_text 
            current_chunk ['_temp_tokens']=chunk_tokens 
        else :
            current_chunk ['_temp_text']=merged_text 
            current_chunk ['_temp_tokens']=merged_tokens 
            for key in ['block_types','text_levels','pages','bboxes']:
                if key in chunk .get ('metadata',{})and key in current_chunk .get ('metadata',{}):
                    if key .endswith ('s'):
                        current_chunk ['metadata'][key ].extend (chunk ['metadata'][key ])
                    else :
                        current_chunk ['metadata'][key ]=current_chunk ['metadata'][key ]or chunk ['metadata'].get (key ,False )
    if current_chunk is not None :
        current_chunk ['text']=current_chunk .pop ('_temp_text')
        merged_chunks .append (current_chunk )
    return merged_chunks 

def _create_structured_chunk (blocks :List [ContentBlock ])->Dict [str ,Any ]:
    if not blocks :
        return {'text':'','metadata':{
        'block_types':[],
        'text_levels':[],
        'pages':[],
        'has_title':False ,
        'bboxes':[],
        'num_blocks':0 ,
        'is_continuation':False ,
        'is_subchunk':False 
        }}
    text_parts =[]
    block_types =[]
    text_levels =set ()
    pages =set ()
    bboxes =[]
    has_title =False 
    is_continuation =False 
    is_subchunk =False 
    for block in blocks :
        if not block .get ('text','').strip ():
            continue 
        block_text =block ['text'].strip ()
        if 'type'in block :
            block_type =block ['type']
            block_types .append (block_type )
            if block_type =='title':
                has_title =True 
        if 'text_level'in block and block ['text_level']is not None :
            text_levels .add (block ['text_level'])
        if 'page_idx'in block and block ['page_idx']is not None :
            pages .add (block ['page_idx'])
        if 'bbox'in block and block ['bbox']and len (block ['bbox'])==4 :
            bboxes .append (block ['bbox'])
        if block .get ('is_continuation',False ):
            is_continuation =True 
        if block .get ('is_subchunk',False ):
            is_subchunk =True 
        text_parts .append (block_text )
    text =' '.join (text_parts )
    metadata :ChunkMetadata ={
    'block_types':block_types ,
    'text_levels':sorted (text_levels )if text_levels else [],
    'pages':sorted (pages )if pages else [],
    'has_title':has_title ,
    'bboxes':bboxes ,
    'num_blocks':len (blocks ),
    'is_continuation':is_continuation ,
    'is_subchunk':is_subchunk 
    }
    return {
    'text':text ,
    'metadata':metadata 
    }

def chunk (
text :Union [str ,List [ContentBlock ],List [dict ]],
chunk_size :int ,
token_counter :Callable [[str ],int ],
memoize :bool =True ,
offsets :bool =False ,
overlap :Optional [Union [float ,int ]]=None ,
cache_maxsize :Optional [int ]=None ,
_recursion_depth :int =0 ,
_start :int =0 ,
adjust_overlap :bool =True ,
)->Union [List [str ],Tuple [List [str ],List [Tuple [int ,int ]]],List [StructuredChunk ]]:
    if isinstance (text ,(list ,dict ))or (isinstance (text ,str )and text .lstrip ().startswith (('[','{'))):
        if isinstance (text ,str ):
            try :
                content_blocks =json .loads (text )
            except json .JSONDecodeError :
                pass 
            else :
                text =content_blocks 
        if isinstance (text ,(list ,dict )):
            if not isinstance (text ,list ):
                text =[text ]
            chunks =_process_structured_blocks (
            text ,
            chunk_size =chunk_size ,
            token_counter =token_counter ,
            overlap =overlap if isinstance (overlap ,(int ,float ))else 0.1 ,
            adjust_overlap =adjust_overlap 
            )
            if offsets :
                chunk_texts =[chunk ['text']for chunk in chunks ]
                chunk_offsets =[]
                offset =0 
                for chunk_text in chunk_texts :
                    chunk_offsets .append ((offset ,offset +len (chunk_text )))
                    offset +=len (chunk_text )
                return chunk_texts ,chunk_offsets 
            return [chunk ['text']for chunk in chunks ]if not offsets else ([chunk ['text']for chunk in chunks ],[])
    return_offsets =offsets 
    local_chunk_size =chunk_size 
    if is_first_call :=not _recursion_depth :
        if memoize :
            token_counter =_memoized_token_counters .setdefault (token_counter ,lru_cache (cache_maxsize )(token_counter ))
        if overlap is not None :
            overlap =math .floor (chunk_size *overlap )if overlap <1 else min (overlap ,chunk_size -1 )
            if overlap >0 :
                local_chunk_size =chunk_size -overlap 
    splitter ,splitter_is_whitespace ,splits =_split_text (text )
    offsets :list =[]
    splitter_len =len (splitter )
    split_lens =[len (split )for split in splits ]
    cum_lens =list (accumulate (split_lens ,initial =0 ))
    split_starts =accumulate ([0 ]+[split_len +splitter_len for split_len in split_lens ])
    split_starts =[start +_start for start in split_starts ]
    num_splits_plus_one =len (splits )+1 
    chunks =[]
    skips =set ()
    for i ,(split ,split_start )in enumerate (zip (splits ,split_starts )):
        if i in skips :
            continue 
        if token_counter (split )>local_chunk_size :
            recursive_overlap =None 
            if overlap is not None and overlap >0 :
                recursive_overlap =overlap /chunk_size 
            new_chunks ,new_offsets =chunk (
            text =split ,
            chunk_size =local_chunk_size ,
            token_counter =token_counter ,
            overlap =recursive_overlap ,
            memoize =memoize ,
            offsets =return_offsets ,
            cache_maxsize =cache_maxsize ,
            _recursion_depth =_recursion_depth +1 ,
            _start =split_start ,
            )
            chunks .extend (new_chunks )
            offsets .extend (new_offsets )
        else :
            final_split_in_chunk_i ,new_chunk =merge_splits (
            splits =splits ,
            cum_lens =cum_lens ,
            chunk_size =local_chunk_size ,
            splitter =splitter ,
            token_counter =token_counter ,
            start =i ,
            high =num_splits_plus_one ,
            )
            skips .update (range (i +1 ,final_split_in_chunk_i ))
            chunks .append (new_chunk )
            chunk_end =split_starts [final_split_in_chunk_i ]-splitter_len *(not splitter_is_whitespace )
            offsets .append ((split_start ,chunk_end ))
    if is_first_call and chunks :
        if isinstance (chunks [0 ],dict )and 'text'in chunks [0 ]:
            return chunks 
        if overlap and len (chunks )>1 :
            processed_chunks =[chunks [0 ]]
            for i in range (1 ,len (chunks )):
                prev_chunk =processed_chunks [-1 ]
                current_chunk =chunks [i ]
                if return_offsets and len (prev_chunk )>0 and len (current_chunk )>0 :
                    overlap_size =min (overlap ,len (prev_chunk )//2 )
                    overlap_start =len (prev_chunk )-overlap_size 
                    overlap_region =prev_chunk [overlap_start :]
                    sentence_end =overlap_region .rfind ('. ')
                    if sentence_end >0 :
                        cut_point =overlap_start +sentence_end +1 
                        current_chunk =prev_chunk [cut_point :].lstrip ()+' '+current_chunk 
                        processed_chunks [-1 ]=prev_chunk [:cut_point ].rstrip ()
                processed_chunks .append (current_chunk )
            chunks =processed_chunks 
            if return_offsets and len (chunks )==len (offsets ):
                for i in range (1 ,len (chunks )):
                    prev_len =len (chunks [i -1 ])
                    offsets [i -1 ]=(offsets [i -1 ][0 ],offsets [i -1 ][0 ]+prev_len )
                    offsets [i ]=(max (offsets [i -1 ][1 ]-overlap ,offsets [i ][0 ]),offsets [i ][1 ])
        if overlap :
            subchunk_size =local_chunk_size 
            subchunks =chunks 
            suboffsets =offsets 
            num_subchunks =len (subchunks )
            subchunks_per_chunk =math .floor (chunk_size /subchunk_size )
            subchunk_stride =math .floor ((chunk_size -overlap )/subchunk_size )
            offsets =[
            (
            suboffsets [(start :=i *subchunk_stride )][0 ],
            suboffsets [min (start +subchunks_per_chunk ,num_subchunks )-1 ][1 ],
            )
            for i in range (max (1 ,math .ceil ((num_subchunks -subchunks_per_chunk )/subchunk_stride )+1 ))
            ]
            chunks =[text [start :end ]for start ,end in offsets ]
        if return_offsets :
            return chunks ,offsets 
        return chunks 
    return chunks ,offsets 

class Chunker :
    def __init__ (self ,chunk_size :int ,token_counter :Callable [[str ],int ])->None :
        self .chunk_size =chunk_size 
        self .token_counter =token_counter 

    def _make_chunk_function (
    self ,
    offsets :bool ,
    overlap :float |int |None ,
    adjust_overlap :bool =True ,
    )->Callable [[str ],list [str ]|tuple [list [str ],list [tuple [int ,int ]]]]:
        def _chunk (text :str )->list [str ]|tuple [list [str ],list [tuple [int ,int ]]]:
            nonlocal adjust_overlap 
            if isinstance (text ,(list ,dict ))or (isinstance (text ,str )and text .lstrip ().startswith ('[')):
                try :
                    if isinstance (text ,str ):
                        content_blocks =json .loads (text )
                    else :
                        content_blocks =text 
                    if not isinstance (content_blocks ,list ):
                        raise ValueError ("Structured input must be a list of content blocks")
                    return _process_structured_blocks (
                    content_blocks ,
                    chunk_size =self .chunk_size ,
                    token_counter =self .token_counter ,
                    overlap =overlap if isinstance (overlap ,(int ,float ))else 0.1 ,
                    )
                except (json .JSONDecodeError ,ValueError )as e :
                    if not isinstance (text ,str ):
                        raise ValueError (f"Invalid structured content: {e }")
            if not isinstance (text ,str ):
                raise TypeError (f"`text` must be a string, list, or dict, not {type (text ).__name__ }.")
            if not isinstance (self .chunk_size ,int ):
                raise TypeError (f"`chunk_size` must be an integer, not {type (self .chunk_size ).__name__ }.")
            if self .chunk_size <1 :
                raise ValueError (f"`chunk_size` must be positive, not {self .chunk_size }.")
            if not callable (self .token_counter ):
                raise TypeError (f"`token_counter` must be callable, not {type (self .token_counter ).__name__ }.")
            if not isinstance (offsets ,bool ):
                raise TypeError (f"`offsets` must be a boolean, not {type (offsets ).__name__ }.")
            if overlap is not None and not isinstance (overlap ,(int ,float )):
                raise TypeError (f"`overlap` must be an integer or a float, not {type (overlap ).__name__ }.")
            return chunk (
            text =text ,
            chunk_size =self .chunk_size ,
            token_counter =self .token_counter ,
            memoize =False ,
            offsets =offsets ,
            overlap =overlap ,
            adjust_overlap =adjust_overlap ,
            )
        return _chunk 

    def __call__ (
    self ,
    text_or_texts :str |Sequence [str ],
    processes :int =1 ,
    progress :bool =False ,
    offsets :bool =False ,
    overlap :int |float |None =None ,
    adjust_overlap :bool =True ,
    )->(
    list [str ]
    |tuple [list [str ],list [tuple [int ,int ]]]
    |list [list [str ]]
    |tuple [list [list [str ]],list [list [tuple [int ,int ]]]]
    ):
        chunk_function =self ._make_chunk_function (offsets =offsets ,overlap =overlap ,adjust_overlap =adjust_overlap )
        if isinstance (text_or_texts ,str ):
            return chunk_function (text_or_texts )
        if progress and processes ==1 :
            text_or_texts =tqdm (text_or_texts )
        if processes ==1 :
            chunks_and_offsets =[chunk_function (text )for text in text_or_texts ]
        else :
            with mpire .WorkerPool (processes ,use_dill =True )as pool :
                chunks_and_offsets =pool .map (chunk_function ,text_or_texts ,progress_bar =progress )
        if offsets :
            chunks ,offsets_ =zip (*chunks_and_offsets )
            return list (chunks ),list (offsets_ )
        return chunks_and_offsets 

def chunkerify (
tokenizer_or_token_counter :str 
|tiktoken .Encoding 
|transformers .PreTrainedTokenizer 
|tokenizers .Tokenizer 
|Callable [[str ],int ],
chunk_size :int |None =None ,
max_token_chars :int |None =None ,
memoize :bool =True ,
cache_maxsize :int |None =None ,
)->Chunker :
    if isinstance (tokenizer_or_token_counter ,str ):
        try :
            import tiktoken 
            tokenizer =tiktoken .encoding_for_model (tokenizer_or_token_counter )
        except Exception :
            try :
                import transformers 
                tokenizer =transformers .AutoTokenizer .from_pretrained (tokenizer_or_token_counter )
            except Exception :
                raise ValueError (
                f'"{tokenizer_or_token_counter }" was provided to `semchunk.chunkerify` as the name of a tokenizer but neither `tiktoken` nor `transformers` have a tokenizer by that name. Perhaps they are not installed or maybe there is a typo in that name?'
                )
        tokenizer_or_token_counter =tokenizer 
    if max_token_chars is None :
        for potential_vocabulary_getter_function in ("token_byte_values","get_vocab"):
            if hasattr (tokenizer_or_token_counter ,potential_vocabulary_getter_function )and callable (
            getattr (tokenizer_or_token_counter ,potential_vocabulary_getter_function )
            ):
                vocab =getattr (tokenizer_or_token_counter ,potential_vocabulary_getter_function )()
                if hasattr (vocab ,"__iter__")and vocab and all (hasattr (token ,"__len__")for token in vocab ):
                    max_token_chars =max (len (token )for token in vocab )
                    break 
    if chunk_size is None :
        if hasattr (tokenizer_or_token_counter ,"model_max_length")and isinstance (
        tokenizer_or_token_counter .model_max_length ,int 
        ):
            chunk_size =tokenizer_or_token_counter .model_max_length 
            if hasattr (tokenizer_or_token_counter ,"encode"):
                with suppress (Exception ):
                    chunk_size -=len (tokenizer_or_token_counter .encode (""))
        else :
            raise ValueError (
            "Your desired chunk size was not passed to `semchunk.chunkerify` and the provided tokenizer either lacks an attribute named 'model_max_length' or that attribute is not an integer. Either specify a chunk size or provide a tokenizer that has a 'model_max_length' attribute that is an integer."
            )
    if hasattr (tokenizer_or_token_counter ,"encode"):
        if "add_special_tokens"in inspect .signature (tokenizer_or_token_counter .encode ).parameters :
            def token_counter (text :str )->int :
                return len (tokenizer_or_token_counter .encode (text ,add_special_tokens =False ))
        else :
            def token_counter (text :str )->int :
                return len (tokenizer_or_token_counter .encode (text ))
    else :
        token_counter =tokenizer_or_token_counter 
    if max_token_chars is not None :
        max_token_chars =max_token_chars -1 
        original_token_counter =token_counter 
        def faster_token_counter (text :str )->int :
            heuristic =chunk_size *6 
            if len (text )>heuristic and original_token_counter (text [:heuristic +max_token_chars ])>chunk_size :
                return chunk_size +1 
            return original_token_counter (text )
        token_counter =faster_token_counter 
    if memoize :
        token_counter =_memoized_token_counters .setdefault (token_counter ,lru_cache (cache_maxsize )(token_counter ))
    return Chunker (chunk_size =chunk_size ,token_counter =token_counter )
