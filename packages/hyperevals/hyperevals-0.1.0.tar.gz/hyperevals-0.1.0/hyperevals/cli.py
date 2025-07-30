"""
Command-line interface for HyperEvals.
"""

import argparse
import sys
from typing import Optional, List

from . import __version__


def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the hyperevals CLI."""
    parser = create_parser()
    parsed_args = parser.parse_args(args)
    
    if parsed_args.version:
        print(f"hyperevals {__version__}")
        return 0
    
    # TODO: Implement main functionality
    print("HyperEvals CLI - Coming soon!")
    print("This will provide command-line access to hyperband-optimized LLM evaluation.")
    return 0


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        prog="hyperevals",
        description="Hyperband-optimized parallelized prompt and model parameter tuning for evaluating LLMs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  hyperevals run config.yaml     # Run evaluation with config file
  hyperevals --version           # Show version information
        """,
    )
    
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show version information and exit",
    )
    
    parser.add_argument(
        "config",
        nargs="?",
        help="Path to configuration file",
    )
    
    return parser


if __name__ == "__main__":
    sys.exit(main()) 