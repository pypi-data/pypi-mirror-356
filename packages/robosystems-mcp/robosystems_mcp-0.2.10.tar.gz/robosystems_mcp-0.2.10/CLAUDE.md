# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

RoboSystems MCP Server is a Model Context Protocol (MCP) server that enables AI-powered interaction with financial data stored in a Neo4j graph database. It's part of the Robo Financial Systems Ecosystem for analyzing company financial reporting processes and accounting system data.

This MCP server provides direct access to the Neo4j graph database used by the RoboSystems application (robosystems.ai), enabling Claude and other AI tools to query financial relationships, reporting structures, and business process automations through Cypher queries.

## Common Development Commands

```bash
# Setup environment
just venv

# Install dependencies  
just install

# Run development server
just dev

# Run with custom Neo4j config
just run db-url="bolt://localhost:7687" username="neo4j" password="password" database="neo4j"

# Run tests
just test

# Run tests with coverage
just test-cov

# Lint and format check
just lint

# Format code
just format

# Type checking
just typecheck

# Create release (patch/minor/major)
just create-release patch

# Clean development artifacts
just clean
```

## Architecture

### Core Components

1. **Server Implementation** (`robosystems_mcp/server.py`)
   - Uses async MCP server with stdio for I/O
   - `neo4jDatabase` class manages Neo4j connections
   - Query validation to prevent write operations
   - Two main tools exposed:
     - `read-neo4j-cypher`: Execute read-only Cypher queries
     - `get-neo4j-schema`: Retrieve database schema

2. **Query Validation**
   - `is_write_query()` function checks for write operations
   - Prevents CREATE, MERGE, SET, DELETE, REMOVE, ADD operations
   - Only allows read queries for data safety

### Testing Structure

- Tests use pytest with async support via pytest-asyncio
- Mock Neo4j driver for unit tests
- Two main test modules:
  - `test_neo4j.py`: Database connection and query execution
  - `test_query_validation.py`: Query validation logic

### Configuration

- Python >=3.12 required
- Core dependencies: mcp>=1.6.0, neo4j>=5.26.0
- Development uses ruff for linting/formatting (88 char lines, 2-space indent)
- uv for dependency management (lock file is gitignored for library flexibility)

## Neo4j Integration

The server connects to Neo4j using the bolt protocol with configurable:
- Database URL (default: bolt://localhost:7687)
- Username/password authentication
- Database name selection

### Graph Database Schema

The Neo4j database contains financial data structured as:
- Companies with accounting systems and reporting relationships
- QuickBooks integration data
- SEC filing relationships
- Financial transactions and accounts
- Process automation workflows

## MCP Protocol Implementation

- Server exposes tools via MCP protocol
- Uses notification options for server lifecycle
- Handles initialization with graph database credentials
- Returns structured data for both query results and schema

## Development Notes

- Run `just lint` before committing code
- uv.lock is gitignored as this is a library project
- Tests mock Neo4j connections to avoid requiring a live database
- Release script creates release branches and bumps versions automatically
- Entry points: CLI via `robosystems-mcp` command or `python -m robosystems_mcp`
- All exceptions in tools are caught and returned as TextContent to prevent server crashes

## Integration with RoboSystems Ecosystem

This MCP server is designed to work with the broader RoboSystems ecosystem:

1. **RoboSystems App** (robosystems.ai):
   - Next.js 14+ frontend application
   - Integrates with QuickBooks and SEC filings
   - Uses both PostgreSQL (via Prisma) and Neo4j databases

2. **RoboSystems Backend Service**:
   - Core API providing financial data processing
   - Handles complex financial calculations and reporting

3. **Data Flow**:
   - Financial data flows from QuickBooks/SEC → RoboSystems App → Neo4j
   - This MCP server provides read-only access to the graph database
   - Enables AI-powered analysis and insights on financial relationships