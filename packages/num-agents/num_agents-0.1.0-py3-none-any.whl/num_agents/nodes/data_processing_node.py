"""
Data Processing Node for the Nüm Agents SDK.

This module provides a specialized node for processing and transforming data,
with support for common data operations and transformations.
"""

import json
import logging
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union

import pandas as pd
import numpy as np

from num_agents.core import Node, SharedStore


class DataFormat(Enum):
    """Enum for different data formats."""
    
    JSON = "json"
    CSV = "csv"
    DATAFRAME = "dataframe"
    DICT = "dict"
    LIST = "list"
    TEXT = "text"
    NUMPY = "numpy"


class DataProcessingNode(Node):
    """
    A specialized node for processing and transforming data.
    
    This node provides a standardized interface for processing data in various
    formats, with support for common data operations and transformations.
    """
    
    def __init__(
        self,
        name: str,
        shared_store: SharedStore,
        input_key: str,
        output_key: str,
        input_format: Union[str, DataFormat] = DataFormat.JSON,
        output_format: Union[str, DataFormat] = DataFormat.JSON,
        transformations: Optional[List[Callable[[Any], Any]]] = None,
        error_handling: str = "log_and_continue",
        **kwargs
    ) -> None:
        """
        Initialize a data processing node.
        
        Args:
            name: The name of the node
            shared_store: The shared store for the agent
            input_key: The key in the shared store to use as input
            output_key: The key in the shared store to store the output
            input_format: The format of the input data
            output_format: The format to convert the output data to
            transformations: Optional list of transformation functions to apply to the data
            error_handling: How to handle errors during processing
                            ("log_and_continue", "raise", "return_none", "return_empty")
            **kwargs: Additional parameters for specific data formats
        """
        super().__init__(name, shared_store)
        
        self.input_key = input_key
        self.output_key = output_key
        
        # Convert input_format to enum if it's a string
        if isinstance(input_format, str):
            try:
                self.input_format = DataFormat(input_format.lower())
            except ValueError:
                raise ValueError(f"Invalid input format: {input_format}")
        else:
            self.input_format = input_format
        
        # Convert output_format to enum if it's a string
        if isinstance(output_format, str):
            try:
                self.output_format = DataFormat(output_format.lower())
            except ValueError:
                raise ValueError(f"Invalid output format: {output_format}")
        else:
            self.output_format = output_format
        
        self.transformations = transformations or []
        self.error_handling = error_handling
        self.additional_params = kwargs
    
    def _process(self) -> None:
        """
        Process the node's logic.
        
        This method retrieves the input data from the shared store, processes it,
        and stores the result in the shared store.
        """
        try:
            # Get the input data
            input_data = self._get_input_data()
            
            if input_data is None:
                logging.warning(f"No input data found at key '{self.input_key}' in shared store.")
                self._handle_error("No input data found.")
                return
            
            # Parse the input data
            parsed_data = self._parse_input(input_data)
            
            # Apply transformations
            processed_data = self._apply_transformations(parsed_data)
            
            # Convert to the output format
            output_data = self._convert_to_output_format(processed_data)
            
            # Store the result in the shared store
            self._set_output_data(output_data)
        
        except Exception as e:
            logging.error(f"Error processing data: {str(e)}")
            self._handle_error(str(e))
    
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
    
    def _set_output_data(self, output_data: Any) -> None:
        """
        Set the output data in the shared store.
        
        Args:
            output_data: The processed data to store
        """
        # Check if the output key is an attribute of the shared store
        if hasattr(self.shared_store, self.output_key):
            setattr(self.shared_store, self.output_key, output_data)
        
        # Check if the shared store has a data dictionary
        elif hasattr(self.shared_store, "data") and isinstance(self.shared_store.data, dict):
            self.shared_store.data[self.output_key] = output_data
    
    def _parse_input(self, input_data: Any) -> Any:
        """
        Parse the input data based on the specified format.
        
        Args:
            input_data: The input data to parse
            
        Returns:
            The parsed data
        """
        try:
            if self.input_format == DataFormat.JSON:
                if isinstance(input_data, str):
                    return json.loads(input_data)
                return input_data  # Assume it's already parsed
            
            elif self.input_format == DataFormat.CSV:
                if isinstance(input_data, str):
                    return pd.read_csv(input_data, **self.additional_params)
                elif hasattr(input_data, "read"):  # File-like object
                    return pd.read_csv(input_data, **self.additional_params)
                return pd.DataFrame(input_data)
            
            elif self.input_format == DataFormat.DATAFRAME:
                if isinstance(input_data, pd.DataFrame):
                    return input_data
                return pd.DataFrame(input_data)
            
            elif self.input_format == DataFormat.DICT:
                if isinstance(input_data, dict):
                    return input_data
                elif isinstance(input_data, str):
                    return json.loads(input_data)
                return dict(input_data)
            
            elif self.input_format == DataFormat.LIST:
                if isinstance(input_data, list):
                    return input_data
                elif isinstance(input_data, str):
                    return json.loads(input_data)
                return list(input_data)
            
            elif self.input_format == DataFormat.TEXT:
                if isinstance(input_data, str):
                    return input_data
                return str(input_data)
            
            elif self.input_format == DataFormat.NUMPY:
                if isinstance(input_data, np.ndarray):
                    return input_data
                return np.array(input_data)
            
            return input_data
        
        except Exception as e:
            logging.error(f"Error parsing input data: {str(e)}")
            if self.error_handling == "raise":
                raise
            return None
    
    def _apply_transformations(self, data: Any) -> Any:
        """
        Apply the specified transformations to the data.
        
        Args:
            data: The data to transform
            
        Returns:
            The transformed data
        """
        if data is None:
            return None
        
        result = data
        
        for transform in self.transformations:
            try:
                result = transform(result)
            except Exception as e:
                logging.error(f"Error applying transformation: {str(e)}")
                if self.error_handling == "raise":
                    raise
                elif self.error_handling == "return_none":
                    return None
                elif self.error_handling == "return_empty":
                    if isinstance(data, pd.DataFrame):
                        return pd.DataFrame()
                    elif isinstance(data, dict):
                        return {}
                    elif isinstance(data, list):
                        return []
                    elif isinstance(data, str):
                        return ""
                    elif isinstance(data, np.ndarray):
                        return np.array([])
                    return None
        
        return result
    
    def _convert_to_output_format(self, data: Any) -> Any:
        """
        Convert the data to the specified output format.
        
        Args:
            data: The data to convert
            
        Returns:
            The converted data
        """
        if data is None:
            return None
        
        try:
            if self.output_format == DataFormat.JSON:
                if isinstance(data, pd.DataFrame):
                    return data.to_json(orient="records")
                elif isinstance(data, np.ndarray):
                    return json.dumps(data.tolist())
                elif isinstance(data, (dict, list)):
                    return json.dumps(data)
                return json.dumps(data)
            
            elif self.output_format == DataFormat.CSV:
                if isinstance(data, pd.DataFrame):
                    return data.to_csv(index=False, **self.additional_params)
                elif isinstance(data, np.ndarray):
                    return pd.DataFrame(data).to_csv(index=False, **self.additional_params)
                elif isinstance(data, (dict, list)):
                    return pd.DataFrame(data).to_csv(index=False, **self.additional_params)
                return str(data)
            
            elif self.output_format == DataFormat.DATAFRAME:
                if isinstance(data, pd.DataFrame):
                    return data
                elif isinstance(data, np.ndarray):
                    return pd.DataFrame(data)
                elif isinstance(data, (dict, list)):
                    return pd.DataFrame(data)
                return pd.DataFrame([data])
            
            elif self.output_format == DataFormat.DICT:
                if isinstance(data, pd.DataFrame):
                    return data.to_dict(orient="records")
                elif isinstance(data, np.ndarray):
                    return {"data": data.tolist()}
                elif isinstance(data, dict):
                    return data
                elif isinstance(data, list):
                    return {"data": data}
                return {"data": data}
            
            elif self.output_format == DataFormat.LIST:
                if isinstance(data, pd.DataFrame):
                    return data.values.tolist()
                elif isinstance(data, np.ndarray):
                    return data.tolist()
                elif isinstance(data, dict):
                    return [data]
                elif isinstance(data, list):
                    return data
                return [data]
            
            elif self.output_format == DataFormat.TEXT:
                if isinstance(data, pd.DataFrame):
                    return data.to_string()
                elif isinstance(data, np.ndarray):
                    return str(data)
                elif isinstance(data, (dict, list)):
                    return json.dumps(data, indent=2)
                return str(data)
            
            elif self.output_format == DataFormat.NUMPY:
                if isinstance(data, pd.DataFrame):
                    return data.values
                elif isinstance(data, np.ndarray):
                    return data
                elif isinstance(data, (dict, list)):
                    return np.array(data)
                return np.array([data])
            
            return data
        
        except Exception as e:
            logging.error(f"Error converting to output format: {str(e)}")
            if self.error_handling == "raise":
                raise
            return None
    
    def _handle_error(self, error_message: str) -> None:
        """
        Handle an error based on the specified error handling strategy.
        
        Args:
            error_message: The error message
        """
        if self.error_handling == "raise":
            raise ValueError(error_message)
        elif self.error_handling == "return_none":
            self._set_output_data(None)
        elif self.error_handling == "return_empty":
            if self.output_format == DataFormat.DATAFRAME:
                self._set_output_data(pd.DataFrame())
            elif self.output_format == DataFormat.DICT:
                self._set_output_data({})
            elif self.output_format == DataFormat.LIST:
                self._set_output_data([])
            elif self.output_format == DataFormat.TEXT:
                self._set_output_data("")
            elif self.output_format == DataFormat.NUMPY:
                self._set_output_data(np.array([]))
            else:
                self._set_output_data(None)
        # For "log_and_continue", we've already logged the error, so do nothing


