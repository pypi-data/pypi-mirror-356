"""
Document validators for financial documents.

This module provides validators for entire financial documents,
including cross-field consistency checks.
"""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union

from invutil.numeric_utils import is_amount_within_tolerance

from .base import DocumentValidator, ValidationResult
from .field_validators import AmountValidator, DateValidator, TextValidator


class InvoiceValidator(DocumentValidator):
    """Validator for invoice documents."""
    
    def __init__(self, field_validators: Optional[Dict[str, Any]] = None):
        """
        Initialize invoice validator with field validators.
        
        Args:
            field_validators: Dictionary mapping field names to field validators
        """
        # Set default field validators if not provided
        if field_validators is None:
            field_validators = {
                "invoice_number": TextValidator(min_length=1, max_length=50),
                "issue_date": DateValidator(),
                "due_date": DateValidator(required=False),
                "total_amount": AmountValidator(min_value=0.01),
                "tax_amount": AmountValidator(min_value=0.0, required=False),
                "net_amount": AmountValidator(min_value=0.0, required=False),
                "seller_name": TextValidator(min_length=1),
                "buyer_name": TextValidator(min_length=1),
            }
        
        super().__init__(field_validators)
    
    def validate_consistency(self, data: Dict[str, Any]) -> ValidationResult:
        """
        Validate cross-field consistency in invoice data.
        
        Args:
            data: Invoice data dictionary
            
        Returns:
            ValidationResult containing validation outcome
        """
        errors = []
        warnings = []
        
        # Check date consistency
        if "issue_date" in data and "due_date" in data and data["due_date"]:
            issue_date = data["issue_date"]
            due_date = data["due_date"]
            
            if isinstance(issue_date, datetime) and isinstance(due_date, datetime):
                if due_date < issue_date:
                    errors.append("Due date cannot be earlier than issue date")
                
                # Warning if due date is too far in the future
                if due_date > issue_date + timedelta(days=90):
                    warnings.append("Due date is more than 90 days after issue date")
        
        # Check amount consistency
        total_amount = data.get("total_amount")
        net_amount = data.get("net_amount")
        tax_amount = data.get("tax_amount")
        
        if isinstance(total_amount, (int, float)) and isinstance(net_amount, (int, float)) and isinstance(tax_amount, (int, float)):
            # Check if total = net + tax
            expected_total = net_amount + tax_amount
            
            if not is_amount_within_tolerance(total_amount, expected_total, tolerance=0.02):
                errors.append(
                    f"Total amount ({total_amount}) does not match net + tax "
                    f"({net_amount} + {tax_amount} = {expected_total})"
                )
        
        # Validate tax rate consistency if tax rate is provided
        tax_rate = data.get("tax_rate")
        if isinstance(tax_rate, (int, float)) and isinstance(net_amount, (int, float)) and isinstance(tax_amount, (int, float)):
            expected_tax = net_amount * (tax_rate / 100.0)
            
            if not is_amount_within_tolerance(tax_amount, expected_tax, tolerance=0.05):
                warnings.append(
                    f"Tax amount ({tax_amount}) does not match expected tax "
                    f"({net_amount} × {tax_rate}% = {expected_tax})"
                )
        
        # Calculate confidence based on errors and warnings
        confidence = 1.0
        if errors:
            confidence = 0.0
        elif warnings:
            # Reduce confidence proportionally to the number of warnings
            confidence = max(0.5, 1.0 - (len(warnings) * 0.1))
        
        return ValidationResult(
            valid=len(errors) == 0,
            confidence=confidence,
            errors=errors,
            warnings=warnings,
            details={"checked_fields": list(data.keys())}
        )


