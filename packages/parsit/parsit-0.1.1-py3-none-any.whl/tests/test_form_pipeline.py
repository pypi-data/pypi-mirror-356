import os
import sys
import subprocess
import shutil
import fitz  # PyMuPDF
from pathlib import Path
import json
import logging
from loguru import logger

# Configure logging
logger.remove()  # Remove default handler
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)
logger.add(
    'test_form_pipeline.log',
    level="DEBUG",
    rotation="1 MB",
    retention="1 day",
    compression="zip"
)

def run_pipeline_with_forms(pdf_path: Path, output_dir: Path) -> bool:
    """Run the pipeline with form detection enabled."""
    try:
        # Clean up previous output directory
        if output_dir.exists():
            logger.warning(f"Removing existing output directory: {output_dir}")
            shutil.rmtree(output_dir, ignore_errors=True)
        
        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Build the command with debug logging
        cmd = [
            sys.executable,
            "-m", "parsit.tools.cli",
            "-p", str(pdf_path.absolute()),
            "-o", str(output_dir.absolute()),
            "--detect-forms",
            "--debug"  # Enable debug logging
        ]
        
        logger.info(f"Running command: {' '.join(cmd)}")
        
        # Run the command and capture output in real-time
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Stream output in real-time
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                logger.info(f"[PIPE] {output.strip()}")
        
        # Get any remaining output
        stdout, stderr = process.communicate()
        
        if stdout:
            logger.info(f"Process stdout: {stdout}")
        if stderr:
            logger.warning(f"Process stderr: {stderr}")
        
        if process.returncode != 0:
            logger.error(f"Process failed with return code {process.returncode}")
            return False
            
        return True
        
    except Exception as e:
        logger.error(f"Error running pipeline: {str(e)}", exc_info=True)
        return False

def analyze_pdf_for_forms(pdf_path: Path) -> dict:
    """Analyze PDF for form fields and return detailed information."""
    result = {
        'has_forms': False,
        'page_count': 0,
        'pages_with_forms': [],
        'form_fields': []
    }
    
    try:
        with fitz.open(pdf_path) as doc:
            result['page_count'] = len(doc)
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                has_forms = False
                
                # Check for form widgets
                widgets = list(page.widgets())
                if widgets:
                    has_forms = True
                    for widget in widgets:
                        result['form_fields'].append({
                            'page': page_num + 1,
                            'type': widget.field_type_string,
                            'name': widget.field_name,
                            'value': widget.field_value,
                            'rect': str(widget.rect)
                        })
                
                # Check for form annotations
                if not has_forms:
                    for annot in page.annots():
                        if annot.type[0] in (fitz.PDF_ANNOT_WIDGET, fitz.PDF_ANNOT_TEXT, 
                                          fitz.PDF_ANNOT_CHOICE, fitz.PDF_ANNOT_SIGNATURE):
                            has_forms = True
                            result['form_fields'].append({
                                'page': page_num + 1,
                                'type': 'annotation',
                                'subtype': annot.type[1],
                                'rect': str(annot.rect)
                            })
                            break
                
                if has_forms:
                    result['pages_with_forms'].append(page_num + 1)
            
            result['has_forms'] = len(result['pages_with_forms']) > 0
            
    except Exception as e:
        logger.error(f"Error analyzing PDF for forms: {str(e)}", exc_info=True)
    
    return result

