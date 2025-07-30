import os
import uuid
from typing import List, Dict, Any, Tuple, Optional
import cv2
import numpy as np
from pathlib import Path
from loguru import logger

def save_signature_images(
    images: List[np.ndarray],
    output_dir: str,
    base_filename: str,
    signature_detections: List[List[Dict[str, Any]]]
) -> List[List[Dict[str, Any]]]:
    """
    Save cropped signature images and update detection results with image paths.
    
    Args:
        images: List of input images (numpy arrays)
        output_dir: Directory to save signature images
        base_filename: Base filename for saved images (without extension)
        signature_detections: List of detections per image
        
    Returns:
        Updated signature detections with 'image_path' added to each detection
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    updated_detections = []
    
    for img_idx, (image, detections) in enumerate(zip(images, signature_detections)):
        if not detections:
            updated_detections.append([])
            continue
            
        page_detections = []
        
        for det_idx, detection in enumerate(detections):
            try:
                # Get bounding box coordinates
                x1, y1, x2, y2 = map(int, detection['bbox'])
                
                # Ensure coordinates are within image bounds
                h, w = image.shape[:2]
                x1, y1 = max(0, x1), max(0, y1)
                x2, y2 = min(w, x2), min(h, y2)
                
                if x2 <= x1 or y2 <= y1:
                    logger.warning(f"Invalid bbox coordinates: {detection['bbox']}")
                    detection['image_path'] = None
                    page_detections.append(detection)
                    continue
                
                # Crop and save the signature
                signature_img = image[y1:y2, x1:x2]
                
                # Generate a unique filename
                sig_id = str(uuid.uuid4())[:8]
                filename = f"{base_filename}_page{img_idx+1}_sig{det_idx+1}_{sig_id}.png"
                filepath = os.path.join(output_dir, filename)
                
                # Save the cropped image
                cv2.imwrite(filepath, cv2.cvtColor(signature_img, cv2.COLOR_RGB2BGR))
                
                # Update detection with image path
                detection['image_path'] = filepath
                page_detections.append(detection)
                
            except Exception as e:
                logger.error(f"Error processing signature {det_idx} on page {img_idx}: {str(e)}")
                detection['image_path'] = None
                page_detections.append(detection)
        
        updated_detections.append(page_detections)
    
    return updated_detections
