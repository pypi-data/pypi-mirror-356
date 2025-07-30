from .server import serve_stdio
from .server import serve_streamable_http


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="PKULAW MCP server for law search"
    )
    parser.add_argument("--type", type=str, choices=["stdio", "streamable-http"], default="stdio", help="MCP server type")
    args = parser.parse_args()

    if args.type == "stdio":
        serve_stdio()
    else:
        serve_streamable_http()


if __name__ == "__main__":
    main()

