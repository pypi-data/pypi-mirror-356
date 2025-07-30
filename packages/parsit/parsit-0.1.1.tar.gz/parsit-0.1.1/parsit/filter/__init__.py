
from pathlib import Path
import tempfile
import logging
from typing import Optional

from parsit.config.drop_reason import DropReason
from parsit.config.enums import SupportedPdfParseMethod
from parsit.filter.document_classifier import document_classifier
from parsit.filter.pdf_meta_scan import pdf_meta_scan
from parsit.filter.pdf_classify_by_type import classify as legacy_classify

logger = logging.getLogger(__name__)

def classify(pdf_bytes: bytes) -> SupportedPdfParseMethod:
    """
    Classify a PDF document to determine if it's text-based or requires OCR.
    Uses a combination of metadata analysis and a deep learning model for classification.
    
    Args:
        pdf_bytes: Raw bytes of the PDF file
        
    Returns:
        SupportedPdfParseMethod: Either TXT (text-based) or OCR (requires OCR)
        
    Raises:
        Exception: If the PDF is encrypted, password-protected, or invalid
    """
    # First, perform basic PDF metadata analysis
    pdf_meta = pdf_meta_scan(pdf_bytes)
    
    # Check if we should drop the PDF
    if pdf_meta.get('_need_drop', False):
        raise Exception(f"PDF meta_scan needs drop, reason: {pdf_meta['_drop_reason']}")
    
    # Check for encryption or password protection
    if pdf_meta.get('is_encrypted', False) or pdf_meta.get('is_needs_password', False):
        raise Exception(f'PDF is encrypted or password protected: {DropReason.ENCRYPTED}')
    
    # If we have images, use the model-based classifier
    if pdf_meta.get('imgs_per_page') and any(pdf_meta['imgs_per_page']):
        try:
            # Save the first page image to a temporary file
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                temp_path = temp_file.name
                # Assuming the first page image is at index 0 in the first page's image list
                if pdf_meta['image_info_per_page'] and pdf_meta['image_info_per_page'][0]:
                    # This is a simplified example - in practice, you'd need to extract the actual image
                    # from the PDF and save it to temp_path
                    pass
            
            # Use the document classifier
            is_text_doc, results = document_classifier.classify_document(temp_path)
            logger.info(f"Document classification results: {results}")
            
            # Clean up temporary file
            try:
                Path(temp_path).unlink(missing_ok=True)
            except Exception as e:
                logger.warning(f"Failed to delete temporary file {temp_path}: {e}")
            
            return SupportedPdfParseMethod.TXT if is_text_doc else SupportedPdfParseMethod.OCR
            
        except Exception as e:
            logger.warning(f"Model-based classification failed, falling back to legacy method: {e}")
    
    # Fall back to legacy classification method
    is_text_pdf, results = legacy_classify(
        pdf_meta['total_page'],
        pdf_meta['page_width_pts'],
        pdf_meta['page_height_pts'],
        pdf_meta['image_info_per_page'],
        pdf_meta['text_len_per_page'],
        pdf_meta['imgs_per_page'],
        pdf_meta['invalid_chars'],
    )
    
    return SupportedPdfParseMethod.TXT if is_text_pdf else SupportedPdfParseMethod.OCR 
