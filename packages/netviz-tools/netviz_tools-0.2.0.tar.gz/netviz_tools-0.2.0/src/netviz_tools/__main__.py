import argparse
from netviz_tools import __version__

def main():
    """Entry point for NetViz Tools CLI."""
    parser = argparse.ArgumentParser(
        description="NetViz Tools command-line interface"
    )
    parser.add_argument(
        "--version", action="version", version=__version__,
        help="Show the version of NetViz Tools"
    )
    parser.add_argument(
        "--verbose", action="store_true",
        help="Enable verbose output"
    )

    subparsers = parser.add_subparsers(
        dest="command", required=True,
        help="Available sub-commands"
    )

    # build sub-command
    build_p = subparsers.add_parser(
        "build", help="Build a network visualization"
    )
    build_p.add_argument(
        "source", help="Path to input data (file or directory)"
    )
    build_p.add_argument(
        "-o", "--output", default="dist/",
        help="Output directory"
    )
    build_p.add_argument(
        "-f", "--format", choices=["png", "html"], default="png",
        help="Output format"
    )

    args = parser.parse_args()

    if args.verbose:
        print(f"[verbose] running `{args.command}` with {args}")

    # If --version, print the version and exit
    if args.command == "version":
        print(f"NetViz Tools version: {__version__}")
        return


    if args.command == "build":

        pass

if __name__ == "__main__":
    main()