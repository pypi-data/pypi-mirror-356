import argparse
from .mcp_time import mcp


def main():
    parser = argparse.ArgumentParser(description="Bouse MCP Time Service")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse", "streamable-http"],
        default="stdio",
        help="Transport type (default: stdio)",
    )
    parser.add_argument("--host", default="127.0.0.1", help="Host address (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=9000, help="Port number (default: 9000)")
    parser.add_argument(
        "--path", default=None, help="Path for HTTP transport (default: /sse for sse, /mcp for streamable-http)"
    )

    args = parser.parse_args()

    # Set default path based on transport type
    if args.transport == "sse" and args.path is None:
        args.path = "/sse"
    elif args.transport == "streamable-http" and args.path is None:
        args.path = "/mcp"

    if args.transport == "stdio":
        # Use default STDIO transport
        mcp.run()
    else:
        # Use HTTP transport (SSE or streamable-http)
        mcp.run(transport=args.transport, host=args.host, port=args.port, path=args.path)


if __name__ == "__main__":
    main()
