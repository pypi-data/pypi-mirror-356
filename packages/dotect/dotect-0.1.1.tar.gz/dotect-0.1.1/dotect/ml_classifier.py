"""
ML-based document classifier.

This module provides a document classifier that uses machine learning
techniques to identify document types based on text content.
"""

import os
import pickle
from typing import Dict, List, Optional, Tuple, Union

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC

from invutil.logger import get_logger

from .base import DetectionResult, DocumentClassifier, DocumentType


logger = get_logger(__name__)


class MLDocumentClassifier(DocumentClassifier):
    """Document classifier using machine learning techniques."""
    
    def __init__(self, model_type: str = "svm"):
        """
        Initialize ML document classifier.
        
        Args:
            model_type: Type of ML model to use ("svm", "nb", etc.)
        """
        super().__init__()
        
        self.model_type = model_type
        self.pipeline = None
        self.label_encoder = LabelEncoder()
        
        # Map string document types to enum values
        self.label_encoder.fit([t.value for t in DocumentType])
    
    def _create_pipeline(self) -> Pipeline:
        """
        Create ML pipeline based on model type.
        
        Returns:
            Scikit-learn pipeline
        """
        if self.model_type == "svm":
            return Pipeline([
                ("vectorizer", TfidfVectorizer(
                    ngram_range=(1, 2),
                    max_features=10000,
                    min_df=2,
                    max_df=0.9
                )),
                ("classifier", SVC(
                    kernel="linear",
                    probability=True,
                    C=1.0,
                    class_weight="balanced"
                ))
            ])
        else:
            raise ValueError(f"Unsupported model type: {self.model_type}")
    
    def train(self, texts: List[str], labels: List[Union[DocumentType, str]], **kwargs) -> None:
        """
        Train the classifier on labeled examples.
        
        Args:
            texts: List of document texts
            labels: List of document type labels
            **kwargs: Additional training parameters
        """
        if not texts or not labels or len(texts) != len(labels):
            raise ValueError("Invalid training data")
        
        # Convert string labels to enum if needed
        processed_labels = []
        for label in labels:
            if isinstance(label, str):
                try:
                    label = DocumentType(label.lower())
                except ValueError:
                    label = DocumentType.UNKNOWN
            processed_labels.append(label.value)
        
        # Encode labels
        y = self.label_encoder.transform(processed_labels)
        
        # Create and train pipeline
        self.pipeline = self._create_pipeline()
        self.pipeline.fit(texts, y)
        
        logger.info(f"Trained {self.model_type} classifier on {len(texts)} examples")
    
    def detect(self, text: str, **kwargs) -> DetectionResult:
        """
        Detect document type using trained classifier.
        
        Args:
            text: Document text to analyze
            **kwargs: Additional detection parameters
            
        Returns:
            DetectionResult containing the detected document type and confidence
        """
        if not text or self.pipeline is None:
            return DetectionResult(
                document_type=DocumentType.UNKNOWN,
                confidence=0.0
            )
        
        # Get prediction probabilities
        proba = self.pipeline.predict_proba([text])[0]
        
        # Get predicted class and confidence
        predicted_idx = np.argmax(proba)
        confidence = proba[predicted_idx]
        
        # Convert back to document type
        predicted_label = self.label_encoder.inverse_transform([predicted_idx])[0]
        try:
            document_type = DocumentType(predicted_label)
        except ValueError:
            document_type = DocumentType.UNKNOWN
        
        # If confidence is too low, return unknown
        if confidence < 0.5:
            document_type = DocumentType.UNKNOWN
            confidence = 1.0 - confidence
        
        return DetectionResult(
            document_type=document_type,
            confidence=confidence,
            metadata={
                "probabilities": {
                    DocumentType(self.label_encoder.inverse_transform([i])[0]): float(p)
                    for i, p in enumerate(proba)
                    if self.label_encoder.inverse_transform([i])[0] in [t.value for t in DocumentType]
                }
            }
        )
    
    def save(self, path: str) -> None:
        """
        Save the trained classifier to disk.
        
        Args:
            path: Path to save the classifier
        """
        if self.pipeline is None:
            raise ValueError("Classifier not trained")
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        
        # Save pipeline and label encoder
        with open(path, "wb") as f:
            pickle.dump({
                "pipeline": self.pipeline,
                "label_encoder": self.label_encoder,
                "model_type": self.model_type
            }, f)
        
        logger.info(f"Saved classifier to {path}")
    
    def load(self, path: str) -> None:
        """
        Load a trained classifier from disk.
        
        Args:
            path: Path to load the classifier from
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"Classifier file not found: {path}")
        
        # Load pipeline and label encoder
        with open(path, "rb") as f:
            data = pickle.load(f)
            self.pipeline = data["pipeline"]
            self.label_encoder = data["label_encoder"]
            self.model_type = data["model_type"]
        
        logger.info(f"Loaded classifier from {path}")
