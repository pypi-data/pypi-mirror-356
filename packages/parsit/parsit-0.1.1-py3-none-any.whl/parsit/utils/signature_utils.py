import os
import cv2
import numpy as np
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any, Union
from dataclasses import dataclass
import logging
from huggingface_hub import hf_hub_download
import onnxruntime as ort
import time

logger = logging.getLogger(__name__)


@dataclass
class SignatureDetection:
    bbox: Tuple[float, float, float, float]  # x1, y1, x2, y2
    confidence: float
    image: Optional[np.ndarray] = None
    image_path: Optional[str] = None


class ONNXSignatureDetector:
    """A class to handle signature detection in documents using ONNX runtime."""
    
    def __init__(self, model_path: Optional[str] = None, device: str = 'cpu'):
        self.input_width = 640
        self.input_height = 640
        self.device = device
        self.session = self._load_model(model_path)
    
    def _load_model(self, model_path: Optional[str] = None) -> ort.InferenceSession:
        if model_path is None or not os.path.exists(model_path):
            model_path = r"D:\parsit\pretrained models\yolov8s.onnx"
            
            if not os.path.exists(model_path):
                raise FileNotFoundError(
                    f"Signature detection model not found at {model_path}. "
                    "Please ensure the model file exists at the specified path."
                )
            
            logger.info(f"Using signature detection model from {model_path}")
        
        # Try to use CUDA if requested, but fall back to CPU if not available
        if self.device == 'cuda':
            try:
                providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
                session = ort.InferenceSession(model_path, providers=providers)
                logger.info("Using CUDA execution provider for signature detection")
                return session
            except Exception as e:
                logger.warning(f"CUDA not available, falling back to CPU: {str(e)}")
        
        # Fall back to CPU
        providers = ['CPUExecutionProvider']
        logger.info("Using CPU execution provider for signature detection")
        try:
            return ort.InferenceSession(model_path, providers=providers)
        except Exception as e:
            logger.error(f"Failed to load ONNX model: {str(e)}")
            raise
    
    def preprocess(self, image: np.ndarray) -> np.ndarray:
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (self.input_width, self.input_height))
        img = img.astype(np.float32) / 255.0
        img = np.transpose(img, (2, 0, 1))
        return np.expand_dims(img, axis=0).astype(np.float32)
    
    def detect(self, 
              image: np.ndarray, 
              output_dir: Optional[str] = None,
              save_crops: bool = False,  # Changed default to False
              conf_threshold: float = 0.5) -> List[SignatureDetection]:
        
        if output_dir and save_crops:
            os.makedirs(output_dir, exist_ok=True)
        
        img_height, img_width = image.shape[:2]
        logger.debug(f"Input image size: {img_width}x{img_height}")
        
        # Save original image for debugging
        if output_dir:
            orig_img_path = os.path.join(output_dir, "original_image.png")
            cv2.imwrite(orig_img_path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
            logger.debug(f"Saved original image to {orig_img_path}")
        
        input_tensor = self.preprocess(image)
        
        input_name = self.session.get_inputs()[0].name
        outputs = self.session.run(None, {input_name: input_tensor})[0]
        
        detections = self._postprocess(outputs, img_width, img_height, conf_threshold)
        logger.debug(f"Raw detections: {detections}")
        
        signature_detections = []
        for i, (x1, y1, x2, y2, confidence) in enumerate(detections, 1):
            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
            logger.debug(f"Detection {i}: bbox=({x1}, {y1}, {x2}, {y2}), confidence={confidence:.2f}")
            
            # Ensure bbox is within image bounds
            x1 = max(0, min(x1, img_width - 1))
            y1 = max(0, min(y1, img_height - 1))
            x2 = max(0, min(x2, img_width))
            y2 = max(0, min(y2, img_height))
            
            if x1 >= x2 or y1 >= y2:
                logger.warning(f"Invalid bbox after clipping: ({x1}, {y1}, {x2}, {y2})")
                continue
                
            signature_img = image[y1:y2, x1:x2]
            logger.debug(f"Signature image size: {signature_img.shape[1]}x{signature_img.shape[0]}")
            
            # Save debug image with detection
            if output_dir:
                debug_img = image.copy()
                cv2.rectangle(debug_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(debug_img, f"Sig {i}: {confidence:.2f}", 
                           (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.5, (0, 255, 0), 2)
                debug_path = os.path.join(output_dir, f"detection_{i}.png")
                cv2.imwrite(debug_path, cv2.cvtColor(debug_img, cv2.COLOR_RGB2BGR))
                logger.debug(f"Saved detection visualization to {debug_path}")
            
            detection = SignatureDetection(
                bbox=(x1, y1, x2, y2),
                confidence=float(confidence),
                image=signature_img,
                image_path=None  # Will be set by caller if needed
            )
            signature_detections.append(detection)
        
        return signature_detections
    
    def _nms(self, boxes: np.ndarray, scores: np.ndarray, iou_threshold: float = 0.5) -> np.ndarray:
        if len(boxes) == 0:
            return np.array([])
            
        x1 = boxes[:, 0]
        y1 = boxes[:, 1]
        x2 = boxes[:, 2]
        y2 = boxes[:, 3]
        
        areas = (x2 - x1 + 1) * (y2 - y1 + 1)
        order = scores.argsort()[::-1]
        
        keep = []
        while order.size > 0:
            i = order[0]
            keep.append(i)
            
            xx1 = np.maximum(x1[i], x1[order[1:]])
            yy1 = np.maximum(y1[i], y1[order[1:]])
            xx2 = np.minimum(x2[i], x2[order[1:]])
            yy2 = np.minimum(y2[i], y2[order[1:]])
            
            w = np.maximum(0.0, xx2 - xx1 + 1)
            h = np.maximum(0.0, yy2 - yy1 + 1)
            
            intersection = w * h
            iou = intersection / (areas[i] + areas[order[1:]] - intersection)
            
            inds = np.where(iou <= iou_threshold)[0]
            order = order[inds + 1]
            
        return np.array(keep)
        
    def _postprocess(self, 
                    outputs: np.ndarray, 
                    img_width: int, 
                    img_height: int,
                    conf_threshold: float) -> np.ndarray:
        outputs = np.transpose(np.squeeze(outputs[0]))
        rows = outputs.shape[0]
        boxes = []
        scores = []
        
        x_factor = img_width / self.input_width
        y_factor = img_height / self.input_height
        
        for i in range(rows):
            classes_scores = outputs[i][4:]
            max_score = np.amax(classes_scores)
            
            if max_score >= conf_threshold:
                x, y, w, h = outputs[i][0], outputs[i][1], outputs[i][2], outputs[i][3]
                left = int((x - w / 2) * x_factor)
                top = int((y - h / 2) * y_factor)
                width = int(w * x_factor)
                height = int(h * y_factor)
                
                boxes.append([left, top, left + width, top + height])
                scores.append(max_score)
        
        if not boxes:
            return np.empty((0, 5))
            
        boxes = np.array(boxes)
        scores = np.array(scores)
        
        keep = self._nms(boxes, scores, iou_threshold=0.5)
        
        if len(keep) == 0:
            return np.empty((0, 5))
            
        boxes = boxes[keep]
        scores = scores[keep]
        
        return np.column_stack((boxes, scores))
    
    def draw_detections(self, 
                       image: np.ndarray, 
                       detections: List[SignatureDetection],
                       color: Tuple[int, int, int] = (0, 255, 0),
                       thickness: int = 2) -> np.ndarray:
        result_img = image.copy()
        
        for det in detections:
            x1, y1, x2, y2 = map(int, det.bbox)
            cv2.rectangle(result_img, (x1, y1), (x2, y2), color, thickness)
            
            label = f"Signature: {det.confidence:.2f}"
            cv2.putText(result_img, label, (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, thickness)
        
        return result_img


# For backward compatibility
SignatureDetector = ONNXSignatureDetector


def process_page_for_signatures(page_image: np.ndarray,
                              output_dir: str,
                              device: str = 'cpu') -> List[Dict[str, Any]]:
    """
    Process a single page image to detect and extract signatures.
    
    Args:
        page_image: Input page image (BGR format)
        output_dir: Directory to save extracted signatures
        device: Device to run detection on ('cpu' or 'cuda')
        
    Returns:
        List of signature detections with metadata
    """
    detector = SignatureDetector(device=device)
    
    # Create signature output directory
    sig_output_dir = os.path.join(output_dir, "signatures")
    os.makedirs(sig_output_dir, exist_ok=True)
    
    # Detect signatures
    detections = detector.detect(page_image, sig_output_dir)
    
    # Convert to serializable format
    result = []
    for i, det in enumerate(detections):
        x1, y1, x2, y2 = map(float, det.bbox)
        result.append({
            "type": "signature",
            "bbox": [x1, y1, x2, y2],
            "confidence": det.confidence,
            "image_path": det.image_path,
            "page": 0  # Will be set by the caller
        })
    
    # Save visualization if we have detections
    if detections:
        vis_img = detector.draw_detections(page_image, detections)
        vis_path = os.path.join(output_dir, "signature_detections.png")
        cv2.imwrite(vis_path, vis_img)
    
    return result
