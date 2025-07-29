from typing import Dict, List, Any, Optional, Tuple, TYPE_CHECKING
from collections import defaultdict
import copy
from .nodes import Node, START, END

if TYPE_CHECKING:
    from .graph import Graph


class ExecutionState:
    """Represents the state of graph execution at a given step."""
    
    def __init__(self, current_node: Node, data: Any, graph_snapshot: 'Graph'):
        self.current_node = current_node
        self.data = data
        self.graph_snapshot = graph_snapshot
        self.step_number = 0


class GraphExecutor:
    """Executes the graph by simplifying it at each step."""
    
    def __init__(self, graph: 'Graph'):
        self.original_graph = graph
        self.execution_history: List[ExecutionState] = []
        
    def execute(self) -> Any:
        """Execute the graph and return the final result."""
        # Start with a copy of the original graph
        current_graph = self._create_simplified_graph(self.original_graph)
        current_node = current_graph.start
        current_data = current_node.execute_with_validation(None)
        
        step = 0
        
        while not isinstance(current_node, END):
            # Save current state
            self.execution_history.append(
                ExecutionState(current_node, current_data, current_graph.clone())
            )
            
            # Handle map-reduce patterns
            map_reduce_config = self._find_map_reduce_config(current_graph, current_node)
            if map_reduce_config:
                current_data = self._execute_map_reduce(
                    current_graph, current_node, current_data, map_reduce_config
                )
                # Move to the reducer node
                _, _, reducer = map_reduce_config
                current_node = reducer
            else:
                # Get successors
                successors = current_graph.get_successors(current_node)
                
                if not successors:
                    raise RuntimeError(f"No path from {current_node} to END node")
                
                if len(successors) == 1:
                    # Simple linear execution
                    next_node = successors[0]
                    current_data = next_node.execute_with_validation(current_data)
                    current_node = next_node
                else:
                    # Handle parallel paths
                    parallel_results = self._execute_parallel_paths(
                        current_graph, current_node, current_data, successors
                    )
                    # Find the merge node (common successor)
                    merge_node = self._find_merge_node(current_graph, successors)
                    # Execute merge node with parallel results
                    current_data = merge_node.execute_with_validation(parallel_results)
                    current_node = merge_node
            
            # Simplify the graph for the next iteration
            if not isinstance(current_node, END):
                current_graph = self._simplify_graph(current_graph, current_node, current_data)
                current_node = current_graph.start
            step += 1
            
            # Safety check
            if step > 1000:
                raise RuntimeError("Graph execution exceeded maximum steps")
        
        # Execute END node
        result = current_node.execute_with_validation(current_data)
        
        # Save final state
        self.execution_history.append(
            ExecutionState(current_node, result, current_graph.clone())
        )
        
        return result
    
    def _create_simplified_graph(self, graph: 'Graph') -> 'Graph':
        """Create a simplified version of the graph."""
        return graph.clone()
    
    def _simplify_graph(self, graph: 'Graph', new_start_node: Node, new_start_data: Any) -> 'Graph':
        """Simplify the graph by making the current node the new START node."""
        # Create a new START node with the current data
        new_start = START()
        new_start.initial_data = {'data': new_start_data}
        
        # Create a new graph with the new START node
        simplified_graph = type(graph)(new_start)
        
        # Copy all nodes and edges starting from the new start node
        visited = set()
        to_visit = [new_start_node]
        
        while to_visit:
            current = to_visit.pop(0)
            if current in visited:
                continue
            visited.add(current)
            
            # Add successors
            for successor in graph.get_successors(current):
                if current == new_start_node:
                    # Connect new START to successors of current node
                    simplified_graph.add_edge(new_start, successor)
                else:
                    # Keep other edges as is
                    simplified_graph.add_edge(current, successor)
                
                if successor not in visited:
                    to_visit.append(successor)
        
        # Copy map-reduce configs that are still relevant
        for source, mapper, reducer in graph.map_reduce_configs:
            if source in visited or source == new_start_node:
                # Update source to new_start if it's the current node
                new_source = new_start if source == new_start_node else source
                simplified_graph.map_reduce_configs.append((new_source, mapper, reducer))
        
        return simplified_graph
    
    def _find_map_reduce_config(self, graph: 'Graph', node: Node) -> Optional[Tuple[Node, Node, Node]]:
        """Find if the current node is part of a map-reduce configuration."""
        for config in graph.map_reduce_configs:
            if config[0] == node:
                return config
        return None
    
    def _execute_map_reduce(self, graph: 'Graph', source_node: Node, 
                           input_data: Any, config: Tuple[Node, Node, Node]) -> Any:
        """Execute a map-reduce pattern."""
        _, mapper_node, reducer_node = config
        
        # Input data should be iterable
        if not hasattr(input_data, '__iter__'):
            raise ValueError(f"Map-reduce source node must return an iterable, got {type(input_data)}")
        
        # Execute mapper for each element
        mapped_results = []
        for item in input_data:
            result = mapper_node.execute_with_validation(item)
            mapped_results.append(result)
        
        # Execute reducer with all mapped results
        return reducer_node.execute_with_validation(mapped_results)
    
    def _execute_parallel_paths(self, graph: 'Graph', current_node: Node, 
                               input_data: Any, successors: List[Node]) -> Any:
        """Execute parallel paths and return results."""
        results = {}
        for successor in successors:
            results[successor] = successor.execute_with_validation(input_data)
        # Return the dict of results for the merge node to process
        return results
    
    def _find_merge_node(self, graph: 'Graph', parallel_nodes: List[Node]) -> Node:
        """Find the common successor (merge node) of parallel paths."""
        # Find all descendants of each parallel node
        descendants_sets = []
        for node in parallel_nodes:
            descendants = set()
            to_visit = [node]
            while to_visit:
                current = to_visit.pop(0)
                descendants.add(current)
                to_visit.extend(graph.get_successors(current))
            descendants_sets.append(descendants)
        
        # Find common descendants
        common_descendants = descendants_sets[0]
        for desc_set in descendants_sets[1:]:
            common_descendants = common_descendants.intersection(desc_set)
        
        # Find the closest common descendant (merge node)
        for node in parallel_nodes:
            for successor in graph.get_successors(node):
                if successor in common_descendants:
                    # This is the merge node, execute it with merged data
                    return successor
        
        raise RuntimeError("No merge node found for parallel paths") 