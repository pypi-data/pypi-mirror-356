from typing import Dict, List, Set, Tuple, Any, Optional
from collections import defaultdict
from .nodes import Node, START, END
from .execution import GraphExecutor


class Graph:
    """Main graph class for task orchestration."""
    
    def __init__(self, start: START):
        if not isinstance(start, START):
            raise ValueError("Graph must be initialized with a START node")
        
        self.start = start
        self.nodes: Set[Node] = {start}
        self.edges: Dict[Node, List[Node]] = defaultdict(list)
        self.reverse_edges: Dict[Node, List[Node]] = defaultdict(list)
        self.map_reduce_configs: List[Tuple[Node, Node, Node]] = []
        
    def add_edge(self, from_node: Node, to_node: Node):
        """Add an edge between two nodes."""
        self.nodes.add(from_node)
        self.nodes.add(to_node)
        self.edges[from_node].append(to_node)
        self.reverse_edges[to_node].append(from_node)
        
    def add_map_reduce(self, source_node: Node, mapper_node: Node, reducer_node: Node):
        """Add a map-reduce pattern between nodes."""
        self.nodes.add(source_node)
        self.nodes.add(mapper_node)
        self.nodes.add(reducer_node)
        self.map_reduce_configs.append((source_node, mapper_node, reducer_node))
        # Add implicit edge from source to reducer for graph traversal
        self.edges[source_node].append(reducer_node)
        self.reverse_edges[reducer_node].append(source_node)
        
    def get_successors(self, node: Node) -> List[Node]:
        """Get all successor nodes of a given node."""
        return self.edges.get(node, [])
    
    def get_predecessors(self, node: Node) -> List[Node]:
        """Get all predecessor nodes of a given node."""
        return self.reverse_edges.get(node, [])
    
    def run(self) -> Any:
        """Execute the graph and return the result."""
        executor = GraphExecutor(self)
        self._executor = executor  # Store for debugging
        return executor.execute()
    
    def clone(self) -> 'Graph':
        """Create a deep copy of the graph."""
        new_graph = Graph(self.start)
        new_graph.nodes = self.nodes.copy()
        new_graph.edges = {k: v[:] for k, v in self.edges.items()}
        new_graph.reverse_edges = {k: v[:] for k, v in self.reverse_edges.items()}
        new_graph.map_reduce_configs = self.map_reduce_configs[:]
        return new_graph 