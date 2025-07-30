"""Configuration for signature detection model."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class SignatureConfig:
    """Configuration for signature detection.
    
    Attributes:
        enabled: Whether signature detection is enabled
        model_weight: Path to the model weights file. If None, will download from Hugging Face Hub
        confidence_threshold: Minimum confidence score for signature detection (0-1)
        iou_threshold: IOU threshold for NMS (0-1)
        device: Device to run the model on ('cpu' or 'cuda')
    """
    enabled: bool = True
    model_weight: Optional[str] = None  # Will download from Hugging Face if None
    confidence_threshold: float = 0.25
    iou_threshold: float = 0.45
    device: str = "cuda"  # Will fall back to CPU if CUDA is not available


# Default configuration
DEFAULT_SIGNATURE_CONFIG = SignatureConfig()
