import copy 
import math 
import os 
import re 
import statistics 
import time 
import warnings 
from typing import List 

import cv2 
import fitz 
import torch 
import numpy as np 
from loguru import logger 
from tqdm import tqdm 

from parsit .config .enums import SupportedPdfParseMethod 
from parsit .config .ocr_content_type import BlockType ,ContentType 
from parsit .data .dataset import Dataset ,PageableData 
from parsit .libs .boxbase import calculate_overlap_area_in_bbox1_area_ratio ,__is_overlaps_y_exceeds_threshold 
from parsit .libs .clean_memory import clean_memory 
from parsit .libs .config_reader import get_local_layoutreader_model_dir ,get_llm_aided_config ,get_device,get_table_recog_config
from parsit .libs .convert_utils import dict_to_list 
from parsit .libs .hash_utils import compute_md5 
from parsit .libs .pdf_image_tools import cut_image_to_pil_image 
from parsit .model .magic_model import MagicModel 
from parsit .post_proc .llm_aided import (
llm_aided_formula ,
llm_aided_text ,
llm_aided_title ,
process_enrichments 
)
from parsit .libs .config_reader import get_enrichment_config 

from parsit .model .sub_modules .model_init import AtomModelSingleton 
from parsit .post_proc .para_split_v3 import para_split 
from parsit .pre_proc .construct_page_dict import ocr_construct_page_component_v2 
from parsit .pre_proc .cut_image import ocr_cut_image_and_table 
from parsit .pre_proc .ocr_detect_all_bboxes import ocr_prepare_bboxes_for_layout_split_v2 
from parsit .pre_proc .ocr_dict_merge import fill_spans_in_blocks ,fix_block_spans_v2 ,fix_discarded_block 
from parsit .pre_proc .ocr_span_list_modify import get_qa_need_list_v2 ,remove_overlaps_low_confidence_spans ,remove_overlaps_min_spans ,remove_x_overlapping_chars 

os .environ ['NO_ALBUMENTATIONS_UPDATE']='1'


def __replace_STX_ETX (text_str :str ):
    """Replace \u0002 and \u0003, as these characters become garbled when extracted using pymupdf. In fact, they were originally quotation marks.
    Drawback: This issue is only observed in English text; it has not been found in Chinese text so far.

        Args:
            text_str (str): raw text

        Returns:
            _type_: replaced text
    """# noqa: E501
    if text_str :
        s =text_str .replace ('\u0002',"'")
        s =s .replace ('\u0003',"'")
        return s 
    return text_str 



def __replace_ligatures (text :str ):
    ligatures ={
    'ﬁ':'fi','ﬂ':'fl','ﬀ':'ff','ﬃ':'ffi','ﬄ':'ffl','ﬅ':'ft','ﬆ':'st'
    }
    return re .sub ('|'.join (map (re .escape ,ligatures .keys ())),lambda m :ligatures [m .group ()],text )


def chars_to_content (span ):

    if len (span ['chars'])==0 :
        pass 
    else :

        span ['chars']=sorted (span ['chars'],key =lambda x :(x ['bbox'][0 ]+x ['bbox'][2 ])/2 )

        # Calculate the width of each character
        char_widths =[char ['bbox'][2 ]-char ['bbox'][0 ]for char in span ['chars']]
        # Calculate the median width
        median_width =statistics .median (char_widths )


        span =remove_x_overlapping_chars (span ,median_width )

        content =''
        for char in span ['chars']:


            char1 =char 
            char2 =span ['chars'][span ['chars'].index (char )+1 ]if span ['chars'].index (char )+1 <len (span ['chars'])else None 
            if char2 and char2 ['bbox'][0 ]-char1 ['bbox'][2 ]>median_width *0.25 and char ['c']!=' 'and char2 ['c']!=' ':
                content +=f"{char ['c']} "
            else :
                content +=char ['c']

        span ['content']=__replace_ligatures (content )

    del span ['chars']


LINE_STOP_FLAG =('.','!','?','。','！','？',')','）','"','”',':','：',';','；',']','】','}','}','>','》','、',',','，','-','—','–',)
LINE_START_FLAG =('(','（','"','“','【','{','《','<','「','『','【','[',)


def fill_char_in_spans (spans ,all_chars ):


    spans =sorted (spans ,key =lambda x :x ['bbox'][1 ])

    for char in all_chars :

        for span in spans :
            if calculate_char_in_span (char ['bbox'],span ['bbox'],char ['c']):
                span ['chars'].append (char )
                break 

    need_ocr_spans =[]
    for span in spans :
        chars_to_content (span )
        if span["type"] == ContentType.Table and len(span.get("content",[]))<2:
            span["likely_image"] = True
            continue
        if span["type"] != ContentType.Text:
            continue
        if len (span ['content'])*span ['height']<span ['width']*0.5 :
        # logger.info(f"maybe empty span: {len(span['content'])}, {span['height']}, {span['width']}")
            need_ocr_spans .append (span )
        del span ['height'],span ['width']
    return need_ocr_spans 



