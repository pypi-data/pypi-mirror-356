"""
Base validation interfaces and abstract classes.

This module provides the core validation interfaces and abstract base classes
that all validators should implement.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple, Union

from pydantic import BaseModel


class ValidationResult(BaseModel):
    """Result of a validation operation."""
    
    valid: bool
    """Whether the validation passed."""
    
    confidence: float
    """Confidence score for the validation (0.0-1.0)."""
    
    errors: List[str] = []
    """List of error messages if validation failed."""
    
    warnings: List[str] = []
    """List of warning messages (issues that don't invalidate the data)."""
    
    details: Dict[str, Any] = {}
    """Additional details about the validation result."""


class Validator(ABC):
    """Base validator interface."""
    
    @abstractmethod
    def validate(self, data: Any) -> ValidationResult:
        """
        Validate the provided data.
        
        Args:
            data: Data to validate
            
        Returns:
            ValidationResult containing validation outcome
        """
        pass


class FieldValidator(Validator):
    """Validator for individual fields."""
    
    @abstractmethod
    def validate_field(self, field_name: str, field_value: Any) -> ValidationResult:
        """
        Validate a specific field.
        
        Args:
            field_name: Name of the field
            field_value: Value of the field
            
        Returns:
            ValidationResult containing validation outcome
        """
        pass
    
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """
        Validate all fields in the data dictionary.
        
        Args:
            data: Dictionary of field names to values
            
        Returns:
            ValidationResult containing validation outcome
        """
        all_valid = True
        all_errors = []
        all_warnings = []
        details = {}
        
        for field_name, field_value in data.items():
            result = self.validate_field(field_name, field_value)
            if not result.valid:
                all_valid = False
                all_errors.extend([f"{field_name}: {error}" for error in result.errors])
            
            all_warnings.extend([f"{field_name}: {warning}" for warning in result.warnings])
            details[field_name] = result.model_dump()
        
        return ValidationResult(
            valid=all_valid,
            confidence=1.0 if all_valid else 0.0,
            errors=all_errors,
            warnings=all_warnings,
            details=details
        )


class DocumentValidator(Validator):
    """Validator for entire documents."""
    
    def __init__(self, field_validators: Optional[Dict[str, FieldValidator]] = None):
        """
        Initialize document validator with field validators.
        
        Args:
            field_validators: Dictionary mapping field names to field validators
        """
        self.field_validators = field_validators or {}
    
    def validate_consistency(self, data: Dict[str, Any]) -> ValidationResult:
        """
        Validate cross-field consistency.
        
        Args:
            data: Document data dictionary
            
        Returns:
            ValidationResult containing validation outcome
        """
        # Default implementation - override in subclasses
        return ValidationResult(valid=True, confidence=1.0)
    
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """
        Validate the entire document.
        
        Args:
            data: Document data dictionary
            
        Returns:
            ValidationResult containing validation outcome
        """
        # First validate individual fields
        all_valid = True
        all_errors = []
        all_warnings = []
        field_details = {}
        
        for field_name, validator in self.field_validators.items():
            if field_name in data:
                result = validator.validate_field(field_name, data[field_name])
                if not result.valid:
                    all_valid = False
                    all_errors.extend([f"{field_name}: {error}" for error in result.errors])
                
                all_warnings.extend([f"{field_name}: {warning}" for warning in result.warnings])
                field_details[field_name] = result.model_dump()
        
        # Then validate cross-field consistency
        consistency_result = self.validate_consistency(data)
        if not consistency_result.valid:
            all_valid = False
            all_errors.extend(consistency_result.errors)
        
        all_warnings.extend(consistency_result.warnings)
        
        # Calculate overall confidence
        field_confidences = [
            details.get("confidence", 0.0) for details in field_details.values()
        ]
        avg_confidence = sum(field_confidences) / len(field_confidences) if field_confidences else 0.0
        consistency_confidence = consistency_result.confidence
        
        # Weight field validation and consistency equally
        overall_confidence = (avg_confidence + consistency_confidence) / 2.0 if all_valid else 0.0
        
        return ValidationResult(
            valid=all_valid,
            confidence=overall_confidence,
            errors=all_errors,
            warnings=all_warnings,
            details={
                "fields": field_details,
                "consistency": consistency_result.model_dump()
            }
        )
