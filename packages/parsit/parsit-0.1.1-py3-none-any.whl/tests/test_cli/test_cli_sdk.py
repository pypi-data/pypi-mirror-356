"""test cli and sdk."""
import logging 
import os 
import sys
import pytest 

# Add the test_cli directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.test_cli.conf import conf
from tests.test_cli.lib import common

import time 
import parsit.model as model_config 
from parsit.data.read_api import read_local_images 
from parsit.data.read_api import read_local_office
from parsit.data.data_reader_writer import S3DataReader, S3DataWriter 
from parsit.config.make_content_config import DropMode, MakeMode 
from parsit.data.data_reader_writer import FileBasedDataWriter, FileBasedDataReader 
from parsit.data.dataset import PymuDocDataset 
from parsit.model.doc_analyze_by_custom_model import doc_analyze 
from parsit.config.enums import SupportedPdfParseMethod 

# Get paths from config
pdf_res_path = conf.conf['pdf_res_path']
code_path = conf.conf['code_path']
pdf_dev_path = conf.conf['pdf_dev_path']

# Use the parsit-pdf.json from the project root
magic_pdf_config = os.path.abspath(os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    'parsit-pdf.json'
))

class TestCli :
    """test cli."""
    @pytest.fixture(autouse=True)
    def setup(self):
        """
        Initialize test environment
        """
        # Skip GPU tests if CUDA is not available
        try:
            import torch
            if not torch.cuda.is_available():
                pytest.skip("CUDA is not available, skipping GPU tests")
        except ImportError:
            pytest.skip("PyTorch is not installed, skipping GPU tests")
            
        # Create necessary directories
        os.makedirs(os.path.join(pdf_dev_path, 'pdf', 'images'), exist_ok=True)
        os.makedirs(os.path.join(pdf_dev_path, 'parsit'), exist_ok=True)
        
        # Update config file if it exists
        if os.path.exists(magic_pdf_config):
            common.update_config_file(magic_pdf_config, "device-mode", "cuda")

        yield 

    @pytest.mark.P0 
    def test_pdf_local_sdk(self):
        """Test PDF SDK with local files."""
        demo_names = []
        pdf_path = os.path.join(pdf_dev_path, 'pdf')
        
        # Create a test PDF if it doesn't exist
        test_pdf = os.path.join(pdf_path, 'test.pdf')
        if not os.path.exists(test_pdf):
            os.makedirs(pdf_path, exist_ok=True)
            with open(test_pdf, 'wb') as f:
                f.write(b'%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n3 0 obj<</Type/Page/Parent 2 0 R/Resources<</Font<</F1 4 0 R>>>>/Contents 5 0 R>>endobj\n4 0 obj<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>endobj\n5 0 obj<</Length 44>>stream\nBT\n/F1 24 Tf\n100 700 Td\n(Test PDF Document) Tj\nET\nendstream\nendobj\nxref\n0 6\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000109 00000 n \n0000000242 00000 n \n0000000299 00000 n \ntrailer\n<</Size 6/Root 1 0 R>>\nstartxref\n364\n%%EOF')
        
        # Get list of PDF files
        for pdf_file in os.listdir(pdf_path):
            if pdf_file.endswith('.pdf'):
                demo_names.append(pdf_file.split('.')[0])
                
        # Skip if no PDF files found
        if not demo_names:
            pytest.skip("No PDF files found for testing")
            
        for demo_name in demo_names:
            pdf_path = os.path.join(pdf_dev_path, 'pdf', f'{demo_name}.pdf')
            local_image_dir = os.path.join(pdf_dev_path, 'pdf', 'images')
            image_dir =str (os .path .basename (local_image_dir ))
            name_without_suff =os .path .basename (pdf_path ).split (".pdf")[0 ]
            dir_path =os .path .join (pdf_dev_path ,'parsit')
            image_writer ,md_writer =FileBasedDataWriter (local_image_dir ),FileBasedDataWriter (dir_path )
            reader1 =FileBasedDataReader ("")
            pdf_bytes =reader1 .read (pdf_path )
            ds =PymuDocDataset (pdf_bytes )
            ## inference
            if ds .classify ()==SupportedPdfParseMethod .OCR :
                infer_result =ds .apply (doc_analyze ,ocr =True )
                ## pipeline
                pipe_result =infer_result .pipe_ocr_mode (image_writer )
            else :
                infer_result =ds .apply (doc_analyze ,ocr =False )
                ## pipeline
                pipe_result =infer_result .pipe_txt_mode (image_writer )
            common .delete_file (dir_path )
            ### draw model result on each page
            infer_result .draw_model (os .path .join (dir_path ,f"{name_without_suff }_model.pdf"))

            ### get model inference result
            model_inference_result =infer_result .get_infer_res ()

            ### draw layout result on each page
            pipe_result .draw_layout (os .path .join (dir_path ,f"{name_without_suff }_layout.pdf"))

            ### draw spans result on each page
            pipe_result .draw_span (os .path .join (dir_path ,f"{name_without_suff }_spans.pdf"))

            ### dump markdown
            md_content =pipe_result .get_markdown (image_dir )
            pipe_result .dump_md (md_writer ,f"{name_without_suff }.md",image_dir )
            ### get content list content
            content_list_content =pipe_result .get_content_list (image_dir )
            pipe_result .dump_content_list (md_writer ,f"{name_without_suff }_content_list.json",image_dir )

            ### get middle json
            middle_json_content =pipe_result .get_middle_json ()
            ### dump middle json
            pipe_result .dump_middle_json (md_writer ,f'{name_without_suff }_middle.json')
            common .sdk_count_folders_and_check_contents (dir_path )

    @pytest .mark .P0 
    def test_pdf_s3_sdk (self ):
        """pdf s3 sdk test."""
        demo_names =list ()
        pdf_path =os .path .join (pdf_dev_path ,'pdf')
        for pdf_file in os .listdir (pdf_path ):
            if pdf_file .endswith ('.pdf'):
                demo_names .append (pdf_file .split ('.')[0 ])
        for demo_name in demo_names :
            pdf_path =os .path .join (pdf_dev_path ,'pdf',f'{demo_name }.pdf')
            local_image_dir =os .path .join (pdf_dev_path ,'pdf','images')
            image_dir =str (os .path .basename (local_image_dir ))
            name_without_suff =os .path .basename (pdf_path ).split (".pdf")[0 ]
            dir_path =os .path .join (pdf_dev_path ,'parsit')
            pass 

    @pytest .mark .P0 
    def test_pdf_local_ppt (self ):
        """pdf sdk auto test."""
        demo_names =list ()
        pdf_path =os .path .join (pdf_dev_path ,'ppt')
        for pdf_file in os .listdir (pdf_path ):
            if pdf_file .endswith ('.pptx'):
                demo_names .append (pdf_file .split ('.')[0 ])
        for demo_name in demo_names :
            pdf_path =os .path .join (pdf_dev_path ,'ppt',f'{demo_name }.pptx')
            local_image_dir =os .path .join (pdf_dev_path ,'parsit','images')
            image_dir =str (os .path .basename (local_image_dir ))
            name_without_suff =os .path .basename (pdf_path ).split (".pptx")[0 ]
            dir_path =os .path .join (pdf_dev_path ,'parsit')
            image_writer ,md_writer =FileBasedDataWriter (local_image_dir ),FileBasedDataWriter (dir_path )
            ds =read_local_office (pdf_path )[0 ]
            common .delete_file (dir_path )

            ds .apply (doc_analyze ,ocr =True ).pipe_txt_mode (image_writer ).dump_md (md_writer ,f"{name_without_suff }.md",image_dir )
            common .sdk_count_folders_and_check_contents (dir_path )



    @pytest .mark .P0 
    def test_pdf_local_image (self ):
        """pdf sdk auto test."""
        demo_names =list ()
        pdf_path =os .path .join (pdf_dev_path ,'images')
        for pdf_file in os .listdir (pdf_path ):
            if pdf_file .endswith ('.jpg'):
                demo_names .append (pdf_file .split ('.')[0 ])
        for demo_name in demo_names :
            pdf_path =os .path .join (pdf_dev_path ,'images',f'{demo_name }.jpg')
            local_image_dir =os .path .join (pdf_dev_path ,'parsit','images')
            image_dir =str (os .path .basename (local_image_dir ))
            name_without_suff =os .path .basename (pdf_path ).split (".jpg")[0 ]
            dir_path =os .path .join (pdf_dev_path ,'parsit')
            common .delete_file (dir_path )
            image_writer ,md_writer =FileBasedDataWriter (local_image_dir ),FileBasedDataWriter (dir_path )
            ds =read_local_images (pdf_path )[0 ]
            ds .apply (doc_analyze ,ocr =True ).pipe_ocr_mode (image_writer ).dump_md (
            md_writer ,f"{name_without_suff }.md",image_dir )
            common .sdk_count_folders_and_check_contents (dir_path )


    @pytest .mark .P0 
    def test_local_image_dir (self ):
        """local image dir."""
        demo_names =list ()
        pdf_path =os .path .join (pdf_dev_path ,'images')
        dir_path =os .path .join (pdf_dev_path ,'parsit')
        local_image_dir =os .path .join (pdf_dev_path ,'parsit','images')
        image_dir =str (os .path .basename (local_image_dir ))
        image_writer ,md_writer =FileBasedDataWriter (local_image_dir ),FileBasedDataWriter (dir_path )
        common .delete_file (dir_path )
        dss =read_local_images (pdf_path ,suffixes =['.png','.jpg'])
        count =0 
        for ds in dss :
            ds .apply (doc_analyze ,ocr =True ).pipe_ocr_mode (image_writer ).dump_md (md_writer ,f"{count }.md",image_dir )
            count +=1 
        common .sdk_count_folders_and_check_contents (dir_path )

    def test_local_doc_parse (self ):

        demo_names =list ()
        pdf_path =os .path .join (pdf_dev_path ,'doc')
        for pdf_file in os .listdir (pdf_path ):
            if pdf_file .endswith ('.docx'):
                demo_names .append (pdf_file .split ('.')[0 ])
        for demo_name in demo_names :
            pdf_path =os .path .join (pdf_dev_path ,'doc',f'{demo_name }.docx')
            local_image_dir =os .path .join (pdf_dev_path ,'parsit','images')
            image_dir =str (os .path .basename (local_image_dir ))
            name_without_suff =os .path .basename (pdf_path ).split (".docx")[0 ]
            dir_path =os .path .join (pdf_dev_path ,'parsit')
            image_writer ,md_writer =FileBasedDataWriter (local_image_dir ),FileBasedDataWriter (dir_path )
            ds =read_local_office (pdf_path )[0 ]
            common .delete_file (dir_path )

            ds .apply (doc_analyze ,ocr =True ).pipe_txt_mode (image_writer ).dump_md (md_writer ,f"{name_without_suff }.md",image_dir )
            common .sdk_count_folders_and_check_contents (dir_path )


    @pytest .mark .P0 
    def test_pdf_cli_auto (self ):
        """magic_pdf cli test auto."""
        time .sleep (2 )
        demo_names =[]
        pdf_path =os .path .join (pdf_dev_path ,'pdf')
        for pdf_file in os .listdir (pdf_path ):
            if pdf_file .endswith ('.pdf'):
                demo_names .append (pdf_file .split ('.')[0 ])
        for demo_name in demo_names :
            res_path =os .path .join (pdf_dev_path ,'parsit')
            common .delete_file (res_path )
            cmd ='magic-pdf -p %s -o %s -m %s'%(os .path .join (
            pdf_path ,f'{demo_name }.pdf'),res_path ,'auto')
            logging .info (cmd )
            os .system (cmd )
            common .cli_count_folders_and_check_contents (
            os .path .join (res_path ,demo_name ,'auto'))

    @pytest .mark .P0 
    def test_pdf_cli_txt (self ):
        """magic_pdf cli test txt."""
        time .sleep (2 )
        demo_names =[]
        pdf_path =os .path .join (pdf_dev_path ,'pdf')
        for pdf_file in os .listdir (pdf_path ):
            if pdf_file .endswith ('.pdf'):
                demo_names .append (pdf_file .split ('.')[0 ])
        for demo_name in demo_names :
            res_path =os .path .join (pdf_dev_path ,'parsit')
            common .delete_file (res_path )
            cmd ='magic-pdf -p %s -o %s -m %s'%(os .path .join (
            pdf_path ,f'{demo_name }.pdf'),res_path ,'txt')
            logging .info (cmd )
            os .system (cmd )
            common .cli_count_folders_and_check_contents (
            os .path .join (res_path ,demo_name ,'txt'))

    @pytest .mark .P0 
    def test_pdf_cli_ocr (self ):
        """magic_pdf cli test ocr."""
        time .sleep (2 )
        demo_names =[]
        pdf_path =os .path .join (pdf_dev_path ,'pdf')
        for pdf_file in os .listdir (pdf_path ):
            if pdf_file .endswith ('.pdf'):
                demo_names .append (pdf_file .split ('.')[0 ])
        for demo_name in demo_names :
            res_path =os .path .join (pdf_dev_path ,'parsit')
            common .delete_file (res_path )
            cmd ='magic-pdf -p %s -o %s -m %s'%(os .path .join (
            pdf_path ,f'{demo_name }.pdf'),res_path ,'ocr')
            logging .info (cmd )
            os .system (cmd )
            common .cli_count_folders_and_check_contents (
            os .path .join (res_path ,demo_name ,'ocr'))

    @pytest .mark .skip (reason ='out-of-date api')
    @pytest .mark .P1 
    def test_pdf_dev_cli_local_jsonl_txt (self ):
        """magic_pdf_dev cli local txt."""
        time .sleep (2 )
        jsonl_path =os .path .join (pdf_dev_path ,'line1.jsonl')
        cmd ='magic-pdf-dev --jsonl %s --method %s'%(jsonl_path ,"txt")
        logging .info (cmd )
        os .system (cmd )

    @pytest .mark .skip (reason ='out-of-date api')
    @pytest .mark .P1 
    def test_pdf_dev_cli_local_jsonl_ocr (self ):
        """magic_pdf_dev cli local ocr."""
        time .sleep (2 )
        jsonl_path =os .path .join (pdf_dev_path ,'line1.jsonl')
        cmd ='magic-pdf-dev --jsonl %s --method %s'%(jsonl_path ,'ocr')
        logging .info (cmd )
        os .system (cmd )

    @pytest .mark .skip (reason ='out-of-date api')
    @pytest .mark .P1 
    def test_pdf_dev_cli_local_jsonl_auto (self ):
        """magic_pdf_dev cli local auto."""
        time .sleep (2 )
        jsonl_path =os .path .join (pdf_dev_path ,'line1.jsonl')
        cmd ='magic-pdf-dev --jsonl %s --method %s'%(jsonl_path ,'auto')
        logging .info (cmd )
        os .system (cmd )

    @pytest .mark .skip (reason ='out-of-date api')
    @pytest .mark .P1 
    def test_pdf_dev_cli_s3_jsonl_txt (self ):
        """magic_pdf_dev cli s3 txt."""
        time .sleep (2 )
        jsonl_path =os .path .join (pdf_dev_path ,'line1.jsonl')
        cmd ='magic-pdf-dev --jsonl %s --method %s'%(jsonl_path ,"txt")
        logging .info (cmd )
        os .system (cmd )

    @pytest .mark .skip (reason ='out-of-date api')
    @pytest .mark .P1 
    def test_pdf_dev_cli_s3_jsonl_ocr (self ):
        """magic_pdf_dev cli s3 ocr."""
        time .sleep (2 )
        jsonl_path =os .path .join (pdf_dev_path ,'line1.jsonl')
        cmd ='magic-pdf-dev --jsonl %s --method %s'%(jsonl_path ,'ocr')
        logging .info (cmd )
        os .system (cmd )

    @pytest .mark .skip (reason ='out-of-date api')
    @pytest .mark .P1 
    def test_pdf_dev_cli_s3_jsonl_auto (self ):
        """magic_pdf_dev cli s3 auto."""
        time .sleep (2 )
        jsonl_path =os .path .join (pdf_dev_path ,'line1.jsonl')
        cmd ='magic-pdf-dev --jsonl %s --method %s'%(jsonl_path ,'auto')
        logging .info (cmd )
        os .system (cmd )

    @pytest .mark .P1 
    def test_pdf_dev_cli_pdf_json_auto (self ):
        """magic_pdf_dev cli pdf+json auto."""
        time .sleep (2 )
        json_path =os .path .join (pdf_dev_path ,'test_model.json')
        pdf_path =os .path .join (pdf_dev_path ,'pdf','test_rearch_report.pdf')
        cmd ='magic-pdf-dev --pdf %s --json %s --method %s'%(pdf_path ,json_path ,'auto')
        logging .info (cmd )
        os .system (cmd )

    @pytest .mark .skip (reason ='out-of-date api')
    @pytest .mark .P1 
    def test_pdf_dev_cli_pdf_json_ocr (self ):
        """magic_pdf_dev cli pdf+json ocr."""
        time .sleep (2 )
        json_path =os .path .join (pdf_dev_path ,'test_model.json')
        pdf_path =os .path .join (pdf_dev_path ,'pdf','test_rearch_report.pdf')
        cmd ='magic-pdf-dev --pdf %s --json %s --method %s'%(pdf_path ,json_path ,'auto')
        logging .info (cmd )
        os .system (cmd )

    @pytest .mark .P1 
    def test_local_magic_pdf_open_rapidai_table (self ):
        """magic pdf cli open rapid ai table."""
        time .sleep (2 )
        #pre_cmd = "cp ~/magic_pdf_html.json ~/parsit-pdf.json"
        #os.system(pre_cmd)
        value ={
        "model":"rapid_table",
        "enable":True ,
        "sub_model":"slanet_plus",
        "max_time":400 
        }
        common .update_config_file (magic_pdf_config ,"table-config",value )
        pdf_path =os .path .join (pdf_dev_path ,"pdf","test_rearch_report.pdf")
        common .delete_file (pdf_res_path )
        cli_cmd ="magic-pdf -p %s -o %s"%(pdf_path ,pdf_res_path )
        os .system (cli_cmd )
        res =common .check_html_table_exists (os .path .join (pdf_res_path ,"test_rearch_report","auto","test_rearch_report.md"))
        assert res is True 


    @pytest .mark .P1 
    def test_local_magic_pdf_doclayout_yolo (self ):
        """magic pdf cli open doclyaout yolo."""
        time .sleep (2 )
        #pre_cmd = "cp ~/magic_pdf_html.json ~/parsit-pdf.json"
        #os.system(pre_cmd)
        value ={
        "model":"doclayout_yolo"
        }
        common .update_config_file (magic_pdf_config ,"layout-config",value )
        pdf_path =os .path .join (pdf_dev_path ,"pdf","test_rearch_report.pdf")
        common .delete_file (pdf_res_path )
        cli_cmd ="magic-pdf -p %s -o %s"%(pdf_path ,pdf_res_path )
        os .system (cli_cmd )
        common .cli_count_folders_and_check_contents (os .path .join (pdf_res_path ,"test_rearch_report","auto"))

    @pytest .mark .skip (reason ="layoutlmv3废弃")
    @pytest .mark .P1 
    def test_local_magic_pdf_layoutlmv3_yolo (self ):
        """magic pdf cli open layoutlmv3."""
        time .sleep (2 )
        value ={
        "model":"layoutlmv3"
        }
        common .update_config_file (magic_pdf_config ,"layout-config",value )
        pdf_path =os .path .join (pdf_dev_path ,"pdf","test_rearch_report.pdf")
        common .delete_file (pdf_res_path )
        cli_cmd ="magic-pdf -p %s -o %s"%(pdf_path ,pdf_res_path )
        os .system (cli_cmd )
        common .cli_count_folders_and_check_contents (os .path .join (pdf_res_path ,"test_rearch_report","auto"))
        #res = common.check_html_table_exists(os.path.join(pdf_res_path, "test_rearch_report", "auto", "test_rearch_report.md"))

    @pytest .mark .P1 
    def test_magic_pdf_cpu (self ):
        """magic pdf cli cpu mode."""
        time .sleep (2 )
        #pre_cmd = "cp ~/magic_pdf_html_table_cpu.json ~/parsit-pdf.json"
        #os.system(pre_cmd)
        value ={
        "model":"rapid_table",
        "enable":True ,
        "sub_model":"slanet_plus",
        "max_time":400 
        }
        common .update_config_file (magic_pdf_config ,"table-config",value )
        common .update_config_file (magic_pdf_config ,"device-mode","cpu")
        pdf_path =os .path .join (pdf_dev_path ,"pdf","test_rearch_report.pdf")
        common .delete_file (pdf_res_path )
        cli_cmd ="magic-pdf -p %s -o %s"%(pdf_path ,pdf_res_path )
        os .system (cli_cmd )
        common .cli_count_folders_and_check_contents (os .path .join (pdf_res_path ,"test_rearch_report","auto"))


    @pytest .mark .P1 
    def test_local_magic_pdf_close_html_table (self ):
        """magic pdf cli close table."""
        time .sleep (2 )
        #pre_cmd = "cp ~/magic_pdf_close_table.json ~/parsit-pdf.json"
        #os.system(pre_cmd)
        value ={
        "model":"rapid_table",
        "enable":False ,
        "sub_model":"slanet_plus",
        "max_time":400 
        }
        common .update_config_file (magic_pdf_config ,"table-config",value )
        pdf_path =os .path .join (pdf_dev_path ,"pdf","test_rearch_report.pdf")
        common .delete_file (pdf_res_path )
        cli_cmd ="magic-pdf -p %s -o %s"%(pdf_path ,pdf_res_path )
        os .system (cli_cmd )
        res =common .check_close_tables (os .path .join (pdf_res_path ,"test_rearch_report","auto","test_rearch_report.md"))
        assert res is True 



if __name__ =='__main__':
    pytest .main ()