def check_form_detection(output_dir: Path) -> bool:
    """Check if form detection produced the expected output files and analyze results."""
    logger.info(f"Checking form detection results in: {output_dir}")
    
    # Find all subdirectories that might contain output
    result_dirs = []
    for root, dirs, _ in os.walk(output_dir):
        for d in dirs:
            if 'auto' in d.lower() or 'output' in d.lower() or 'result' in d.lower():
                result_dirs.append(Path(root) / d)
    
    if not result_dirs:
        result_dirs = [output_dir]
    
    success = True
    
    for result_dir in result_dirs:
        logger.info(f"Checking directory: {result_dir}")
        
        # Check for expected output files
        expected_files = [
            "*.pdf",  # At least one PDF output
            "*.json",  # Some JSON output
        ]
        
        found_files = []
        for pattern in expected_files:
            matches = list(result_dir.glob(pattern))
            if not matches:
                logger.warning(f"No files matching {pattern} found in {result_dir}")
                success = False
            else:
                found_files.extend(matches)
        
        # Look for form data JSON
        form_data_files = list(result_dir.glob("*form*data*.json")) + list(result_dir.glob("*form*invoice*.json"))
        if not form_data_files:
            logger.warning(f"No form data JSON file found in {result_dir}")
            success = False
        else:
            for form_file in form_data_files:
                try:
                    with open(form_file, 'r', encoding='utf-8') as f:
                        form_data = json.load(f)
                        logger.info(f"Found form data in {form_file.name}: {len(form_data)} items")
                        if form_data:
                            logger.debug(f"Sample form data: {json.dumps(form_data[0], indent=2, ensure_ascii=False)[:500]}...")

                except Exception as e:
                    logger.error(f"Error reading form data from {form_file}: {str(e)}")
                    success = False
        
        # Analyze the output PDF for form fields
        pdf_files = list(result_dir.glob("*.pdf"))
        if not pdf_files:
            logger.warning(f"No PDF files found in {result_dir}")
            success = False
        else:
            for pdf_file in pdf_files:
                if 'origin' in pdf_file.name.lower():
                    logger.info(f"Analyzing original PDF: {pdf_file}")
                    original_analysis = analyze_pdf_for_forms(pdf_file)
                    logger.info(f"Original PDF analysis: Has forms: {original_analysis['has_forms']}, "
                               f"Pages with forms: {original_analysis['pages_with_forms']}")
                elif 'layout' in pdf_file.name.lower() or 'span' in pdf_file.name.lower():
                    logger.info(f"Analyzing processed PDF: {pdf_file}")
                    processed_analysis = analyze_pdf_for_forms(pdf_file)
                    logger.info(f"Processed PDF analysis: Has forms: {processed_analysis['has_forms']}, "
                               f"Pages with forms: {processed_analysis['pages_with_forms']}")

    return success

def main():
    # Test with the Form.pdf file
    test_pdfs = [
        Path("demo/Form.pdf"),
        Path("demo/w8.pdf"),
    ]
    
    all_success = True
    
    for pdf_path in test_pdfs:
        if not pdf_path.exists():
            logger.error(f"PDF file not found: {pdf_path}")
            all_success = False
            continue
        
        # Create a unique output directory for this test
        test_name = pdf_path.stem
        output_dir = Path(f"test_output_{test_name}")
        
        logger.info(f"\n{'='*80}")
        logger.info(f"Starting form detection test with {pdf_path}")
        logger.info(f"Output directory: {output_dir.absolute()}")
        
        # Analyze the original PDF
        logger.info("\nAnalyzing original PDF...")
        original_analysis = analyze_pdf_for_forms(pdf_path)
        logger.info(f"Original PDF has forms: {original_analysis['has_forms']}")
        if original_analysis['has_forms']:
            logger.info(f"Pages with forms: {original_analysis['pages_with_forms']}")
            logger.info(f"Found {len(original_analysis['form_fields'])} form fields")
        
        # Run the pipeline with form detection
        logger.info("\nRunning pipeline with form detection...")
        success = run_pipeline_with_forms(pdf_path, output_dir)
        
        if success:
            logger.info("\nPipeline completed successfully")
            
            # Check the output
            logger.info("\nVerifying output...")
            if check_form_detection(output_dir):
                logger.info(" Form detection test PASSED")
            else:
                logger.error(" Form detection test FAILED - some expected output files are missing or invalid")
                all_success = False
        else:
            logger.error(" Pipeline failed")
            all_success = False
    
    # Final result
    logger.info("\n" + "="*80)
    if all_success:
        logger.info(" ALL TESTS PASSED SUCCESSFULLY")
    else:
        logger.error("Pipeline failed")
        logger.error(str(result))
