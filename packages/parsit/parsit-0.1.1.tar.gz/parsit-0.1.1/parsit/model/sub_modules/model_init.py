import torch 
from loguru import logger 

from parsit .config .constants import MODEL_NAME 
from parsit .model .model_list import AtomicModel 
from parsit .model .sub_modules .language_detection .yolov11 .YOLOv11 import YOLOv11LangDetModel 
from parsit .model .sub_modules .layout .doclayout_yolo .DocLayoutYOLO import DocLayoutYOLOModel 
from parsit .model .sub_modules .mfd .yolov8 .YOLOv8 import YOLOv8MFDModel 
from parsit .model .sub_modules .mfr .unimernet .Unimernet import UnimernetModel 
from parsit .model .sub_modules .ocr .paddleocr2pytorch .pytorch_paddle import PytorchPaddleOCR 
from parsit .model .sub_modules .table .rapidtable .rapid_table import RapidTableModel 
from parsit .model .sub_modules .signature .yolov8_signature .YOLOv8 import YOLOv8SignatureModel 
# try:
#     from magic_pdf_ascend_plugin.libs.license_verifier import (
#         LicenseExpiredError, LicenseFormatError, LicenseSignatureError,
#         load_license)
#     from magic_pdf_ascend_plugin.model_plugin.ocr.paddleocr.ppocr_273_npu import ModifiedPaddleOCR
#     from magic_pdf_ascend_plugin.model_plugin.table.rapidtable.rapid_table_npu import RapidTableModel
#     license_key = load_license()
#     logger.info(f'Using Ascend Plugin Success, License id is {license_key["payload"]["id"]},'
#                 f' License expired at {license_key["payload"]["date"]["end_date"]}')
# except Exception as e:
#     if isinstance(e, ImportError):
#         pass
#     elif isinstance(e, LicenseFormatError):
#         logger.error('Ascend Plugin: Invalid license format. Please check the license file.')
#     elif isinstance(e, LicenseSignatureError):
#         logger.error('Ascend Plugin: Invalid signature. The license may be tampered with.')
#     elif isinstance(e, LicenseExpiredError):
#         logger.error('Ascend Plugin: License has expired. Please renew your license.')
#     elif isinstance(e, FileNotFoundError):
#         logger.error('Ascend Plugin: Not found License file.')
#     else:
#         logger.error(f'Ascend Plugin: {e}')
#     from parsit.model.sub_modules.ocr.paddleocr.ppocr_273_mod import ModifiedPaddleOCR
#     # from parsit.model.sub_modules.ocr.paddleocr.ppocr_291_mod import ModifiedPaddleOCR
#     from parsit.model.sub_modules.table.rapidtable.rapid_table import RapidTableModel


def table_model_init (table_model_type ,model_path ,max_time ,_device_ ='cpu',lang =None ,table_sub_model_name =None ):
    if table_model_type ==MODEL_NAME .STRUCT_EQTABLE :
        from parsit .model .sub_modules .table .structeqtable .struct_eqtable import StructTableModel 
        table_model =StructTableModel (model_path ,max_new_tokens =2048 ,max_time =max_time )
    elif table_model_type ==MODEL_NAME .TABLE_MASTER :
        from parsit .model .sub_modules .table .tablemaster .tablemaster_paddle import TableMasterPaddleModel 
        config ={
        'model_dir':model_path ,
        'device':_device_ 
        }
        table_model =TableMasterPaddleModel (config )
    elif table_model_type ==MODEL_NAME .RAPID_TABLE :
        atom_model_manager =AtomModelSingleton ()
        ocr_engine =atom_model_manager .get_atom_model (
        atom_model_name ='ocr',
        ocr_show_log =False ,
        det_db_box_thresh =0.5 ,
        det_db_unclip_ratio =1.6 ,
        lang =lang 
        )
        table_model =RapidTableModel (ocr_engine ,table_sub_model_name )
    else :
        logger .error ('table model type not allow')
        exit (1 )

    return table_model 


def mfd_model_init (weight ,device ='cpu'):
    if str (device ).startswith ('npu'):
        device =torch .device (device )
    mfd_model =YOLOv8MFDModel (weight ,device )
    return mfd_model 


def mfr_model_init (weight_dir ,cfg_path ,device ='cpu'):
    mfr_model =UnimernetModel (weight_dir ,cfg_path ,device )
    return mfr_model 


def layout_model_init (weight ,config_file ,device ):
    from parsit .model .sub_modules .layout .layoutlmv3 .model_init import Layoutlmv3_Predictor 
    model =Layoutlmv3_Predictor (weight ,config_file ,device )
    return model 


def doclayout_yolo_model_init (weight ,device ='cpu'):
    if str (device ).startswith ('npu'):
        device =torch .device (device )
    model =DocLayoutYOLOModel (weight ,device )
    return model 


def langdetect_model_init (langdetect_model_weight ,device ='cpu'):
    if str (device ).startswith ('npu'):
        device =torch .device (device )
    model =YOLOv11LangDetModel (langdetect_model_weight ,device )
    return model 


