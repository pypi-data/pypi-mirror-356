"""Test script for signature detection functionality."""
import os
import sys
import cv2
import numpy as np
from pathlib import Path
from loguru import logger
from typing import List, Dict, Any, Optional
import time

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from parsit.utils.signature_utils import SignatureDetector, process_page_for_signatures
from parsit.utils.image_utils import save_signature_images

def test_signature_detection(
    image_path: str, 
    output_dir: str,
    model_path: Optional[str] = None,
    backend: str = 'auto',
    conf_threshold: float = 0.5,
    save_crops: bool = True,
    visualize: bool = True
) -> Dict[str, Any]:
    """
    Test the signature detection on a single image.
    
    Args:
        image_path: Path to the input image file
        output_dir: Directory to save output files
        model_path: Path to the model file (None for default)
        backend: Backend to use ('yolo', 'onnx', or 'auto')
        conf_threshold: Confidence threshold for detections
        save_crops: Whether to save cropped signature images
        visualize: Whether to save visualization of detections
        
    Returns:
        Dictionary containing detection results and metrics
    """
    start_time = time.time()
    
    # Create output directories
    os.makedirs(output_dir, exist_ok=True)
    crops_dir = os.path.join(output_dir, 'crops')
    vis_dir = os.path.join(output_dir, 'visualization')
    os.makedirs(crops_dir, exist_ok=True)
    os.makedirs(vis_dir, exist_ok=True)
    
    # Load the image
    if not os.path.exists(image_path):
        logger.error(f"Image file not found: {image_path}")
        return {"error": "Image file not found", "success": False}
    
    image = cv2.imread(image_path)
    if image is None:
        logger.error(f"Failed to load image: {image_path}")
        return {"error": "Failed to load image", "success": False}
    
    logger.info(f"Loaded image: {image_path} (shape: {image.shape})")
    
    # Initialize detector
    try:
        detector = SignatureDetector(
            model_path=model_path,
            backend=backend,
            conf_threshold=conf_threshold,
            device='cuda' if torch.cuda.is_available() else 'cpu'
        )
        logger.info(f"Initialized {backend} backend")
    except Exception as e:
        logger.error(f"Failed to initialize detector: {str(e)}")
        return {"error": f"Detector initialization failed: {str(e)}", "success": False}
    
    # Process the image
    try:
        process_start = time.time()
        detections = detector.detect(
            image=image,
            output_dir=crops_dir if save_crops else None,
            conf_threshold=conf_threshold
        )
        process_time = time.time() - process_start
        
        logger.info(f"Detected {len(detections)} signatures in {process_time:.2f} seconds")
        
        # Save visualization if requested
        if visualize and detections:
            vis_img = detector.draw_detections(image, detections)
            vis_path = os.path.join(vis_dir, f"{Path(image_path).stem}_detections.jpg")
            cv2.imwrite(vis_path, vis_img)
            logger.info(f"Saved visualization to {vis_path}")
        
        # Prepare results
        result = {
            "success": True,
            "num_detections": len(detections),
            "processing_time": process_time,
            "image_size": f"{image.shape[1]}x{image.shape[0]}",
            "detections": [
                {
                    "bbox": [int(x) for x in det.bbox],
                    "confidence": float(det.confidence),
                    "image_path": det.image_path
                }
                for det in detections
            ],
            "visualization_path": os.path.join(vis_dir, f"{Path(image_path).stem}_detections.jpg") 
                if visualize and detections else None
        }
        
        return result
        
    except Exception as e:
        logger.error(f"Error during detection: {str(e)}")
        return {"error": f"Detection failed: {str(e)}", "success": False}
    finally:
        total_time = time.time() - start_time
        logger.info(f"Total processing time: {total_time:.2f} seconds")
    
    # Create BatchAnalyze instance with signature detection enabled
    batch_analyze = BatchAnalyze(
        model_manager=model_manager,
        batch_ratio=1,
        show_log=True,
        layout_model=None,
        formula_enable=False,
        table_enable=False,
        signature_enable=True,
        signature_config=signature_config,
        output_dir=output_dir
    )
    
    # Prepare input data (list of tuples: (image, ocr_enable, lang))
    images_with_extra_info = [(image, False, 'en')]
    
    # Run signature detection
    logger.info("Running signature detection...")
    results = batch_analyze(images_with_extra_info)
    
    # Process and display results
    if not results or not results[0]:
        logger.warning("No results returned from batch analysis")
        return
    
    # Get the first (and only) result
    detections = results[0]
    logger.info(f"Found {len(detections)} detections")
    
    # Draw bounding boxes on the image
    output_image = image.copy()
    for i, det in enumerate(detections):
        if 'bbox' in det:
            x1, y1, x2, y2 = map(int, det['bbox'])
            confidence = det.get('score', 0)
            
            # Draw rectangle
            color = (0, 255, 0)  # Green
            cv2.rectangle(output_image, (x1, y1), (x2, y2), color, 2)
            
            # Draw label
            label = f"Signature: {confidence:.2f}"
            cv2.putText(output_image, label, (x1, y1 - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
    # Save the output image
    output_path = os.path.join(output_dir, "detection_result.jpg")
    cv2.imwrite(output_path, output_image)
    logger.info(f"Saved detection result to: {output_path}")
    
    # Print detection details
    for i, det in enumerate(detections):
        if 'bbox' in det:
            x1, y1, x2, y2 = map(int, det['bbox'])
            confidence = det.get('score', 0)
            image_path = det.get('image_path', 'Not saved')
            
            logger.info(f"Detection {i+1}:")
            logger.info(f"  Bounding box: ({x1}, {y1}, {x2}, {y2})")
            logger.info(f"  Confidence: {confidence:.4f}")
            logger.info(f"  Saved to: {image_path}")

if __name__ == "__main__":
    # Example usage
    test_image_path = "path/to/your/document_with_signature.jpg"
    output_directory = "output/signature_detection"
    
    # Create output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)
    
    # Configure logger
    logger.remove()
    logger.add(
        os.path.join(output_directory, "signature_detection.log"),
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
    )
    logger.add(sys.stderr, level="INFO")
    
    logger.info("Starting signature detection test")
    test_signature_detection(test_image_path, output_directory)
    logger.info("Signature detection test completed")
