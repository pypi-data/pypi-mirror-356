"""
Valider - Validation framework for financial document processing.

This package provides validation mechanisms with well-defined interfaces
for validating financial document data.
"""

from .base import Validator, FieldValidator, DocumentValidator, ValidationResult
from .field_validators import (
    AmountValidator, DateValidator, TextValidator,
    TaxIDValidator, PercentageValidator
)
from .document_validators import (
    InvoiceValidator, ReceiptValidator, BankStatementValidator
)

__version__ = "0.1.0"

__all__ = [
    # Base classes
    "Validator", "FieldValidator", "DocumentValidator", "ValidationResult",
    
    # Field validators
    "AmountValidator", "DateValidator", "TextValidator",
    "TaxIDValidator", "PercentageValidator",
    
    # Document validators
    "InvoiceValidator", "ReceiptValidator", "BankStatementValidator",
]
