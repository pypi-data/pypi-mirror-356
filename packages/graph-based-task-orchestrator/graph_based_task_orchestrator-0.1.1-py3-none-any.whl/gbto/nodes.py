from abc import ABC, abstractmethod
from typing import Any, Optional, Type, get_type_hints, get_origin, get_args
from pydantic import BaseModel, ValidationError, create_model
import inspect
import logging

logger = logging.getLogger(__name__)


class Node(ABC):
    """Base class for all nodes in the graph."""
    
    def __init__(self):
        self.node_id = id(self)
        self._input_type = None
        self._output_type = None
        self._setup_validation()
    
    def _setup_validation(self):
        """Setup input/output validation based on type hints."""
        try:
            # Get type hints from the execute method of the actual class, not the base class
            hints = get_type_hints(self.__class__.execute)
            
            # Get input type (first parameter after self)
            sig = inspect.signature(self.__class__.execute)
            params = list(sig.parameters.values())
            if len(params) > 1:  # Skip 'self'
                input_param = params[1]
                if input_param.name in hints:
                    self._input_type = hints[input_param.name]
            
            # Get return type
            if 'return' in hints:
                self._output_type = hints['return']
                
            logger.debug(f"Setup validation for {self.__class__.__name__}: input={self._input_type}, output={self._output_type}")
                
        except Exception as e:
            logger.debug(f"Could not setup validation for {self.__class__.__name__}: {e}")
    
    def _validate_input(self, input_data: Any) -> Any:
        """Validate input data against type hints."""
        if self._input_type is None or self._input_type == Any:
            return input_data
            
        try:
            # Handle Pydantic models
            if isinstance(self._input_type, type) and issubclass(self._input_type, BaseModel):
                if isinstance(input_data, self._input_type):
                    return input_data
                elif isinstance(input_data, dict):
                    return self._input_type(**input_data)
                else:
                    # Try to create model with single field
                    try:
                        return self._input_type(value=input_data)
                    except:
                        # If that fails, try to parse the data as is
                        return self._input_type.model_validate(input_data)
            
            # Handle basic type validation
            if not self._is_valid_type(input_data, self._input_type):
                raise TypeError(
                    f"Input validation failed for {self.__class__.__name__}: "
                    f"expected {self._input_type}, got {type(input_data).__name__}"
                )
                
        except ValidationError as e:
            raise ValueError(
                f"Input validation failed for {self.__class__.__name__}: {e}"
            ) from e
        except Exception as e:
            raise ValueError(
                f"Input validation failed for {self.__class__.__name__}: {str(e)}"
            ) from e
            
        return input_data
    
    def _validate_output(self, output_data: Any) -> Any:
        """Validate output data against type hints."""
        if self._output_type is None or self._output_type == Any:
            return output_data
            
        try:
            # Handle Pydantic models
            if isinstance(self._output_type, type) and issubclass(self._output_type, BaseModel):
                if isinstance(output_data, self._output_type):
                    return output_data
                elif isinstance(output_data, dict):
                    return self._output_type(**output_data)
                else:
                    return self._output_type(value=output_data)
            
            # Handle basic type validation
            if not self._is_valid_type(output_data, self._output_type):
                raise TypeError(
                    f"Output validation failed for {self.__class__.__name__}: "
                    f"expected {self._output_type}, got {type(output_data).__name__}"
                )
                
        except ValidationError as e:
            raise ValueError(
                f"Output validation failed for {self.__class__.__name__}: {e}"
            ) from e
            
        return output_data
    
    def _is_valid_type(self, value: Any, expected_type: Type) -> bool:
        """Check if value matches expected type."""
        # Handle Optional types
        origin = get_origin(expected_type)
        if origin is not None:
            args = get_args(expected_type)
            if origin == type(None):  # Handle None type
                return value is None
            # Handle Union types (including Optional)
            if hasattr(origin, '__name__') and origin.__name__ == 'Union':
                return any(self._is_valid_type(value, arg) for arg in args)
            # Handle generic types like List, Dict, etc.
            if origin in (list, tuple, dict, set):
                if not isinstance(value, origin):
                    return False
                # For now, we'll do basic type checking
                return True
        
        # Direct type check
        return isinstance(value, expected_type)
    
    def execute_with_validation(self, input_data: Any) -> Any:
        """Execute with input/output validation."""
        try:
            # Validate input
            validated_input = self._validate_input(input_data)
            
            # Execute
            result = self.execute(validated_input)
            
            # Validate output
            validated_output = self._validate_output(result)
            
            return validated_output
        except Exception as e:
            # Log the error with context
            logger.error(f"Error in {self.__class__.__name__}.execute_with_validation: {e}")
            raise
    
    @abstractmethod
    def execute(self, input_data: Any) -> Any:
        """Execute the node's logic with the given input data."""
        pass
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.node_id})"


class START(Node):
    """Special node that provides initial data to the graph."""
    
    def __init__(self, **kwargs):
        # Don't call super().__init__() yet to avoid validation setup
        self.node_id = id(self)
        self.initial_data = kwargs
        self._input_type = None
        self._output_type = None
        # No validation setup for START node
    
    def execute(self, input_data: Any = None) -> Any:
        """Return the initial data."""
        # If there's only one key-value pair, return just the value
        if len(self.initial_data) == 1:
            return next(iter(self.initial_data.values()))
        return self.initial_data
    
    def execute_with_validation(self, input_data: Any) -> Any:
        """START node doesn't validate input, just returns initial data."""
        return self.execute(input_data)


class END(Node):
    """Special node that marks the end of the graph execution."""
    
    def __init__(self):
        super().__init__()
        self.result = None
    
    def execute(self, input_data: Any) -> Any:
        """Store and return the final result."""
        self.result = input_data
        return input_data 