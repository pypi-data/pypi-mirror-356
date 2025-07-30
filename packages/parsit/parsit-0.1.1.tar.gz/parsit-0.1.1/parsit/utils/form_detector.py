import fitz  # PyMuPDF
from typing import Dict, List, Tuple, Optional, Union, Any, Generator
import io
import logging
from loguru import logger
import re

def log_form_field(field):
    """Log detailed information about a form field."""
    try:
        raw_field_value = field.field_value
        normalized_value = re.sub(r'\s+', ' ', str(raw_field_value)).strip()
        field_info = {
            'type': field.field_type_string,
            'name': field.field_name,
            'value': normalized_value,
            'rect': str(field.rect),
            'readonly': getattr(field, 'is_readonly', False),
            'field_type': field.field_type,
            'field_flags': getattr(field, 'field_flags', 0)
        }
        logger.debug(f"Found form field: {field_info}")
        return field_info
    except Exception as e:
        logger.warning(f"Error logging form field: {e}")
        # Return basic field info even if some attributes are missing
        raw_field_value_fallback = getattr(field, 'field_value', '')
        normalized_value_fallback = re.sub(r'\s+', ' ', str(raw_field_value_fallback)).strip()
        return {
            'type': getattr(field, 'field_type_string', 'unknown'),
            'name': getattr(field, 'field_name', 'unknown'),
            'value': normalized_value_fallback,
            'rect': str(getattr(field, 'rect', ''))
        }

def get_form_fields(doc: fitz.Document) -> Generator[tuple[int, Any], None, None]:
    """
    Generator that yields all form fields in the document with their page numbers.
    
    Args:
        doc: PyMuPDF Document object
        
    Yields:
        Tuple of (page_num, field) for each form field in the document
    """
    for page_num in range(len(doc)):
        page = doc[page_num]
        for widget in page.widgets():
            yield page_num, widget

def detect_form_fields_per_page(pdf_bytes: bytes) -> Dict[int, dict]:
    """
    Detect form fields in the PDF and return detailed information per page.
    
    Args:
        pdf_bytes: PDF file as bytes
        
    Returns:
        Dict[int, dict]: Dictionary mapping page numbers (0-based) to a dictionary
                       containing form field information for that page
    """
    logger.info("Starting form field detection")
    result = {}
    
    try:
        # Log the first 100 bytes of the PDF to verify it's valid
        logger.debug(f"PDF bytes length: {len(pdf_bytes)}")
        
        # Try to open the PDF with different methods
        doc = None
        try:
            # First try opening as bytes
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            logger.debug("Successfully opened PDF from bytes")
        except Exception as e:
            logger.error(f"Failed to open PDF from bytes: {str(e)}")
            # Try opening from a temporary file as fallback
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                tmp.write(pdf_bytes)
                tmp_path = tmp.name
            try:
                doc = fitz.open(tmp_path)
                logger.debug("Successfully opened PDF from temporary file")
                os.unlink(tmp_path)
            except Exception as e2:
                logger.error(f"Also failed to open PDF from temp file: {str(e2)}")
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
                raise e
        
        if doc is None:
            logger.error("Failed to open PDF with all methods")
            return {}
            
        total_pages = len(doc)
        logger.info(f"Processing {total_pages} pages")
        
        # Initialize result with empty fields list for each page
        result = {i: {'has_forms': False, 'fields': []} for i in range(total_pages)}
        
        # Process each page for form fields
        for page_num in range(total_pages):
            try:
                page = doc[page_num]
                logger.debug(f"Processing page {page_num}")
                
                # Get all widgets on the page
                widgets = list(page.widgets())
                logger.info(f"Found {len(widgets)} widgets on page {page_num}")
                
                if widgets:
                    result[page_num]['has_forms'] = True
                    for widget in widgets:
                        try:
                            field_info = log_form_field(widget)
                            if field_info:
                                result[page_num]['fields'].append(field_info)
                        except Exception as e:
                            logger.warning(f"Error processing widget on page {page_num}: {str(e)}")
                
                logger.debug(f"Page {page_num} form fields: {len(result[page_num]['fields'])}")
                
            except Exception as e:
                logger.error(f"Error processing page {page_num}: {str(e)}")
                continue
                
        doc.close()
        logger.info(f"Completed form field detection. Found forms on {sum(1 for v in result.values() if v['has_forms'])} pages")
        
    except Exception as e:
        logger.error(f"Error in detect_form_fields_per_page: {str(e)}", exc_info=True)
        # Return empty result on error
        return {}
        
    return result

def get_form_field_details(page) -> List[Dict[str, Any]]:
    """
    Get detailed information about form fields on a page.
    
    Args:
        page: PyMuPDF page object
        
    Returns:
        List of dictionaries containing form field information
    """
    form_fields = []
    
    # Process widgets (form fields)
    for field in page.widgets():
        field_rect = field.rect
        form_fields.append({
            'type': 'widget',
            'field_type': field.field_type_string,
            'field_name': field.field_name,
            'rect': (field_rect.x0, field_rect.y0, field_rect.x1, field_rect.y1),
            'value': field.field_value,
        })
    
    # Process annotations that might be form elements
    for annot in page.annots():
        if annot.type[0] in (
            fitz.PDF_ANNOT_WIDGET,
            fitz.PDF_ANNOT_TEXT,
            fitz.PDF_ANNOT_CHOICE,
            fitz.PDF_ANNOT_SIGNATURE
        ):
            annot_rect = annot.rect
            form_fields.append({
                'type': 'annotation',
                'annotation_type': annot.type[1],
                'rect': (annot_rect.x0, annot_rect.y0, annot_rect.x1, annot_rect.y1),
                'content': annot.info.get('content', ''),
            })
    
    return form_fields
