"""Static validator for graph structures using AST analysis and type checking."""

import ast
import inspect
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any, Optional, Type, Union
from dataclasses import dataclass
from collections import defaultdict
import importlib.util
from pydantic import BaseModel
import logging

from .nodes import Node, START, END
from .graph import Graph


logger = logging.getLogger(__name__)


@dataclass
class NodeInfo:
    """Information about a node extracted from static analysis."""
    name: str
    class_name: str
    input_type: Optional[Type] = None
    output_type: Optional[Type] = None
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    is_start: bool = False
    is_end: bool = False
    is_valid: bool = True
    errors: Optional[List[str]] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []


@dataclass
class EdgeInfo:
    """Information about an edge between nodes."""
    from_node: str
    to_node: str
    edge_type: str = "normal"  # normal, map_reduce
    line_number: Optional[int] = None


@dataclass
class GraphInfo:
    """Information about a graph extracted from static analysis."""
    name: str
    start_node: Optional[str] = None
    nodes: Optional[Dict[str, NodeInfo]] = None
    edges: Optional[List[EdgeInfo]] = None
    map_reduce_configs: Optional[List[Tuple[str, str, str]]] = None
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    errors: Optional[List[str]] = None
    
    def __post_init__(self):
        if self.nodes is None:
            self.nodes = {}
        if self.edges is None:
            self.edges = []
        if self.map_reduce_configs is None:
            self.map_reduce_configs = []
        if self.errors is None:
            self.errors = []


