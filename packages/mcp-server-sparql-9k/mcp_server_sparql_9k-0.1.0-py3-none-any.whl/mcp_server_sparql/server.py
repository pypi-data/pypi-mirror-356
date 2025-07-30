import json
import argparse
from typing import Dict, Any, List, Union

from SPARQLWrapper import SPARQLWrapper, JSON, SPARQLExceptions
from mcp.server.fastmcp import FastMCP


class SPARQLServer:
    def __init__(self, endpoint_url: str):
        self.endpoint_url = endpoint_url
        self.sparql = SPARQLWrapper(endpoint_url)
        self.sparql.setReturnFormat(JSON)
    
    def query(self, query_string: str) -> Any:
        """Execute a SPARQL query and return the results"""
        try:
            self.sparql.setQuery(query_string)
            results = self.sparql.query().convert()
            return results
        except SPARQLExceptions.EndPointNotFound:
            return {"error": f"SPARQL endpoint not found: {self.endpoint_url}"}
        except Exception as e:
            return {"error": f"Query error: {str(e)}"}


def parse_args():
    parser = argparse.ArgumentParser(description="MCP SPARQL Query Server")
    parser.add_argument(
        "--endpoint",
        help="SPARQL endpoint URL (e.g., http://dbpedia.org/sparql)"
    )
    parser.add_argument(
        "--config",
        help="Path to JSON configuration file for multiple endpoints"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    mcp = FastMCP("SPARQL Query Server")

    def register_tool(ep_name: str, server: SPARQLServer, description: str) -> None:
        @mcp.tool(name=f"query_{ep_name}", description=description)
        def query(query_string: str) -> Any:
            return server.query(query_string)

    if args.config:
        with open(args.config, "r") as f:
            config = json.load(f)
        endpoints = config.get("endpoints", [])
        if not endpoints:
            raise ValueError("No endpoints found in config file")

        for ep in endpoints:
            name = ep["name"]
            url = ep["url"]
            instructions = ep.get("instructions", "")
            sparql_server = SPARQLServer(endpoint_url=url)

            query_doc = f"""Execute a SPARQL query against the endpoint {url}.
{instructions}

Args:
    query_string: A valid SPARQL query string

Returns:
    The query results in JSON format
"""

            register_tool(name, sparql_server, query_doc)
    elif args.endpoint:
        sparql_server = SPARQLServer(endpoint_url=args.endpoint)

        query_doc = f"""Execute a SPARQL query against the endpoint {sparql_server.endpoint_url}.

Args:
    query_string: A valid SPARQL query string

Returns:
    The query results in JSON format
"""

        register_tool("default", sparql_server, query_doc)
    else:
        raise ValueError("Provide --endpoint or --config")

    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
