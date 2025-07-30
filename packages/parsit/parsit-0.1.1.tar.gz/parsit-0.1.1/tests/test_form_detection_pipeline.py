import sys
import os
import logging
from loguru import logger
from pathlib import Path
import fitz  # PyMuPDF

# Add the project root to Python path
sys.path.insert(0, os.path.abspath('.'))

# Import the form detector directly
from parsit.utils.form_detector import detect_form_fields_per_page

def main():
    # Set up logging
    logger.remove()
    logger.add(sys.stderr, level="DEBUG")
    
    # Test with Form.pdf
    pdf_path = Path("demo/Form.pdf")
    if not pdf_path.exists():
        logger.error(f"File not found: {pdf_path}")
        return
    
    logger.info(f"Testing form detection on: {pdf_path}")
    
    # Read the PDF file
    with open(pdf_path, 'rb') as f:
        pdf_bytes = f.read()
    
    logger.info(f"PDF size: {len(pdf_bytes)} bytes")
    
    # Run form detection
    try:
        form_pages = detect_form_fields_per_page(pdf_bytes)
        logger.info(f"Form detection result: {form_pages}")
        
        # Additional verification
        if any(form_pages.values()):
            logger.success("Form fields detected!")
            for page_num, has_forms in form_pages.items():
                if has_forms:
                    logger.info(f"Page {page_num} has form fields")
        else:
            logger.warning("No form fields detected. This may be incorrect.")
            
            # Try opening with PyMuPDF directly
            try:
                doc = fitz.open(pdf_path)
                for page_num in range(len(doc)):
                    page = doc[page_num]
                    widgets = list(page.widgets())
                    logger.warning(f"Direct PyMuPDF check - Page {page_num} has {len(widgets)} widgets")
                    for widget in widgets:
                        logger.warning(f"  Widget: {widget.field_type_string} - {widget.field_name}")
                doc.close()
            except Exception as e:
                logger.error(f"Error in direct PyMuPDF check: {e}")
                
    except Exception as e:
        logger.error(f"Error during form detection: {e}", exc_info=True)

if __name__ == "__main__":
    main()
