import os 
import shutil 
import tempfile 
import io
from pathlib import Path 
from PIL import Image

import click 
import fitz 
from loguru import logger 

import parsit .model as model_config 
from parsit .data .batch_build_dataset import batch_build_dataset 
from parsit .data .data_reader_writer import FileBasedDataReader 
from parsit .data .dataset import Dataset 
from parsit .libs .version import __version__ 
from parsit .tools .common import batch_do_parse ,do_parse ,parse_pdf_methods 
from parsit .libs .config_reader import get_convert_html_tables_config
from parsit .utils .office_to_pdf import convert_file_to_pdf 

pdf_suffixes =['.pdf']
ms_office_suffixes =['.ppt','.pptx','.doc','.docx']
image_suffixes =['.png','.jpeg','.jpg']


@click .command ()
@click .version_option (__version__ ,
'--version',
'-v',
help ='display the version and exit')
@click .option (
'-p',
'--path',
'path',
type =click .Path (exists =True ),
required =True ,
help ='local filepath or directory. support PDF, PPT, PPTX, DOC, DOCX, PNG, JPG files',
)
@click .option (
'-o',
'--output-dir',
'output_dir',
type =click .Path (),
required =True ,
help ='output local directory',
)
@click .option (
'-m',
'--method',
'method',
type =parse_pdf_methods ,
help ="""the method for parsing pdf.
ocr: using ocr technique to extract information from pdf.
txt: suitable for the text-based pdf only and outperform ocr.
auto: automatically choose the best method for parsing pdf from ocr and txt.
without method specified, auto will be used by default.""",
default ='auto',
)
@click .option (
'-l',
'--lang',
'lang',
type =str ,
help ="""
    Input the languages in the pdf (if known) to improve OCR accuracy.  Optional.
    You should input "Abbreviation" with language form url:
    https://paddlepaddle.github.io/PaddleOCR/latest/en/ppocr/blog/multi_languages.html#5-support-languages-and-abbreviations
    """,
default =None ,
)
@click .option (
'-d',
'--debug',
'debug_able',
type =bool ,
help ='Enables detailed debugging information during the execution of the CLI commands.',
default =False ,
)
@click .option (
'-s',
'--start',
'start_page_id',
type =int ,
help ='The starting page for PDF parsing, beginning from 0.',
default =0 ,
)
@click .option (
'-e',
'--end',
'end_page_id',
type =int ,
help ='The ending page for PDF parsing, beginning from 0.',
default =None ,
)
@click .option (
'--enable-chunking/--disable-chunking',
'enable_chunking',
default =False ,
help ='Enable or disable semantic chunking of the document content.',
)
@click .option (
'--detect-signatures/--no-detect-signatures',
'detect_signatures',
default =None ,
help ='Enable or disable signature detection in the document.',
)
@click .option (
'--chunk-size',
type =int ,
default =1024 ,
help ='Size of each chunk in tokens. Default is 1000.',
)
@click .option (
'--chunk-overlap',
type =int ,
default =40 ,
help ='Number of tokens to overlap between chunks. Default is 200.',
)
@click .option (
'--detect-forms/--no-detect-forms',
'detect_forms',
help ='Enable detection and special handling of interactive form fields in PDFs',
required =False ,
default =False ,
)
@click .option (
'--convert-html-tables/--no-convert-html-tables',
'convert_html_tables',
help ='Convert HTML tables to Markdown format in the output',
required =False ,
default =None ,
)
def cli (path ,output_dir ,method ,lang ,debug_able ,start_page_id ,end_page_id ,enable_chunking ,chunk_size ,chunk_overlap ,detect_forms ,convert_html_tables ,detect_signatures):
    # Get HTML table conversion config
    html_table_config = get_convert_html_tables_config()
    
    # Override with CLI flag if provided
    if convert_html_tables is not None:
        html_table_config['enable'] = convert_html_tables
    
    # Set the final value
    convert_html_tables = html_table_config['enable']
    os .makedirs (output_dir ,exist_ok =True )
    temp_dir =tempfile .mkdtemp ()
    def read_fn(path_str):
        path = Path(path_str) if not isinstance(path_str, Path) else path_str
        if path.suffix.lower() in ms_office_suffixes:
            convert_file_to_pdf(str(path), temp_dir)
            fn = os.path.join(temp_dir, f'{path.stem}.pdf')
        elif path.suffix.lower() in image_suffixes:
            try:
                # First try opening as image and converting to PDF
                img = Image.open(path)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Create PDF in memory
                pdf_bytes = io.BytesIO()
                img.save(pdf_bytes, 'PDF', resolution=300.0)
                pdf_bytes = pdf_bytes.getvalue()
                
                # Save to temp file
                fn = os.path.join(temp_dir, f'{path.stem}.pdf')
                with open(fn, 'wb') as f:
                    f.write(pdf_bytes)
                    
            except Exception as img_e:
                # Fallback to PyMuPDF if PIL fails
                try:
                    with open(str(path), 'rb') as f:
                        bits = f.read()
                    doc = fitz.open(stream=bits, filetype=path.suffix[1:])
                    pdf_bytes = doc.convert_to_pdf()
                    fn = os.path.join(temp_dir, f'{path.stem}.pdf')
                    with open(fn, 'wb') as f:
                        f.write(pdf_bytes)
                except Exception as fitz_e:
                    raise Exception(f'Failed to process image: {img_e} (PIL), {fitz_e} (PyMuPDF)')
                    
        elif path.suffix.lower() in pdf_suffixes:
            fn = str(path)
        else:
            raise Exception(f'Unsupported file format: {path.suffix}')

        disk_rw = FileBasedDataReader(os.path.dirname(fn))
        return disk_rw.read(os.path.basename(fn))

    def parse_doc (doc_path :Path ,dataset :Dataset |None =None ):
        try :
            file_name =str (Path (doc_path ).stem )
            if dataset is None :
                pdf_data_or_dataset =read_fn (doc_path )
            else :
                pdf_data_or_dataset =dataset 
            do_parse (
            output_dir ,
            file_name ,
            pdf_data_or_dataset ,
            [],
            method ,
            debug_able ,
            start_page_id =start_page_id ,
            end_page_id =end_page_id ,
            lang =lang ,
            f_dump_chunk =enable_chunking ,
            chunk_size =chunk_size ,
            chunk_overlap =chunk_overlap ,
            detect_forms =detect_forms ,
            convert_html_tables =convert_html_tables ,
            detect_signatures=detect_signatures,
            )

        except Exception as e :
            logger .exception (e )

    if os.path.isfile(path):
        try:
            if Path(path).suffix.lower() in pdf_suffixes:
                do_parse(
                    output_dir=output_dir,
                    pdf_file_name=path,
                    pdf_bytes_or_dataset=read_fn(path),
                    model_list=[],
                    parse_method=method,
                    debug_able=debug_able,
                    start_page_id=start_page_id,
                    end_page_id=end_page_id,
                    lang=lang,
                    f_dump_chunk=enable_chunking,
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap,
                    detect_forms=detect_forms,
                    convert_html_tables=convert_html_tables,
                    detect_signatures=detect_signatures
                )
            elif Path(path).suffix.lower() in ms_office_suffixes:
                with tempfile.TemporaryDirectory() as temp_dir:
                    pdf_path = os.path.join(temp_dir, f"{Path(path).stem}.pdf")
                    convert_file_to_pdf(path, pdf_path)
                    do_parse(
                        output_dir=output_dir,
                        pdf_file_name=pdf_path,
                        pdf_bytes_or_dataset=read_fn(pdf_path),
                        model_list=[],
                        parse_method=method,
                        debug_able=debug_able,
                        start_page_id=start_page_id,
                        end_page_id=end_page_id,
                        lang=lang,
                        f_dump_chunk=enable_chunking,
                        chunk_size=chunk_size,
                        chunk_overlap=chunk_overlap,
                        detect_forms=detect_forms,
                        convert_html_tables=convert_html_tables,
                        detect_signatures=detect_signatures
                    )
            elif Path(path).suffix.lower() in image_suffixes:
                with tempfile.TemporaryDirectory() as temp_dir:
                    pdf_path = os.path.join(temp_dir, f"{Path(path).stem}.pdf")
                    image = Image.open(path)
                    image.convert('RGB').save(pdf_path, 'PDF', resolution=100.0)
                    do_parse(
                        output_dir=output_dir,
                        pdf_file_name=pdf_path,
                        pdf_bytes_or_dataset=read_fn(pdf_path),
                        model_list=[],
                        parse_method=method,
                        debug_able=debug_able,
                        start_page_id=start_page_id,
                        end_page_id=end_page_id,
                        lang=lang,
                        f_dump_chunk=enable_chunking,
                        chunk_size=chunk_size,
                        chunk_overlap=chunk_overlap,
                        detect_forms=detect_forms,
                        convert_html_tables=convert_html_tables,
                        detect_signatures=detect_signatures
                    )
            else:
                raise ValueError(f'Unsupported file type: {path}')
        except Exception as e:
            logger.exception(f"Error processing file {path}: {e}")
            raise
    else:
        with tempfile .TemporaryDirectory ()as temp_dir :
            doc_paths =[]
            for doc_path in Path (path ).glob ('*'):
                if doc_path .suffix in pdf_suffixes +image_suffixes +ms_office_suffixes :
                    if doc_path .suffix in ms_office_suffixes :
                        convert_file_to_pdf (str (doc_path ),temp_dir )
                        doc_path =Path (os .path .join (temp_dir ,f'{doc_path .stem }.pdf'))
                    elif doc_path .suffix in image_suffixes :
                        with open (str (doc_path ),'rb')as f :
                            bits =f .read ()
                            pdf_bytes =fitz .open (stream =bits ).convert_to_pdf ()
                        fn =os .path .join (temp_dir ,f'{doc_path .stem }.pdf')
                        with open (fn ,'wb')as f :
                            f .write (pdf_bytes )
                        doc_path =Path (fn )
                    doc_paths .append (doc_path )
            
            if doc_paths :
                datasets =batch_build_dataset (doc_paths ,4 ,lang )
                batch_do_parse (
                    output_dir ,
                    [str (doc_path .stem )for doc_path in doc_paths ],
                    datasets ,
                    method ,
                    debug_able ,
                    lang =lang ,
                    detect_forms =detect_forms ,
                    convert_html_tables =convert_html_tables ,
                    detect_signatures=detect_signatures,
                )
            else :
                parse_doc (Path (path ))


if __name__ =='__main__':
    cli ()
