"""
Validation Node for the Nüm Agents SDK.

This module provides a specialized node for validating data against schemas,
rules, and constraints, with support for different validation strategies.
"""

import json
import logging
import re
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union

import jsonschema
import pandas as pd
import numpy as np

from num_agents.core import Node, SharedStore


class ValidationStrategy(Enum):
    """Enum for different validation strategies."""
    
    JSON_SCHEMA = "json_schema"
    PANDAS_SCHEMA = "pandas_schema"
    CUSTOM_FUNCTION = "custom_function"
    REGEX = "regex"
    TYPE_CHECK = "type_check"
    RANGE_CHECK = "range_check"
    REQUIRED_FIELDS = "required_fields"


class ValidationResult:
    """Class to represent the result of a validation operation."""
    
    def __init__(
        self,
        is_valid: bool,
        errors: Optional[List[Dict[str, Any]]] = None,
        warnings: Optional[List[Dict[str, Any]]] = None
    ) -> None:
        """
        Initialize a validation result.
        
        Args:
            is_valid: Whether the validation passed
            errors: Optional list of validation errors
            warnings: Optional list of validation warnings
        """
        self.is_valid = is_valid
        self.errors = errors or []
        self.warnings = warnings or []
    
    def __bool__(self) -> bool:
        """
        Return whether the validation passed.
        
        Returns:
            True if the validation passed, False otherwise
        """
        return self.is_valid
    
    def add_error(self, message: str, path: Optional[str] = None, details: Optional[Dict[str, Any]] = None) -> None:
        """
        Add an error to the validation result.
        
        Args:
            message: The error message
            path: Optional path to the error location
            details: Optional additional details about the error
        """
        self.is_valid = False
        self.errors.append({
            "message": message,
            "path": path,
            "details": details or {}
        })
    
    def add_warning(self, message: str, path: Optional[str] = None, details: Optional[Dict[str, Any]] = None) -> None:
        """
        Add a warning to the validation result.
        
        Args:
            message: The warning message
            path: Optional path to the warning location
            details: Optional additional details about the warning
        """
        self.warnings.append({
            "message": message,
            "path": path,
            "details": details or {}
        })
    
    def merge(self, other: "ValidationResult") -> None:
        """
        Merge another validation result into this one.
        
        Args:
            other: The validation result to merge
        """
        self.is_valid = self.is_valid and other.is_valid
        self.errors.extend(other.errors)
        self.warnings.extend(other.warnings)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the validation result to a dictionary.
        
        Returns:
            A dictionary representation of the validation result
        """
        return {
            "is_valid": self.is_valid,
            "errors": self.errors,
            "warnings": self.warnings
        }


class Validator(ABC):
    """Abstract base class for validators."""
    
    @abstractmethod
    def validate(self, data: Any) -> ValidationResult:
        """
        Validate the data.
        
        Args:
            data: The data to validate
            
        Returns:
            A validation result
        """
        pass


class JsonSchemaValidator(Validator):
    """Validator for JSON Schema validation."""
    
    def __init__(self, schema: Dict[str, Any]) -> None:
        """
        Initialize a JSON Schema validator.
        
        Args:
            schema: The JSON Schema to validate against
        """
        self.schema = schema
    
    def validate(self, data: Any) -> ValidationResult:
        """
        Validate the data against the JSON Schema.
        
        Args:
            data: The data to validate
            
        Returns:
            A validation result
        """
        result = ValidationResult(True)
        
        try:
            jsonschema.validate(instance=data, schema=self.schema)
        except jsonschema.exceptions.ValidationError as e:
            result.add_error(
                message=str(e),
                path=".".join(str(p) for p in e.path),
                details={"schema_path": ".".join(str(p) for p in e.schema_path)}
            )
        except Exception as e:
            result.add_error(message=f"Validation error: {str(e)}")
        
        return result


class CustomFunctionValidator(Validator):
    """Validator for custom validation functions."""
    
    def __init__(self, validation_function: Callable[[Any], Union[bool, ValidationResult]]) -> None:
        """
        Initialize a custom function validator.
        
        Args:
            validation_function: A function that takes data and returns a boolean or ValidationResult
        """
        self.validation_function = validation_function
    
    def validate(self, data: Any) -> ValidationResult:
        """
        Validate the data using the custom function.
        
        Args:
            data: The data to validate
            
        Returns:
            A validation result
        """
        try:
            result = self.validation_function(data)
            
            if isinstance(result, ValidationResult):
                return result
            elif isinstance(result, bool):
                return ValidationResult(result)
            else:
                return ValidationResult(bool(result))
        
        except Exception as e:
            result = ValidationResult(False)
            result.add_error(message=f"Validation function error: {str(e)}")
            return result


class RegexValidator(Validator):
    """Validator for regular expression validation."""
    
    def __init__(self, pattern: str, field: Optional[str] = None) -> None:
        """
        Initialize a regex validator.
        
        Args:
            pattern: The regular expression pattern to match
            field: Optional field name to validate (if None, validates the entire data as a string)
        """
        self.pattern = pattern
        self.regex = re.compile(pattern)
        self.field = field
    
    def validate(self, data: Any) -> ValidationResult:
        """
        Validate the data against the regex pattern.
        
        Args:
            data: The data to validate
            
        Returns:
            A validation result
        """
        result = ValidationResult(True)
        
        try:
            if self.field is not None:
                if isinstance(data, dict) and self.field in data:
                    value = data[self.field]
                elif hasattr(data, self.field):
                    value = getattr(data, self.field)
                else:
                    result.add_error(message=f"Field '{self.field}' not found in data")
                    return result
            else:
                value = data
            
            if not isinstance(value, str):
                value = str(value)
            
            if not self.regex.match(value):
                result.add_error(
                    message=f"Value does not match pattern '{self.pattern}'",
                    path=self.field
                )
        
        except Exception as e:
            result.add_error(message=f"Regex validation error: {str(e)}")
        
        return result


class TypeValidator(Validator):
    """Validator for type checking."""
    
    def __init__(self, expected_type: Any, field: Optional[str] = None) -> None:
        """
        Initialize a type validator.
        
        Args:
            expected_type: The expected type or types
            field: Optional field name to validate (if None, validates the entire data)
        """
        self.expected_type = expected_type
        self.field = field
    
    def validate(self, data: Any) -> ValidationResult:
        """
        Validate the data's type.
        
        Args:
            data: The data to validate
            
        Returns:
            A validation result
        """
        result = ValidationResult(True)
        
        try:
            if self.field is not None:
                if isinstance(data, dict) and self.field in data:
                    value = data[self.field]
                elif hasattr(data, self.field):
                    value = getattr(data, self.field)
                else:
                    result.add_error(message=f"Field '{self.field}' not found in data")
                    return result
            else:
                value = data
            
            if not isinstance(value, self.expected_type):
                result.add_error(
                    message=f"Expected type {self.expected_type.__name__}, got {type(value).__name__}",
                    path=self.field
                )
        
        except Exception as e:
            result.add_error(message=f"Type validation error: {str(e)}")
        
        return result


class RangeValidator(Validator):
    """Validator for range checking."""
    
    def __init__(
        self,
        min_value: Optional[Any] = None,
        max_value: Optional[Any] = None,
        field: Optional[str] = None
    ) -> None:
        """
        Initialize a range validator.
        
        Args:
            min_value: Optional minimum value (inclusive)
            max_value: Optional maximum value (inclusive)
            field: Optional field name to validate (if None, validates the entire data)
        """
        self.min_value = min_value
        self.max_value = max_value
        self.field = field
    
    def validate(self, data: Any) -> ValidationResult:
        """
        Validate the data's range.
        
        Args:
            data: The data to validate
            
        Returns:
            A validation result
        """
        result = ValidationResult(True)
        
        try:
            if self.field is not None:
                if isinstance(data, dict) and self.field in data:
                    value = data[self.field]
                elif hasattr(data, self.field):
                    value = getattr(data, self.field)
                else:
                    result.add_error(message=f"Field '{self.field}' not found in data")
                    return result
            else:
                value = data
            
            if self.min_value is not None and value < self.min_value:
                result.add_error(
                    message=f"Value {value} is less than minimum {self.min_value}",
                    path=self.field
                )
            
            if self.max_value is not None and value > self.max_value:
                result.add_error(
                    message=f"Value {value} is greater than maximum {self.max_value}",
                    path=self.field
                )
        
        except Exception as e:
            result.add_error(message=f"Range validation error: {str(e)}")
        
        return result


class RequiredFieldsValidator(Validator):
    """Validator for required fields."""
    
    def __init__(self, required_fields: List[str]) -> None:
        """
        Initialize a required fields validator.
        
        Args:
            required_fields: List of required field names
        """
        self.required_fields = required_fields
    
    def validate(self, data: Any) -> ValidationResult:
        """
        Validate that the data has all required fields.
        
        Args:
            data: The data to validate
            
        Returns:
            A validation result
        """
        result = ValidationResult(True)
        
        try:
            if isinstance(data, dict):
                for field in self.required_fields:
                    if field not in data:
                        result.add_error(message=f"Required field '{field}' is missing")
            
            elif hasattr(data, "__dict__"):
                for field in self.required_fields:
                    if not hasattr(data, field):
                        result.add_error(message=f"Required field '{field}' is missing")
            
            else:
                result.add_error(message="Data is not a dictionary or object with attributes")
        
        except Exception as e:
            result.add_error(message=f"Required fields validation error: {str(e)}")
        
        return result


class ValidationNode(Node):
    """
    A specialized node for validating data.
    
    This node provides a standardized interface for validating data against
    schemas, rules, and constraints, with support for different validation
    strategies.
    """
    
    def __init__(
        self,
        name: str,
        shared_store: SharedStore,
        input_key: str,
        result_key: str,
        validators: List[Validator],
        fail_on_error: bool = False,
        **kwargs
    ) -> None:
        """
        Initialize a validation node.
        
        Args:
            name: The name of the node
            shared_store: The shared store for the agent
            input_key: The key in the shared store to use as input
            result_key: The key in the shared store to store the validation result
            validators: List of validators to apply to the data
            fail_on_error: Whether to raise an exception if validation fails
            **kwargs: Additional parameters
        """
        super().__init__(name, shared_store)
        
        self.input_key = input_key
        self.result_key = result_key
        self.validators = validators
        self.fail_on_error = fail_on_error
        self.additional_params = kwargs
    
    def _process(self) -> None:
        """
        Process the node's logic.
        
        This method retrieves the input data from the shared store, validates it,
        and stores the validation result in the shared store.
        """
        try:
            # Get the input data
            input_data = self._get_input_data()
            
            if input_data is None:
                logging.warning(f"No input data found at key '{self.input_key}' in shared store.")
                result = ValidationResult(False)
                result.add_error(message=f"No input data found at key '{self.input_key}'")
                self._set_result(result)
                
                if self.fail_on_error:
                    raise ValueError(f"No input data found at key '{self.input_key}'")
                
                return
            
            # Validate the data
            result = self._validate_data(input_data)
            
            # Store the result in the shared store
            self._set_result(result)
            
            # Raise an exception if validation failed and fail_on_error is True
            if self.fail_on_error and not result.is_valid:
                error_messages = [error["message"] for error in result.errors]
                raise ValueError(f"Validation failed: {', '.join(error_messages)}")
        
        except Exception as e:
            logging.error(f"Error validating data: {str(e)}")
            
            if self.fail_on_error:
                raise
            
            # Create a validation result with the error
            result = ValidationResult(False)
            result.add_error(message=f"Validation error: {str(e)}")
            self._set_result(result)
    
    def _get_input_data(self) -> Any:
        """
        Get the input data from the shared store.
        
        Returns:
            The input data, or None if no data is found
        """
        # Check if the input key is an attribute of the shared store
        if hasattr(self.shared_store, self.input_key):
            return getattr(self.shared_store, self.input_key)
        
        # Check if the shared store has a data dictionary
        if hasattr(self.shared_store, "data") and isinstance(self.shared_store.data, dict):
            return self.shared_store.data.get(self.input_key)
        
        return None
    
    def _set_result(self, result: ValidationResult) -> None:
        """
        Set the validation result in the shared store.
        
        Args:
            result: The validation result to store
        """
        # Convert the result to a dictionary
        result_dict = result.to_dict()
        
        # Check if the result key is an attribute of the shared store
        if hasattr(self.shared_store, self.result_key):
            setattr(self.shared_store, self.result_key, result_dict)
        
        # Check if the shared store has a data dictionary
        elif hasattr(self.shared_store, "data") and isinstance(self.shared_store.data, dict):
            self.shared_store.data[self.result_key] = result_dict
    
    def _validate_data(self, data: Any) -> ValidationResult:
        """
        Validate the data using all validators.
        
        Args:
            data: The data to validate
            
        Returns:
            A validation result
        """
        # Initialize the result as valid
        result = ValidationResult(True)
        
        # Apply each validator and merge the results
        for validator in self.validators:
            validator_result = validator.validate(data)
            result.merge(validator_result)
        
        return result


def create_validator(
    strategy: Union[str, ValidationStrategy],
    **kwargs
) -> Validator:
    """
    Create a validator based on the specified strategy.
    
    Args:
        strategy: The validation strategy to use
        **kwargs: Additional parameters for the validator
    
    Returns:
        A validator instance
    """
    # Convert strategy to enum if it's a string
    if isinstance(strategy, str):
        try:
            strategy = ValidationStrategy(strategy.lower())
        except ValueError:
            raise ValueError(f"Invalid validation strategy: {strategy}")
    
    # Create the validator based on the strategy
    if strategy == ValidationStrategy.JSON_SCHEMA:
        schema = kwargs.get("schema")
        if not schema:
            raise ValueError("JSON Schema validation requires a schema")
        return JsonSchemaValidator(schema)
    
    elif strategy == ValidationStrategy.CUSTOM_FUNCTION:
        validation_function = kwargs.get("validation_function")
        if not validation_function:
            raise ValueError("Custom function validation requires a validation_function")
        return CustomFunctionValidator(validation_function)
    
    elif strategy == ValidationStrategy.REGEX:
        pattern = kwargs.get("pattern")
        if not pattern:
            raise ValueError("Regex validation requires a pattern")
        field = kwargs.get("field")
        return RegexValidator(pattern, field)
    
    elif strategy == ValidationStrategy.TYPE_CHECK:
        expected_type = kwargs.get("expected_type")
        if not expected_type:
            raise ValueError("Type validation requires an expected_type")
        field = kwargs.get("field")
        return TypeValidator(expected_type, field)
    
    elif strategy == ValidationStrategy.RANGE_CHECK:
        min_value = kwargs.get("min_value")
        max_value = kwargs.get("max_value")
        if min_value is None and max_value is None:
            raise ValueError("Range validation requires at least one of min_value or max_value")
        field = kwargs.get("field")
        return RangeValidator(min_value, max_value, field)
    
    elif strategy == ValidationStrategy.REQUIRED_FIELDS:
        required_fields = kwargs.get("required_fields")
        if not required_fields:
            raise ValueError("Required fields validation requires a list of required_fields")
        return RequiredFieldsValidator(required_fields)
    
    else:
        raise ValueError(f"Unsupported validation strategy: {strategy}")
