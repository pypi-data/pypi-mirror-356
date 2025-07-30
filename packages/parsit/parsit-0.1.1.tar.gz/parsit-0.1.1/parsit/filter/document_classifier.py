from typing import Dict, Tuple, Optional, List
from pathlib import Path
import logging
import numpy as np
from PIL import Image
from transformers import AutoImageProcessor, AutoModelForImageClassification
import torch
from torchvision import transforms

logger = logging.getLogger(__name__)

class DocumentClassifier:
    def __init__(self, model_name: str = "microsoft/dit-base-finetuned-rvlcdip"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.processor = AutoImageProcessor.from_pretrained(model_name)
        self.model = AutoModelForImageClassification.from_pretrained(model_name)
        self.model = self.model.to(self.device)
        self.model.eval()
        
        # Define the transformation pipeline
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        
        # RVL-CDIP class names
        self.class_names = [
            "letter", "form", "email", "handwritten", "advertisement",
            "scientific report", "scientific publication", "specification", "file folder", "news article",
            "budget", "invoice", "presentation", "questionnaire", "resume",
            "memo"
        ]
        
        # Map document types to our classification (text vs non-text)
        self.text_document_types = {
            "letter", "email", "scientific report", "scientific publication",
            "news article", "resume", "memo"
        }
    
    def preprocess_image(self, image: Image.Image) -> torch.Tensor:
        """Preprocess the image for the model."""
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image = self.transform(image)
        return image.unsqueeze(0).to(self.device)
    
    def classify_document(self, image_path: str) -> Tuple[bool, Dict]:
        """
        Classify a document image.
        
        Args:
            image_path: Path to the document image
            
        Returns:
            tuple: (is_text_document, confidence_scores)
        """
        try:
            # Load and preprocess image
            image = Image.open(image_path)
            inputs = self.preprocess_image(image)
            
            # Get model predictions
            with torch.no_grad():
                outputs = self.model(inputs)
                probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
                
            # Get top prediction
            probs, indices = torch.topk(probabilities, k=5)
            probs = probs.squeeze().cpu().numpy()
            indices = indices.squeeze().cpu().numpy()
            
            # Create results dictionary
            results = {
                "predictions": [],
                "is_text_document": False,
                "top_prediction": None,
                "confidence": 0.0
            }
            
            for i, (prob, idx) in enumerate(zip(probs, indices)):
                class_name = self.class_names[idx]
                is_text = class_name in self.text_document_types
                results["predictions"].append({
                    "class": class_name,
                    "confidence": float(prob),
                    "is_text": is_text
                })
                
                # Update top prediction
                if i == 0:
                    results["top_prediction"] = class_name
                    results["confidence"] = float(prob)
                    results["is_text_document"] = is_text
            
            return results["is_text_document"], results
            
        except Exception as e:
            logger.error(f"Error in document classification: {str(e)}")
            # Default to non-text document on error
            return False, {"error": str(e), "is_text_document": False}

# Global instance for easy access
document_classifier = DocumentClassifier()
