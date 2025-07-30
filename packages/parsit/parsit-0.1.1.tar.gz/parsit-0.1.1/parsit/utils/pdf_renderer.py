import fitz  # PyMuPDF
import pypdfium2
from typing import Dict, List, Tuple, Optional, Union, Any, BinaryIO
import io
import logging
import tempfile
import os
import time
from pathlib import Path
from loguru import logger
import re

def log_page_info(page: fitz.Page, page_num: int):
    """Log detailed information about a PDF page and return page metadata.
    
    Args:
        page: PyMuPDF Page object
        page_num: Page number (0-based)
        
    Returns:
        dict: Dictionary containing page metadata
    """
    try:
        widgets = list(page.widgets())
        page_info = {
            'page_num': page_num,
            'rotation': page.rotation,
            'rect': str(page.rect),
            'crop_box': str(page.cropbox),
            'mediabox_size': f"{page.mediabox.width:.1f}x{page.mediabox.height:.1f}",
            'has_forms': len(widgets) > 0,
            'num_widgets': len(widgets),
            'widget_types': [w.field_type_string for w in widgets]
        }
        logger.debug(f"Page {page_num} info: {page_info}")
        return page_info
    except Exception as e:
        logger.warning(f"Error logging page info: {e}")
        return {'page_num': page_num, 'error': str(e)}

