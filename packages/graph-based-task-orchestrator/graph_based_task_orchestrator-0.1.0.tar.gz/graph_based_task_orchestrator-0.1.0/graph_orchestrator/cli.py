#!/usr/bin/env python3
"""CLI tool for static validation of graph structures."""

import argparse
import sys
import logging
from pathlib import Path
from typing import List, Optional
import importlib.util
import inspect
from typing import get_type_hints

from .static_validator import StaticGraphValidator, GraphInfo, NodeInfo
from .enhanced_validator import EnhancedGraphValidator
from .nodes import Node


def setup_logging(verbose: bool = False):
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(levelname)s: %(message)s'
    )


def validate_files(file_paths: List[Path], enhanced: bool = False, verbose: bool = False) -> int:
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


def validate_directory(directory: Path, pattern: str = "*.py", enhanced: bool = False, verbose: bool = False) -> int:
    """Validate all Python files in a directory."""
    files = list(directory.glob(pattern))
    if not files:
        print(f"No files matching pattern '{pattern}' found in {directory}")
        return 0
    
    return validate_files(files, enhanced, verbose)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Static validator for graph structures",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate a single file
  python -m graph_orchestrator.cli validate examples/validation_example.py
  
  # Validate with enhanced type checking
  python -m graph_orchestrator.cli validate --enhanced examples/validation_example.py
  
  # Validate all Python files in a directory
  python -m graph_orchestrator.cli validate --directory examples/
  
  # Validate with verbose output
  python -m graph_orchestrator.cli validate -v examples/linear_graph.py
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate graph structures')
    validate_parser.add_argument(
        'files',
        nargs='*',
        type=Path,
        help='Python files to validate'
    )
    validate_parser.add_argument(
        '-d', '--directory',
        type=Path,
        help='Validate all Python files in directory'
    )
    validate_parser.add_argument(
        '-p', '--pattern',
        default='*.py',
        help='File pattern for directory validation (default: *.py)'
    )
    validate_parser.add_argument(
        '-e', '--enhanced',
        action='store_true',
        help='Use enhanced validation with deep type checking'
    )
    validate_parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    # Analyze command (future feature)
    analyze_parser = subparsers.add_parser('analyze', help='Analyze graph structure')
    analyze_parser.add_argument('file', type=Path, help='Python file to analyze')
    analyze_parser.add_argument(
        '--show-types',
        action='store_true',
        help='Show input/output types for each node'
    )
    analyze_parser.add_argument(
        '--show-flow',
        action='store_true',
        help='Show data flow through the graph'
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    if args.command == 'validate':
        if args.directory:
            return validate_directory(args.directory, args.pattern, args.enhanced, args.verbose)
        elif args.files:
            return validate_files(args.files, args.enhanced, args.verbose)
        else:
            print("Error: Either provide files or use --directory option")
            return 1
    
    elif args.command == 'analyze':
        print("Analysis feature coming soon!")
        return 0
    
    return 0


if __name__ == '__main__':
    sys.exit(main()) 