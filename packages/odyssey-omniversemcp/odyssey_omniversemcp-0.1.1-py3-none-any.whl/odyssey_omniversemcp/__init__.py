#!/usr/bin/env python3
"""
Isaac Sim MCP Server Entry Point

This file serves as the main entry point for the Isaac Sim MCP server.
Simply run this file to start the MCP server.
"""

from isaac_mcp import mcp

def main():
    """Main entry point for the Isaac Sim MCP server"""
    print("Starting Isaac Sim MCP Server...")
    print("Make sure Isaac Sim with the MCP extension is running on localhost:8766")
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()