# MCP Server SPARQL

A Model Context Protocol (MCP) server that provides tools for querying SPARQL endpoints.

## Usage

Example usage for querying a single SPARQL endpoint or multiple endpoints defined in a configuration file.

### uvx

```json
"mcpServers": {
  "mcp-server-sparql": {
    "command": "uvx",
    "args": ["mcp-server-sparql", "--endpoint", "https://query.wikidata.org/sparql"],
  }
}
```

To load multiple endpoints from a configuration file:

```json
"mcpServers": {
  "mcp-server-sparql": {
    "command": "uvx",
    "args": ["mcp-server-sparql", "--config", "config.json"],
  }
}
```

### Tool: `query`

Execute a SPARQL query against the configured endpoint.

**Parameters:**

- `query_string`: A valid SPARQL query string

**Returns:**

- The query results in JSON format

For configuring multiple endpoints see [docs/config.md](docs/config.md).