class ReceiptValidator(DocumentValidator):
    """Validator for receipt documents."""
    
    def __init__(self, field_validators: Optional[Dict[str, Any]] = None):
        """
        Initialize receipt validator with field validators.
        
        Args:
            field_validators: Dictionary mapping field names to field validators
        """
        # Set default field validators if not provided
        if field_validators is None:
            field_validators = {
                "receipt_number": TextValidator(min_length=1, max_length=50, required=False),
                "date": DateValidator(),
                "total_amount": AmountValidator(min_value=0.01),
                "tax_amount": AmountValidator(min_value=0.0, required=False),
                "merchant_name": TextValidator(min_length=1),
            }
        
        super().__init__(field_validators)
    
    def validate_consistency(self, data: Dict[str, Any]) -> ValidationResult:
        """
        Validate cross-field consistency in receipt data.
        
        Args:
            data: Receipt data dictionary
            
        Returns:
            ValidationResult containing validation outcome
        """
        errors = []
        warnings = []
        
        # Check date is not in the future
        if "date" in data:
            receipt_date = data["date"]
            
            if isinstance(receipt_date, datetime):
                if receipt_date > datetime.now() + timedelta(days=1):  # Allow for timezone differences
                    errors.append("Receipt date cannot be in the future")
        
        # Check amount consistency
        total_amount = data.get("total_amount")
        items_total = 0.0
        
        # Sum up line items if available
        if "items" in data and isinstance(data["items"], list):
            for item in data["items"]:
                if isinstance(item, dict) and "amount" in item:
                    items_total += float(item["amount"])
            
            # Check if total matches sum of items
            if isinstance(total_amount, (int, float)) and items_total > 0:
                if not is_amount_within_tolerance(total_amount, items_total, tolerance=0.02):
                    warnings.append(
                        f"Total amount ({total_amount}) does not match sum of items ({items_total})"
                    )
        
        # Calculate confidence based on errors and warnings
        confidence = 1.0
        if errors:
            confidence = 0.0
        elif warnings:
            # Reduce confidence proportionally to the number of warnings
            confidence = max(0.5, 1.0 - (len(warnings) * 0.1))
        
        return ValidationResult(
            valid=len(errors) == 0,
            confidence=confidence,
            errors=errors,
            warnings=warnings,
            details={"checked_fields": list(data.keys())}
        )


class BankStatementValidator(DocumentValidator):
    """Validator for bank statement documents."""
    
    def __init__(self, field_validators: Optional[Dict[str, Any]] = None):
        """
        Initialize bank statement validator with field validators.
        
        Args:
            field_validators: Dictionary mapping field names to field validators
        """
        # Set default field validators if not provided
        if field_validators is None:
            field_validators = {
                "account_number": TextValidator(min_length=5),
                "start_date": DateValidator(),
                "end_date": DateValidator(),
                "opening_balance": AmountValidator(),
                "closing_balance": AmountValidator(),
                "bank_name": TextValidator(min_length=1),
            }
        
        super().__init__(field_validators)
    
    def validate_consistency(self, data: Dict[str, Any]) -> ValidationResult:
        """
        Validate cross-field consistency in bank statement data.
        
        Args:
            data: Bank statement data dictionary
            
        Returns:
            ValidationResult containing validation outcome
        """
        errors = []
        warnings = []
        
        # Check date consistency
        if "start_date" in data and "end_date" in data:
            start_date = data["start_date"]
            end_date = data["end_date"]
            
            if isinstance(start_date, datetime) and isinstance(end_date, datetime):
                if end_date < start_date:
                    errors.append("End date cannot be earlier than start date")
        
        # Check balance consistency
        opening_balance = data.get("opening_balance")
        closing_balance = data.get("closing_balance")
        transactions_sum = 0.0
        
        # Sum up transactions if available
        if "transactions" in data and isinstance(data["transactions"], list):
            for transaction in data["transactions"]:
                if isinstance(transaction, dict) and "amount" in transaction:
                    transactions_sum += float(transaction["amount"])
            
            # Check if closing = opening + transactions_sum
            if isinstance(opening_balance, (int, float)) and isinstance(closing_balance, (int, float)):
                expected_closing = opening_balance + transactions_sum
                
                if not is_amount_within_tolerance(closing_balance, expected_closing, tolerance=0.01):
                    errors.append(
                        f"Closing balance ({closing_balance}) does not match opening balance + "
                        f"transactions ({opening_balance} + {transactions_sum} = {expected_closing})"
                    )
        
        # Calculate confidence based on errors and warnings
        confidence = 1.0
        if errors:
            confidence = 0.0
        elif warnings:
            # Reduce confidence proportionally to the number of warnings
            confidence = max(0.5, 1.0 - (len(warnings) * 0.1))
        
        return ValidationResult(
            valid=len(errors) == 0,
            confidence=confidence,
            errors=errors,
            warnings=warnings,
            details={"checked_fields": list(data.keys())}
        )
