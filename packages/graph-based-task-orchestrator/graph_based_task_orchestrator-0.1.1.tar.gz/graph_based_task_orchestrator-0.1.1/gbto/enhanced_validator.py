"""Enhanced validator with deep type inspection for graph structures."""

import ast
import sys
import importlib.util
import inspect
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any, Optional, Type, Union, get_type_hints, get_origin, get_args
from dataclasses import dataclass
from collections import defaultdict
import logging

from pydantic import BaseModel

from .static_validator import StaticGraphValidator, GraphInfo, NodeInfo, EdgeInfo, TypeChecker
from .nodes import Node, START, END


logger = logging.getLogger(__name__)


class ModuleLoader:
    """Load Python modules dynamically for type inspection."""
    
    @staticmethod
    def load_module_from_path(file_path: Path) -> Optional[Any]:
        """Load a Python module from file path."""
        try:
            spec = importlib.util.spec_from_file_location("temp_module", file_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                # Add module to sys.modules temporarily
                sys.modules["temp_module"] = module
                spec.loader.exec_module(module)
                return module
        except Exception as e:
            logger.error(f"Failed to load module from {file_path}: {e}")
            return None
        finally:
            # Clean up
            if "temp_module" in sys.modules:
                del sys.modules["temp_module"]
    
    @staticmethod
    def get_class_from_module(module: Any, class_name: str) -> Optional[Type]:
        """Get a class from a module by name."""
        try:
            return getattr(module, class_name, None)
        except Exception as e:
            logger.error(f"Failed to get class {class_name}: {e}")
            return None


class EnhancedTypeChecker(TypeChecker):
    """Enhanced type checker with deep inspection capabilities."""
    
    @staticmethod
    def extract_node_types(node_class: Type[Node]) -> Tuple[Optional[Type], Optional[Type]]:
        """Extract input and output types from a Node class."""
        try:
            # Get type hints from the execute method
            hints = get_type_hints(node_class.execute)
            
            # Get input type (first parameter after self)
            sig = inspect.signature(node_class.execute)
            params = list(sig.parameters.values())
            
            input_type = None
            if len(params) > 1:  # Skip 'self'
                input_param = params[1]
                if input_param.name in hints:
                    input_type = hints[input_param.name]
            
            # Get return type
            output_type = hints.get('return', None)
            
            return input_type, output_type
            
        except Exception as e:
            logger.debug(f"Could not extract types from {node_class.__name__}: {e}")
            return None, None
    
    @staticmethod
    def check_pydantic_compatibility(output_model: Type[BaseModel], input_model: Type[BaseModel]) -> Tuple[bool, Optional[str]]:
        """Check if two Pydantic models are compatible."""
        try:
            # Get fields from both models
            output_fields = output_model.__fields__
            input_fields = input_model.__fields__
            
            # Check if all required input fields can be satisfied by output fields
            for field_name, field_info in input_fields.items():
                if field_info.is_required() and field_name not in output_fields:
                    return False, f"Required field '{field_name}' not found in output"
                
                # Check type compatibility if field exists in both
                if field_name in output_fields:
                    output_type = output_fields[field_name].type_
                    input_type = field_info.type_
                    
                    compatible, error = EnhancedTypeChecker.check_type_compatibility(output_type, input_type)
                    if not compatible:
                        return False, f"Field '{field_name}': {error}"
            
            return True, None
            
        except Exception as e:
            logger.debug(f"Error checking Pydantic compatibility: {e}")
            return True, None  # Be permissive on errors
    
    @staticmethod
    def check_list_compatibility(output_type: Type, input_type: Type) -> Tuple[bool, Optional[str]]:
        """Check compatibility of List types."""
        output_origin = get_origin(output_type)
        input_origin = get_origin(input_type)
        
        if output_origin == list and input_origin == list:
            output_args = get_args(output_type)
            input_args = get_args(input_type)
            
            if output_args and input_args:
                return EnhancedTypeChecker.check_type_compatibility(output_args[0], input_args[0])
        
        return False, f"List type mismatch: {output_type} vs {input_type}"


class EnhancedGraphValidator(StaticGraphValidator):
    """Enhanced validator with deep type inspection."""
    
    def __init__(self):
        super().__init__()
        self.loaded_classes: Dict[str, Type[Node]] = {}
        
    def validate_file(self, file_path: Union[str, Path]) -> Tuple[bool, List[str], List[str]]:
        """Validate a Python file with enhanced type checking."""
        file_path = Path(file_path)
        
        # First do basic validation
        is_valid, errors, warnings = super().validate_file(file_path)
        
        # Then do enhanced validation if basic validation found graphs
        if hasattr(self, '_last_graphs'):
            for graph_info in self._last_graphs:
                self._enhanced_validate_graph(graph_info, file_path)
        
        return len(self.errors) == 0, self.errors, self.warnings
    
    def _validate_graph(self, graph_info: GraphInfo):
        """Override to store graphs for enhanced validation."""
        if not hasattr(self, '_last_graphs'):
            self._last_graphs = []
        self._last_graphs.append(graph_info)
        super()._validate_graph(graph_info)
    
    def _enhanced_validate_graph(self, graph_info: GraphInfo, file_path: Path):
        """Perform enhanced validation with type loading."""
        # Load the module
        module = ModuleLoader.load_module_from_path(file_path)
        if not module:
            self.warnings.append(f"Could not load module for enhanced validation: {file_path}")
            return
        
        # Load node classes
        self._load_node_classes(graph_info, module)
        
        # Perform enhanced type checking
        self._enhanced_type_checking(graph_info)
        
        # Check map-reduce type compatibility
        self._check_map_reduce_types(graph_info)
    
    def _load_node_classes(self, graph_info: GraphInfo, module: Any):
        """Load actual node classes from module."""
        for node_name, node_info in graph_info.nodes.items():
            if node_info.class_name in ["START", "END"]:
                continue
                
            node_class = ModuleLoader.get_class_from_module(module, node_info.class_name)
            if node_class:
                self.loaded_classes[node_name] = node_class
                
                # Extract actual types
                input_type, output_type = EnhancedTypeChecker.extract_node_types(node_class)
                node_info.input_type = input_type
                node_info.output_type = output_type
            else:
                # Try to find the class in imported modules
                self._try_load_from_imports(node_info, module)
    
    def _try_load_from_imports(self, node_info: NodeInfo, module: Any):
        """Try to load node class from imported modules."""
        # This is a simplified version - in practice, we'd need to parse imports
        # and resolve them properly
        pass
    
    def _enhanced_type_checking(self, graph_info: GraphInfo):
        """Perform enhanced type checking with loaded classes."""
        for edge in graph_info.edges:
            from_node = graph_info.nodes.get(edge.from_node)
            to_node = graph_info.nodes.get(edge.to_node)
            
            if not from_node or not to_node:
                continue
                
            # Skip START/END nodes
            if from_node.is_start or to_node.is_end:
                continue
            
            # Check with actual loaded types
            if from_node.output_type and to_node.input_type:
                compatible, error = self._check_enhanced_compatibility(
                    from_node.output_type, 
                    to_node.input_type,
                    from_node.name,
                    to_node.name
                )
                
                if not compatible:
                    self.errors.append(
                        f"Type incompatibility: {from_node.name} ({from_node.class_name}) -> "
                        f"{to_node.name} ({to_node.class_name}): {error}"
                    )
    
    def _check_enhanced_compatibility(self, output_type: Type, input_type: Type, 
                                    from_name: str, to_name: str) -> Tuple[bool, Optional[str]]:
        """Enhanced compatibility checking with better error messages."""
        # Handle Any types
        if output_type == Any or input_type == Any:
            return True, None
        
        # Direct match
        if output_type == input_type:
            return True, None
        
        # Check Pydantic models
        if (inspect.isclass(output_type) and issubclass(output_type, BaseModel) and
            inspect.isclass(input_type) and issubclass(input_type, BaseModel)):
            return EnhancedTypeChecker.check_pydantic_compatibility(output_type, input_type)
        
        # Check List types
        if get_origin(output_type) == list and get_origin(input_type) == list:
            return EnhancedTypeChecker.check_list_compatibility(output_type, input_type)
        
        # Standard type checking
        return EnhancedTypeChecker.check_type_compatibility(output_type, input_type)
    
    def _check_map_reduce_types(self, graph_info: GraphInfo):
        """Check type compatibility in map-reduce patterns."""
        for source_name, mapper_name, reducer_name in graph_info.map_reduce_configs:
            source = graph_info.nodes.get(source_name)
            mapper = graph_info.nodes.get(mapper_name)
            reducer = graph_info.nodes.get(reducer_name)
            
            if not all([source, mapper, reducer]):
                continue
            
            # Check mapper input compatibility
            if source.output_type and mapper.input_type:
                # For map-reduce, source output should be a list
                if get_origin(source.output_type) == list:
                    list_element_type = get_args(source.output_type)[0] if get_args(source.output_type) else Any
                    compatible, error = self._check_enhanced_compatibility(
                        list_element_type,
                        mapper.input_type,
                        source_name,
                        mapper_name
                    )
                    if not compatible:
                        self.errors.append(
                            f"Map-reduce type error: {source_name} list elements incompatible "
                            f"with {mapper_name} input: {error}"
                        )
            
            # Check reducer input compatibility
            if mapper.output_type and reducer.input_type:
                # Reducer should accept a list of mapper outputs
                if get_origin(reducer.input_type) == list:
                    list_element_type = get_args(reducer.input_type)[0] if get_args(reducer.input_type) else Any
                    compatible, error = self._check_enhanced_compatibility(
                        mapper.output_type,
                        list_element_type,
                        mapper_name,
                        reducer_name
                    )
                    if not compatible:
                        self.errors.append(
                            f"Map-reduce type error: {mapper_name} output incompatible "
                            f"with {reducer_name} list elements: {error}"
                        ) 