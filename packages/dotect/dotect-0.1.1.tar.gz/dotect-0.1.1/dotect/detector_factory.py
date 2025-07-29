"""
Unified detector factory for creating document detectors.

This module provides a factory for creating appropriate document detectors
based on detection method preferences.
"""

from enum import Enum
from typing import Optional, Union

from .base import DocumentDetector
from .rule_detector import RuleBasedDetector
from .ml_classifier import MLDocumentClassifier


class DetectionMethod(str, Enum):
    """Enumeration of supported detection methods."""
    
    RULE_BASED = "rule_based"
    ML = "ml"
    HYBRID = "hybrid"


class DetectorFactory:
    """Factory for creating document detectors."""
    
    def __init__(
        self,
        preferred_method: DetectionMethod = DetectionMethod.HYBRID,
        ml_model_path: Optional[str] = None
    ):
        """
        Initialize detector factory.
        
        Args:
            preferred_method: Preferred detection method
            ml_model_path: Path to pre-trained ML model (if using ML method)
        """
        self.preferred_method = preferred_method
        self.ml_model_path = ml_model_path
    
    def create_detector(
        self, 
        method: Optional[Union[DetectionMethod, str]] = None,
        **kwargs
    ) -> DocumentDetector:
        """
        Create an appropriate document detector.
        
        Args:
            method: Detection method to use (defaults to preferred_method)
            **kwargs: Additional parameters for the detector
            
        Returns:
            A document detector instance
        """
        # Use preferred method if not specified
        if method is None:
            method = self.preferred_method
        
        # Convert string to enum if needed
        if isinstance(method, str):
            try:
                method = DetectionMethod(method.lower())
            except ValueError:
                method = self.preferred_method
        
        # Create detector based on method
        if method == DetectionMethod.RULE_BASED:
            return RuleBasedDetector()
        
        elif method == DetectionMethod.ML:
            classifier = MLDocumentClassifier(
                model_type=kwargs.get("model_type", "svm")
            )
            
            # Load pre-trained model if available
            model_path = kwargs.get("model_path", self.ml_model_path)
            if model_path:
                try:
                    classifier.load(model_path)
                except Exception as e:
                    # Fall back to rule-based if model loading fails
                    print(f"Failed to load ML model: {str(e)}")
                    return RuleBasedDetector()
            
            return classifier
        
        elif method == DetectionMethod.HYBRID:
            # For hybrid method, we'll use both detectors and combine their results
            # This is a placeholder for now - in a real implementation, we would
            # create a hybrid detector that uses both methods
            return HybridDetector(
                rule_detector=RuleBasedDetector(),
                ml_detector=self.create_detector(DetectionMethod.ML, **kwargs)
            )
        
        else:
            raise ValueError(f"Unsupported detection method: {method}")


class HybridDetector(DocumentDetector):
    """Hybrid document detector that combines rule-based and ML approaches."""
    
    def __init__(
        self,
        rule_detector: RuleBasedDetector,
        ml_detector: MLDocumentClassifier,
        rule_weight: float = 0.4,
        ml_weight: float = 0.6
    ):
        """
        Initialize hybrid detector.
        
        Args:
            rule_detector: Rule-based detector instance
            ml_detector: ML-based detector instance
            rule_weight: Weight for rule-based detection (0.0-1.0)
            ml_weight: Weight for ML-based detection (0.0-1.0)
        """
        super().__init__()
        
        self.rule_detector = rule_detector
        self.ml_detector = ml_detector
        self.rule_weight = rule_weight
        self.ml_weight = ml_weight
        
        # Normalize weights
        total_weight = self.rule_weight + self.ml_weight
        if total_weight > 0:
            self.rule_weight /= total_weight
            self.ml_weight /= total_weight
    
    def detect(self, text: str, **kwargs) -> DetectionResult:
        """
        Detect document type using hybrid approach.
        
        Args:
            text: Document text to analyze
            **kwargs: Additional detection parameters
            
        Returns:
            DetectionResult containing the detected document type and confidence
        """
        # Get results from both detectors
        rule_result = self.rule_detector.detect(text, **kwargs)
        
        try:
            ml_result = self.ml_detector.detect(text, **kwargs)
        except Exception:
            # Fall back to rule-based if ML fails
            return rule_result
        
        # If both agree, return the result with higher confidence
        if rule_result.document_type == ml_result.document_type:
            if rule_result.confidence >= ml_result.confidence:
                return rule_result
            else:
                return ml_result
        
        # If they disagree, use weighted confidence
        rule_score = rule_result.confidence * self.rule_weight
        ml_score = ml_result.confidence * self.ml_weight
        
        if rule_score >= ml_score:
            # Adjust confidence to reflect disagreement
            rule_result.confidence = rule_score / (rule_score + ml_score) * rule_result.confidence
            return rule_result
        else:
            # Adjust confidence to reflect disagreement
            ml_result.confidence = ml_score / (rule_score + ml_score) * ml_result.confidence
            return ml_result
