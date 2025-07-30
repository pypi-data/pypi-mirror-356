"""
Neo4j database operations for MCP tools.

This module provides the core database functionality that can be shared
between different MCP implementations.
"""

import logging
import re
from typing import Any, Dict, List, Optional, cast
from typing_extensions import LiteralString
from neo4j import GraphDatabase

logger = logging.getLogger(__name__)


def is_write_query(query: str) -> bool:
  """Check if a Cypher query contains write operations."""
  return (
    re.search(r"\b(MERGE|CREATE|SET|DELETE|REMOVE|ADD)\b", query, re.IGNORECASE)
    is not None
  )


class Neo4jDatabase:
  """Neo4j database connection and query execution."""

  def __init__(
    self, neo4j_uri: str, neo4j_username: str, neo4j_password: str, graph_database: str
  ):
    """Initialize connection to the neo4j database."""
    logger.debug(f"Initializing database connection to {neo4j_uri}")
    self.driver = GraphDatabase.driver(
      neo4j_uri, auth=(neo4j_username, neo4j_password), database=graph_database
    )
    self.driver.verify_connectivity()
    self.graph_database = graph_database

  def execute_query(
    self, query: str, params: Optional[Dict[str, Any]] = None
  ) -> List[Dict[str, Any]]:
    """Execute a Cypher query and return results as a list of dictionaries."""
    logger.debug(f"Executing query: {query}")
    try:
      result = self.driver.execute_query(
        cast(LiteralString, query),
        parameters=params or {},
        database=self.graph_database,
      )
      counters = vars(result.summary.counters)
      if is_write_query(query):
        logger.debug(f"Write query affected {counters}")
        return [counters]
      else:
        results = [dict(r) for r in result.records]
        logger.debug(f"Read query returned {len(results)} rows")
        return results
    except Exception as e:
      logger.error(f"Database error executing query: {e}\n{query}")
      raise

  def execute_schema_query(self) -> List[Dict[str, Any]]:
    """Execute the standard schema query."""
    schema_query = """
CALL apoc.meta.data() YIELD label, property, type, other, unique, index, elementType
WHERE elementType = 'node' AND NOT label STARTS WITH '_'
WITH label, 
    COLLECT(CASE 
        WHEN type <> 'RELATIONSHIP' 
        THEN [property, type + CASE WHEN unique THEN " unique" ELSE "" END + CASE WHEN index THEN " indexed" ELSE "" END] 
        ELSE NULL 
    END) AS attributesList,
    COLLECT(CASE 
        WHEN type = 'RELATIONSHIP' AND other IS NOT NULL 
        THEN [property, head(other)] 
        ELSE NULL 
    END) AS relationshipsList
WITH label, 
    [x IN attributesList WHERE x IS NOT NULL] AS filteredAttributes, 
    [x IN relationshipsList WHERE x IS NOT NULL] AS filteredRelationships
RETURN label, 
    apoc.map.fromPairs(filteredAttributes) AS attributes, 
    apoc.map.fromPairs(filteredRelationships) AS relationships
        """
    return self.execute_query(schema_query)

  def close(self) -> None:
    """Close the Neo4j Driver."""
    self.driver.close()


# Legacy alias for backward compatibility
neo4jDatabase = Neo4jDatabase