class FilterNode(DataProcessingNode):
    """
    A specialized data processing node for filtering data.
    
    This node extends the base DataProcessingNode to add support for
    filtering data based on specified conditions.
    """
    
    def __init__(
        self,
        name: str,
        shared_store: SharedStore,
        input_key: str,
        output_key: str,
        filter_condition: Callable[[Any], bool],
        input_format: Union[str, DataFormat] = DataFormat.JSON,
        output_format: Union[str, DataFormat] = DataFormat.JSON,
        **kwargs
    ) -> None:
        """
        Initialize a filter node.
        
        Args:
            name: The name of the node
            shared_store: The shared store for the agent
            input_key: The key in the shared store to use as input
            output_key: The key in the shared store to store the output
            filter_condition: A function that takes an item and returns True if it should be kept
            input_format: The format of the input data
            output_format: The format to convert the output data to
            **kwargs: Additional parameters for specific data formats
        """
        super().__init__(
            name,
            shared_store,
            input_key,
            output_key,
            input_format,
            output_format,
            **kwargs
        )
        self.filter_condition = filter_condition
    
    def _apply_transformations(self, data: Any) -> Any:
        """
        Apply the filter condition to the data.
        
        Args:
            data: The data to filter
            
        Returns:
            The filtered data
        """
        if data is None:
            return None
        
        try:
            if isinstance(data, pd.DataFrame):
                # For DataFrames, use the filter condition as a boolean mask
                mask = data.apply(self.filter_condition, axis=1)
                return data[mask]
            
            elif isinstance(data, list):
                # For lists, filter items that satisfy the condition
                return [item for item in data if self.filter_condition(item)]
            
            elif isinstance(data, dict):
                # For dictionaries, filter key-value pairs that satisfy the condition
                return {k: v for k, v in data.items() if self.filter_condition((k, v))}
            
            elif isinstance(data, np.ndarray):
                # For NumPy arrays, filter items that satisfy the condition
                mask = np.array([self.filter_condition(item) for item in data])
                return data[mask]
            
            # For other types, return the data if it satisfies the condition, None otherwise
            return data if self.filter_condition(data) else None
        
        except Exception as e:
            logging.error(f"Error applying filter: {str(e)}")
            if self.error_handling == "raise":
                raise
            return None