def calculate_char_in_span (char_bbox ,span_bbox ,char ,span_height_radio =0.33 ):
    char_center_x =(char_bbox [0 ]+char_bbox [2 ])/2 
    char_center_y =(char_bbox [1 ]+char_bbox [3 ])/2 
    span_center_y =(span_bbox [1 ]+span_bbox [3 ])/2 
    span_height =span_bbox [3 ]-span_bbox [1 ]

    if (
    span_bbox [0 ]<char_center_x <span_bbox [2 ]
    and span_bbox [1 ]<char_center_y <span_bbox [3 ]
    and abs (char_center_y -span_center_y )<span_height *span_height_radio 
    ):
        return True 
    else :


        if char in LINE_STOP_FLAG :
            if (
            (span_bbox [2 ]-span_height )<char_bbox [0 ]<span_bbox [2 ]
            and char_center_x >span_bbox [0 ]
            and span_bbox [1 ]<char_center_y <span_bbox [3 ]
            and abs (char_center_y -span_center_y )<span_height *span_height_radio 
            ):
                return True 
        elif char in LINE_START_FLAG :
            if (
            span_bbox [0 ]<char_bbox [2 ]<(span_bbox [0 ]+span_height )
            and char_center_x <span_bbox [2 ]
            and span_bbox [1 ]<char_center_y <span_bbox [3 ]
            and abs (char_center_y -span_center_y )<span_height *span_height_radio 
            ):
                return True 
        else :
            return False 


def remove_tilted_line (text_blocks ):
    for block in text_blocks :
        remove_lines =[]
        for line in block ['lines']:
            cosine ,sine =line ['dir']

            angle_radians =math .atan2 (sine ,cosine )

            angle_degrees =math .degrees (angle_radians )
            if 2 <abs (angle_degrees )<88 :
                remove_lines .append (line )
        for line in remove_lines :
            block ['lines'].remove (line )


def calculate_contrast (img ,img_mode )->float :

    if img_mode =='rgb':

        gray_img =cv2 .cvtColor (img ,cv2 .COLOR_RGB2GRAY )
    elif img_mode =='bgr':

        gray_img =cv2 .cvtColor (img ,cv2 .COLOR_BGR2GRAY )
    else :
        raise ValueError ("Invalid image mode. Please provide 'rgb' or 'bgr'.")


    mean_value =np .mean (gray_img )
    std_dev =np .std (gray_img )

    contrast =std_dev /(mean_value +1e-6 )
    # logger.debug(f"contrast: {contrast}")
    return round (contrast ,2 )

    # @measure_time
def txt_spans_extract_v2 (pdf_page ,spans ,all_bboxes ,all_discarded_blocks ,lang ):

# text_blocks_raw = pdf_page.get_text('rawdict', flags=fitz.TEXT_PRESERVE_WHITESPACE | fitz.TEXT_MEDIABOX_CLIP)['blocks']


#text_blocks_raw = pdf_page.get_text('rawdict', flags=fitz.TEXT_PRESERVE_LIGATURES | fitz.TEXT_PRESERVE_WHITESPACE | fitz.TEXT_MEDIABOX_CLIP)['blocks']


    text_blocks_raw =pdf_page .get_text ('rawdict',flags =fitz .TEXTFLAGS_TEXT )['blocks']
    # text_blocks = pdf_page.get_text('dict', flags=fitz.TEXTFLAGS_TEXT)['blocks']


    remove_tilted_line (text_blocks_raw )

    all_pymu_chars =[]
    for block in text_blocks_raw :
        for line in block ['lines']:
            cosine ,sine =line ['dir']
            if abs (cosine )<0.9 or abs (sine )>0.1 :
                continue 
            for span in line ['spans']:
                all_pymu_chars .extend (span ['chars'])


    span_height_list =[]
    for span in spans :
        if span ['type']in [ContentType .InterlineEquation ,ContentType .Image ,ContentType .Table ]:
            continue 
        span_height =span ['bbox'][3 ]-span ['bbox'][1 ]
        span ['height']=span_height 
        span ['width']=span ['bbox'][2 ]-span ['bbox'][0 ]
        span_height_list .append (span_height )
    if len (span_height_list )==0 :
        return spans 
    else :
        median_span_height =statistics .median (span_height_list )

    useful_spans =[]
    unuseful_spans =[]

    vertical_spans =[]
    for span in spans :
        if span ['type']in [ContentType .InterlineEquation ,ContentType .Image ,ContentType .Table ]:
            continue 
        for block in all_bboxes +all_discarded_blocks :
            if block [7 ]in [BlockType .ImageBody ,BlockType .TableBody ,BlockType .InterlineEquation ]:
                continue 
            if calculate_overlap_area_in_bbox1_area_ratio (span ['bbox'],block [0 :4 ])>0.5 :
                if span ['height']>median_span_height *3 and span ['height']>span ['width']*3 :
                    vertical_spans .append (span )
                elif block in all_bboxes :
                    useful_spans .append (span )
                else :
                    unuseful_spans .append (span )

                break 

    """垂直的span框直接用pymu的line进行填充"""
    if len (vertical_spans )>0 :
        text_blocks =pdf_page .get_text ('dict',flags =fitz .TEXTFLAGS_TEXT )['blocks']
        all_pymu_lines =[]
        for block in text_blocks :
            for line in block ['lines']:
                all_pymu_lines .append (line )

        for pymu_line in all_pymu_lines :
            for span in vertical_spans :
                if calculate_overlap_area_in_bbox1_area_ratio (pymu_line ['bbox'],span ['bbox'])>0.5 :
                    for pymu_span in pymu_line ['spans']:
                        span ['content']+=pymu_span ['text']
                    break 

        for span in vertical_spans :
            if len (span ['content'])==0 :
                spans .remove (span )

    """水平的span框如果没有char则用ocr进行填充"""
    new_spans =[]

    # for span in useful_spans +unuseful_spans :
    #     if span ['type']in [ContentType .Text ]:
    for span in spans:
        if span["type"] in [ContentType.Text,ContentType.Table]:
            span ['chars']=[]
            new_spans .append (span )

    need_ocr_spans =fill_char_in_spans (new_spans ,all_pymu_chars )

    if len (need_ocr_spans )>0 :


    # atom_model_manager = AtomModelSingleton()
    # ocr_model = atom_model_manager.get_atom_model(
    #     atom_model_name='ocr',
    #     ocr_show_log=False,
    #     det_db_box_thresh=0.3,
    #     lang=lang
    # )

        for span in need_ocr_spans :

            span_img =cut_image_to_pil_image (span ['bbox'],pdf_page ,mode ='cv2')


            if calculate_contrast (span_img ,img_mode ='bgr')<=0.17 :
                spans .remove (span )
                continue 
                # pass

            span ['content']=''
            span ['score']=1 
            span ['np_img']=span_img 


            # ocr_res = ocr_model.ocr(span_img, det=False)
            # if ocr_res and len(ocr_res) > 0:
            #     if len(ocr_res[0]) > 0:
            #         ocr_text, ocr_score = ocr_res[0][0]
            #         # logger.info(f"ocr_text: {ocr_text}, ocr_score: {ocr_score}")
            #         if ocr_score > 0.5 and len(ocr_text) > 0:
            #             span['content'] = ocr_text
            #             span['score'] = float(round(ocr_score, 2))
            #         else:
            #             spans.remove(span)

    return spans 


