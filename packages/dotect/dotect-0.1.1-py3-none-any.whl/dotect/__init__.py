"""
Dotect - Document detection and classification for financial documents.

This package provides tools for detecting and classifying financial documents
based on their content, structure, and metadata.
"""

from .base import DocumentDetector, DocumentClassifier, DetectionResult, DocumentType
from .rule_detector import RuleBasedDetector
from .ml_classifier import MLDocumentClassifier
from .detector_factory import DetectionMethod, DetectorFactory, HybridDetector

__version__ = "0.1.0"

__all__ = [
    # Base classes
    "DocumentDetector", "DocumentClassifier", "DetectionResult", "DocumentType",
    
    # Detectors
    "RuleBasedDetector", "MLDocumentClassifier", "HybridDetector",
    
    # Factory
    "DetectionMethod", "DetectorFactory",
]
