# Configuring Multiple SPARQL Endpoints

`mcp-server-sparql` can be configured to expose multiple SPARQL endpoints at once. Tools will be generated dynamically for each endpoint defined in a JSON configuration file.

## Configuration File Structure

Create a JSON file with the following structure:

```json
{
  "endpoints": [
    {
      "name": "probe",
      "url": "https://probe.stad.gent/sparql",
      "instructions": "Use this endpoint for testing queries."
    },
    {
      "name": "production",
      "url": "https://stad.gent/sparql",
      "instructions": "Production dataset. Do not run heavy experimental queries."
    }
  ]
}
```

- `name` – unique identifier. The tool will be registered as `query_<name>`.
- `url` – SPARQL endpoint URL.
- `instructions` – text inserted in the tool description to guide the LLM about when to use this endpoint.

## Running the Server

Pass the configuration file path to the server:

```bash
uvx mcp-server-sparql --config config.json
```

Each endpoint will register a tool named `query_<name>` accepting a single `query_string` parameter.