def model_init (model_name :str ):
    from transformers import LayoutLMv3ForTokenClassification 
    device_name =get_device ()
    bf_16_support =False 
    if device_name .startswith ("cuda"):
        bf_16_support =torch .cuda .is_bf16_supported ()
    elif device_name .startswith ("mps"):
        bf_16_support =True 

    device =torch .device (device_name )
    if model_name =='layoutreader':

        layoutreader_model_dir =get_local_layoutreader_model_dir ()
        if os .path .exists (layoutreader_model_dir ):
            model =LayoutLMv3ForTokenClassification .from_pretrained (
            layoutreader_model_dir 
            )
        else :
            logger .warning (
            'local layoutreader model not exists, use online model from huggingface'
            )
            model =LayoutLMv3ForTokenClassification .from_pretrained (
            'hantian/layoutreader'
            )
        if bf_16_support :
            model .to (device ).eval ().bfloat16 ()
        else :
            model .to (device ).eval ()
    else :
        logger .error ('model name not allow')
        exit (1 )
    return model 


class ModelSingleton :
    _instance =None 
    _models ={}

    def __new__ (cls ,*args ,**kwargs ):
        if cls ._instance is None :
            cls ._instance =super ().__new__ (cls )
        return cls ._instance 

    def get_model (self ,model_name :str ):
        if model_name not in self ._models :
            self ._models [model_name ]=model_init (model_name =model_name )
        return self ._models [model_name ]


def do_predict (boxes :List [List [int ]],model )->List [int ]:
    from parsit .model .sub_modules .reading_oreder .layoutreader .helpers import (
    boxes2inputs ,parse_logits ,prepare_inputs )

    with warnings .catch_warnings ():
        warnings .filterwarnings ("ignore",category =FutureWarning ,module ="transformers")

        inputs =boxes2inputs (boxes )
        inputs =prepare_inputs (inputs ,model )
        logits =model (**inputs ).logits .cpu ().squeeze (0 )
    return parse_logits (logits ,len (boxes ))


def cal_block_index (fix_blocks ,sorted_bboxes ):
    if not fix_blocks :
        return []

    for block in fix_blocks :
    # Ensure block has required fields
        if not isinstance (block ,dict ):
            continue 

            # Initialize lines if missing
        if 'lines'not in block :
            block ['lines']=[]

            # Ensure bbox exists and is valid
        if 'bbox'not in block or not block ['bbox']:
            block ['bbox']=[0 ,0 ,0 ,0 ]# Default bbox if missing
            if sorted_bboxes :
                block ['index']=0 # Default index
            continue 

            # Process lines if they exist
        line_index_list =[]
        if block ['lines']:
            try :
                for line in block ['lines']:
                    if isinstance (line ,dict )and 'bbox'in line and sorted_bboxes :
                        try :
                            line ['index']=sorted_bboxes .index (line ['bbox'])
                            line_index_list .append (line ['index'])
                        except (ValueError ,IndexError ):
                            continue 

                if line_index_list :
                    block ['index']=statistics .median (line_index_list )
                elif 'bbox'in block and sorted_bboxes :
                    block ['index']=sorted_bboxes .index (block ['bbox'])
            except Exception as e :
                logger .warning (f"Error processing block lines: {e }")
                if 'bbox'in block and sorted_bboxes :
                    block ['index']=sorted_bboxes .index (block ['bbox'])
        elif 'bbox'in block and sorted_bboxes :
            block ['index']=sorted_bboxes .index (block ['bbox'])

            # Handle special block types
        if block .get ('type')in [BlockType .ImageBody ,BlockType .TableBody ,
        BlockType .Title ,BlockType .InterlineEquation ]:
            if 'real_lines'in block :
                block ['virtual_lines']=copy .deepcopy (block .get ('lines',[]))
                block ['lines']=copy .deepcopy (block .get ('real_lines',[]))
                if 'real_lines'in block :
                    del block ['real_lines']

                    # Handle xycut sorting if needed
    if sorted_bboxes is None :
        block_bboxes =[]
        for block in fix_blocks :
            if 'bbox'in block and block ['bbox']:
                block ['bbox']=[max (0 ,x )for x in block ['bbox']]
                block_bboxes .append (block ['bbox'])

            if block .get ('type')in [BlockType .ImageBody ,BlockType .TableBody ,
            BlockType .Title ,BlockType .InterlineEquation ]:
                if 'real_lines'in block :
                    block ['virtual_lines']=copy .deepcopy (block .get ('lines',[]))
                    block ['lines']=copy .deepcopy (block .get ('real_lines',[]))
                    if 'real_lines'in block :
                        del block ['real_lines']

    return fix_blocks 


