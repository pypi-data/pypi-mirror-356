from collections import defaultdict
from typing import Dict, List, Set, Tuple, Any, Optional, Union

from .execution import GraphExecutor
from .nodes import Node, START, GraphNode


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
        # Cache for GraphNode instances to ensure the same graph maps to the same node
        self._graph_node_cache: Dict["Graph", GraphNode] = {}

    def _ensure_node(
        self, node_or_graph: Union[Node, "Graph"], name: Optional[str] = None
    ) -> Node:
        """Convert a Graph to a GraphNode if necessary."""
        if isinstance(node_or_graph, Graph):
            # Check if we already have a GraphNode for this graph
            if node_or_graph not in self._graph_node_cache:
                self._graph_node_cache[node_or_graph] = GraphNode(node_or_graph, name)
            return self._graph_node_cache[node_or_graph]
        elif isinstance(node_or_graph, Node):
            return node_or_graph
        else:
            raise ValueError(f"Expected Node or Graph, got {type(node_or_graph)}")

    def add_edge(self, from_node: Union[Node, "Graph"], to_node: Union[Node, "Graph"]):
        """Add an edge between two nodes or graphs."""
        from_node = self._ensure_node(from_node)
        to_node = self._ensure_node(to_node)

        self.nodes.add(from_node)
        self.nodes.add(to_node)
        self.edges[from_node].append(to_node)
        self.reverse_edges[to_node].append(from_node)

    def add_map_reduce(
        self,
        source_node: Union[Node, "Graph"],
        mapper_node: Union[Node, "Graph"],
        reducer_node: Union[Node, "Graph"],
    ):
        """Add a map-reduce pattern between nodes or graphs."""
        source_node = self._ensure_node(source_node)
        mapper_node = self._ensure_node(mapper_node)
        reducer_node = self._ensure_node(reducer_node)

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

    def clone(self) -> "Graph":
        """Create a deep copy of the graph."""
        new_graph = Graph(self.start)
        new_graph.nodes = self.nodes.copy()
        new_graph.edges = {k: v[:] for k, v in self.edges.items()}
        new_graph.reverse_edges = {k: v[:] for k, v in self.reverse_edges.items()}
        new_graph.map_reduce_configs = self.map_reduce_configs[:]
        # Copy the cache as well
        new_graph._graph_node_cache = self._graph_node_cache.copy()
        return new_graph
