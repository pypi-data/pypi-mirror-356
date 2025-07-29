"""
Field validators for common financial document fields.

This module provides validators for common fields found in financial documents
such as amounts, dates, tax IDs, etc.
"""

import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Pattern, Union

from invutil.date_utils import is_valid_date, parse_date_multilingual
from invutil.numeric_utils import is_amount_within_tolerance, parse_amount

from .base import FieldValidator, ValidationResult


class AmountValidator(FieldValidator):
    """Validator for monetary amounts."""
    
    def __init__(
        self, 
        min_value: float = 0.0,
        max_value: float = 1e9,
        required: bool = True
    ):
        """
        Initialize amount validator.
        
        Args:
            min_value: Minimum valid amount
            max_value: Maximum valid amount
            required: Whether the field is required
        """
        self.min_value = min_value
        self.max_value = max_value
        self.required = required
    
    def validate_field(self, field_name: str, field_value: Any) -> ValidationResult:
        """
        Validate a monetary amount field.
        
        Args:
            field_name: Name of the field
            field_value: Value of the field (string or number)
            
        Returns:
            ValidationResult containing validation outcome
        """
        # Handle missing value
        if field_value is None or (isinstance(field_value, str) and not field_value.strip()):
            if self.required:
                return ValidationResult(
                    valid=False,
                    confidence=0.0,
                    errors=[f"Field {field_name} is required"]
                )
            else:
                return ValidationResult(valid=True, confidence=1.0)
        
        # Parse string to float if needed
        amount = field_value
        if isinstance(field_value, str):
            parsed = parse_amount(field_value)
            if parsed is None:
                return ValidationResult(
                    valid=False,
                    confidence=0.0,
                    errors=[f"Invalid amount format: {field_value}"]
                )
            amount = parsed
        
        # Validate range
        if not isinstance(amount, (int, float)):
            return ValidationResult(
                valid=False,
                confidence=0.0,
                errors=[f"Amount must be a number, got {type(amount).__name__}"]
            )
        
        if amount < self.min_value:
            return ValidationResult(
                valid=False,
                confidence=0.0,
                errors=[f"Amount {amount} is below minimum {self.min_value}"]
            )
        
        if amount > self.max_value:
            return ValidationResult(
                valid=False,
                confidence=0.0,
                errors=[f"Amount {amount} exceeds maximum {self.max_value}"]
            )
        
        return ValidationResult(valid=True, confidence=1.0)


class DateValidator(FieldValidator):
    """Validator for date fields."""
    
    def __init__(
        self,
        min_date: Optional[Union[datetime, str]] = None,
        max_date: Optional[Union[datetime, str]] = None,
        required: bool = True,
        languages: Optional[List[str]] = None
    ):
        """
        Initialize date validator.
        
        Args:
            min_date: Minimum valid date
            max_date: Maximum valid date
            required: Whether the field is required
            languages: List of language codes for date parsing
        """
        self.required = required
        self.languages = languages or ["en", "de", "fr", "pl", "es"]
        
        # Parse string dates if provided
        self.min_date = None
        if min_date is not None:
            if isinstance(min_date, str):
                self.min_date = parse_date_multilingual(min_date, self.languages)
            else:
                self.min_date = min_date
        
        self.max_date = None
        if max_date is not None:
            if isinstance(max_date, str):
                self.max_date = parse_date_multilingual(max_date, self.languages)
            else:
                self.max_date = max_date
    
    def validate_field(self, field_name: str, field_value: Any) -> ValidationResult:
        """
        Validate a date field.
        
        Args:
            field_name: Name of the field
            field_value: Value of the field (string or datetime)
            
        Returns:
            ValidationResult containing validation outcome
        """
        # Handle missing value
        if field_value is None or (isinstance(field_value, str) and not field_value.strip()):
            if self.required:
                return ValidationResult(
                    valid=False,
                    confidence=0.0,
                    errors=[f"Field {field_name} is required"]
                )
            else:
                return ValidationResult(valid=True, confidence=1.0)
        
        # Parse string to datetime if needed
        date_value = field_value
        if isinstance(field_value, str):
            parsed = parse_date_multilingual(field_value, self.languages)
            if parsed is None:
                return ValidationResult(
                    valid=False,
                    confidence=0.0,
                    errors=[f"Invalid date format: {field_value}"]
                )
            date_value = parsed
        
        # Validate date type
        if not isinstance(date_value, datetime):
            return ValidationResult(
                valid=False,
                confidence=0.0,
                errors=[f"Date must be a datetime object, got {type(date_value).__name__}"]
            )
        
        # Validate range
        if self.min_date and date_value < self.min_date:
            return ValidationResult(
                valid=False,
                confidence=0.0,
                errors=[f"Date {date_value} is before minimum {self.min_date}"]
            )
        
        if self.max_date and date_value > self.max_date:
            return ValidationResult(
                valid=False,
                confidence=0.0,
                errors=[f"Date {date_value} is after maximum {self.max_date}"]
            )
        
        return ValidationResult(valid=True, confidence=1.0)