def insert_lines_into_block (block_bbox ,line_height ,page_w ,page_h ):

    x0 ,y0 ,x1 ,y1 =block_bbox 

    block_height =y1 -y0 
    block_weight =x1 -x0 


    if line_height *2 <block_height :
        if (
        block_height >page_h *0.25 and page_w *0.5 >block_weight >page_w *0.25 
        ):
            lines =int (block_height /line_height )
        else :

            if block_weight >page_w *0.4 :
                lines =3 
            elif block_weight >page_w *0.25 :
                lines =int (block_height /line_height )
            else :
                if block_height /block_weight >1.2 :
                    return [[x0 ,y0 ,x1 ,y1 ]]
                else :
                    lines =2 

        line_height =(y1 -y0 )/lines 


        current_y =y0 


        lines_positions =[]

        for i in range (lines ):
            lines_positions .append ([x0 ,current_y ,x1 ,current_y +line_height ])
            current_y +=line_height 
        return lines_positions 

    else :
        return [[x0 ,y0 ,x1 ,y1 ]]


def sort_lines_by_model (fix_blocks ,page_w ,page_h ,line_height ,footnote_blocks ):
    page_line_list =[]

    def add_lines_to_block (b ):
        line_bboxes =insert_lines_into_block (b ['bbox'],line_height ,page_w ,page_h )
        b ['lines']=[]
        for line_bbox in line_bboxes :
            b ['lines'].append ({'bbox':line_bbox ,'spans':[]})
        page_line_list .extend (line_bboxes )

    for block in fix_blocks :
        if block ['type']in [
        BlockType .Text ,BlockType .Title ,
        BlockType .ImageCaption ,BlockType .ImageFootnote ,
        BlockType .TableCaption ,BlockType .TableFootnote 
        ]:
            if len (block ['lines'])==0 :
                add_lines_to_block (block )
            elif block ['type']in [BlockType .Title ]and len (block ['lines'])==1 and (block ['bbox'][3 ]-block ['bbox'][1 ])>line_height *2 :
                block ['real_lines']=copy .deepcopy (block ['lines'])
                add_lines_to_block (block )
            else :
                for line in block ['lines']:
                    bbox =line ['bbox']
                    page_line_list .append (bbox )
        elif block ['type']in [BlockType .ImageBody ,BlockType .TableBody ,BlockType .InterlineEquation ]:
            block ['real_lines']=copy .deepcopy (block ['lines'])
            add_lines_to_block (block )

    for block in footnote_blocks :
        footnote_block ={'bbox':block [:4 ]}
        add_lines_to_block (footnote_block )

    if len (page_line_list )>200 :
        return None 


    x_scale =1000.0 /page_w 
    y_scale =1000.0 /page_h 
    boxes =[]
    # logger.info(f"Scale: {x_scale}, {y_scale}, Boxes len: {len(page_line_list)}")
    for left ,top ,right ,bottom in page_line_list :
        if left <0 :
            logger .warning (
            f'left < 0, left: {left }, right: {right }, top: {top }, bottom: {bottom }, page_w: {page_w }, page_h: {page_h }'
            )# noqa: E501
            left =0 
        if right >page_w :
            logger .warning (
            f'right > page_w, left: {left }, right: {right }, top: {top }, bottom: {bottom }, page_w: {page_w }, page_h: {page_h }'
            )# noqa: E501
            right =page_w 
        if top <0 :
            logger .warning (
            f'top < 0, left: {left }, right: {right }, top: {top }, bottom: {bottom }, page_w: {page_w }, page_h: {page_h }'
            )# noqa: E501
            top =0 
        if bottom >page_h :
            logger .warning (
            f'bottom > page_h, left: {left }, right: {right }, top: {top }, bottom: {bottom }, page_w: {page_w }, page_h: {page_h }'
            )# noqa: E501
            bottom =page_h 

        left =round (left *x_scale )
        top =round (top *y_scale )
        right =round (right *x_scale )
        bottom =round (bottom *y_scale )
        assert (
        1000 >=right >=left >=0 and 1000 >=bottom >=top >=0 
        ),f'Invalid box. right: {right }, left: {left }, bottom: {bottom }, top: {top }'# noqa: E126, E121
        boxes .append ([left ,top ,right ,bottom ])
    model_manager =ModelSingleton ()
    model =model_manager .get_model ('layoutreader')
    with torch .no_grad ():
        orders =do_predict (boxes ,model )
    sorted_bboxes =[page_line_list [i ]for i in orders ]

    return sorted_bboxes 