def create_hybrid_pdf_with_form_pages(
    pdf_bytes: bytes, 
    form_pages: Dict[int, dict],
    scale: float = 2.0,
    dpi: int = 300
) -> bytes:
    """
    Create a hybrid PDF where pages with forms are flattened to preserve text formatting.
    
    Args:
        pdf_bytes: Original PDF as bytes
        form_pages: Dictionary mapping page numbers to form field information
        scale: Unused, kept for compatibility
        dpi: Unused, kept for compatibility
        
    Returns:
        bytes: New PDF with form fields flattened
    """
    start_time = time.time()
    logger.info("Starting hybrid PDF creation with form flattening")
    
    if not any(info.get('has_forms', False) for info in form_pages.values()):
        logger.info("No pages with forms to process")
        return pdf_bytes  # No pages with forms, return original
    
    tmp_path = None
    try:
        # Create a temporary file for the original PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(pdf_bytes)
            tmp_path = tmp_file.name
        
        logger.debug(f"Created temporary file at: {tmp_path}")
        
        # Open the original PDF with PyMuPDF
        doc = fitz.open(tmp_path)
        total_pages = len(doc)
        logger.info(f"Processing {total_pages} pages, {sum(1 for v in form_pages.values() if v.get('has_forms', False))} with forms")
        
        # Create a new PDF for the output
        new_doc = fitz.open()
        
        for page_num in range(total_pages):
            page = doc[page_num]
            page_info = log_page_info(page, page_num)
            
            if form_pages.get(page_num, {}).get('has_forms', False):
                logger.debug(f"Processing form fields on page {page_num}")
                page_start_time = time.time()
                
                try:
                    # Create a new page with the same dimensions
                    new_page = new_doc.new_page(
                        width=page.rect.width,
                        height=page.rect.height
                    )
                    
                    # Copy the page content (without form fields)
                    new_page.show_pdf_page(
                        new_page.rect,  # Target rectangle
                        doc,             # Source document
                        page_num         # Source page number
                    )
                    
                    # Flatten form fields (this converts form fields to regular text/graphics)
                    new_page.wrap_contents()
                    
                    # Get form fields for this page
                    form_fields = form_pages[page_num].get('fields', [])
                    
                    # Draw form field values as text
                    for field in form_fields:
                        try:
                            field_type = field.get('type', '')
                            raw_field_value = field.get('value', '') # Preserve original for potential logging
                            
                            # Normalize whitespace: replace multiple spaces/tabs/newlines with a single space, and strip
                            # Also convert to string to be safe, as .get might return non-string
                            field_value = re.sub(r'\s+', ' ', str(raw_field_value)).strip()
                            
                            if not field_value: # Check after normalization
                                continue
                                
                            # Parse the rectangle from string if needed
                            if isinstance(field.get('rect'), str):
                                # Parse string like "Rect(72.0, 72.0, 216.0, 90.0)"
                                rect_str = field['rect'].replace('Rect(', '').replace(')', '')
                                x0, y0, x1, y1 = map(float, rect_str.split(','))
                                rect = fitz.Rect(x0, y0, x1, y1)
                            else:
                                rect = field.get('rect')
                            
                            if not rect:
                                continue
                                
                            # Add padding to the rectangle
                            padding = 2
                            rect = fitz.Rect(
                                rect.x0 + padding,
                                rect.y0 + padding,
                                rect.x1 - padding,
                                rect.y1 - padding
                            )
                            
                            # Try multiple font sizes to find the best fit
                            font_sizes = [11, 10, 9, 8, 7, 6]
                            text_fitted = False
                            
                            for font_size in font_sizes:
                                # Create a temporary text object to measure the text
                                rc = new_page.insert_textbox(
                                    rect,
                                    str(field_value),
                                    fontname='Helv',
                                    fontsize=font_size,
                                    color=(0, 0, 0),
                                    align=0,  # Left align
                                    expandtabs=4,
                                    rotate=0,
                                    morph=None,
                                    overlay=False  # Don't actually insert yet
                                )
                                
                                if rc > 0:  # Text fits with this font size
                                    # Now insert it for real with the same parameters
                                    new_page.insert_textbox(
                                        rect,
                                        str(field_value),
                                        fontname='Helv',
                                        fontsize=font_size,
                                        color=(0, 0, 0),
                                        align=0,
                                        expandtabs=4,
                                        rotate=0,
                                        morph=None,
                                        overlay=True
                                    )
                                    text_fitted = True
                                    break
                            
                            if not text_fitted:
                                # If we couldn't fit with any font size, try truncating
                                max_chars = int(len(str(field_value)) * (rect.width / 100))  # Rough estimate
                                if max_chars > 3:  # Only truncate if we can show at least 3 chars + "..."
                                    truncated_text = str(field_value)[:max_chars-3] + "..."
                                    new_page.insert_textbox(
                                        rect,
                                        truncated_text,
                                        fontname='Helv',
                                        fontsize=6,  # Smallest font size
                                        color=(0, 0, 0),
                                        align=0,
                                        overlay=True
                                    )
                                logger.warning(f"Text didn't fit in form field, using fallback: {field_value}")
                                
                        except Exception as e:
                            logger.error(f"Error processing form field {field.get('name', 'unknown')}: {str(e)}")
                    
                    # Remove any remaining form fields from the new page
                    try:
                        for widget in new_page.widgets():
                            new_page.delete_widget(widget)
                        # Ensure changes are applied
                        new_page.clean_contents()
                    except Exception as e:
                        logger.warning(f"Error removing form fields: {str(e)}")
                    
                    page_end_time = time.time()
                    logger.debug(f"Processed form fields on page {page_num} in {page_end_time - page_start_time:.2f}s")
                    
                except Exception as page_error:
                    logger.error(f"Error processing page {page_num}: {str(page_error)}", exc_info=True)
                    # Fall back to original page if processing fails
                    new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
                    continue
                
            else:
                # Page doesn't have forms, copy it as-is
                new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
        
        # Save the new PDF to a bytes buffer
        output_buffer = io.BytesIO()
        new_doc.save(output_buffer)
        output_bytes = output_buffer.getvalue()
        
        # Clean up
        new_doc.close()
        doc.close()
        
        end_time = time.time()
        logger.info(f"Created hybrid PDF in {end_time - start_time:.2f}s. Size: {len(output_bytes)} bytes")
        
        return output_bytes
        
    except Exception as e:
        logger.error(f"Error creating hybrid PDF: {str(e)}", exc_info=True)
        raise  # Re-raise the exception to be handled by the caller
        
    finally:
        # Clean up temporary file if it exists
        if tmp_path and os.path.exists(tmp_path):
            max_attempts = 3
            for attempt in range(max_attempts):
                try:
                    os.unlink(tmp_path)
                    break  # Successfully deleted, exit the loop
                except PermissionError as e:
                    if attempt == max_attempts - 1:  # Last attempt
                        logger.warning(f"Failed to delete temporary file after {max_attempts} attempts: {tmp_path}")
                    else:
                        time.sleep(0.1)  # Short delay before retry
                except Exception as e:
                    logger.warning(f"Error deleting temporary file {tmp_path}: {e}")
                    break  # For other errors, don't retry

def render_page_as_image(
    page: 'fitz.Page',
    scale: float = 2.0,
    dpi: int = 300
) -> 'fitz.Pixmap':
    """
    Render a PDF page as a high-resolution image.
    
    Args:
        page: PyMuPDF Page object
        scale: Scale factor (default: 2.0)
        dpi: DPI for the output image (default: 300)
        
    Returns:
        fitz.Pixmap: Rendered page as a pixmap
    """
    zoom = dpi / 72  # 72 DPI is the default PDF resolution
    mat = fitz.Matrix(zoom * scale, zoom * scale)
    return page.get_pixmap(matrix=mat, alpha=False)
