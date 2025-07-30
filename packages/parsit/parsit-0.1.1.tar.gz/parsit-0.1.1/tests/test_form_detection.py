import os
import sys
import json
import fitz
import traceback
from pathlib import Path
from loguru import logger

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath('.'))

try:
    from parsit.utils.form_detector import detect_form_fields_per_page
    from parsit.utils.pdf_renderer import create_hybrid_pdf_with_form_pages
except ImportError as e:
    logger.error(f"Failed to import required modules: {e}")
    sys.exit(1)

def extract_form_fields(pdf_bytes):
    """Extract form fields from PDF bytes."""
    try:
        doc = fitz.open(stream=pdf_bytes, filetype='pdf')
        fields = {}
        for page_num in range(len(doc)):
            page = doc[page_num]
            try:
                widgets = list(page.widgets())
                if widgets:
                    fields[page_num] = []
                    for widget in widgets:
                        try:
                            fields[page_num].append({
                                'type': str(widget.field_type).split('.')[-1],
                                'rect': str(widget.rect),
                                'field_name': str(widget.field_name),
                                'field_value': str(widget.field_value) if widget.field_value is not None else None,
                            })
                        except Exception as e:
                            logger.warning(f"Error processing widget on page {page_num}: {e}")
            except Exception as e:
                logger.warning(f"Error processing page {page_num}: {e}")
        return fields
    except Exception as e:
        logger.error(f"Error extracting form fields: {e}")
        return {}

def test_form_detection(pdf_path):
    """Test form detection and hybrid PDF generation on a PDF file."""
    logger.info(f"\n{'='*80}")
    logger.info(f"Testing form detection on: {pdf_path}")
    logger.info(f"{'='*80}")
    
    try:
        # Read the PDF
        with open(pdf_path, 'rb') as f:
            pdf_bytes = f.read()
        
        # Extract form fields from original PDF
        logger.info("Extracting form fields from original PDF...")
        original_fields = extract_form_fields(pdf_bytes)
        logger.info(f"Original PDF form fields: {json.dumps(original_fields, indent=2, default=str)}")
        
        # Test form detection
        logger.info("Detecting form fields...")
        form_pages = detect_form_fields_per_page(pdf_bytes)
        logger.info(f"Form pages detected: {form_pages}")
        
        # Test hybrid PDF generation if form fields were detected
        if any(form_pages.values()):
            logger.info("Creating hybrid PDF...")
            hybrid_pdf_bytes = create_hybrid_pdf_with_form_pages(pdf_bytes, form_pages)
            
            # Save the hybrid PDF for inspection
            output_path = str(Path(pdf_path).with_stem(f"{Path(pdf_path).stem}_hybrid"))
            with open(output_path, 'wb') as f:
                f.write(hybrid_pdf_bytes)
            logger.info(f"Hybrid PDF saved to: {output_path}")
            
            # Extract form fields from hybrid PDF for comparison
            logger.info("Extracting form fields from hybrid PDF...")
            hybrid_fields = extract_form_fields(hybrid_pdf_bytes)
            logger.info(f"Hybrid PDF form fields: {json.dumps(hybrid_fields, indent=2, default=str)}")
            
            # Compare original and hybrid form fields
            if original_fields != hybrid_fields:
                logger.warning("Form fields differ between original and hybrid PDFs")
                
                # Find differences
                for page_num in set(original_fields) | set(hybrid_fields):
                    orig = original_fields.get(page_num, [])
                    hybrid = hybrid_fields.get(page_num, [])
                    if orig != hybrid:
                        logger.warning(f"Page {page_num} differences:")
                        logger.warning(f"Original: {orig}")
                        logger.warning(f"Hybrid:   {hybrid}")
            
            return {
                'original_fields': original_fields,
                'hybrid_fields': hybrid_fields,
                'hybrid_pdf_path': output_path
            }
        else:
            logger.warning("No form fields detected in the PDF")
            return None
            
    except Exception as e:
        logger.error(f"Error processing {pdf_path}: {e}")
        logger.error(traceback.format_exc())
        return None

if __name__ == "__main__":
    # Set up logging
    logger.remove()
    logger.add(
        sys.stderr,
        level="DEBUG",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )
    
    # Test with provided PDFs
    test_pdfs = [
        "demo/w8.pdf",
        "demo/Form.pdf"
    ]
    
    # Create output directory if it doesn't exist
    os.makedirs("test_output", exist_ok=True)
    
    for pdf_path in test_pdfs:
        if not os.path.exists(pdf_path):
            logger.error(f"File not found: {pdf_path}")
            continue
            
        logger.info(f"\n{'='*80}")
        logger.info(f"Testing: {pdf_path}")
        logger.info(f"{'='*80}")
        
        result = test_form_detection(pdf_path)
        if result:
            logger.success(f"Test completed for {pdf_path}")
            logger.info(f"Hybrid PDF saved to: {result['hybrid_pdf_path']}")
            
            # Save results to JSON file
            output_file = os.path.join("test_output", f"{Path(pdf_path).stem}_results.json")
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'pdf_path': pdf_path,
                    'original_fields': result['original_fields'],
                    'hybrid_fields': result['hybrid_fields'],
                    'hybrid_pdf_path': result['hybrid_pdf_path']
                }, f, indent=2, ensure_ascii=False)
            logger.info(f"Results saved to: {output_file}")
    
    logger.info("\nTest completed!")