def ocr_model_init (show_log :bool =False ,
det_db_box_thresh =0.3 ,
lang =None ,
use_dilation =True ,
det_db_unclip_ratio =1.8 ,
):
    if lang is not None and lang !='':
    # model = ModifiedPaddleOCR(
        model =PytorchPaddleOCR (
        show_log =show_log ,
        det_db_box_thresh =det_db_box_thresh ,
        lang =lang ,
        use_dilation =use_dilation ,
        det_db_unclip_ratio =det_db_unclip_ratio ,
        )
    else :
    # model = ModifiedPaddleOCR(
        model =PytorchPaddleOCR (
        show_log =show_log ,
        det_db_box_thresh =det_db_box_thresh ,
        use_dilation =use_dilation ,
        det_db_unclip_ratio =det_db_unclip_ratio ,
        )
    return model 


class AtomModelSingleton :
    _instance =None 
    _models ={}

    def __new__ (cls ,*args ,**kwargs ):
        if cls ._instance is None :
            cls ._instance =super ().__new__ (cls )
        return cls ._instance 

    def get_atom_model (self ,atom_model_name :str ,**kwargs ):

        lang =kwargs .get ('lang',None )
        layout_model_name =kwargs .get ('layout_model_name',None )
        table_model_name =kwargs .get ('table_model_name',None )

        if atom_model_name in [AtomicModel .OCR ]:
            key =(atom_model_name ,lang )
        elif atom_model_name in [AtomicModel .Layout ]:
            key =(atom_model_name ,layout_model_name )
        elif atom_model_name in [AtomicModel .Table ]:
            key =(atom_model_name ,table_model_name ,lang )
        else :
            key =atom_model_name 

        if key not in self ._models :
            self ._models [key ]=atom_model_init (model_name =atom_model_name ,**kwargs )
        return self ._models [key ]

def atom_model_init (model_name :str ,**kwargs ):
    logger.info(f'Initializing model: {model_name}')
    logger.debug(f'Model kwargs: {kwargs}')
    
    if model_name ==MODEL_NAME .YOLO_V8_MFD :
        logger.debug('Initializing YOLO_V8_MFD model')
        return mfd_model_init (**kwargs )
    elif model_name ==MODEL_NAME .UniMerNet_v2_Small :
        logger.debug('Initializing UniMerNet_v2_Small model')
        return mfr_model_init (**kwargs )
    elif model_name ==MODEL_NAME .LAYOUTLMv3 :
        logger.debug('Initializing LAYOUTLMv3 model')
        return layout_model_init (**kwargs )
    elif model_name ==MODEL_NAME .DocLayout_YOLO :
        logger.debug('Initializing DocLayout_YOLO model')
        return doclayout_yolo_model_init (**kwargs )
    elif model_name ==MODEL_NAME .YOLO_V11_LangDetect :
        logger.debug('Initializing YOLO_V11_LangDetect model')
        return langdetect_model_init (**kwargs )
    elif model_name ==MODEL_NAME .RAPID_TABLE :
        logger.debug('Initializing RAPID_TABLE model')
        return table_model_init (MODEL_NAME .RAPID_TABLE ,**kwargs )
    elif model_name ==MODEL_NAME .TABLE_MASTER :
        logger.debug('Initializing TABLE_MASTER model')
        return table_model_init (MODEL_NAME .TABLE_MASTER ,**kwargs )
    elif model_name ==MODEL_NAME .STRUCT_EQTABLE :
        logger.debug('Initializing STRUCT_EQTABLE model')
        return table_model_init (MODEL_NAME .STRUCT_EQTABLE ,**kwargs )
    elif model_name == MODEL_NAME.YOLO_V8_SIGNATURE:
        logger.debug('Initializing YOLO_V8_SIGNATURE model')
        weight = kwargs.get('weight')
        device = kwargs.get('device', 'cpu')
        return YOLOv8SignatureModel(weight=weight, device=device)
    elif model_name ==AtomicModel .MFR :
        logger.debug('Initializing MFR model')
        atom_model =mfr_model_init (
        kwargs .get ('mfr_weight_dir'),
        kwargs .get ('mfr_cfg_path'),
        kwargs .get ('device')
        )
    elif model_name ==AtomicModel .OCR :
        logger.debug('Initializing OCR model')
        atom_model =ocr_model_init (
        kwargs .get ('ocr_show_log'),
        kwargs .get ('det_db_box_thresh'),
        kwargs .get ('lang'),
        )
    elif model_name ==AtomicModel .Table :
        logger.debug('Initializing Table model')
        atom_model =table_model_init (
        kwargs .get ('table_model_name'),
        kwargs .get ('table_model_path'),
        kwargs .get ('table_max_time'),
        kwargs .get ('device'),
        kwargs .get ('lang'),
        kwargs .get ('table_sub_model_name')
        )
    elif model_name ==AtomicModel .LangDetect :
        logger.debug('Initializing LangDetect model')
        if kwargs .get ('langdetect_model_name')==MODEL_NAME .YOLO_V11_LangDetect :
            atom_model =langdetect_model_init (
            kwargs .get ('langdetect_model_weight'),
            kwargs .get ('device')
            )
        else :
            logger.error(f'Langdetect model name not allowed: {kwargs.get("langdetect_model_name")}')
            exit (1 )
    else :
        logger.error(f'Model name not allowed: {model_name}')
        logger.error(f'Available model names: {[x for x in dir(MODEL_NAME) if not x.startswith("__")]}')
        exit (1 )

    if atom_model is None :
        logger.error(f'Model initialization failed for {model_name} with kwargs: {kwargs}')
        exit (1 )
    else :
        return atom_model 