def get_line_height (blocks ):
    page_line_height_list =[]
    for block in blocks :
        if block ['type']in [
        BlockType .Text ,BlockType .Title ,
        BlockType .ImageCaption ,BlockType .ImageFootnote ,
        BlockType .TableCaption ,BlockType .TableFootnote 
        ]:
            for line in block ['lines']:
                bbox =line ['bbox']
                page_line_height_list .append (int (bbox [3 ]-bbox [1 ]))
    if len (page_line_height_list )>0 :
        return statistics .median (page_line_height_list )
    else :
        return 10 


def process_groups (groups ,body_key ,caption_key ,footnote_key ):
    body_blocks =[]
    caption_blocks =[]
    footnote_blocks =[]
    for i ,group in enumerate (groups ):
        group [body_key ]['group_id']=i 
        body_blocks .append (group [body_key ])
        for caption_block in group [caption_key ]:
            caption_block ['group_id']=i 
            caption_blocks .append (caption_block )
        for footnote_block in group [footnote_key ]:
            footnote_block ['group_id']=i 
            footnote_blocks .append (footnote_block )
    return body_blocks ,caption_blocks ,footnote_blocks 


def process_block_list (blocks ,body_type ,block_type ):
    indices =[block ['index']for block in blocks ]
    median_index =statistics .median (indices )

    body_bbox =next ((block ['bbox']for block in blocks if block .get ('type')==body_type ),[])

    return {
    'type':block_type ,
    'bbox':body_bbox ,
    'blocks':blocks ,
    'index':median_index ,
    }


def revert_group_blocks (blocks ):
    image_groups ={}
    table_groups ={}
    new_blocks =[]
    for block in blocks :
        if block ['type']in [BlockType .ImageBody ,BlockType .ImageCaption ,BlockType .ImageFootnote ]:
            group_id =block ['group_id']
            if group_id not in image_groups :
                image_groups [group_id ]=[]
            image_groups [group_id ].append (block )
        elif block ['type']in [BlockType .TableBody ,BlockType .TableCaption ,BlockType .TableFootnote ]:
            group_id =block ['group_id']
            if group_id not in table_groups :
                table_groups [group_id ]=[]
            table_groups [group_id ].append (block )
        else :
            new_blocks .append (block )

    for group_id ,blocks in image_groups .items ():
        new_blocks .append (process_block_list (blocks ,BlockType .ImageBody ,BlockType .Image ))

    for group_id ,blocks in table_groups .items ():
        new_blocks .append (process_block_list (blocks ,BlockType .TableBody ,BlockType .Table ))

    return new_blocks 


def remove_outside_spans (spans ,all_bboxes ,all_discarded_blocks ):
    def get_block_bboxes (blocks ,block_type_list ):
        return [block [0 :4 ]for block in blocks if block [7 ]in block_type_list ]

    image_bboxes =get_block_bboxes (all_bboxes ,[BlockType .ImageBody ])
    table_bboxes =get_block_bboxes (all_bboxes ,[BlockType .TableBody ])
    other_block_type =[]
    for block_type in BlockType .__dict__ .values ():
        if not isinstance (block_type ,str ):
            continue 
        if block_type not in [BlockType .ImageBody ,BlockType .TableBody ]:
            other_block_type .append (block_type )
    other_block_bboxes =get_block_bboxes (all_bboxes ,other_block_type )
    discarded_block_bboxes =get_block_bboxes (all_discarded_blocks ,[BlockType .Discarded ])

    new_spans =[]

    for span in spans :
        span_bbox =span ['bbox']
        span_type =span ['type']

        if any (calculate_overlap_area_in_bbox1_area_ratio (span_bbox ,block_bbox )>0.4 for block_bbox in 
        discarded_block_bboxes ):
            new_spans .append (span )
            continue 

        if span_type ==ContentType .Image :
            if any (calculate_overlap_area_in_bbox1_area_ratio (span_bbox ,block_bbox )>0.5 for block_bbox in 
            image_bboxes ):
                new_spans .append (span )
        elif span_type ==ContentType .Table :
            if any (calculate_overlap_area_in_bbox1_area_ratio (span_bbox ,block_bbox )>0.5 for block_bbox in 
            table_bboxes ):
                new_spans .append (span )
        else :
            if any (calculate_overlap_area_in_bbox1_area_ratio (span_bbox ,block_bbox )>0.5 for block_bbox in 
            other_block_bboxes ):
                new_spans .append (span )

    return new_spans 


