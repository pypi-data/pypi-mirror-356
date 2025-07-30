from . import server
from .database import Neo4jDatabase, is_write_query
from .tools import Neo4jMCPTools
import asyncio
import argparse


def main():
  """Main entry point for the package."""
  asyncio.run(server.main())


# Export modular components for library usage
__all__ = ["main", "server", "Neo4jDatabase", "Neo4jMCPTools", "is_write_query"]
