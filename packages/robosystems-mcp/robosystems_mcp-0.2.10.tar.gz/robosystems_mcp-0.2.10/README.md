# RoboSystems MCP Server

A Model Context Protocol (MCP) server implementation that enables AI-powered interaction with financial data stored in a Neo4j graph database. Part of the Robo Financial Systems Ecosystem, this server provides read-only access to analyze company financial reporting processes, accounting system data (including QuickBooks integrations), and automated reporting workflows.

## Architecture

This MCP server integrates with the broader RoboSystems ecosystem:

- **RoboSystems App** ([robosystems.ai](https://robosystems.ai)): Web application for financial reporting
- **Neo4j Graph Database**: Stores financial relationships and reporting structures
- **RoboSystems Backend**: Core API for financial data processing

## Features

- **Read-only Cypher queries** against financial graph data
- **Schema exploration** to understand the financial data model
- **Secure authentication** with Neo4j credentials
- **Query validation** to prevent write operations

## Installation

### Prerequisites

- Python 3.12+
- Neo4j database access
- MCP client (Claude Desktop, VS Code extension, etc.)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/robosystems-mcp.git
cd robosystems-mcp
```

2. Set up the environment:
```bash
# Using just (recommended)
just venv

# Or manually
pip install uv
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

## Usage

### Development Mode

Run the MCP server in development mode:

```bash
just dev
# or
mcp dev robosystems_mcp/server.py
```

### Production Mode

Run with specific Neo4j connection parameters:

```bash
just run db-url="bolt://localhost:7687" username="neo4j" password="password" database="neo4j"
# or
uv run robosystems-mcp --db-url bolt://localhost:7687 --username neo4j --password password --database neo4j
```

### MCP Configuration

To use with Claude Desktop, add this configuration to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "robosystems": {
      "command": "uv",
      "args": [
        "run",
        "robosystems-mcp",
        "--db-url", "bolt://localhost:7687",
        "--username", "neo4j",
        "--password", "your-password",
        "--database", "neo4j"
      ],
      "cwd": "/path/to/robosystems-mcp"
    }
  }
}
```

## Available Tools

### 1. Financial Data Query Tool

**Tool name**: `mcp_robosystems_read_graph_cypher`

Execute Cypher read queries to explore financial data:

```cypher
// Example: Find all companies and their QuickBooks connections
MATCH (c:Company)-[:HAS_QUICKBOOKS]->(qb:QuickBooksAuth)
RETURN c.name as company, qb.realmId as quickbooks_id
```

**Input**:
- `query` (string): The Cypher query to execute

**Returns**: Array of objects representing query results

### 2. Financial Data Schema Tool

**Tool name**: `mcp_robosystems_get_graph_schema`

Retrieve the complete financial data model schema.

**Input**: None required

**Returns**: 
- Node types with attributes and relationships
- Property types for each attribute
- Relationship directions and types

## Graph Database Schema

The Neo4j database contains financial data structured as:

- **Companies**: Business entities with accounting systems
- **QuickBooks Integration**: Synchronized accounting data
- **SEC Filings**: Regulatory reporting relationships
- **Financial Transactions**: Accounting entries and movements
- **Process Automation**: RPA workflows for financial processes

## Development

### Running Tests

```bash
just test
# or
uv run pytest
```

### Code Quality

```bash
# Run linting
just lint

# Format code
just format

# Type checking
just typecheck
```

### Creating a Release

```bash
just create-release patch  # or minor/major
```

## Project Structure

```
robosystems-mcp/
├── robosystems_mcp/          # Main package
│   ├── __init__.py
│   └── server.py           # MCP server implementation
├── tests/                  # Test suite
│   ├── test_neo4j.py      # Database tests
│   └── test_query_validation.py
├── pyproject.toml         # Project configuration
├── justfile              # Development commands
└── CLAUDE.md             # Claude Code guidance
```

## Security Considerations

- **Read-only access**: Only SELECT queries are allowed
- **Query validation**: Prevents CREATE, MERGE, DELETE operations
- **Credential management**: Uses environment variables or secure parameter passing
- **Connection encryption**: SSL/TLS for Neo4j connections

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

[To be determined]

## Support

For issues or questions:
- Create an issue on GitHub
- Contact the RoboSystems team

## Ecosystem Links

- [RoboSystems App](https://robosystems.ai)