def parse_page_core (
    page_doc :PageableData,
    magic_model,
    page_id,
    pdf_bytes_md5,
    imageWriter,
    parse_mode,
    lang,
    checkTableContent,
):
    need_drop =False 
    drop_reason =[]

    """从magic_model对象中获取后面会用到的区块信息"""
    img_groups =magic_model .get_imgs_v2 (page_id )
    table_groups =magic_model .get_tables_v2 (page_id )

    """对image和table的区块分组"""
    img_body_blocks ,img_caption_blocks ,img_footnote_blocks =process_groups (
    img_groups ,'image_body','image_caption_list','image_footnote_list'
    )

    table_body_blocks ,table_caption_blocks ,table_footnote_blocks =process_groups (
    table_groups ,'table_body','table_caption_list','table_footnote_list'
    )

    discarded_blocks =magic_model .get_discarded (page_id )
    text_blocks =magic_model .get_text_blocks (page_id )
    title_blocks =magic_model .get_title_blocks (page_id )
    inline_equations ,interline_equations ,interline_equation_blocks =magic_model .get_equations (page_id )
    page_w ,page_h =magic_model .get_page_size (page_id )

    def merge_title_blocks (blocks ,x_distance_threshold =0.1 *page_w ):
        def merge_two_bbox (b1 ,b2 ):
            x_min =min (b1 ['bbox'][0 ],b2 ['bbox'][0 ])
            y_min =min (b1 ['bbox'][1 ],b2 ['bbox'][1 ])
            x_max =max (b1 ['bbox'][2 ],b2 ['bbox'][2 ])
            y_max =max (b1 ['bbox'][3 ],b2 ['bbox'][3 ])
            return x_min ,y_min ,x_max ,y_max 

        def merge_two_blocks (b1 ,b2 ):

            b1 ['bbox']=merge_two_bbox (b1 ,b2 )


            line1 =b1 ['lines'][0 ]
            line2 =b2 ['lines'][0 ]
            line1 ['bbox']=merge_two_bbox (line1 ,line2 )
            line1 ['spans'].extend (line2 ['spans'])

            return b1 ,b2 


        y_overlapping_blocks =[]
        title_bs =[b for b in blocks if b ['type']==BlockType .Title ]
        while title_bs :
            block1 =title_bs .pop (0 )
            current_row =[block1 ]
            to_remove =[]
            for block2 in title_bs :
                if (
                __is_overlaps_y_exceeds_threshold (block1 ['bbox'],block2 ['bbox'],0.9 )
                and len (block1 ['lines'])==1 
                and len (block2 ['lines'])==1 
                ):
                    current_row .append (block2 )
                    to_remove .append (block2 )
            for b in to_remove :
                title_bs .remove (b )
            y_overlapping_blocks .append (current_row )


        to_remove_blocks =[]
        for row in y_overlapping_blocks :
            if len (row )==1 :
                continue 


            row .sort (key =lambda x :x ['bbox'][0 ])

            merged_block =row [0 ]
            for i in range (1 ,len (row )):
                left_block =merged_block 
                right_block =row [i ]

                left_height =left_block ['bbox'][3 ]-left_block ['bbox'][1 ]
                right_height =right_block ['bbox'][3 ]-right_block ['bbox'][1 ]

                if (
                right_block ['bbox'][0 ]-left_block ['bbox'][2 ]<x_distance_threshold 
                and left_height *0.95 <right_height <left_height *1.05 
                ):
                    merged_block ,to_remove_block =merge_two_blocks (merged_block ,right_block )
                    to_remove_blocks .append (to_remove_block )
                else :
                    merged_block =right_block 

        for b in to_remove_blocks :
            blocks .remove (b )

    """将所有区块的bbox整理到一起"""

    interline_equation_blocks =[]
    if len (interline_equation_blocks )>0 :
        all_bboxes ,all_discarded_blocks ,footnote_blocks =ocr_prepare_bboxes_for_layout_split_v2 (
        img_body_blocks ,img_caption_blocks ,img_footnote_blocks ,
        table_body_blocks ,table_caption_blocks ,table_footnote_blocks ,
        discarded_blocks ,
        text_blocks ,
        title_blocks ,
        interline_equation_blocks ,
        page_w ,
        page_h ,
        )
    else :
        all_bboxes ,all_discarded_blocks ,footnote_blocks =ocr_prepare_bboxes_for_layout_split_v2 (
        img_body_blocks ,img_caption_blocks ,img_footnote_blocks ,
        table_body_blocks ,table_caption_blocks ,table_footnote_blocks ,
        discarded_blocks ,
        text_blocks ,
        title_blocks ,
        interline_equations ,
        page_w ,
        page_h ,
        )

    """获取所有的spans信息"""
    spans =magic_model .get_all_spans (page_id )

    """在删除重复span之前，应该通过image_body和table_body的block过滤一下image和table的span"""
    """顺便删除大水印并保留abandon的span"""
    spans =remove_outside_spans (spans ,all_bboxes ,all_discarded_blocks )

    """删除重叠spans中置信度较低的那些"""
    spans ,dropped_spans_by_confidence =remove_overlaps_low_confidence_spans (spans )
    """删除重叠spans中较小的那些"""
    spans ,dropped_spans_by_span_overlap =remove_overlaps_min_spans (spans )

    """根据parse_mode，构造spans，主要是文本类的字符填充"""
    if parse_mode ==SupportedPdfParseMethod .TXT :
        spans =txt_spans_extract_v2 (page_doc ,spans ,all_bboxes ,all_discarded_blocks ,lang )
    elif parse_mode ==SupportedPdfParseMethod .OCR :
        pass 
    else :
        raise Exception ('parse_mode must be txt or ocr')

    """先处理不需要排版的discarded_blocks"""
    discarded_block_with_spans ,spans =fill_spans_in_blocks (
    all_discarded_blocks ,spans ,0.4 
    )
    fix_discarded_blocks =fix_discarded_block (discarded_block_with_spans )

    """如果当前页面没有有效的bbox则跳过"""
    if len (all_bboxes )==0 :
        logger .warning (f'skip this page, not found useful bbox, page_id: {page_id }')
        return ocr_construct_page_component_v2 (
        [],
        [],
        page_id ,
        page_w ,
        page_h ,
        [],
        [],
        [],
        interline_equations ,
        fix_discarded_blocks ,
        need_drop ,
        drop_reason ,
        )

    """对image和table截图"""
    spans =ocr_cut_image_and_table (
    spans ,page_doc ,page_id ,pdf_bytes_md5 ,imageWriter 
    )

    """span填充进block"""
    block_with_spans ,spans =fill_spans_in_blocks (all_bboxes ,spans ,0.5 )

    """对block进行fix操作"""
    fix_blocks =fix_block_spans_v2 (block_with_spans )

    """同一行被断开的titile合并"""
    merge_title_blocks (fix_blocks )

    """获取所有line并计算正文line的高度"""
    line_height =get_line_height (fix_blocks )

    """获取所有line并对line排序"""
    sorted_bboxes =sort_lines_by_model (fix_blocks ,page_w ,page_h ,line_height ,footnote_blocks )

    """根据line的中位数算block的序列关系"""
    fix_blocks =cal_block_index (fix_blocks ,sorted_bboxes )

    """将image和table的block还原回group形式参与后续流程"""
    fix_blocks =revert_group_blocks (fix_blocks )

    """重排block"""
    for i ,block in enumerate (fix_blocks ):
        if 'index'not in block :
            block ['index']=i *1000 # Large spacing to avoid conflicts

    sorted_blocks =sorted (fix_blocks ,key =lambda b :b ['index'])

    """block内重排(img和table的block内多个caption或footnote的排序)"""
    for block in sorted_blocks :
        if block ['type']in [BlockType .Image ,BlockType .Table ]and 'blocks'in block :
            for i ,sub_block in enumerate (block ['blocks']):
                if 'index'not in sub_block :
                    sub_block ['index']=i *1000 
            block ['blocks']=sorted (block ['blocks'],key =lambda b :b ['index'])

    if checkTableContent:
        for block in fix_blocks:
            if block["type"] != BlockType.Table:
                continue
            likely_image = False
            for sub_block in block["blocks"]:
                if sub_block["type"] != BlockType.TableBody:
                    continue
                if any(
                    [
                        span.get("likely_image", False)
                        for line in sub_block["lines"]
                        for span in line["spans"]
                    ]
                ):
                    likely_image = True
                    break

            if not likely_image:
                continue

            block["type"] = BlockType.Image
            for sub_block in block["blocks"]:
                if sub_block["type"] == BlockType.TableBody:
                    sub_block["type"] = BlockType.ImageBody
                    for line in sub_block["lines"]:
                        for span in line["spans"]:
                            if span["type"] == ContentType.Table:
                                span["type"] = ContentType.Image
                elif sub_block["type"] == BlockType.TableCaption:
                    sub_block["type"] = BlockType.ImageCaption
                elif sub_block["type"] == BlockType.TableFootnote:
                    sub_block["type"] = BlockType.ImageFootnote

    """获取QA需要外置的list"""
    images ,tables ,interline_equations =get_qa_need_list_v2 (sorted_blocks )

    """构造pdf_info_dict"""
    page_info =ocr_construct_page_component_v2 (
    sorted_blocks ,
    [],
    page_id ,
    page_w ,
    page_h ,
    [],
    images ,
    tables ,
    interline_equations ,
    fix_discarded_blocks ,
    need_drop ,
    drop_reason ,
    )
    return page_info 


