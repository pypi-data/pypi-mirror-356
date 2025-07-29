"""
Rule-based document detector.

This module provides a document detector that uses keyword matching and
rule-based heuristics to identify document types.
"""

import re
from typing import Dict, List, Optional, Set, Tuple

from invutil.logger import get_logger

from .base import DetectionResult, DocumentDetector, DocumentType


logger = get_logger(__name__)


class RuleBasedDetector(DocumentDetector):
    """Document detector using keyword matching and rule-based heuristics."""
    
    def __init__(self):
        """Initialize rule-based detector with default keyword sets."""
        super().__init__()
        
        # Define keyword sets for each document type
        self.keywords: Dict[DocumentType, Set[str]] = {
            DocumentType.INVOICE: {
                "invoice", "inv", "bill", "billing", "purchase order",
                "tax invoice", "vat invoice", "factura", "rechnung",
                "faktura", "facture", "fattura"
            },
            DocumentType.RECEIPT: {
                "receipt", "rcpt", "sales receipt", "cash receipt",
                "payment receipt", "ticket", "bon", "quittung", "recibo",
                "reçu", "scontrino"
            },
            DocumentType.BANK_STATEMENT: {
                "bank statement", "account statement", "statement of account",
                "banking statement", "bank record", "kontoauszug", "relevé bancaire",
                "extracto bancario", "estratto conto"
            }
        }
        
        # Define regex patterns for each document type
        self.patterns: Dict[DocumentType, List[re.Pattern]] = {
            DocumentType.INVOICE: [
                re.compile(r"\b(?:invoice|inv)(?:\s+number|\s+no|\s+#|:)\s*[a-z0-9\-_/]+", re.IGNORECASE),
                re.compile(r"\b(?:bill\s+to|sold\s+to):", re.IGNORECASE),
                re.compile(r"\b(?:payment\s+terms|due\s+date):", re.IGNORECASE),
            ],
            DocumentType.RECEIPT: [
                re.compile(r"\b(?:receipt|rcpt)(?:\s+number|\s+no|\s+#|:)", re.IGNORECASE),
                re.compile(r"\btransaction(?:\s+number|\s+no|\s+#|:)", re.IGNORECASE),
                re.compile(r"\bthank\s+you\s+for\s+your\s+(?:purchase|business)", re.IGNORECASE),
                re.compile(r"\bcashier:", re.IGNORECASE),
            ],
            DocumentType.BANK_STATEMENT: [
                re.compile(r"\b(?:account|acct)(?:\s+number|\s+no|\s+#|:)\s*[a-z0-9\-_*]+", re.IGNORECASE),
                re.compile(r"\b(?:opening|closing)\s+balance", re.IGNORECASE),
                re.compile(r"\btransaction\s+(?:history|details|summary)", re.IGNORECASE),
                re.compile(r"\b(?:deposits|withdrawals|debits|credits)", re.IGNORECASE),
            ]
        }
    
    def detect(self, text: str, **kwargs) -> DetectionResult:
        """
        Detect document type using rule-based approach.
        
        Args:
            text: Document text to analyze
            **kwargs: Additional detection parameters
            
        Returns:
            DetectionResult containing the detected document type and confidence
        """
        if not text:
            return DetectionResult(
                document_type=DocumentType.UNKNOWN,
                confidence=0.0
            )
        
        # Calculate scores for each document type
        scores: Dict[DocumentType, float] = {}
        
        # Check keywords
        for doc_type, keywords in self.keywords.items():
            keyword_count = sum(1 for keyword in keywords if keyword.lower() in text.lower())
            keyword_score = min(0.7, keyword_count * 0.1)
            scores[doc_type] = keyword_score
        
        # Check patterns
        for doc_type, patterns in self.patterns.items():
            pattern_count = sum(1 for pattern in patterns if pattern.search(text))
            pattern_score = min(0.8, pattern_count * 0.2)
            scores[doc_type] = max(scores.get(doc_type, 0.0), pattern_score)
        
        # Find best match
        best_type = DocumentType.UNKNOWN
        best_score = 0.3  # Minimum threshold
        
        for doc_type, score in scores.items():
            if score > best_score:
                best_type = doc_type
                best_score = score
        
        # Apply additional heuristics
        if best_type != DocumentType.UNKNOWN:
            # Check for strong indicators
            if best_type == DocumentType.INVOICE:
                if re.search(r"\binvoice\b", text, re.IGNORECASE):
                    best_score = min(1.0, best_score + 0.2)
            elif best_type == DocumentType.RECEIPT:
                if re.search(r"\breceipt\b", text, re.IGNORECASE):
                    best_score = min(1.0, best_score + 0.2)
            elif best_type == DocumentType.BANK_STATEMENT:
                if re.search(r"\bbank\s+statement\b", text, re.IGNORECASE):
                    best_score = min(1.0, best_score + 0.2)
        
        logger.debug(f"Document detection scores: {scores}")
        
        return DetectionResult(
            document_type=best_type,
            confidence=best_score,
            metadata={"scores": scores}
        )