class GraphVisitor(ast.NodeVisitor):
    """AST visitor to extract graph construction patterns."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.graphs: List[GraphInfo] = []
        self.current_graph: Optional[GraphInfo] = None
        self.node_assignments: Dict[str, NodeInfo] = {}
        self.imports: Dict[str, str] = {}
        
    def visit_Import(self, node: ast.Import):
        """Track imports."""
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name
            self.imports[name] = alias.name
        self.generic_visit(node)
        
    def visit_ImportFrom(self, node: ast.ImportFrom):
        """Track from imports."""
        module = node.module or ""
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name
            self.imports[name] = f"{module}.{alias.name}"
        self.generic_visit(node)
    
    def visit_Assign(self, node: ast.Assign):
        """Detect node and graph assignments."""
        if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            var_name = node.targets[0].id
            
            # Check for Graph instantiation
            if isinstance(node.value, ast.Call):
                if self._is_graph_instantiation(node.value):
                    self._handle_graph_creation(var_name, node.value, node.lineno)
                elif self._is_node_instantiation(node.value):
                    self._handle_node_creation(var_name, node.value, node.lineno)
        
        self.generic_visit(node)
    
    def visit_Call(self, node: ast.Call):
        """Detect method calls on graph objects."""
        if isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                obj_name = node.func.value.id
                method_name = node.func.attr
                
                # Check if this is a graph method call
                if self.current_graph and obj_name == self.current_graph.name:
                    if method_name == "add_edge":
                        self._handle_add_edge(node)
                    elif method_name == "add_map_reduce":
                        self._handle_add_map_reduce(node)
        
        self.generic_visit(node)
    
    def _is_graph_instantiation(self, call_node: ast.Call) -> bool:
        """Check if a call creates a Graph instance."""
        if isinstance(call_node.func, ast.Name):
            return call_node.func.id == "Graph"
        elif isinstance(call_node.func, ast.Attribute):
            return call_node.func.attr == "Graph"
        return False
    
    def _is_node_instantiation(self, call_node: ast.Call) -> bool:
        """Check if a call creates a Node instance."""
        if isinstance(call_node.func, ast.Name):
            class_name = call_node.func.id
            return class_name in ["START", "END"] or class_name.endswith("Node") or class_name in self.imports
        return False
    
    def _handle_graph_creation(self, var_name: str, call_node: ast.Call, line_no: int):
        """Handle Graph() instantiation."""
        graph_info = GraphInfo(
            name=var_name,
            file_path=self.file_path,
            line_number=line_no
        )
        
        # Extract start node from keyword arguments
        for keyword in call_node.keywords:
            if keyword.arg == "start":
                if isinstance(keyword.value, ast.Name):
                    graph_info.start_node = keyword.value.id
        
        self.graphs.append(graph_info)
        self.current_graph = graph_info
    
    def _handle_node_creation(self, var_name: str, call_node: ast.Call, line_no: int):
        """Handle node instantiation."""
        class_name = ""
        if isinstance(call_node.func, ast.Name):
            class_name = call_node.func.id
        
        node_info = NodeInfo(
            name=var_name,
            class_name=class_name,
            file_path=self.file_path,
            line_number=line_no,
            is_start=class_name == "START",
            is_end=class_name == "END"
        )
        
        self.node_assignments[var_name] = node_info
        
        # Add to current graph if exists
        if self.current_graph:
            self.current_graph.nodes[var_name] = node_info
    
    def _handle_add_edge(self, call_node: ast.Call):
        """Handle g.add_edge(from_node, to_node) calls."""
        if len(call_node.args) >= 2:
            from_node = self._get_node_name(call_node.args[0])
            to_node = self._get_node_name(call_node.args[1])
            
            if from_node and to_node and self.current_graph:
                edge = EdgeInfo(
                    from_node=from_node,
                    to_node=to_node,
                    line_number=call_node.lineno
                )
                self.current_graph.edges.append(edge)
    
    def _handle_add_map_reduce(self, call_node: ast.Call):
        """Handle g.add_map_reduce(source, mapper, reducer) calls."""
        if len(call_node.args) >= 3:
            source = self._get_node_name(call_node.args[0])
            mapper = self._get_node_name(call_node.args[1])
            reducer = self._get_node_name(call_node.args[2])
            
            if source and mapper and reducer and self.current_graph:
                self.current_graph.map_reduce_configs.append((source, mapper, reducer))
    
    def _get_node_name(self, node: ast.AST) -> Optional[str]:
        """Extract node variable name from AST node."""
        if isinstance(node, ast.Name):
            return node.id
        return None


class TypeChecker:
    """Check type compatibility between nodes."""
    
    @staticmethod
    def check_type_compatibility(output_type: Optional[Type], input_type: Optional[Type]) -> Tuple[bool, Optional[str]]:
        """Check if output type is compatible with input type."""
        # If either type is None or Any, consider it compatible
        if output_type is None or input_type is None:
            return True, None
        
        if output_type == Any or input_type == Any:
            return True, None
        
        # Direct type match
        if output_type == input_type:
            return True, None
        
        # Check if output_type is a subclass of input_type
        try:
            if inspect.isclass(output_type) and inspect.isclass(input_type):
                if issubclass(output_type, input_type):
                    return True, None
        except TypeError:
            pass
        
        # Check Pydantic model compatibility
        if TypeChecker._are_pydantic_models_compatible(output_type, input_type):
            return True, None
        
        return False, f"Type mismatch: {output_type} is not compatible with {input_type}"
    
    @staticmethod
    def _are_pydantic_models_compatible(output_type: Type, input_type: Type) -> bool:
        """Check if two Pydantic models are compatible."""
        try:
            if (inspect.isclass(output_type) and issubclass(output_type, BaseModel) and
                inspect.isclass(input_type) and issubclass(input_type, BaseModel)):
                # For now, we'll consider them compatible if they're both Pydantic models
                # More sophisticated checking could compare fields
                return True
        except:
            pass
        return False


class StaticGraphValidator:
    """Main validator for static graph analysis."""
    
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        
    def validate_file(self, file_path: Union[str, Path]) -> Tuple[bool, List[str], List[str]]:
        """Validate a Python file containing graph definitions."""
        file_path = Path(file_path)
        
        if not file_path.exists():
            self.errors.append(f"File not found: {file_path}")
            return False, self.errors, self.warnings
        
        try:
            # Parse the file
            with open(file_path, 'r') as f:
                tree = ast.parse(f.read(), filename=str(file_path))
            
            # Extract graph information
            visitor = GraphVisitor(str(file_path))
            visitor.visit(tree)
            
            # Validate each graph
            for graph_info in visitor.graphs:
                self._validate_graph(graph_info)
            
            # Check if any graphs were found
            if not visitor.graphs:
                self.warnings.append(f"No graph definitions found in {file_path}")
            
            return len(self.errors) == 0, self.errors, self.warnings
            
        except SyntaxError as e:
            self.errors.append(f"Syntax error in {file_path}: {e}")
            return False, self.errors, self.warnings
        except Exception as e:
            self.errors.append(f"Error analyzing {file_path}: {e}")
            return False, self.errors, self.warnings
    
    def _validate_graph(self, graph_info: GraphInfo):
        """Validate a single graph structure."""
        # Check for start node
        if not graph_info.start_node:
            self.errors.append(f"Graph '{graph_info.name}' has no start node")
            return
        
        # Validate structure
        self._check_connectivity(graph_info)
        self._check_for_cycles(graph_info)
        self._check_type_compatibility(graph_info)
        self._validate_map_reduce_patterns(graph_info)
    
    def _check_connectivity(self, graph_info: GraphInfo):
        """Check if all nodes are reachable from start."""
        # Build adjacency list
        adjacency = defaultdict(set)
        for edge in graph_info.edges:
            adjacency[edge.from_node].add(edge.to_node)
        
        # Add map-reduce edges
        for source, mapper, reducer in graph_info.map_reduce_configs:
            adjacency[source].add(reducer)
        
        # DFS from start node
        visited = set()
        stack = [graph_info.start_node]
        
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                stack.extend(adjacency[node])
        
        # Check for unreachable nodes
        all_nodes = set(graph_info.nodes.keys())
        unreachable = all_nodes - visited
        
        if unreachable:
            self.warnings.append(
                f"Graph '{graph_info.name}' has unreachable nodes: {', '.join(unreachable)}"
            )
    
    def _check_for_cycles(self, graph_info: GraphInfo):
        """Check for cycles in the graph."""
        # Build adjacency list
        adjacency = defaultdict(set)
        for edge in graph_info.edges:
            adjacency[edge.from_node].add(edge.to_node)
        
        # Add map-reduce edges
        for source, mapper, reducer in graph_info.map_reduce_configs:
            adjacency[source].add(reducer)
        
        # DFS to detect cycles
        WHITE, GRAY, BLACK = 0, 1, 2
        color = defaultdict(lambda: WHITE)
        
        def has_cycle(node: str) -> bool:
            color[node] = GRAY
            
            for neighbor in adjacency[node]:
                if color[neighbor] == GRAY:
                    return True
                if color[neighbor] == WHITE and has_cycle(neighbor):
                    return True
            
            color[node] = BLACK
            return False
        
        # Check from all nodes
        for node in graph_info.nodes:
            if color[node] == WHITE:
                if has_cycle(node):
                    self.errors.append(f"Graph '{graph_info.name}' contains a cycle")
                    break
    
    def _check_type_compatibility(self, graph_info: GraphInfo):
        """Check type compatibility between connected nodes."""
        # This is a simplified check - in a real implementation,
        # we would need to load the actual node classes and inspect their types
        for edge in graph_info.edges:
            from_node = graph_info.nodes.get(edge.from_node)
            to_node = graph_info.nodes.get(edge.to_node)
            
            if from_node and to_node:
                # Skip type checking for START/END nodes
                if from_node.is_start or to_node.is_end:
                    continue
                
                # Here we would check actual type compatibility
                # For now, we'll just add a placeholder
                if from_node.output_type and to_node.input_type:
                    compatible, error = TypeChecker.check_type_compatibility(
                        from_node.output_type, to_node.input_type
                    )
                    if not compatible:
                        self.errors.append(
                            f"Type incompatibility in edge {edge.from_node} -> {edge.to_node}: {error}"
                        )
    
    def _validate_map_reduce_patterns(self, graph_info: GraphInfo):
        """Validate map-reduce configurations."""
        for source, mapper, reducer in graph_info.map_reduce_configs:
            # Check that all nodes exist
            if source not in graph_info.nodes:
                self.errors.append(f"Map-reduce source node '{source}' not found")
            if mapper not in graph_info.nodes:
                self.errors.append(f"Map-reduce mapper node '{mapper}' not found")
            if reducer not in graph_info.nodes:
                self.errors.append(f"Map-reduce reducer node '{reducer}' not found") 