def pdf_parse_union (
model_list ,
dataset :Dataset ,
imageWriter ,
parse_mode ,
start_page_id =0 ,
end_page_id =None ,
debug_mode =False ,
lang =None ,
):

    pdf_bytes_md5 =compute_md5 (dataset .data_bits ())

    pdf_info_dict ={}

    table_config = get_table_recog_config()
    strictlyCheck = table_config.get("strictly_check", True)
    checkTableContent = strictlyCheck and parse_mode == SupportedPdfParseMethod.TXT

    magic_model =MagicModel (model_list ,dataset )

    end_page_id =(
    end_page_id 
    if end_page_id is not None and end_page_id >=0 
    else len (dataset )-1 
    )

    if end_page_id >len (dataset )-1 :
        logger .warning ('end_page_id is out of range, use pdf_docs length')
        end_page_id =len (dataset )-1 


        # start_time = time.time()

        # for page_id, page in enumerate(dataset):
    for page_id ,page in tqdm (enumerate (dataset ),total =len (dataset ),desc ="Processing pages"):

    # if debug_mode:
    # time_now = time.time()
    # logger.info(
    #     f'page_id: {page_id}, last_page_cost_time: {round(time.time() - start_time, 2)}'
    # )
    # start_time = time_now


        if start_page_id <=page_id <=end_page_id :
            page_info =parse_page_core (
            page ,magic_model ,page_id ,pdf_bytes_md5 ,imageWriter ,parse_mode ,lang ,checkTableContent
            )
        else :
            page_info =page .get_page_info ()
            page_w =page_info .w 
            page_h =page_info .h 
            page_info =ocr_construct_page_component_v2 (
            [],[],page_id ,page_w ,page_h ,[],[],[],[],[],True ,'skip page'
            )
        pdf_info_dict [f'page_{page_id }']=page_info 

    need_ocr_list =[]
    img_crop_list =[]
    text_block_list =[]
    for pange_id ,page_info in pdf_info_dict .items ():
        for block in page_info ['preproc_blocks']:
            if block ['type']in ['table','image']:
                for sub_block in block ['blocks']:
                    if sub_block ['type']in ['image_caption','image_footnote','table_caption','table_footnote']:
                        text_block_list .append (sub_block )
            elif block ['type']in ['text','title']:
                text_block_list .append (block )
        for block in page_info ['discarded_blocks']:
            text_block_list .append (block )
    for block in text_block_list :
        for line in block ['lines']:
            for span in line ['spans']:
                if 'np_img'in span :
                    need_ocr_list .append (span )
                    img_crop_list .append (span ['np_img'])
                    span .pop ('np_img')
    if len (img_crop_list )>0 :
    # Get OCR results for this language's images
        atom_model_manager =AtomModelSingleton ()
        ocr_model =atom_model_manager .get_atom_model (
        atom_model_name ='ocr',
        ocr_show_log =False ,
        det_db_box_thresh =0.3 ,
        lang =lang 
        )
        # rec_start = time.time()
        ocr_res_list =ocr_model .ocr (img_crop_list ,det =False ,tqdm_enable =True )[0 ]
        # Verify we have matching counts
        assert len (ocr_res_list )==len (need_ocr_list ),f'ocr_res_list: {len (ocr_res_list )}, need_ocr_list: {len (need_ocr_list )}'
        # Process OCR results for this language
        for index ,span in enumerate (need_ocr_list ):
            ocr_text ,ocr_score =ocr_res_list [index ]
            span ['content']=ocr_text 
            span ['score']=float (f"{ocr_score :.3f}")
            # rec_time = time.time() - rec_start
            # logger.info(f'ocr-dynamic-rec time: {round(rec_time, 2)}, total images processed: {len(img_crop_list)}')


    """分段"""
    para_split (pdf_info_dict )


    llm_aided_config =get_llm_aided_config ()


    if llm_aided_config is not None and isinstance (llm_aided_config ,dict ):

        formula_aided_config =llm_aided_config .get ('formula_aided',None )
        if formula_aided_config is not None and formula_aided_config .get ('enable',False ):
            llm_aided_formula (pdf_info_dict ,formula_aided_config )

        text_aided_config =llm_aided_config .get ('text_aided',None )
        if text_aided_config is not None and text_aided_config .get ('enable',False ):
            llm_aided_text_start_time =time .time ()
            llm_aided_text (pdf_info_dict ,text_aided_config )
            logger .info (f'llm aided text time: {round (time .time ()-llm_aided_text_start_time ,2 )}')

        title_aided_config =llm_aided_config .get ('title_aided',None )
        if title_aided_config is not None and title_aided_config .get ('enable',False ):
            llm_aided_title_start_time =time .time ()
            llm_aided_title (pdf_info_dict ,title_aided_config )
            logger .info (f'llm aided title time: {round (time .time ()-llm_aided_title_start_time ,2 )}')


    enrichment_config =get_enrichment_config ()
    if enrichment_config is not None :
    # Get the images directory from the imageWriter
        images_dir =None 
        try :
        # Try to get the base directory from the imageWriter
            if hasattr (imageWriter ,'_parent_dir'):
                images_dir =imageWriter ._parent_dir 
                logger .debug (f'Using images directory from _parent_dir: {images_dir }')
                # If we can't get the directory directly, try to find it in the PDF info
            if not images_dir and 'pdf_info'in pdf_info_dict and len (pdf_info_dict ['pdf_info'])>0 :
                first_page =pdf_info_dict ['pdf_info'][0 ]
                if 'image_path'in first_page :
                # Extract the directory from the first image path
                    images_dir =os .path .dirname (first_page ['image_path'])
                    logger .debug (f'Extracted images directory from image_path: {images_dir }')

            if not images_dir :
                logger .warning ('Could not determine images directory for summarization')
            else :
            # Ensure the directory exists
                if not os .path .exists (images_dir ):
                    logger .warning (f'Images directory does not exist: {images_dir }')
                    images_dir =None 
        except Exception as e :
            logger .error (f'Error getting images directory: {e }')
            images_dir =None 

        process_enrichments (pdf_info_dict ,enrichment_config ,images_dir )
        logger .debug (f"Using images directory: {images_dir }"if images_dir else "No images directory available")

    if 'signature_data' in locals() and signature_data and any(signature_data):
        for page_idx, page_sigs in enumerate(signature_data):
            if not page_sigs:
                continue
            page_key = f'page_{page_idx}'
            if page_key in pdf_info_dict:
                if 'para_blocks' not in pdf_info_dict[page_key]:
                    pdf_info_dict[page_key]['para_blocks'] = []
                for sig in page_sigs:
                    sig_block = {
                        'type': 'signature',
                        'bbox': sig.get('bbox', []),
                        'confidence': sig.get('score', sig.get('confidence', 0.0)),
                        'image_path': sig.get('image_path', ''),
                        'page_idx': page_idx
                    }
                    pdf_info_dict[page_key]['para_blocks'].append(sig_block)
    pdf_info_list = dict_to_list(pdf_info_dict)
    new_pdf_info_dict = {
        'pdf_info': pdf_info_list,
        'signature_data': signature_data if 'signature_data' in locals() else []
    }

    clean_memory (get_device ())

    return new_pdf_info_dict 


if __name__ =='__main__':
    pass 
