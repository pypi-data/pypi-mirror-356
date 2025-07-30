from typing import List, Tuple, Optional
from pathlib import Path
import fitz  # PyMuPDF
from PIL import Image
import io
import tempfile
import logging

logger = logging.getLogger(__name__)

def extract_page_image(
    pdf_bytes: bytes,
    page_num: int = 0,
    dpi: int = 200,
    output_path: Optional[str] = None
) -> Optional[str]:
    """
    Extract an image from a specific page of a PDF.
    
    Args:
        pdf_bytes: Raw bytes of the PDF file
        page_num: Page number to extract (0-based)
        dpi: DPI for the output image
        output_path: Optional path to save the image. If None, a temporary file will be created.
        
    Returns:
        Path to the saved image file, or None if extraction failed
    """
    try:
        # Open the PDF from bytes
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        # Check if page number is valid
        if page_num < 0 or page_num >= len(doc):
            logger.warning(f"Page number {page_num} is out of range (0-{len(doc)-1})")
            return None
        
        # Get the page
        page = doc.load_page(page_num)
        
        # Calculate zoom factor for desired DPI (72 is the default PDF DPI)
        zoom = dpi / 72
        mat = fitz.Matrix(zoom, zoom)
        
        # Render page to an image (pixmap)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        
        # Convert to PIL Image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        # Save to file
        if output_path is None:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                output_path = temp_file.name
        
        img.save(output_path, 'PNG', dpi=(dpi, dpi))
        return output_path
        
    except Exception as e:
        logger.error(f"Error extracting page image: {e}")
        return None

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extract text from a PDF file."""
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}")
        return ""

def is_text_based_pdf(pdf_bytes: bytes, min_text_ratio: float = 0.1) -> bool:
    """
    Check if a PDF is text-based by analyzing the text-to-page ratio.
    
    Args:
        pdf_bytes: Raw bytes of the PDF file
        min_text_ratio: Minimum ratio of text to total pages to consider as text-based
        
    Returns:
        bool: True if the PDF is text-based, False otherwise
    """
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        if len(doc) == 0:
            return False
            
        text_pages = 0
        for page in doc:
            text = page.get_text()
            if text.strip():  # If page has any text
                text_pages += 1
                
        ratio = text_pages / len(doc)
        return ratio >= min_text_ratio
        
    except Exception as e:
        logger.error(f"Error checking if PDF is text-based: {e}")
        return False