class AggregationNode(DataProcessingNode):
    """
    A specialized data processing node for aggregating data.
    
    This node extends the base DataProcessingNode to add support for
    aggregating data using specified aggregation functions.
    """
    
    def __init__(
        self,
        name: str,
        shared_store: SharedStore,
        input_key: str,
        output_key: str,
        aggregation_functions: Dict[str, Callable[[Any], Any]],
        group_by: Optional[Union[str, List[str]]] = None,
        input_format: Union[str, DataFormat] = DataFormat.DATAFRAME,
        output_format: Union[str, DataFormat] = DataFormat.DATAFRAME,
        **kwargs
    ) -> None:
        """
        Initialize an aggregation node.
        
        Args:
            name: The name of the node
            shared_store: The shared store for the agent
            input_key: The key in the shared store to use as input
            output_key: The key in the shared store to store the output
            aggregation_functions: A dictionary mapping column names to aggregation functions
            group_by: Optional column(s) to group by before aggregation
            input_format: The format of the input data
            output_format: The format to convert the output data to
            **kwargs: Additional parameters for specific data formats
        """
        super().__init__(
            name,
            shared_store,
            input_key,
            output_key,
            input_format,
            output_format,
            **kwargs
        )
        self.aggregation_functions = aggregation_functions
        self.group_by = group_by
    
    def _apply_transformations(self, data: Any) -> Any:
        """
        Apply the aggregation functions to the data.
        
        Args:
            data: The data to aggregate
            
        Returns:
            The aggregated data
        """
        if data is None:
            return None
        
        try:
            # Convert to DataFrame if not already
            if not isinstance(data, pd.DataFrame):
                data = pd.DataFrame(data)
            
            # Group by if specified
            if self.group_by:
                grouped = data.groupby(self.group_by)
                return grouped.agg(self.aggregation_functions).reset_index()
            
            # Otherwise, aggregate the entire DataFrame
            return pd.DataFrame({
                col: [func(data[col])]
                for col, func in self.aggregation_functions.items()
                if col in data.columns
            })
        
        except Exception as e:
            logging.error(f"Error applying aggregation: {str(e)}")
            if self.error_handling == "raise":
                raise
            return None
