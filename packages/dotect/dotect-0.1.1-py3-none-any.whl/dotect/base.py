"""
Base document detection interfaces and abstract classes.

This module provides the core detection interfaces and abstract base classes
that all document detectors should implement.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union

from pydantic import BaseModel, Field


class DocumentType(str, Enum):
    """Enumeration of supported document types."""
    
    INVOICE = "invoice"
    RECEIPT = "receipt"
    BANK_STATEMENT = "bank_statement"
    UNKNOWN = "unknown"


class DetectionResult(BaseModel):
    """Result of a document detection operation."""
    
    document_type: DocumentType = DocumentType.UNKNOWN
    """Detected document type."""
    
    confidence: float = 0.0
    """Confidence score for the detection (0.0-1.0)."""
    
    metadata: Dict[str, Any] = Field(default_factory=dict)
    """Additional metadata about the detection process."""


class DocumentDetector(ABC):
    """Base document detector interface."""
    
    @abstractmethod
    def detect(self, text: str, **kwargs) -> DetectionResult:
        """
        Detect the type of document from the provided text.
        
        Args:
            text: Document text to analyze
            **kwargs: Additional detection parameters
            
        Returns:
            DetectionResult containing the detected document type and confidence
        """
        pass
    
    def detect_document_type(self, text: str, **kwargs) -> Tuple[DocumentType, float]:
        """
        Detect the document type and return it with confidence.
        
        This is a convenience method that returns just the document type and confidence.
        
        Args:
            text: Document text to analyze
            **kwargs: Additional detection parameters
            
        Returns:
            Tuple of (document_type, confidence)
        """
        result = self.detect(text, **kwargs)
        return result.document_type, result.confidence
    
    @property
    def supported_types(self) -> List[DocumentType]:
        """
        Get the list of document types this detector can identify.
        
        Returns:
            List of supported document types
        """
        return list(DocumentType)


class DocumentClassifier(DocumentDetector):
    """Base document classifier interface."""
    
    @abstractmethod
    def train(self, texts: List[str], labels: List[Union[DocumentType, str]], **kwargs) -> None:
        """
        Train the classifier on labeled examples.
        
        Args:
            texts: List of document texts
            labels: List of document type labels
            **kwargs: Additional training parameters
        """
        pass
    
    @abstractmethod
    def save(self, path: str) -> None:
        """
        Save the trained classifier to disk.
        
        Args:
            path: Path to save the classifier
        """
        pass
    
    @abstractmethod
    def load(self, path: str) -> None:
        """
        Load a trained classifier from disk.
        
        Args:
            path: Path to load the classifier from
        """
        pass
