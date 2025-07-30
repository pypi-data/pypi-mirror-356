"""Graph visualization module for displaying graph structures."""

import sys

sys.path.insert(0, "..")

import logging
import os
import tempfile
import webbrowser
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class GraphVisualizer:
    """Visualizes Graph objects using various backends."""

    def __init__(self, graph: "Graph"):
        """Initialize the visualizer with a graph instance."""
        self.graph = graph

    def to_dot(self) -> str:
        """Convert the graph to Graphviz DOT format."""
        lines = ["digraph G {"]
        lines.append("  rankdir=TB;")
        lines.append("  node [shape=box, style=rounded];")

        # Style for special nodes
        lines.append("  START [shape=ellipse, style=filled, fillcolor=lightgreen];")
        lines.append("  END [shape=ellipse, style=filled, fillcolor=lightcoral];")

        # Track GraphNode instances
        graph_nodes = set()

        # Add all nodes
        for node in self.graph.nodes:
            node_name = self._get_node_name(node)
            node_class = node.__class__.__name__

            if node_class == "GraphNode":
                graph_nodes.add(node)
                lines.append(
                    f'  "{node_name}" [shape=box3d, style=filled, fillcolor=lightblue, label="{node.name if hasattr(node, "name") else node_name}"];'
                )
            elif node_class not in ["START", "END"]:
                lines.append(f'  "{node_name}" [label="{node_class}"];')

        # Add regular edges
        for from_node, to_nodes in self.graph.edges.items():
            from_name = self._get_node_name(from_node)
            for to_node in to_nodes:
                to_name = self._get_node_name(to_node)
                lines.append(f'  "{from_name}" -> "{to_name}";')

        # Add map-reduce patterns with special styling
        for source, mapper, reducer in self.graph.map_reduce_configs:
            source_name = self._get_node_name(source)
            mapper_name = self._get_node_name(mapper)
            reducer_name = self._get_node_name(reducer)

            # Create a subgraph for map-reduce pattern
            lines.append(f"  subgraph cluster_mr_{id(source)} {{")
            lines.append(f"    style=dashed;")
            lines.append(f"    color=blue;")
            lines.append(f'    label="Map-Reduce";')
            lines.append(f'    "{mapper_name}" [style=filled, fillcolor=lightyellow];')
            lines.append(f"  }}")

            # Dotted lines for map-reduce connections
            lines.append(
                f'  "{source_name}" -> "{mapper_name}" [style=dashed, color=blue, label="map"];'
            )
            lines.append(
                f'  "{mapper_name}" -> "{reducer_name}" [style=dashed, color=blue, label="reduce"];'
            )

        lines.append("}")
        return "\n".join(lines)

    def to_mermaid(self) -> str:
        """Convert the graph to Mermaid format."""
        lines = ["graph TB"]

        # Track GraphNode instances
        graph_nodes = set()
        node_id_map = {}

        # Create safe node IDs
        for i, node in enumerate(self.graph.nodes):
            node_class = node.__class__.__name__
            if node_class == "START":
                node_id_map[node] = "START"
            elif node_class == "END":
                node_id_map[node] = "END"
            else:
                node_id_map[node] = f"N{i}"

        # Add node definitions
        for node in self.graph.nodes:
            node_id = node_id_map[node]
            node_class = node.__class__.__name__

            if node_class == "START":
                lines.append(f"    {node_id}([START])")
            elif node_class == "END":
                lines.append(f"    {node_id}([END])")
            elif node_class == "GraphNode":
                graph_nodes.add(node)
                # Use a simple label to avoid Mermaid syntax issues
                if hasattr(node, "name") and node.name:
                    label = (
                        str(node.name)
                        .replace('"', "")
                        .replace("'", "")
                        .replace("_", " ")
                    )
                else:
                    label = "SubGraph"
                lines.append(f"    {node_id}[{label}]")
            else:
                lines.append(f"    {node_id}[{node_class}]")

        # Add edges
        for from_node, to_nodes in self.graph.edges.items():
            from_id = node_id_map.get(from_node)
            if from_id:
                for to_node in to_nodes:
                    to_id = node_id_map.get(to_node)
                    if to_id:
                        lines.append(f"    {from_id} --> {to_id}")

        # Add map-reduce patterns
        for source, mapper, reducer in self.graph.map_reduce_configs:
            source_id = node_id_map.get(source)
            mapper_id = node_id_map.get(mapper)
            reducer_id = node_id_map.get(reducer)

            if source_id and mapper_id and reducer_id:
                lines.append(f"    {source_id} -.->|map| {mapper_id}")
                lines.append(f"    {mapper_id} -.->|reduce| {reducer_id}")

        # Add styling for graph nodes
        if graph_nodes:
            graph_node_ids = [
                node_id_map[node] for node in graph_nodes if node in node_id_map
            ]
            if graph_node_ids:
                for node_id in graph_node_ids:
                    lines.append(
                        f"    style {node_id} fill:#e1f5fe,stroke:#01579b,stroke-width:2px"
                    )

        return "\n".join(lines)

    def to_html(self, title: str = "Graph Visualization") -> str:
        """Generate an HTML page with the graph visualization."""
        mermaid_code = self.to_mermaid()

        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 2px solid #4CAF50;
            padding-bottom: 10px;
        }}
        .info {{
            background-color: #e8f5e9;
            padding: 10px;
            border-radius: 4px;
            margin-bottom: 20px;
        }}
        .mermaid {{
            text-align: center;
            background-color: white;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }}
        .legend {{
            margin-top: 20px;
            padding: 15px;
            background-color: #f5f5f5;
            border-radius: 4px;
        }}
        .legend h3 {{
            margin-top: 0;
            color: #666;
        }}
        .legend-item {{
            display: inline-block;
            margin-right: 20px;
            margin-bottom: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        
        <div class="info">
            <strong>Graph Statistics:</strong>
            <ul>
                <li>Total Nodes: {len(self.graph.nodes)}</li>
                <li>Total Edges: {sum(len(targets) for targets in self.graph.edges.values())}</li>
                <li>Map-Reduce Patterns: {len(self.graph.map_reduce_configs)}</li>
            </ul>
        </div>
        
        <div class="mermaid">
{mermaid_code}
        </div>
        
        <div class="legend">
            <h3>Legend</h3>
            <div class="legend-item">⬤ START node (green)</div>
            <div class="legend-item">⬤ END node (red)</div>
            <div class="legend-item">□ Regular node</div>
            <div class="legend-item">▭ Sub-graph node (blue)</div>
            <div class="legend-item">→ Regular edge</div>
            <div class="legend-item">⇢ Map-reduce connection</div>
        </div>
    </div>
    
    <script>
        mermaid.initialize({{ 
            startOnLoad: true,
            theme: 'default',
            flowchart: {{
                useMaxWidth: true,
                htmlLabels: true,
                curve: 'basis'
            }}
        }});
    </script>
</body>
</html>"""

        return html

    def visualize(
        self, output_path: Optional[Path] = None, open_browser: bool = True
    ) -> Path:
        """Generate visualization and optionally open in browser."""
        if output_path is None:
            # Create temporary file
            fd, output_path = tempfile.mkstemp(suffix=".html", prefix="graph_viz_")
            os.close(fd)
            output_path = Path(output_path)

        # Generate HTML
        html_content = self.to_html(title=f"Graph Visualization - {output_path.stem}")

        # Write to file
        output_path.write_text(html_content)
        logger.info(f"Visualization saved to: {output_path}")

        # Open in browser if requested
        if open_browser:
            webbrowser.open(f"file://{output_path.absolute()}")
            logger.info("Opening visualization in browser...")

        return output_path

    def _get_node_id(self, node) -> str:
        """Get a valid Mermaid node ID."""
        class_name = node.__class__.__name__
        if class_name in ["START", "END"]:
            return class_name
        return f"node_{id(node)}"

    def _get_node_name(self, node) -> str:
        """Get a human-readable node name."""
        class_name = node.__class__.__name__
        if class_name in ["START", "END"]:
            return class_name
        elif hasattr(node, "name"):
            return node.name
        else:
            return f"{class_name}_{id(node)}"


def visualize_from_file(
    file_path: Path, output_path: Optional[Path] = None, open_browser: bool = True
) -> Optional[Path]:
    """Extract and visualize graphs from a Python file."""
    import importlib.util
    import inspect
    import sys
    from .graph import Graph  # Import Graph here to use it in this function

    try:
        # Add the file's directory to Python path temporarily
        file_dir = file_path.parent.absolute()
        sys.path.insert(0, str(file_dir))

        # Also add the parent directory if it exists (for package imports)
        if file_dir.parent.exists():
            sys.path.insert(0, str(file_dir.parent))

        try:
            # Load the module
            module_name = file_path.stem
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec is None or spec.loader is None:
                logger.error(f"Could not load module from {file_path}")
                return None

            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module  # Register the module

            # Capture graphs created during execution
            created_graphs = []
            original_init = Graph.__init__

            def capture_init(self, *args, **kwargs):
                original_init(self, *args, **kwargs)
                created_graphs.append(self)

            # Temporarily replace Graph.__init__ to capture instances
            Graph.__init__ = capture_init

            try:
                spec.loader.exec_module(module)

                # Find Graph instances in module globals
                graphs = []
                for name, obj in inspect.getmembers(module):
                    if hasattr(obj, "__class__") and obj.__class__.__name__ == "Graph":
                        graphs.append((name, obj))

                # If no global graphs found, check if there's a main() function
                if not graphs and hasattr(module, "main"):
                    logger.info(
                        "No global Graph instances found, executing main() function..."
                    )
                    # Execute main() to create graphs
                    module.main()

                    # Use captured graphs
                    if created_graphs:
                        for i, graph in enumerate(created_graphs):
                            graphs.append((f"graph_{i}", graph))

                if not graphs:
                    logger.warning(f"No Graph instances found in {file_path}")
                    return None

                # Visualize the first graph found (or could be extended to handle multiple)
                graph_name, graph = graphs[0]
                logger.info(f"Visualizing graph '{graph_name}' from {file_path}")

                visualizer = GraphVisualizer(graph)
                return visualizer.visualize(output_path, open_browser)

            finally:
                # Restore original Graph.__init__
                Graph.__init__ = original_init

        finally:
            # Clean up sys.path
            if str(file_dir) in sys.path:
                sys.path.remove(str(file_dir))
            if str(file_dir.parent) in sys.path:
                sys.path.remove(str(file_dir.parent))
            # Clean up sys.modules
            if module_name in sys.modules:
                del sys.modules[module_name]

    except Exception as e:
        logger.error(f"Error visualizing file {file_path}: {e}")
        import traceback

        logger.debug(traceback.format_exc())
        return None
