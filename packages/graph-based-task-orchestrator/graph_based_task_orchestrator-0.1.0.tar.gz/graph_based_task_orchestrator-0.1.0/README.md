# Graph-Based Task Orchestrator

A simple yet powerful task orchestration library for Python based on graph data structures.

## Features

- **Linear Graph Execution**: Create simple pipelines where each node passes data to the next
- **Parallel Paths**: Split execution into multiple parallel paths and merge results
- **Map-Reduce Pattern**: Dynamically create parallel execution paths for iterable data
- **Graph Simplification**: At each execution step, the graph is simplified by moving the START node forward
- **Execution History**: Full execution history for debugging, retrying, and replaying
- **Data Validation**: Type hints and Pydantic model validation for inputs and outputs

## Installation

Using pip:
```bash
pip install -e .
```

Using uv (recommended):
```bash
uv pip install -e .
```

This will install the package in editable mode and make the `graph-validate` command available globally.

## Quick Start

### 1. Linear Graph

```python
from graph_orchestrator import Graph, START, END, Node

class MultiplierByTwo(Node):
    def execute(self, input_data):
        return input_data * 2

# Create graph
start = START(s=10)
end = END()
g = Graph(start=start)

# Build pipeline
multiplier = MultiplierByTwo()
g.add_edge(start, multiplier)
g.add_edge(multiplier, end)

# Run
result = g.run()  # Returns 20
```

### 2. Parallel Paths

```python
# Create parallel paths that merge
g.add_edge(start, node1)
g.add_edge(node1, node2)  # Path 1
g.add_edge(node1, node3)  # Path 2
g.add_edge(node2, merger)
g.add_edge(node3, merger)
g.add_edge(merger, end)
```

### 3. Map-Reduce

```python
# Map-reduce pattern
g.add_edge(start, list_generator)
g.add_map_reduce(list_generator, mapper, reducer)
g.add_edge(reducer, end)
```

## Creating Custom Nodes

Simply inherit from the `Node` class and implement the `execute` method:

```python
from graph_orchestrator import Node

class MyCustomNode(Node):
    def execute(self, input_data):
        # Your logic here
        return processed_data
```

### With Type Validation

Use type hints and Pydantic models for automatic validation:

```python
from typing import List
from pydantic import BaseModel
from graph_orchestrator import Node

class InputModel(BaseModel):
    name: str
    age: int

class OutputModel(BaseModel):
    message: str
    
class ValidatedNode(Node):
    def execute(self, input_data: InputModel) -> OutputModel:
        return OutputModel(
            message=f"Hello {input_data.name}, you are {input_data.age} years old"
        )
```

## Static Validation

The library includes a powerful static validation tool that can analyze your graph structures before runtime, checking for:
- Type compatibility between connected nodes
- Graph cycles
- Unreachable nodes
- Pydantic model field compatibility
- Map-reduce pattern correctness

### Using the Validation Tool

#### Method 1: Using the installed command (after `uv pip install -e .`):
```bash
# Basic validation
graph-validate validate examples/validation_example.py

# Enhanced validation with deep type checking
graph-validate validate --enhanced examples/validation_example.py

# Validate directory
graph-validate validate --directory examples/

# Verbose output
graph-validate validate -v examples/map_reduce_graph.py
```

#### Method 2: Using the convenience script:
```bash
# Basic validation
./scripts/validate.sh basic examples/validation_example.py

# Enhanced validation
./scripts/validate.sh enhanced examples/

# Validate all examples
./scripts/validate.sh examples

# Run validation demo
./scripts/validate.sh demo
```

#### Method 3: Direct Python scripts:
```bash
# Simple validation script
python validate.py examples/validation_example.py

# With enhanced type checking
python validate.py examples/validation_example.py --enhanced

# Using the module directly
python -m graph_orchestrator.cli validate examples/validation_example.py
```

### Validation Features

1. **AST Analysis**: Parses Python files to extract graph construction patterns
2. **Type Checking**: Validates type compatibility between node connections
3. **Structural Validation**: Checks for cycles, unreachable nodes, and missing connections
4. **Pydantic Support**: Deep inspection of Pydantic model compatibility
5. **Map-Reduce Validation**: Ensures correct types in map-reduce patterns

### Example Validation Output

```
============================================================
File: examples/invalid_graph.py
============================================================

❌ Errors (2):
  • Type incompatibility: node_a (NodeA) -> node_b (NodeB): Type mismatch: OutputModel is not compatible with int
  • Graph 'cyclic_graph' contains a cycle

⚠️  Warnings (1):
  • Graph 'g' has unreachable nodes: orphan_node

❌ Validation failed!
```

## Examples

See the `examples/` directory for complete working examples:
- `linear_graph.py` - Simple linear pipeline
- `parallel_graph.py` - Parallel execution paths with merging
- `map_reduce_graph.py` - Map-reduce pattern
- `validation_example.py` - Data validation with Pydantic
- `debug_example.py` - Execution history and debugging

Run all examples:
```bash
python test_all_features.py
```

Run validation examples:
```bash
python validate_graphs.py
```

### Quick Validation Commands

Using Make (recommended for development):
```bash
make validate-examples        # Validate all examples
make validate FILE=myfile.py  # Validate specific file
make validate-demo           # Run validation demo
```

Using the shell script:
```bash
./scripts/validate.sh examples  # Validate all examples
./scripts/validate.sh help      # Show all available commands
```

Using the installed command:
```bash
graph-validate validate --help  # Show validation options
```
