"""
Core MCP tools for Neo4j operations.

This module provides the core tool implementations that can be used both
as standalone MCP tools and as library functions in other applications.
"""

import logging
from typing import Any, Dict, List, Optional, Union
import mcp.types as types
from .database import Neo4jDatabase, is_write_query

logger = logging.getLogger(__name__)


class Neo4jMCPTools:
  """Core MCP tools for Neo4j operations that can be used standalone or embedded."""

  def __init__(self, database: Neo4jDatabase):
    """Initialize with a Neo4j database connection."""
    self.db = database

  def get_tool_definitions(self) -> List[types.Tool]:
    """Get MCP tool definitions."""
    return [
      types.Tool(
        name="read-neo4j-cypher",
        description="Execute a Cypher query on the neo4j database",
        inputSchema={
          "type": "object",
          "properties": {
            "query": {
              "type": "string",
              "description": "Cypher read query to execute against the financial graph database. Common node types include Companies, FinancialReports, AccountingEntries, and AutomationProcesses.",
            },
          },
          "required": ["query"],
        },
      ),
      types.Tool(
        name="get-neo4j-schema",
        description="List all node types, their attributes and their relationships TO other node-types in the neo4j database",
        inputSchema={
          "type": "object",
          "properties": {},
        },
      ),
    ]

  def get_tool_definitions_as_dict(self) -> List[Dict[str, Any]]:
    """Get tool definitions as dictionaries (for HTTP APIs)."""
    tools = self.get_tool_definitions()
    return [
      {
        "name": tool.name,
        "description": tool.description,
        "inputSchema": tool.inputSchema,
      }
      for tool in tools
    ]

  async def execute_schema_tool(
    self,
  ) -> Union[List[types.TextContent], List[Dict[str, Any]]]:
    """Execute the schema tool."""
    try:
      results = self.db.execute_schema_query()
      return results
    except Exception as e:
      logger.error(f"Error executing schema tool: {e}")
      raise

  async def execute_cypher_tool(
    self, arguments: Dict[str, Any], return_raw: bool = False
  ) -> Union[List[types.TextContent], List[Dict[str, Any]]]:
    """Execute the cypher tool."""
    try:
      if arguments is None:
        raise ValueError("No arguments provided")

      if "query" not in arguments:
        raise ValueError("Query parameter is required")

      if is_write_query(arguments["query"]):
        raise ValueError("Only MATCH queries are allowed for read-query")

      results = self.db.execute_query(arguments["query"])

      if return_raw:
        return results
      else:
        return [types.TextContent(type="text", text=str(results))]

    except Exception as e:
      logger.error(f"Error executing cypher tool: {e}")
      if return_raw:
        raise
      else:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]

  async def call_tool(
    self,
    name: str,
    arguments: Optional[Dict[str, Any]] = None,
    return_raw: bool = False,
  ) -> Union[List[types.TextContent], List[Dict[str, Any]]]:
    """Call a tool by name."""
    if name == "get-neo4j-schema":
      return await self.execute_schema_tool()
    elif name == "read-neo4j-cypher":
      return await self.execute_cypher_tool(arguments or {}, return_raw)
    else:
      error_msg = f"Unknown tool: {name}"
      if return_raw:
        raise ValueError(error_msg)
      else:
        return [types.TextContent(type="text", text=f"Error: {error_msg}")]

  def close(self):
    """Close the database connection."""
    self.db.close()
