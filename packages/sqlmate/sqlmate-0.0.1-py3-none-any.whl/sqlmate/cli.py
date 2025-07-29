"""Command line interface for SQLMate."""

import argparse
import sys
from .version import get_version, print_version


def create_parser():
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog="sqlmate",
        description="SQLMate - A simple SQL utility package"
    )
    
    parser.add_argument(
        "--version", "-v",
        action="store_true",
        help="Show version information"
    )
    
    return parser


def main():
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args()
    
    if args.version:
        print_version()
        return 0
    
    # If no arguments provided, show help
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())