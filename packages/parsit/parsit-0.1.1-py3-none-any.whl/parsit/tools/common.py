import json
import os 
import re
import sys
import subprocess
import pkg_resources
import time
import datetime
from pathlib import Path

import click 
import fitz 
import torch
from typing import Dict, List, Optional, Union, Any
from loguru import logger

# Import form detection utilities
from parsit.utils.form_detector import detect_form_fields_per_page
from parsit.utils.pdf_renderer import create_hybrid_pdf_with_form_pages
from loguru import logger 

import parsit.model as model_config 
from parsit.config.enums import SupportedPdfParseMethod 
from parsit.config.make_content_config import DropMode, MakeMode 
from parsit.data.data_reader_writer import FileBasedDataWriter 
from parsit.data.dataset import Dataset, PymuDocDataset 
from parsit.libs.draw_bbox import draw_char_bbox 
from parsit.libs.pdf_check import detect_invalid_chars
from parsit.model.doc_analyze_by_custom_model import (batch_doc_analyze,
doc_analyze)
from parsit.operators.models import InferenceResult
from parsit.forms.form_config import get_form_invoice_enhancement_config
from parsit.utils.form_detector import detect_form_fields_per_page
from parsit.utils.pdf_renderer import create_hybrid_pdf_with_form_pages


