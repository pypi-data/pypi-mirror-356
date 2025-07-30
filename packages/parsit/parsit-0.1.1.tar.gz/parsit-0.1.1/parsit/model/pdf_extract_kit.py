# flake8: noqa
import os 
import time 

import cv2 
import torch 
import yaml 
from loguru import logger 

os .environ ['NO_ALBUMENTATIONS_UPDATE']='1'

from parsit .config .constants import *
from parsit .model .model_list import AtomicModel 
from parsit .model .sub_modules .model_init import AtomModelSingleton 
from parsit .model .sub_modules .model_utils import (
clean_vram ,crop_img ,get_res_list_from_layout_res )
from parsit .model .sub_modules .ocr .paddleocr2pytorch .ocr_utils import (
get_adjusted_mfdetrec_res ,get_ocr_result_list )


class CustomPEKModel :

    def __init__ (self ,ocr :bool =False ,show_log :bool =False ,**kwargs ):
        """
        ======== model init ========
        """

        current_file_path =os .path .abspath (__file__ )

        current_dir =os .path .dirname (current_file_path )

        root_dir =os .path .dirname (current_dir )

        model_config_dir =os .path .join (root_dir ,'resources','model_config')

        config_path =os .path .join (model_config_dir ,'model_configs.yaml')
        with open (config_path ,'r',encoding ='utf-8')as f :
            self .configs =yaml .load (f ,Loader =yaml .FullLoader )


            # layout config
        self .layout_config =kwargs .get ('layout_config')
        self .layout_model_name =self .layout_config .get (
        'model',MODEL_NAME .DocLayout_YOLO 
        )

        # formula config
        self .formula_config =kwargs .get ('formula_config')
        self .mfd_model_name =self .formula_config .get (
        'mfd_model',MODEL_NAME .YOLO_V8_MFD 
        )
        self .mfr_model_name =self .formula_config .get (
        'mfr_model',MODEL_NAME .UniMerNet_v2_Small 
        )
        self .apply_formula =self .formula_config .get ('enable',True )

        # table config
        self .table_config =kwargs .get ('table_config')
        self .apply_table =self .table_config .get ('enable',False )
        self .table_max_time =self .table_config .get ('max_time',TABLE_MAX_TIME_VALUE )
        self .table_model_name =self .table_config .get ('model',MODEL_NAME .RAPID_TABLE )
        self .table_sub_model_name =self .table_config .get ('sub_model',None )

        # ocr config
        self .apply_ocr = ocr 
        self .lang = kwargs .get ('lang', None )

        # signature config
        self .signature_config = kwargs .get ('signature_config', {} )
        self .apply_signature = self .signature_config .get ('enable', False )
        self .signature_model_name = self .signature_config .get ('model', MODEL_NAME .YOLO_V8_SIGNATURE )

        logger .info (
        'DocAnalysis init, this may take some times, layout_model: {}, apply_formula: {}, apply_ocr: {}, '
        'apply_table: {}, table_model: {}, apply_signature: {}, lang: {}'.format (
        self .layout_model_name ,
        self .apply_formula ,
        self .apply_ocr ,
        self .apply_table ,
        self .table_model_name ,
        self .apply_signature ,
        self .lang ,
        )
        )

        self .device =kwargs .get ('device','cpu')

        logger .info ('using device: {}'.format (self .device ))
        models_dir =kwargs .get (
        'models_dir',os .path .join (root_dir ,'resources','models')
        )
        logger .info ('using models_dir: {}'.format (models_dir ))

        atom_model_manager =AtomModelSingleton ()


        if self .apply_formula :

            self .mfd_model =atom_model_manager .get_atom_model (
            atom_model_name =AtomicModel .MFD ,
            mfd_weights =str (
            os .path .join (
            models_dir ,self .configs ['weights'][self .mfd_model_name ]
            )
            ),
            device =self .device ,
            )


            mfr_weight_dir =str (
            os .path .join (models_dir ,self .configs ['weights'][self .mfr_model_name ])
            )
            mfr_cfg_path =str (os .path .join (model_config_dir ,'UniMERNet','demo.yaml'))

            self .mfr_model =atom_model_manager .get_atom_model (
            atom_model_name =AtomicModel .MFR ,
            mfr_weight_dir =mfr_weight_dir ,
            mfr_cfg_path =mfr_cfg_path ,
            device =self .device ,
            )


        if self .layout_model_name == MODEL_NAME.LAYOUTLMv3:
            self.layout_model = atom_model_manager.get_atom_model(
                atom_model_name=MODEL_NAME.LAYOUTLMv3,
                layout_weights=str(
                    os.path.join(
                        models_dir, self.configs['weights'][self.layout_model_name]
                    )
                ),
                layout_config_file=str(
                    os.path.join(
                        model_config_dir, 'layoutlmv3', 'layoutlmv3_base_inference.yaml'
                    )
                ),
                device='cpu' if str(self.device).startswith("mps") else self.device,
            )
        elif self.layout_model_name == MODEL_NAME.DocLayout_YOLO:
            self.layout_model = atom_model_manager.get_atom_model(
                atom_model_name=MODEL_NAME.DocLayout_YOLO,
                weight=str(
                    os.path.join(
                        models_dir, self.configs['weights'][self.layout_model_name]
                    )
                ),
                device=self.device,
            )

        self .ocr_model =atom_model_manager .get_atom_model (
        atom_model_name =AtomicModel .OCR ,
        ocr_show_log =show_log ,
        det_db_box_thresh =0.3 ,
        lang =self .lang 
        )
        # init table model
        if self .apply_table :
            table_model_dir =self .configs ['weights'][self .table_model_name ]
            self .table_model =atom_model_manager .get_atom_model (
            atom_model_name =AtomicModel .Table ,
            table_model_name =self .table_model_name ,
            table_model_path =str (os .path .join (models_dir ,table_model_dir )),
            table_max_time =self .table_max_time ,
            device =self .device ,
            ocr_engine =self .ocr_model ,
            table_sub_model_name =self .table_sub_model_name 
            )
            
        # signature model
        if self.apply_signature:
            try:
                self.signature_model = atom_model_manager.get_atom_model(
                    atom_model_name=self.signature_model_name,
                    weight=str(os.path.join(models_dir, self.configs['weights'][self.signature_model_name])),
                    device=self.device,
                )
                logger.info('Signature model initialized successfully')
            except Exception as e:
                logger.warning(f'Failed to initialize signature model: {str(e)}')
                self.apply_signature = False

        logger .info ('DocAnalysis init done!')

    def __call__(self, image, output_dir=None):
        # Store original image for signature detection
        original_image = image.copy()
        
        # Run layout detection
        layout_start = time.time()
        layout_res = []
        if self.layout_model_name == MODEL_NAME.LAYOUTLMv3:
            # layoutlmv3
            layout_res = self.layout_model(image, ignore_catids=[])
        elif self.layout_model_name == MODEL_NAME.DocLayout_YOLO:
            layout_res = self.layout_model.predict(image)

        layout_cost = round(time.time() - layout_start, 2)
        logger.info(f'layout detection time: {layout_cost}')
        
        # Run signature detection if enabled
        if self.apply_signature and hasattr(self, 'signature_model'):
            try:
                signature_start = time.time()
                # Get signature detections
                signature_detections = self.signature_model.detect(original_image)
                signature_cost = round(time.time() - signature_start, 2)
                logger.info(f'signature detection time: {signature_cost}, found {len(signature_detections)} signatures')
                
                # Process and save signature detections
                for i, detection in enumerate(signature_detections):
                    # Add to layout results
                    signature_res = {
                        'bbox': detection['bbox'],  # [x1, y1, x2, y2]
                        'category_id': CATEGORY_ID.SIGNATURE,  # Make sure this is defined in your constants
                        'score': float(detection['confidence']),
                        'type': 'signature'
                    }
                    layout_res.append(signature_res)
                    
                    # Save cropped signature image if output_dir is provided
                    if output_dir:
                        from parsit.utils.image_utils import save_cropped_image
                        os.makedirs(output_dir, exist_ok=True)
                        output_path = os.path.join(output_dir, f'signature_{i}.png')
                        x1, y1, x2, y2 = map(int, detection['bbox'])
                        cropped_img = original_image[y1:y2, x1:x2]
                        save_cropped_image(cropped_img, output_path)
                        logger.info(f'Saved signature to {output_path}')
                        
            except Exception as e:
                logger.warning(f'Error during signature detection: {str(e)}')

        if self .apply_formula :

            mfd_start =time .time ()
            mfd_res =self .mfd_model .predict (image )
            logger .info (f'mfd time: {round (time .time ()-mfd_start ,2 )}')


            mfr_start =time .time ()
            formula_list =self .mfr_model .predict (mfd_res ,image )
            layout_res .extend (formula_list )
            mfr_cost =round (time .time ()-mfr_start ,2 )
            logger .info (f'formula nums: {len (formula_list )}, mfr time: {mfr_cost }')


        clean_vram (self .device ,vram_threshold =6 )


        ocr_res_list ,table_res_list ,single_page_mfdetrec_res =(
        get_res_list_from_layout_res (layout_res )
        )


        ocr_start =time .time ()
        # Process each area that requires OCR processing
        for res in ocr_res_list :
            new_image ,useful_list =crop_img (res ,image ,crop_paste_x =50 ,crop_paste_y =50 )
            adjusted_mfdetrec_res =get_adjusted_mfdetrec_res (single_page_mfdetrec_res ,useful_list )

            # OCR recognition
            new_image =cv2 .cvtColor (new_image ,cv2 .COLOR_RGB2BGR )

            if self .apply_ocr :
                ocr_res =self .ocr_model .ocr (new_image ,mfd_res =adjusted_mfdetrec_res )[0 ]
            else :
                ocr_res =self .ocr_model .ocr (new_image ,mfd_res =adjusted_mfdetrec_res ,rec =False )[0 ]

                # Integration results
            if ocr_res :
                ocr_result_list =get_ocr_result_list (ocr_res ,useful_list )
                layout_res .extend (ocr_result_list )

        ocr_cost =round (time .time ()-ocr_start ,2 )
        if self .apply_ocr :
            logger .info (f"ocr time: {ocr_cost }")
        else :
            logger .info (f"det time: {ocr_cost }")

        # debug_dir = Path("debug_out").absolute()
        # debug_dir.mkdir(exist_ok=True, parents=True)
        # logger.warning(f"Debug images will be saved to: {debug_dir}")
        if self .apply_table :
            table_start =time .time ()
            for  res in table_res_list:
                # debug_file = debug_dir / f"debug_table_p{idx}_{timestamp}.jpg"
                # logger.warning(f"saving debug image to: {debug_file}")
                # cv2.imwrite(str(debug_file), cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
                print(image)
                new_image ,_ =crop_img (res ,image )
                print(image)
                # debug_file = debug_dir / f"debug_table_p{idx}_{timestamp}.jpg"
                # logger.warning(f"saving debug image to: {debug_file}")
                # cv2.imwrite(str(debug_file), cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR))
                single_table_start_time =time .time ()
                html_code =None 
                if self .table_model_name ==MODEL_NAME .STRUCT_EQTABLE :
                    with torch .no_grad ():
                        table_result =self .table_model .predict (new_image ,'html')
                        if len (table_result )>0 :
                            html_code =table_result [0 ]
                elif self .table_model_name ==MODEL_NAME .TABLE_MASTER :
                    html_code =self .table_model .img2html (new_image )
                elif self .table_model_name ==MODEL_NAME .RAPID_TABLE :
                    html_code ,table_cell_bboxes ,logic_points ,elapse =self .table_model .predict (
                    new_image 
                    )
                run_time =time .time ()-single_table_start_time 
                if run_time >self .table_max_time :
                    logger .warning (
                    f'table recognition processing exceeds max time {self .table_max_time }s'
                    )

                if html_code :
                    expected_ending =html_code .strip ().endswith (
                    '</html>'
                    )or html_code .strip ().endswith ('</table>')
                    if expected_ending :
                        res ['html']=html_code 
                    else :
                        logger .warning (
                        'table recognition processing fails, not found expected HTML table end'
                        )
                else :
                    logger .warning (
                    'table recognition processing fails, not get html return'
                    )
            logger .info (f'table time: {round (time .time ()-table_start ,2 )}')

        return layout_res 
