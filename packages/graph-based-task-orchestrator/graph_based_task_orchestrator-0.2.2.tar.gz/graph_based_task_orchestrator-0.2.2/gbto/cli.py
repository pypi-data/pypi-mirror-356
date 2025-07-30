#!/usr/bin/env python3
"""CLI tool for static validation of graph structures."""

import argparse
import logging
import sys
from pathlib import Path
from typing import List, Optional

from .enhanced_validator import EnhancedGraphValidator
from .static_validator import StaticGraphValidator
from .visualizer import visualize_from_file


def setup_logging(verbose: bool = False):
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")


def validate_files(
    file_paths: List[Path], enhanced: bool = False, verbose: bool = False
) -> int:
    """Validate multiple files and return exit code."""
    setup_logging(verbose)

    total_errors = 0
    total_warnings = 0

    for file_path in file_paths:
        print(f"\n{'=' * 60}")
        print(f"Validating: {file_path}")
        print(f"{'=' * 60}")

        if enhanced:
            validator = EnhancedGraphValidator()
        else:
            validator = StaticGraphValidator()

        is_valid, errors, warnings = validator.validate_file(file_path)

        if errors:
            print(f"\n❌ Errors ({len(errors)}):")
            for error in errors:
                print(f"  • {error}")
            total_errors += len(errors)

        if warnings:
            print(f"\n⚠️  Warnings ({len(warnings)}):")
            for warning in warnings:
                print(f"  • {warning}")
            total_warnings += len(warnings)

        if is_valid:
            print(f"\n✅ {file_path} is valid!")
        else:
            print(f"\n❌ {file_path} has validation errors!")

    print(f"\n{'=' * 60}")
    print(f"Summary: {total_errors} errors, {total_warnings} warnings")
    print(f"{'=' * 60}")

    return 0 if total_errors == 0 else 1


def validate_directory(
    directory: Path,
    pattern: str = "*.py",
    enhanced: bool = False,
    verbose: bool = False,
) -> int:
    """Validate all Python files in a directory."""
    files = list(directory.glob(pattern))
    if not files:
        print(f"No files matching pattern '{pattern}' found in {directory}")
        return 0

    return validate_files(files, enhanced, verbose)


def visualize_file(
    file_path: Path,
    output: Optional[Path] = None,
    no_browser: bool = False,
    format: str = "html",
) -> int:
    """Visualize graph from a Python file."""
    setup_logging(True)  # Enable logging for visualization

    print(f"\n{'=' * 60}")
    print(f"Visualizing: {file_path}")
    print(f"{'=' * 60}")

    if not file_path.exists():
        print(f"❌ Error: File '{file_path}' not found")
        return 1

    try:
        result = visualize_from_file(file_path, output, not no_browser)
        if result:
            print(f"\n✅ Visualization saved to: {result}")
            if not no_browser:
                print("📊 Opening in browser...")
            return 0
        else:
            print(f"\n❌ Failed to visualize graph from {file_path}")
            return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Static validator and visualizer for graph structures",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate a single file
  graph-validate validate examples/validation_example.py
  
  # Validate with enhanced type checking
  graph-validate validate --enhanced examples/validation_example.py
  
  # Validate all Python files in a directory
  graph-validate validate --directory examples/
  
  # Visualize a graph
  graph-validate visualize examples/linear_graph.py
  
  # Save visualization to specific file
  graph-validate visualize examples/map_reduce_graph.py -o my_graph.html
  
  # Generate visualization without opening browser
  graph-validate visualize examples/subgraph_example.py --no-browser
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Validate command
    validate_parser = subparsers.add_parser(
        "validate", help="Validate graph structures"
    )
    validate_parser.add_argument(
        "files", nargs="*", type=Path, help="Python files to validate"
    )
    validate_parser.add_argument(
        "-d", "--directory", type=Path, help="Validate all Python files in directory"
    )
    validate_parser.add_argument(
        "-p",
        "--pattern",
        default="*.py",
        help="File pattern for directory validation (default: *.py)",
    )
    validate_parser.add_argument(
        "-e",
        "--enhanced",
        action="store_true",
        help="Use enhanced validation with deep type checking",
    )
    validate_parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )

    # Visualize command
    visualize_parser = subparsers.add_parser(
        "visualize", help="Visualize graph structure"
    )
    visualize_parser.add_argument(
        "file", type=Path, help="Python file containing graph to visualize"
    )
    visualize_parser.add_argument(
        "-o", "--output", type=Path, help="Output file path (default: temporary file)"
    )
    visualize_parser.add_argument(
        "--no-browser", action="store_true", help="Do not open visualization in browser"
    )
    visualize_parser.add_argument(
        "-f",
        "--format",
        choices=["html", "dot", "mermaid"],
        default="html",
        help="Output format (default: html)",
    )

    # Analyze command (future feature)
    analyze_parser = subparsers.add_parser("analyze", help="Analyze graph structure")
    analyze_parser.add_argument("file", type=Path, help="Python file to analyze")
    analyze_parser.add_argument(
        "--show-types",
        action="store_true",
        help="Show input/output types for each node",
    )
    analyze_parser.add_argument(
        "--show-flow", action="store_true", help="Show data flow through the graph"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    if args.command == "validate":
        if args.directory:
            return validate_directory(
                args.directory, args.pattern, args.enhanced, args.verbose
            )
        elif args.files:
            return validate_files(args.files, args.enhanced, args.verbose)
        else:
            print("Error: Either provide files or use --directory option")
            return 1

    elif args.command == "visualize":
        return visualize_file(args.file, args.output, args.no_browser, args.format)

    elif args.command == "analyze":
        print("Analysis feature coming soon!")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