def _ensure_html_to_markdown_deps():
    required = {'beautifulsoup4', 'tabulate'}
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed
    
    if missing:
        logger.info(f"Installing missing packages for HTML table conversion: {', '.join(missing)}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])


def _convert_html_tables_to_markdown(md_content: str) -> str:
    """
    Convert HTML tables in the markdown content to markdown tables.
    
    Args:
        md_content: The markdown content containing HTML tables
        
    Returns:
        str: The content with HTML tables converted to markdown, or original content if conversion fails
    """
    if not md_content or not isinstance(md_content, str):
        return md_content
        
    try:
        # First, try to find and process tables
        from bs4 import BeautifulSoup
        from parsit.libs.config_reader import get_convert_html_tables_config
        
        # Get the configuration
        config = get_convert_html_tables_config()
        fallback_to_html = config.get('fallback_to_html', True)
        
        # Check if there are any tables in the content
        if '<table' not in md_content.lower():
            return md_content  # No tables found, return as is
            
        # Parse the HTML content
        soup = BeautifulSoup(md_content, 'html.parser')
        
        # Find all tables
        tables = soup.find_all('table')
        if not tables:
            return md_content  # No tables found, return as is
            
        # Process each table
        for table in tables:
            # Replace the table with a placeholder
            placeholder = f"[[TABLE_{tables.index(table)}_PLACEHOLDER]]"
            table.replace_with(placeholder)
        
        # Get the text with placeholders
        text_content = str(soup)
        
        # Now process each table and replace placeholders
        for i, table in enumerate(tables):
            # Convert table to markdown
            from parsit.utils.html_to_markdown import convert_html_table_to_markdown
            markdown_table, success = convert_html_table_to_markdown(str(table))
            
            # Replace the placeholder with the markdown table or original HTML based on success
            placeholder = f"[[TABLE_{i}_PLACEHOLDER]]"
            if success and markdown_table:
                text_content = text_content.replace(placeholder, markdown_table)
            elif fallback_to_html:
                # Fall back to original HTML table if conversion fails and fallback is enabled
                text_content = text_content.replace(placeholder, str(table))
            
        # Clean up any remaining HTML tags except tables
        soup = BeautifulSoup(text_content, 'html.parser')
        
        # Get all text content, preserving table structure
        result = []
        for element in soup.contents:
            if element.name == 'table':
                # Keep tables as they are (either converted to markdown or original HTML)
                result.append(str(element))
            else:
                # For non-table elements, get the text content
                result.append(element.get_text('\n', strip=True))
        
        # Join all parts and clean up
        result = '\n\n'.join(result)
        
        # Clean up excessive whitespace
        result = '\n'.join(line.strip() for line in result.split('\n') if line.strip())
        return re.sub(r'\n{3,}', '\n\n', result.strip())
        
    except Exception as e:
        logger.warning(f"Error processing HTML tables: {str(e)}")
        # If anything fails, return the original content
        return md_content

# from io import BytesIO
# from pypdf import PdfReader, PdfWriter


def prepare_env(output_dir, pdf_file_name, method):
    # Convert to Path object if not already
    pdf_path = Path(pdf_file_name)
    # Use the stem (filename without extension) for the directory name
    output_base = pdf_path.stem
    # Create the output directory directly under output_dir/doc_name
    local_parent_dir = os.path.join(output_dir, output_base)
    
    # Create images and signatures directories
    images_dir = os.path.join(local_parent_dir, 'images')
    signatures_dir = os.path.join(images_dir, 'signatures')
    
    # Ensure directories exist
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(signatures_dir, exist_ok=True)
    
    return images_dir, local_parent_dir


    # def convert_pdf_bytes_to_bytes_by_pypdf(pdf_bytes, start_page_id=0, end_page_id=None):

    #     pdf_file = BytesIO(pdf_bytes)

    #     reader = PdfReader(pdf_file)

    #     writer = PdfWriter()

    #     end_page_id = end_page_id if end_page_id is not None and end_page_id >= 0 else len(reader.pages) - 1
    #     if end_page_id > len(reader.pages) - 1:
    #         logger.warning("end_page_id is out of range, use pdf_docs length")
    #         end_page_id = len(reader.pages) - 1
    #     for i, page in enumerate(reader.pages):
    #         if start_page_id <= i <= end_page_id:
    #             writer.add_page(page)

    #     output_buffer = BytesIO()

    #     writer.write(output_buffer)

    #     converted_pdf_bytes = output_buffer.getvalue()
    #     return converted_pdf_bytes


def convert_pdf_bytes_to_bytes_by_pymupdf (pdf_bytes ,start_page_id =0 ,end_page_id =None ):
    document =fitz .open ('pdf',pdf_bytes )
    output_document =fitz .open ()
    end_page_id =(
    end_page_id 
    if end_page_id is not None and end_page_id >=0 
    else len (document )-1 
    )
    if end_page_id >len (document )-1 :
        logger .warning ('end_page_id is out of range, use pdf_docs length')
        end_page_id =len (document )-1 
    output_document .insert_pdf (document ,from_page =start_page_id ,to_page =end_page_id )
    output_bytes =output_document .tobytes ()
    return output_bytes 


def _do_parse(
    output_dir,
    pdf_file_name,
    pdf_bytes_or_dataset,
    model_list,
    parse_method,
    debug_able=False,
    f_draw_span_bbox=True,
    f_draw_layout_bbox=True,
    f_dump_md=True,
    f_dump_middle_json=True,
    f_dump_model_json=True,
    f_dump_orig_pdf=True,
    f_dump_content_list=True,
    f_make_md_mode=MakeMode.MM_MD,
    f_draw_model_bbox=False,
    f_draw_line_sort_bbox=False,
    f_draw_char_bbox=False,
    start_page_id=0,
    end_page_id=None,
    lang=None,
    layout_model=None,
    formula_enable=None,
    table_enable=None,
    f_dump_chunk=False,
    chunk_size=1000,
    chunk_overlap=200,
    detect_forms=False,
    convert_html_tables=False,
    detect_signatures=None,
):
    from parsit.operators.models import InferenceResult 
    
    # Set up base directory and filename at the start
    base_filename = os.path.splitext(os.path.basename(pdf_file_name))[0]
    local_parent_dir = os.path.join(output_dir, base_filename)
    
    # Create necessary directories
    images_dir = os.path.join(local_parent_dir, 'images')
    signatures_dir = os.path.join(images_dir, 'signatures')
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(signatures_dir, exist_ok=True)
    
    if debug_able:
        logger.warning('debug mode is on')
        f_draw_model_bbox = True 
        f_draw_line_sort_bbox = True 
        # f_draw_char_bbox = True

    if isinstance(pdf_bytes_or_dataset, bytes):
        original_pdf_bytes = pdf_bytes_or_dataset
        pdf_bytes = original_pdf_bytes  # Default to original bytes
        
        # Handle form detection and hybrid PDF generation before any conversion
        form_data = {}
        if detect_forms:
            form_config = get_form_invoice_enhancement_config()
            if form_config.get('enable', False):
                logger.info("Form detection is enabled in config")
                try:
                    # Detect form fields in the original PDF
                    form_data = detect_form_fields_per_page(original_pdf_bytes)
                    
                    if form_data and 'pages' in form_data and any(page_info.get('has_forms', False) for page_info in form_data['pages'].values()):
                        # Log which pages have forms
                        form_pages = [str(p) for p, info in form_data['pages'].items() if info.get('has_forms', False)]
                        logger.info(f"Detected form fields on pages: {', '.join(form_pages)}")
                        
                        # Create a hybrid PDF with form pages rendered as images
                        logger.info("Creating hybrid PDF with form pages rendered as images...")
                        try:
                            hybrid_pdf_bytes = create_hybrid_pdf_with_form_pages(original_pdf_bytes, form_data['pages'])
                            if hybrid_pdf_bytes:
                                logger.info(f"Hybrid PDF created successfully. Size: {len(hybrid_pdf_bytes)} bytes")
                                # Use the hybrid PDF for the rest of the pipeline
                                pdf_bytes = hybrid_pdf_bytes
                                
                                # Verify the hybrid PDF
                                try:
                                    hybrid_doc = fitz.open(stream=hybrid_pdf_bytes, filetype="pdf")
                                    logger.info(f"Hybrid PDF verification: {len(hybrid_doc)} pages")
                                    hybrid_doc.close()
                                except Exception as e:
                                    logger.warning(f"Error verifying hybrid PDF: {str(e)}")
                            else:
                                logger.warning("Failed to create hybrid PDF, using original PDF")
                        except Exception as e:
                            logger.error(f"Error creating hybrid PDF: {str(e)}", exc_info=True)
                    else:
                        logger.info("No form fields detected in the PDF")
                        
                        # Debug: Check if we can detect widgets directly in the original PDF
                        try:
                            doc = fitz.open(stream=original_pdf_bytes, filetype="pdf")
                            for page_num in range(len(doc)):
                                page = doc[page_num]
                                widgets = list(page.widgets())
                                if widgets:
                                    logger.warning(f"Direct widget check found {len(widgets)} widgets on page {page_num}")
                                    for widget in widgets:
                                        logger.warning(f"  Widget: {widget.field_type_string} - {widget.field_name}")
                                else:
                                    logger.debug(f"No widgets found on page {page_num}")
                            doc.close()
                        except Exception as e:
                            logger.error(f"Error in direct widget check: {str(e)}")
                            
                except Exception as e:
                    logger.error(f"Error during form detection: {str(e)}", exc_info=True)
                    form_data = {}
            else:
                logger.info("Form detection is disabled in config")
        else:
            logger.info("Form detection is disabled via CLI flag")
        
        # Now apply any page range conversion if needed
        if start_page_id != 0 or (end_page_id is not None and end_page_id < len(fitz.open('pdf', pdf_bytes)) - 1):
            logger.info(f"Applying page range: {start_page_id} to {end_page_id}")
            pdf_bytes = convert_pdf_bytes_to_bytes_by_pymupdf(pdf_bytes, start_page_id, end_page_id)
        
        # Create dataset from the (possibly modified) PDF bytes
        ds = PymuDocDataset(pdf_bytes, lang=lang)
        
        # Get base directory and filename
        base_filename = os.path.splitext(os.path.basename(pdf_file_name))[0]
        local_parent_dir = os.path.join(output_dir, base_filename)
        
        # Process each page for signatures if enabled
        signature_data = []
        
        # Check if signature detection is enabled
        if detect_signatures is None:
            # Check config if not explicitly set
            try:
                from parsit.libs.config_reader import read_config
                config = read_config()
                detect_signatures = config.get('signature-config', {}).get('enable', False)
                logger.info(f"Signature detection from config: {detect_signatures}")
            except Exception as e:
                logger.warning(f"Could not read signature config: {e}")
                detect_signatures = False
        
        if detect_signatures:
            try:
                from parsit.utils.signature_utils import ONNXSignatureDetector
                import cv2
                import numpy as np
                
                # Get model path from config or use default
                model_path = None
                try:
                    from parsit.libs.config_reader import read_config
                    config = read_config()
                    model_path = config.get('signature-config', {}).get('model_weight', None)
                    if model_path and not os.path.isabs(model_path):
                        model_path = os.path.join(os.path.dirname(__file__), '..', '..', model_path)
                except Exception as e:
                    logger.warning(f"Could not get model path from config: {e}")
                    model_path = r"D:\parsit\pretrained models\yolov8s.onnx"
                
                # Initialize detector with config or default values
                confidence_threshold = 0.5
                iou_threshold = 0.45
                try:
                    confidence_threshold = config.get('signature-config', {}).get('confidence_threshold', 0.5)
                    iou_threshold = config.get('signature-config', {}).get('iou_threshold', 0.45)
                except:
                    pass
                
                logger.info(f"Initializing signature detector with model: {model_path}")
                signature_detector = ONNXSignatureDetector(
                    model_path=model_path,
                    device='cuda' if torch.cuda.is_available() else 'cpu'
                )

                # Create document-specific output directories
                doc_name = os.path.splitext(os.path.basename(pdf_file_name))[0]
                doc_dir = os.path.join(output_dir, doc_name)
                
                # Create images and signatures directories
                images_dir = os.path.join(doc_dir, 'images')
                signatures_dir = os.path.join(images_dir, 'signatures')
                
                # Ensure directories exist
                os.makedirs(images_dir, exist_ok=True)
                os.makedirs(signatures_dir, exist_ok=True)

                # Process each page for signatures before creating InferenceResult
                doc = fitz.open(stream=pdf_bytes, filetype="pdf")

                # Initialize signature data structure: one list per page
                signature_data = [[] for _ in range(len(doc))]

                for page_num in range(len(doc)):
                    page = doc[page_num]
                    page_rect = page.rect  # Get page dimensions in points
                    
                    # Log page dimensions for debugging
                    logger.debug(f"Page {page_num + 1} dimensions: {page_rect.width}x{page_rect.height} points")
                    
                    # Directory structure already created above
                    
                    # Create a higher resolution pixmap for better detection
                    zoom = 2.0  # Zoom factor for higher DPI
                    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))  # Higher DPI for better detection
                    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, 3)
                    
                    # Log pixmap dimensions for debugging
                    logger.debug(f"Pixmap dimensions: {pix.width}x{pix.height} pixels (zoom: {zoom}x)")

                    # Log original image dimensions
                    logger.debug(f"Original pixmap dimensions: {pix.width}x{pix.height}")
                    logger.debug(f"Page dimensions (points): {page_rect.width}x{page_rect.height}")
                    
                    # Detect signatures with confidence threshold
                    logger.debug(f"Running signature detection on image of size {img.shape[1]}x{img.shape[0]}")
                    detections = signature_detector.detect(
                        img,
                        conf_threshold=confidence_threshold
                    )
                    logger.debug(f"Found {len(detections)} potential signatures")

                    # Process detections for this page
                    for det_idx, det in enumerate(detections, 1):
                        if not det.image.size:  # Skip empty detections
                            continue

                        # Save the signature image (clean, without bounding boxes)
                        sig_filename = f"page_{page_num + 1:03d}_signature_{det_idx:03d}.png"
                        sig_path = os.path.join(signatures_dir, sig_filename)
                        rel_sig_path = os.path.join("images", "signatures", sig_filename).replace('\\', '/')
                        
                        # Get the signature image from the detection (already cropped)
                        sig_img = det.image
                        if sig_img is not None and sig_img.size > 0:
                            # Convert from RGB to BGR for OpenCV
                            sig_img_bgr = cv2.cvtColor(sig_img, cv2.COLOR_RGB2BGR)
                            # Save the clean signature image
                            cv2.imwrite(sig_path, sig_img_bgr)
                            logger.debug(f"Saved clean signature image to {sig_path}")
                        
                        try:
                            # Get the original detection coordinates (in pixmap pixels)
                            x1, y1, x2, y2 = map(int, det.bbox)
                            
                            # Log the original detection bbox and page dimensions
                            logger.debug(f"Original detection bbox (pixels): ({x1}, {y1}, {x2}, {y2})")
                            logger.debug(f"Pixmap dimensions: {pix.width}x{pix.height}, Page dimensions: {page_rect.width}x{page_rect.height} points")
                            
                            # Calculate scale factors from pixmap to PDF points
                            scale_x = page_rect.width / pix.width
                            scale_y = page_rect.height / pix.height
                            logger.debug(f"Scale factors - X: {scale_x:.4f}, Y: {scale_y:.4f} (points/pixel)")
                            
                            # Convert to PDF points
                            x1_pt = x1 * scale_x
                            y1_pt = y1 * scale_y
                            x2_pt = x2 * scale_x
                            y2_pt = y2 * scale_y
                            logger.debug(f"Bounding box in PDF points (before padding): ({x1_pt:.1f}, {y1_pt:.1f}, {x2_pt:.1f}, {y2_pt:.1f})")
                            
                            # Add padding in points (5mm = ~14.17 points)
                            padding_pts = 14.17
                            x1_pt = max(0, x1_pt - padding_pts)
                            y1_pt = max(0, y1_pt - padding_pts)
                            x2_pt = min(page_rect.width, x2_pt + padding_pts)
                            y2_pt = min(page_rect.height, y2_pt + padding_pts)
                            logger.debug(f"Bounding box in PDF points (after padding): ({x1_pt:.1f}, {y1_pt:.1f}, {x2_pt:.1f}, {y2_pt:.1f})")
                            
                            # Create a rectangle for the signature area
                            sig_rect = fitz.Rect(x1_pt, y1_pt, x2_pt, y2_pt)
                            
                            # Log detailed signature rectangle information
                            logger.debug(f"Signature rectangle (points): {sig_rect}")
                            logger.debug(f"Signature rectangle dimensions: {sig_rect.width:.1f}x{sig_rect.height:.1f} points")
                            
                            # Print detailed debug info to console
                            print("\n=== SIGNATURE EXTRACTION DEBUG ===")
                            print(f"Original detection (pixels): ({x1}, {y1}, {x2}, {y2}) [W: {x2-x1}, H: {y2-y1}]")
                            print(f"Pixmap size: {pix.width}x{pix.height} pixels")
                            print(f"Page size: {page_rect.width}x{page_rect.height} points")
                            print(f"Scale factors - X: {scale_x:.4f}, Y: {scale_y:.4f} (points/pixel)")
                            print(f"Bounding box in PDF points: ({x1_pt:.1f}, {y1_pt:.1f}, {x2_pt:.1f}, {y2_pt:.1f})")
                            print(f"After padding: ({x1_pt:.1f}, {y1_pt:.1f}, {x2_pt:.1f}, {y2_pt:.1f})")
                            print(f"Signature rect: {sig_rect}")
                            print(f"Signature rect size: {sig_rect.width:.1f}x{sig_rect.height:.1f} points")
                            print("=== END DEBUG ===\n")
                            
                            try:
                                # Skip debug image generation entirely
                                pass
                            except Exception as e:
                                logger.error(f"Error processing signature: {str(e)}", exc_info=True)
                                raise
                            
                            # Add to signature data with relative path
                            if page_num not in signature_data:
                                signature_data[page_num] = []
                            
                            # Save signature metadata
                            sig_meta = {
                                'type': 'signature',
                                'image_path': rel_sig_path,
                                'page_idx': page_num,
                                'confidence': float(det.confidence),
                                'bbox': [x1, y1, x2, y2],
                                'bbox_pts': [x1_pt, y1_pt, x2_pt, y2_pt],
                                'width': x2 - x1,
                                'height': y2 - y1
                            }
                            signature_data[page_num].append(sig_meta)
                            
                            logger.debug(f"Saved signature metadata: {sig_meta}")
                            
                        except Exception as e:
                            logger.error(f"Failed to process signature detection: {str(e)}", exc_info=True)
                            continue

                # Count total signatures
                total_signatures = sum(len(page_sigs) for page_sigs in signature_data)
                logger.info(f"Detected {total_signatures} signatures across {len(doc)} pages")
                doc.close()

            except Exception as e:
                logger.error(f"Error during signature detection: {e}")
                signature_data = []
        
        # Store form detection info in the dataset for later use
        if detect_forms and 'form_data' in locals() and form_data:
            # Convert form_data to a serializable format if needed
            serializable_form_pages = {}
            for page_num, page_info in form_data['pages'].items():
                if isinstance(page_info, dict):
                    serializable_form_pages[page_num] = {
                        'has_forms': page_info.get('has_forms', False),
                        'fields': [
                            {
                                'name': field.get('name'),
                                'type': field.get('type'),
                                'value': field.get('value'),
                                'rect': str(field.get('rect', '')),
                                'readonly': field.get('readonly', False)
                            }
                            for field in page_info.get('fields', [])
                        ]
                    }
            
            # Store in the dataset for downstream processing
            hybrid_created = 'hybrid_pdf_bytes' in locals() and hybrid_pdf_bytes is not None
            ds.form_data = {
                'has_forms': any(page.get('has_forms', False) for page in serializable_form_pages.values()),
                'pages': serializable_form_pages,
                'hybrid_pdf_created': hybrid_created
            }
            
            logger.info(f"Stored form data for {len(serializable_form_pages)} pages in dataset")
            setattr(ds, '_hybrid_pdf_created', True)
    else:
        ds = pdf_bytes_or_dataset
    
    pdf_bytes = ds._raw_data 
    local_image_dir ,local_md_dir =prepare_env (output_dir ,pdf_file_name ,parse_method )

    image_writer ,md_writer =FileBasedDataWriter (local_image_dir ),FileBasedDataWriter (local_md_dir )
    image_dir =str (os .path .basename (local_image_dir ))

    form_data = None
    if hasattr(ds, 'form_data'):
        form_data = ds.form_data
        logger.info(f"Found form data in dataset with {len(form_data.get('pages', {}))} pages")

    if len(model_list) == 0:
        if model_config.__use_inside_model__:
            if parse_method == 'auto':
                if ds.classify() == SupportedPdfParseMethod.TXT:
                    infer_result = ds.apply(
                        doc_analyze,
                        ocr=False,
                        lang=ds._lang,
                        layout_model=layout_model,
                        formula_enable=formula_enable,
                        table_enable=table_enable,
                    )
                    pipe_result = infer_result.pipe_txt_mode(
                        image_writer, debug_mode=True, lang=ds._lang
                    )
                else:
                    infer_result = ds.apply(
                        doc_analyze,
                        ocr=True,
                        lang=ds._lang,
                        layout_model=layout_model,
                        formula_enable=formula_enable,
                        table_enable=table_enable,
                    )
                    pipe_result = infer_result.pipe_ocr_mode(
                        image_writer, debug_mode=True, lang=ds._lang
                    )
            elif parse_method == 'txt':
                infer_result = ds.apply(
                    doc_analyze,
                    ocr=False,
                    lang=ds._lang,
                    layout_model=layout_model,
                    formula_enable=formula_enable,
                    table_enable=table_enable,
                )
                pipe_result = infer_result.pipe_txt_mode(
                    image_writer, debug_mode=True, lang=ds._lang
                )
            elif parse_method == 'ocr':
                infer_result = ds.apply(
                    doc_analyze,
                    ocr=True,
                    lang=ds._lang,
                    layout_model=layout_model,
                    formula_enable=formula_enable,
                    table_enable=table_enable,
                )
                pipe_result = infer_result.pipe_ocr_mode(
                    image_writer, debug_mode=True, lang=ds._lang
                )
            else:
                logger.error('unknown parse method')
                exit(1)
        else:
            logger.error('need model list input')
            exit(2)
    else:
        # Create InferenceResult with form data if available
        form_invoice_data = []
        if detect_forms and form_data and 'pages' in form_data:
            logger.info(f"Processing form data for {len(form_data['pages'])} pages")
            for page_num, page_info in form_data['pages'].items():
                try:
                    page_fields = []
                    for field in page_info.get('fields', []):
                        field_info = {
                            'name': field.get('name', 'unnamed'),
                            'type': field.get('type', 'text'),
                            'value': field.get('value', ''),
                            'rect': str(field.get('rect', '')),
                            'readonly': field.get('readonly', False)
                        }
                        page_fields.append(field_info)
                    
                    if page_fields:
                        form_invoice_data.append({
                            'page_no': int(page_num) + 1,  # Convert to 1-based
                            'extraction_result': {
                                'fields': page_fields
                            }
                        })
                except Exception as e:
                    logger.error(f"Error processing form data for page {page_num}: {str(e)}")
            
        # Create InferenceResult with form data and signature data
        logger.info(f"Creating InferenceResult with form_data: {bool(form_data)} and signature_data")
        
        # Prepare form data if available
        form_invoice_data = form_data.get('pages', []) if form_data else None
        
        # Prepare signature data if available
        sig_data = signature_data if 'signature_data' in locals() and signature_data and any(signature_data) else None
        
        # Create inference result with form data and signature data
        infer_result = InferenceResult(
            inference_results=pipe_res.get('pdf_info', []),
            dataset=ds,
            form_invoice_data=form_invoice_data,
            signature_data=sig_data
        )
        
        # Debug logging
        if hasattr(infer_result, '_form_invoice_data'):
            logger.info(f"InferResult form data set: {bool(infer_result._form_invoice_data)}")
        else:
            logger.warning("InferResult does not have _form_invoice_data attribute")
            
        if hasattr(infer_result, '_signature_data'):
            sig_count = sum(len(sigs) for sigs in sig_data.values()) if sig_data else 0
            logger.info(f"InferResult signature data set with {sig_count} signatures")
        else:
            logger.warning("InferResult does not have _signature_data attribute")
            
        if parse_method == 'ocr':
            pipe_result = infer_result.pipe_ocr_mode(
                image_writer, debug_mode=True, lang=ds._lang
            )
        elif parse_method == 'txt':
            pipe_result = infer_result.pipe_txt_mode(
                image_writer, debug_mode=True, lang=ds._lang
            )
        else:
            if ds.classify() == SupportedPdfParseMethod.TXT:
                pipe_result = infer_result.pipe_txt_mode(
                    image_writer, debug_mode=True, lang=ds._lang
                )
            else:
                pipe_result = infer_result.pipe_ocr_mode(
                    image_writer, debug_mode=True, lang=ds._lang
                )


    # Get base filename without path for output files
    base_filename = os.path.splitext(os.path.basename(pdf_file_name))[0]
    
    # Save output PDFs directly in the document's output directory
    if f_draw_model_bbox:
        output_path = os.path.join(local_parent_dir, f'{base_filename}_model.pdf')
        infer_result.draw_model(output_path)

    if f_draw_layout_bbox:
        output_path = os.path.join(local_parent_dir, f'{base_filename}_layout.pdf')
        pipe_result.draw_layout(output_path)
        
    if f_draw_span_bbox:
        output_path = os.path.join(local_parent_dir, f'{base_filename}_spans.pdf')
        pipe_result.draw_span(output_path)

    if f_draw_line_sort_bbox:
        output_path = os.path.join(local_parent_dir, f'{base_filename}_line_sort.pdf')
        pipe_result.draw_line_sort(output_path)

    if f_draw_char_bbox:
        output_path = os.path.join(local_parent_dir, f'{base_filename}_char_bbox.pdf')
        draw_char_bbox(pdf_bytes, local_parent_dir, f'{base_filename}_char_bbox.pdf')

    if f_dump_md:
        try:
            # Use the document's output directory for markdown file
            md_filename = f'{base_filename}.md'
            md_path = os.path.join(local_parent_dir, md_filename)
            
            logger.info(f"Starting markdown dump for {pdf_file_name} to {md_path}")
            logger.info(f"Markdown writer type: {type(md_writer).__name__}")
            logger.info(f"Image dir: {image_dir}")
            
            # Ensure the output directory exists
            os.makedirs(local_parent_dir, exist_ok=True)
            
            try:
                # Get markdown content from pipe_result
                logger.info("Generating markdown content...")
                md_content = pipe_result.get_markdown(
                    image_dir,
                    drop_mode=DropMode.NONE,
                    md_make_mode=f_make_md_mode
                )
                
                # Add signature sections if signatures were detected
                if signature_data and any(signature_data):
                    logger.info("Adding signature sections to markdown")
                    signature_sections = []
                    
                    # Process each page with signatures
                    for page_num, page_sigs in enumerate(signature_data):
                        if not page_sigs:
                            continue
                        if not isinstance(md_content, str):
                            md_content = ""
                        
                        # Add section header for this page if it has signatures
                        md_content += f"\n\n---\n\n# Signatures on Page {page_num + 1}\n"
                        
                        # Add each signature on this page
                        for sig_idx, sig in enumerate(page_sigs, 1):
                            if isinstance(sig, dict):
                                sig_text = f"- Signature {sig_idx}"
                                if 'confidence' in sig:
                                    sig_text += f" (confidence: {sig['confidence']:.2f})"
                                if 'image_path' in sig:
                                    sig_text += f"\n  ![Signature {sig_idx}]({sig['image_path']})\n"
                                signature_sections.append(sig_text)
                    
                    # Add all signature sections to the markdown
                    if signature_sections:
                        md_content += "\n".join(signature_sections)
                
                # Handle HTML table conversion if enabled
                if convert_html_tables and md_content and isinstance(md_content, str):
                    _ensure_html_to_markdown_deps()
                    logger.info("Converting HTML tables to markdown...")
                    
                    try:
                        # Clean up any HTML/body wrappers
                        if md_content.strip().startswith('<html>') or md_content.strip().startswith('<body>'):
                            from bs4 import BeautifulSoup
                            soup = BeautifulSoup(md_content, 'html.parser')
                            if soup.body:
                                md_content = str(soup.body)
                        
                        # Convert tables
                        processed_md = _convert_html_tables_to_markdown(md_content)
                        md_content = processed_md
                        
                    except Exception as e:
                        logger.error(f"Error converting HTML tables: {str(e)}", exc_info=True)
                        logger.info("Falling back to original markdown content")
                
                # Ensure the directory exists before writing
                os.makedirs(os.path.dirname(md_path), exist_ok=True)
                
                # Write the final markdown to file
                logger.info(f"Writing markdown to {md_path}")
                try:
                    with open(md_path, 'w', encoding='utf-8') as f:
                        f.write(md_content if isinstance(md_content, str) else str(md_content))
                    
                    file_size = os.path.getsize(md_path)
                    logger.info(f"Successfully wrote markdown to {md_path} ({file_size} bytes)")
                    
                except Exception as write_error:
                    logger.error(f"Error writing markdown file: {str(write_error)}", exc_info=True)
                    
                    # Fall back to default behavior if our custom handling fails
                    try:
                        logger.info("Falling back to default markdown dump")
                        pipe_result.dump_md(
                            md_writer,
                            f'{base_filename}.md',
                            image_dir,
                            drop_mode=DropMode.NONE,
                            md_make_mode=f_make_md_mode,
                        )
                        
                        # Verify the fallback file was created
                        fallback_md_path = os.path.join(local_md_dir, f'{os.path.basename(pdf_file_name)}.md')
                        if os.path.exists(fallback_md_path):
                            if fallback_md_path != md_path:  # Only move if paths are different
                                try:
                                    os.replace(fallback_md_path, md_path)
                                    logger.info(f"Moved markdown file from {fallback_md_path} to {md_path}")
                                except Exception as move_error:
                                    logger.warning(f"Could not move {fallback_md_path} to {md_path}: {move_error}")
                                    # If move failed, use the fallback path
                                    md_path = fallback_md_path
                            
                            file_size = os.path.getsize(md_path)
                            logger.info(f"Markdown file created successfully at {md_path} ({file_size} bytes)")
                        else:
                            logger.error(f"Fallback markdown file was not created at {fallback_md_path}")
                            
                    except Exception as dump_error:
                        logger.error(f"Failed to generate markdown with fallback method: {str(dump_error)}", exc_info=True)
                        
            except Exception as e:
                logger.error(f"Error during markdown generation: {str(e)}", exc_info=True)
                raise
                
        except Exception as e:
            logger.error(f"Critical error during markdown generation: {str(e)}", exc_info=True)

    if f_dump_middle_json:
        try:
            # Save directly in the output directory (local_md_dir is already set to the correct path)
            middle_json_path = os.path.join(local_md_dir, f'{os.path.splitext(os.path.basename(pdf_file_name))[0]}_info.json')
            logger.info(f"Dumping middle JSON to {middle_json_path}")
            
            # Get the JSON data directly from infer_result
            json_data = infer_result.get_infer_res()
            
            # Write the JSON to file with signature data included
            with open(middle_json_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Middle JSON file with signature data created successfully at {middle_json_path}")
            
        except Exception as e:
            logger.error(f"Error dumping middle JSON: {str(e)}", exc_info=True)

    if f_dump_model_json:
        try:
            # Save directly in the output directory (local_md_dir is already set to the correct path)
            model_json_path = os.path.join(local_md_dir, f'{os.path.splitext(os.path.basename(pdf_file_name))[0]}_dets.json')
            
            # Initialize model_json as a dictionary
            model_json = {}
            
            # Get the model inference results if available
            if hasattr(infer_result, '_infer_res') and infer_result._infer_res is not None:
                if isinstance(infer_result._infer_res, (dict, list)):
                    model_json = infer_result._infer_res
                elif hasattr(infer_result._infer_res, '__dict__'):
                    model_json = infer_result._infer_res.__dict__
            
            # Ensure model_json is a dictionary
            if not isinstance(model_json, dict):
                model_json = {'data': model_json}
            
            # Add signature data if available
            if 'signature_data' in locals() and signature_data and any(signature_data):
                model_json['signatures'] = signature_data
            
            # Write the model JSON with signature data included
            with open(model_json_path, 'w', encoding='utf-8') as f:
                json.dump(model_json, f, indent=2, ensure_ascii=False)
            logger.info(f"Model JSON file with signature data created successfully at {model_json_path}")
            
        except Exception as e:
            logger.error(f"Error dumping model JSON: {str(e)}", exc_info=True)
    
    # Dump form data if form detection was enabled and the feature is enabled in config
    if detect_forms:
        try:
            form_config = get_form_invoice_enhancement_config()
            if form_config.get('enable', False):
                if hasattr(infer_result, 'dump_form_invoice_data') and hasattr(infer_result, '_form_invoice_data') and infer_result._form_invoice_data:
                    output_formats = form_config.get("output_formats", ["json"])
                    base_output_path = os.path.join(local_md_dir, os.path.basename(pdf_file_name))
                    logger.info(f"Dumping form data to {base_output_path} with formats: {output_formats}")
                    infer_result.dump_form_invoice_data(md_writer, base_output_path, output_formats)
                    
                    # Verify form data files were created
                    for fmt in output_formats:
                        output_file = f"{base_output_path}_form_invoice_data.{fmt}"
                        if os.path.exists(output_file):
                            file_size = os.path.getsize(output_file)
                            logger.info(f"Form data {fmt} file created successfully at {output_file} ({file_size} bytes)")
                        else:
                            logger.error(f"Form data {fmt} file was not created at {output_file}")
                else:
                    logger.info("No form data to dump or form data dumping not available")
            else:
                logger.info("Form data dumping is disabled in config")
        except Exception as e:
            logger.error(f"Error during form data processing: {str(e)}", exc_info=True)

    if f_dump_orig_pdf:
        try:
            output_pdf_path = os.path.join(local_md_dir, f'{os.path.basename(pdf_file_name)}_origin.pdf')
            logger.info(f"Writing original PDF to {output_pdf_path}")
            md_writer.write(
                f'{os.path.basename(pdf_file_name)}_origin.pdf',
                pdf_bytes,
            )
            if os.path.exists(output_pdf_path):
                file_size = os.path.getsize(output_pdf_path)
                logger.info(f"Original PDF file created successfully at {output_pdf_path} ({file_size} bytes)")
            else:
                logger.error(f"Original PDF file was not created at {output_pdf_path}")
        except Exception as e:
            logger.error(f"Error writing original PDF: {str(e)}", exc_info=True)

        # Always generate content list if chunking is enabled
    if f_dump_content_list or f_dump_chunk:
        try:
            # Ensure the output directory exists
            os.makedirs(local_md_dir, exist_ok=True)
            logger.info(f"Ensured output directory exists: {local_md_dir}")
            
            # Get just the base filename without path or extension
            base_filename = os.path.splitext(os.path.basename(pdf_file_name))[0]
            logger.info(f"Base filename: {base_filename}")
            
            # Create safe filenames
            content_list_path = os.path.join(local_md_dir, f'{base_filename}_content_list.json')
            temp_content_list_path = os.path.join(local_md_dir, f'temp_{base_filename}_content_list.json')
            
            logger.info(f'Writing content list to: {content_list_path}')
            
            # Get content list data
            logger.info("Generating content list...")
            content_list = pipe_result.get_content_list(image_dir)
            logger.info(f"Content list generated with {len(content_list) if content_list else 0} items")
            
            # Convert to JSON string
            json_str = json.dumps(content_list, ensure_ascii=False, indent=4)
            
            # Write to a temporary file first
            logger.info(f"Writing to temporary file: {temp_content_list_path}")
            with open(temp_content_list_path, 'w', encoding='utf-8') as f:
                f.write(json_str)
            
            logger.info(f'Temporary file written successfully')

            # Verify temp file was written
            if not os.path.exists(temp_content_list_path):
                raise IOError(f"Failed to write to temporary file: {temp_content_list_path}")
                
            temp_file_size = os.path.getsize(temp_content_list_path)
            logger.info(f"Temporary file written successfully ({temp_file_size} bytes)")
            
            # Remove existing file if it exists
            if os.path.exists(content_list_path):
                logger.info(f"Removing existing file: {content_list_path}")
                os.remove(content_list_path)
            
            # Move to final location
            logger.info(f"Moving temporary file to final location: {content_list_path}")
            os.rename(temp_content_list_path, content_list_path)
            
            # Verify final file
            if os.path.exists(content_list_path):
                final_file_size = os.path.getsize(content_list_path)
                logger.info(f"Content list file created successfully at {content_list_path} ({final_file_size} bytes)")
            else:
                logger.error(f"Content list file was not created at {content_list_path}")
                
        except Exception as e:
            logger.error(f'Error writing content list: {str(e)}', exc_info=True)
            
            # Clean up temp file if it exists
            if 'temp_content_list_path' in locals() and os.path.exists(temp_content_list_path):
                try:
                    logger.info(f"Cleaning up temporary file: {temp_content_list_path}")
                    os.remove(temp_content_list_path)
                except Exception as cleanup_error:
                    logger.error(f"Error cleaning up temporary file: {str(cleanup_error)}")
            raise

    if f_dump_chunk:
        try:
            from parsit.chunking.process import process as chunk_process
            
            logger.info("Starting chunking process...")
            
            # Verify the content list file exists before trying to read it
            if not os.path.exists(content_list_path):
                raise FileNotFoundError(f"Content list file not found at: {content_list_path}")

            logger.info(f'Reading content list from: {content_list_path}')
            file_size = os.path.getsize(content_list_path)
            logger.info(f'Content list file size: {file_size} bytes')
            
            with open(content_list_path, 'r', encoding='utf-8') as f:
                content_data = json.load(f)
            
            logger.info(f'Successfully loaded content list with {len(content_data) if isinstance(content_data, list) else "unknown"} items')

            # Create a safe output filename
            base_filename = os.path.splitext(os.path.basename(pdf_file_name))[0]
            chunks_path = os.path.join(local_md_dir, f'{base_filename}_chunks.json')
            logger.info(f'Will write chunks to: {chunks_path}')

            # Save content data to a temporary input file first
            temp_input_path = os.path.join(local_md_dir, f'temp_{base_filename}_input.json')
            logger.info(f'Writing content data to temporary input file: {temp_input_path}')
            
            with open(temp_input_path, 'w', encoding='utf-8') as f:
                json.dump(content_data, f, ensure_ascii=False, indent=4)
            
            logger.info(f'Temporary input file written successfully')

            # Process chunks and write to a temporary output file
            temp_chunks_path = os.path.join(local_md_dir, f'temp_{base_filename}_chunks.json')
            logger.info(f'Processing chunks with size={chunk_size}, overlap={chunk_overlap}, output={temp_chunks_path}')
            
            try:
                # Run the chunking process
                chunk_process(
                    temp_input_path,
                    output_path=temp_chunks_path,
                    chunk_size=chunk_size,
                    target_overlap=chunk_overlap
                )
                
                # Verify the output file was created
                if not os.path.exists(temp_chunks_path):
                    raise RuntimeError(f"Chunking process did not create output file at {temp_chunks_path}")
                    
                output_size = os.path.getsize(temp_chunks_path)
                logger.info(f'Chunking completed successfully. Output size: {output_size} bytes')
                
            except Exception as chunk_error:
                logger.error(f'Error during chunking process: {str(chunk_error)}', exc_info=True)
                raise
                
            finally:
                # Clean up the temporary input file
                try:
                    if os.path.exists(temp_input_path):
                        logger.info(f'Removing temporary input file: {temp_input_path}')
                        os.remove(temp_input_path)
                except Exception as cleanup_error:
                    logger.error(f'Error removing temporary input file: {str(cleanup_error)}')

            # Move the temporary output file to the final location
            logger.info(f'Moving temporary chunks file to final location: {chunks_path}')
            
            # Remove existing file if it exists
            if os.path.exists(chunks_path):
                logger.info(f'Removing existing chunks file: {chunks_path}')
                os.remove(chunks_path)
                
            # Perform the move
            os.rename(temp_chunks_path, chunks_path)
            
            # Verify the final file
            if os.path.exists(chunks_path):
                final_size = os.path.getsize(chunks_path)
                logger.info(f'Successfully wrote chunks to: {chunks_path} ({final_size} bytes)')
            else:
                logger.error(f'Failed to create final chunks file at: {chunks_path}')

        except Exception as e:
            logger.error(f'Error during chunking: {str(e)}', exc_info=True)
            
            # Clean up any remaining temporary files
            for temp_file in ['temp_input_path', 'temp_chunks_path']:
                if temp_file in locals() and os.path.exists(eval(temp_file)):
                    try:
                        logger.info(f'Cleaning up temporary file: {eval(temp_file)}')
                        os.remove(eval(temp_file))
                    except Exception as cleanup_error:
                        logger.error(f'Error cleaning up {temp_file}: {str(cleanup_error)}')
            
            # Re-raise the exception to maintain the original error
            raise

def do_parse (
output_dir ,
pdf_file_name ,
pdf_bytes_or_dataset ,
model_list ,
parse_method ,
debug_able =False ,
f_draw_span_bbox =True ,
f_draw_layout_bbox =True ,
f_dump_md =True ,
f_dump_middle_json =True ,
f_dump_model_json =True ,
f_dump_orig_pdf =True ,
f_dump_content_list =True ,
f_make_md_mode =MakeMode .MM_MD ,
f_draw_model_bbox =False ,
f_draw_line_sort_bbox =False ,
f_draw_char_bbox =False ,
start_page_id =0 ,
end_page_id =None ,
lang =None ,
layout_model =None ,
formula_enable =None ,
table_enable =None ,
f_dump_chunk =False ,
chunk_size =1000 ,
chunk_overlap =200 ,
detect_forms=False,
convert_html_tables=False,
detect_signatures=None,
):
    parallel_count =1 
    if os .environ .get ('parsit_PARALLEL_INFERENCE_COUNT'):
        parallel_count =int (os .environ ['parsit_PARALLEL_INFERENCE_COUNT'])

    if parallel_count >1 :
        if isinstance (pdf_bytes_or_dataset ,bytes ):
            pdf_bytes =convert_pdf_bytes_to_bytes_by_pymupdf (
            pdf_bytes_or_dataset ,start_page_id ,end_page_id 
            )
            ds =PymuDocDataset (pdf_bytes ,lang =lang )
        else :
            ds =pdf_bytes_or_dataset 
        batch_do_parse (output_dir ,[pdf_file_name ],[ds ],parse_method ,debug_able ,
        f_draw_span_bbox =f_draw_span_bbox ,
        f_draw_layout_bbox =f_draw_layout_bbox ,
        f_dump_md =f_dump_md ,
        f_dump_middle_json =f_dump_middle_json ,
        f_dump_model_json =f_dump_model_json ,
        f_dump_orig_pdf =f_dump_orig_pdf ,
        f_dump_content_list =f_dump_content_list ,
        f_make_md_mode =f_make_md_mode ,
        f_draw_model_bbox =f_draw_model_bbox ,
        f_draw_line_sort_bbox =f_draw_line_sort_bbox ,
        f_draw_char_bbox =f_draw_char_bbox ,
        lang =lang ,
        f_dump_chunk =f_dump_chunk ,
        chunk_size =chunk_size ,
        chunk_overlap =chunk_overlap ,
        detect_forms=detect_forms,
        convert_html_tables=convert_html_tables,
        detect_signatures=detect_signatures,
        )
    else :
        _do_parse (output_dir ,pdf_file_name ,pdf_bytes_or_dataset ,model_list ,parse_method ,debug_able ,
        start_page_id =start_page_id ,
        end_page_id =end_page_id ,
        lang =lang ,
        layout_model =layout_model ,
        formula_enable =formula_enable ,
        table_enable =table_enable ,
        f_draw_span_bbox =f_draw_span_bbox ,
        f_draw_layout_bbox =f_draw_layout_bbox ,
        f_dump_md =f_dump_md ,
        f_dump_middle_json =f_dump_middle_json ,
        f_dump_model_json =f_dump_model_json ,
        f_dump_orig_pdf =f_dump_orig_pdf ,
        f_dump_content_list =f_dump_content_list ,
        f_make_md_mode =f_make_md_mode ,
        f_draw_model_bbox =f_draw_model_bbox ,
        f_draw_line_sort_bbox =f_draw_line_sort_bbox ,
        f_draw_char_bbox =f_draw_char_bbox ,
        f_dump_chunk =f_dump_chunk ,
        chunk_size =chunk_size ,
        chunk_overlap =chunk_overlap ,
        detect_forms=detect_forms,
        convert_html_tables=convert_html_tables,
        detect_signatures=detect_signatures,
        )


def batch_do_parse (
output_dir ,
pdf_file_names :list [str ] ,
pdf_bytes_or_datasets :list [bytes |Dataset ] ,
parse_method ,
debug_able =False ,
f_draw_span_bbox =True ,
f_draw_layout_bbox =True ,
f_dump_md =True ,
f_dump_middle_json =True ,
f_dump_model_json =True ,
f_dump_orig_pdf =True ,
f_dump_content_list =True ,
f_make_md_mode =MakeMode .MM_MD ,
f_draw_model_bbox =False ,
f_draw_line_sort_bbox =False ,
f_draw_char_bbox =False ,
lang =None ,
layout_model =None ,
formula_enable =None ,
table_enable =None ,
f_dump_chunk =False ,
chunk_size =1000 ,
chunk_overlap =200 ,
detect_forms=False,
convert_html_tables=False,
detect_signatures=None,
):
    dss =[]
    for v in pdf_bytes_or_datasets :
        if isinstance (v ,bytes ):
            dss .append (PymuDocDataset (v ,lang =lang ))
        else :
            dss .append (v )

    infer_results =batch_doc_analyze (dss ,parse_method ,lang =lang ,layout_model =layout_model ,formula_enable =formula_enable ,table_enable =table_enable )
    for idx ,infer_result in enumerate (infer_results ):
        infer_result = InferenceResult(
            output_dir=output_dir,
            filename=pdf_file_names[idx],
            dataset=pdf_bytes_or_datasets[idx],
            model_list=infer_result.get_infer_res(),
            parse_method=parse_method,
            f_draw_span_bbox=f_draw_span_bbox,
            f_draw_layout_bbox=f_draw_layout_bbox,
            f_dump_md=f_dump_md,
            f_dump_middle_json=f_dump_middle_json,
            f_dump_model_json=f_dump_model_json,
            f_dump_orig_pdf=f_dump_orig_pdf,
            f_dump_content_list=f_dump_content_list,
            f_make_md_mode=f_make_md_mode,
            f_draw_model_bbox=f_draw_model_bbox,
            f_draw_line_sort_bbox=f_draw_line_sort_bbox,
            f_draw_char_bbox=f_draw_char_bbox,
            layout_model=layout_model,
            formula_enable=formula_enable,
            table_enable=table_enable,
            f_dump_chunk=f_dump_chunk,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        # Store form data in the inference result if available in dataset
        if hasattr(pdf_bytes_or_datasets[idx], 'form_data'):
            infer_result.form_data = pdf_bytes_or_datasets[idx].form_data
            logger.info(f"Added form data to inference result: {bool(infer_result.form_data)}")
        _do_parse(
            output_dir=output_dir,
            pdf_file_name=pdf_file_names[idx],
            pdf_bytes_or_dataset=pdf_bytes_or_datasets[idx],
            model_list=infer_result.get_infer_res(),
            parse_method=parse_method,
            debug_able=debug_able,
            f_draw_span_bbox=f_draw_span_bbox,
            f_draw_layout_bbox=f_draw_layout_bbox,
            f_dump_md=f_dump_md,
            f_dump_middle_json=f_dump_middle_json,
            f_dump_model_json=f_dump_model_json,
            f_dump_orig_pdf=f_dump_orig_pdf,
            f_dump_content_list=f_dump_content_list,
            f_make_md_mode=f_make_md_mode,
            f_draw_model_bbox=f_draw_model_bbox,
            f_draw_line_sort_bbox=f_draw_line_sort_bbox,
            f_draw_char_bbox=f_draw_char_bbox,
            lang=lang,
            layout_model=layout_model,
            formula_enable=formula_enable,
            table_enable=table_enable,
            f_dump_chunk=f_dump_chunk,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            detect_forms=detect_forms,
            convert_html_tables=convert_html_tables,
        )


parse_pdf_methods =click .Choice (['ocr','txt','auto'])
