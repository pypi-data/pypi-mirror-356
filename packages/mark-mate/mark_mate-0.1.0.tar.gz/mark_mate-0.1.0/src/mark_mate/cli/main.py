#!/usr/bin/env python3
"""
MarkMate CLI Main Entry Point

Command-line interface for MarkMate: Your AI Teaching Assistant for Assignments and Assessment
"""

import argparse
import sys
from typing import List, Optional

from . import consolidate, extract, scan, grade


def create_parser() -> argparse.ArgumentParser:
    """Create the main argument parser with subcommands."""
    parser = argparse.ArgumentParser(
        prog="mark-mate",
        description="MarkMate: Your AI Teaching Assistant for Assignments and Assessment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  mark-mate consolidate submissions/
  mark-mate scan processed_submissions/ --output github_urls.txt
  mark-mate extract processed_submissions/ --output results.json
  mark-mate grade results.json rubric.txt --output grades.json

For more help on a specific command:
  mark-mate <command> --help
        """
    )
    
    parser.add_argument(
        "--version", 
        action="version", 
        version="MarkMate 0.1.0"
    )
    
    subparsers = parser.add_subparsers(
        dest="command",
        help="Available commands",
        metavar="COMMAND"
    )
    
    # Add subcommand parsers
    consolidate.add_parser(subparsers)
    scan.add_parser(subparsers)
    extract.add_parser(subparsers)
    grade.add_parser(subparsers)
    
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args(argv)
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        # Route to appropriate command handler
        if args.command == "consolidate":
            return consolidate.main(args)
        elif args.command == "scan":
            return scan.main(args)
        elif args.command == "extract":
            return extract.main(args)
        elif args.command == "grade":
            return grade.main(args)
        else:
            print(f"Unknown command: {args.command}", file=sys.stderr)
            return 1
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())