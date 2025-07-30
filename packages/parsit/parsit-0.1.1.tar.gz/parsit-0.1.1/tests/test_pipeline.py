import os
import sys
import subprocess
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('pipeline_test.log')
    ]
)
logger = logging.getLogger(__name__)

def run_pipeline_with_forms(pdf_path, output_dir):
    """Run the pipeline with form detection enabled."""
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Build the command
        cmd = [
            sys.executable,  # Use the current Python interpreter
            "-m", "parsit.tools.cli",
            "-p", str(pdf_path),
            "-o", str(output_dir),
            "--detect-forms",
            "--debug"  # Enable debug output
        ]
        
        logger.info(f"Running command: {' '.join(cmd)}")
        
        # Run the command and capture output
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True
        )
        
        # Log the output
        if result.stdout:
            logger.info("Command output (stdout):")
            logger.info(result.stdout)
        
        if result.stderr:
            logger.error("Command output (stderr):")
            logger.error(result.stderr)
            
        return True, result
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed with return code {e.returncode}")
        logger.error(f"Error output: {e.stderr}")
        return False, e
    except Exception as e:
        logger.error(f"Error running pipeline: {str(e)}")
        return False, e

if __name__ == "__main__":
    # Test with the Form.pdf file
    pdf_path = Path("demo/Form.pdf")
    output_dir = Path("test_output/pipeline_test")
    
    logger.info(f"Starting pipeline test with {pdf_path}")
    success, result = run_pipeline_with_forms(pdf_path, output_dir)
    
    if success:
        logger.info("Pipeline completed successfully")
        # Check output files
        output_files = list(output_dir.rglob("*"))
        logger.info(f"Generated {len(output_files)} output files:")
        for f in output_files:
            logger.info(f"  - {f.relative_to(output_dir)}")
    else:
        logger.error("Pipeline failed")
        logger.error(str(result))
