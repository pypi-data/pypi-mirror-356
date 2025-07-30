
import json 
import os 
from typing import Dict, Any, Optional

from loguru import logger 

from parsit.config.constants import MODEL_NAME 
from parsit.libs.commons import parse_bucket_key 


CONFIG_FILE_NAME =os .getenv ('PARSIT_TOOLS_CONFIG_JSON','parsit-pdf.json')
DEFAULT_CONFIG = {}

_cached_config = None

def read_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Read configuration from a file or return default config."""
    global _cached_config
    
    # Return cached config if available
    if _cached_config is not None:
        return _cached_config
    
    if config_path is None:
        config_path = os.path.join(os.path.expanduser('~'), CONFIG_FILE_NAME)
    
    logger.info(f'Reading configuration from {config_path}')
    
    if not os.path.exists(config_path):
        logger.warning(f'Config file not found at {config_path}, using default config')
        _cached_config = DEFAULT_CONFIG.copy()
        return _cached_config
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            _cached_config = json.load(f)
        return _cached_config
    except Exception as e:
        logger.error(f'Error reading config file: {str(e)}')
        _cached_config = DEFAULT_CONFIG.copy()
        return _cached_config


def get_s3_config (bucket_name :str ):

    config =read_config ()

    bucket_info =config .get ('bucket_info')
    if bucket_name not in bucket_info :
        access_key ,secret_key ,storage_endpoint =bucket_info ['[default]']
    else :
        access_key ,secret_key ,storage_endpoint =bucket_info [bucket_name ]

    if access_key is None or secret_key is None or storage_endpoint is None :
        raise Exception (f'ak, sk or endpoint not found in {CONFIG_FILE_NAME }')

        # logger.info(f"get_s3_config: ak={access_key}, sk={secret_key}, endpoint={storage_endpoint}")

    return access_key ,secret_key ,storage_endpoint 


def get_s3_config_dict (path :str ):
    access_key ,secret_key ,storage_endpoint =get_s3_config (get_bucket_name (path ))
    return {'ak':access_key ,'sk':secret_key ,'endpoint':storage_endpoint }


def get_bucket_name (path ):
    bucket ,key =parse_bucket_key (path )
    return bucket 


def get_local_models_dir ():
    config =read_config ()
    models_dir =config .get ('models-dir')
    if models_dir is None :
        logger .warning (f"'models-dir' not found in {CONFIG_FILE_NAME }, use '/tmp/models' as default")
        return '/tmp/models'
    else :
        return models_dir 


def get_local_layoutreader_model_dir ():
    config =read_config ()
    layoutreader_model_dir =config .get ('layoutreader-model-dir')
    if layoutreader_model_dir is None or not os .path .exists (layoutreader_model_dir ):
        home_dir =os .path .expanduser ('~')
        layoutreader_at_modelscope_dir_path =os .path .join (home_dir ,'.cache/modelscope/hub/ppaanngggg/layoutreader')
        logger .warning (f"'layoutreader-model-dir' not exists, use {layoutreader_at_modelscope_dir_path } as default")
        return layoutreader_at_modelscope_dir_path 
    else :
        return layoutreader_model_dir 


def get_device ():
    config =read_config ()
    device =config .get ('device-mode')
    if device is None :
        logger .warning (f"'device-mode' not found in {CONFIG_FILE_NAME }, use 'cpu' as default")
        return 'cpu'
    else :
        return device 


def get_table_recog_config ():
    config =read_config ()
    table_config =config .get ('table-config')
    if table_config is None :
        logger .warning (f"'table-config' not found in {CONFIG_FILE_NAME }, use 'False' as default")
        return json .loads (f'{{"model": "{MODEL_NAME .RAPID_TABLE }","enable": false, "max_time": 400}}')
    else :
        return table_config 


def get_layout_config ():
    config =read_config ()
    layout_config =config .get ('layout-config')
    if layout_config is None :
        logger .warning (f"'layout-config' not found in {CONFIG_FILE_NAME }, use '{MODEL_NAME .LAYOUTLMv3 }' as default")
        return json .loads (f'{{"model": "{MODEL_NAME .LAYOUTLMv3 }"}}')
    else :
        return layout_config 


def get_formula_config ():
    config =read_config ()
    formula_config =config .get ('formula-config')
    if formula_config is None :
        logger .warning (f"'formula-config' not found in {CONFIG_FILE_NAME }, use 'True' as default")
        return json .loads (f'{{"mfd_model": "{MODEL_NAME .YOLO_V8_MFD }","mfr_model": "{MODEL_NAME .UniMerNet_v2_Small }","enable": true}}')
    else :
        return formula_config 

def get_llm_aided_config ():
    config =read_config ()
    llm_aided_config =config .get ('llm-aided-config')
    if llm_aided_config is None :
        logger .warning (f"'llm-aided-config' not found in {CONFIG_FILE_NAME }, use 'None' as default")
        return False 
    else :
        return llm_aided_config 


def get_enrichment_config ():
    config =read_config ()
    enrichment_config =config .get ('enrichment-config')
    if enrichment_config is None :
        logger .warning (f"'enrichment-config' not found in {CONFIG_FILE_NAME }, use 'None' as default")
        return None 
    return enrichment_config 


def get_latex_delimiter_config():
    config = read_config()
    return config.get('latex-delimiter-config', {
        'display': {'left': '$$', 'right': '$$'},
        'inline': {'left': '$', 'right': '$'}
    })


def get_convert_html_tables_config():
    """
    Get HTML table conversion configuration.
    
    Returns:
        dict: Dictionary with 'enable' (bool) and 'fallback_to_html' (bool) options
    """
    config = read_config()
    
    # Check for legacy config (direct boolean)
    if 'convert-html-tables' in config:
        return {
            'enable': config.get('convert-html-tables', False),
            'fallback_to_html': True  # Default to True for backward compatibility
        }
    
    # Check for new config structure
    html_config = config.get('html_table_conversion', {})
    return {
        'enable': html_config.get('enable', False),
        'fallback_to_html': html_config.get('fallback_to_html', True)
    }


def get_signature_config():
    """
    Get signature detection configuration.
    
    Returns:
        dict: Dictionary with signature detection configuration
    """
    config = read_config()
    signature_config = config.get('signature-config', {})
    
    # Default values if not specified in config
    default_config = {
        'enable': False,
        'model': 'yolo_v8_signature',
        'confidence_threshold': 0.5,
        'iou_threshold': 0.45,
        'device': 'auto',
        'model_weight': 'yolov8n-signature.pt'
    }
    
    # Update default values with any user-specified values
    for key, value in signature_config.items():
        if key in default_config:
            default_config[key] = value
    
    return default_config


if __name__ =='__main__':
    ak ,sk ,endpoint =get_s3_config ('llm-raw')