class TextValidator(FieldValidator):
    """Validator for text fields."""
    
    def __init__(
        self,
        min_length: int = 0,
        max_length: int = 1000,
        pattern: Optional[Union[str, Pattern]] = None,
        required: bool = True
    ):
        """
        Initialize text validator.
        
        Args:
            min_length: Minimum text length
            max_length: Maximum text length
            pattern: Optional regex pattern for validation
            required: Whether the field is required
        """
        self.min_length = min_length
        self.max_length = max_length
        self.required = required
        
        if pattern is not None and isinstance(pattern, str):
            self.pattern = re.compile(pattern)
        else:
            self.pattern = pattern
    
    def validate_field(self, field_name: str, field_value: Any) -> ValidationResult:
        """
        Validate a text field.
        
        Args:
            field_name: Name of the field
            field_value: Value of the field
            
        Returns:
            ValidationResult containing validation outcome
        """
        # Handle missing value
        if field_value is None or (isinstance(field_value, str) and not field_value.strip()):
            if self.required:
                return ValidationResult(
                    valid=False,
                    confidence=0.0,
                    errors=[f"Field {field_name} is required"]
                )
            else:
                return ValidationResult(valid=True, confidence=1.0)
        
        # Ensure value is a string
        if not isinstance(field_value, str):
            return ValidationResult(
                valid=False,
                confidence=0.0,
                errors=[f"Field {field_name} must be a string, got {type(field_value).__name__}"]
            )
        
        # Validate length
        if len(field_value) < self.min_length:
            return ValidationResult(
                valid=False,
                confidence=0.0,
                errors=[f"Field {field_name} is too short (min: {self.min_length})"]
            )
        
        if len(field_value) > self.max_length:
            return ValidationResult(
                valid=False,
                confidence=0.0,
                errors=[f"Field {field_name} is too long (max: {self.max_length})"]
            )
        
        # Validate pattern
        if self.pattern and not self.pattern.match(field_value):
            return ValidationResult(
                valid=False,
                confidence=0.0,
                errors=[f"Field {field_name} does not match required pattern"]
            )
        
        return ValidationResult(valid=True, confidence=1.0)


class TaxIDValidator(TextValidator):
    """Validator for tax identification numbers."""
    
    COUNTRY_PATTERNS = {
        # VAT ID patterns for various countries
        "PL": r"^PL[0-9]{10}$",  # Poland
        "DE": r"^DE[0-9]{9}$",   # Germany
        "FR": r"^FR[A-Z0-9]{2}[0-9]{9}$",  # France
        "GB": r"^GB[0-9]{9}$|^GB[0-9]{12}$|^GBGD[0-9]{3}$|^GBHA[0-9]{3}$",  # UK
        "IT": r"^IT[0-9]{11}$",  # Italy
        "ES": r"^ES[A-Z0-9][0-9]{7}[A-Z0-9]$",  # Spain
        "NL": r"^NL[0-9]{9}B[0-9]{2}$",  # Netherlands
    }
    
    def __init__(
        self,
        country: Optional[str] = None,
        required: bool = True
    ):
        """
        Initialize tax ID validator.
        
        Args:
            country: Country code for specific validation pattern
            required: Whether the field is required
        """
        pattern = None
        if country and country.upper() in self.COUNTRY_PATTERNS:
            pattern = self.COUNTRY_PATTERNS[country.upper()]
        
        super().__init__(
            min_length=5,
            max_length=30,
            pattern=pattern,
            required=required
        )
        
        self.country = country
    
    def validate_field(self, field_name: str, field_value: Any) -> ValidationResult:
        """
        Validate a tax ID field.
        
        Args:
            field_name: Name of the field
            field_value: Value of the field
            
        Returns:
            ValidationResult containing validation outcome
        """
        # Basic text validation
        result = super().validate_field(field_name, field_value)
        if not result.valid:
            return result
        
        # Skip further validation if field is empty and not required
        if not field_value and not self.required:
            return ValidationResult(valid=True, confidence=1.0)
        
        # If no country was specified at init but value has country prefix
        if not self.country and isinstance(field_value, str) and len(field_value) >= 2:
            country_prefix = field_value[:2].upper()
            if country_prefix in self.COUNTRY_PATTERNS:
                pattern = re.compile(self.COUNTRY_PATTERNS[country_prefix])
                if not pattern.match(field_value):
                    return ValidationResult(
                        valid=False,
                        confidence=0.0,
                        errors=[f"Invalid {country_prefix} tax ID format"]
                    )
        
        # Additional validation could be added here (checksum, etc.)
        
        return ValidationResult(valid=True, confidence=1.0)


class PercentageValidator(AmountValidator):
    """Validator for percentage values."""
    
    def __init__(self, required: bool = True):
        """
        Initialize percentage validator.
        
        Args:
            required: Whether the field is required
        """
        super().__init__(min_value=0.0, max_value=100.0, required=required)
    
    def validate_field(self, field_name: str, field_value: Any) -> ValidationResult:
        """
        Validate a percentage field.
        
        Args:
            field_name: Name of the field
            field_value: Value of the field
            
        Returns:
            ValidationResult containing validation outcome
        """
        # Basic amount validation
        result = super().validate_field(field_name, field_value)
        
        # Additional percentage-specific validation could be added here
        
        return result
