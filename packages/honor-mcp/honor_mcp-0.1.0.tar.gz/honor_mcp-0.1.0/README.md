# Honor MCP Server

An MCP (Model Context Protocol) server for interacting with the Honor Platform API.

## Installation

```bash
pip install honor-mcp
```

## Configuration

The server requires the `HONOR_MCP_API_KEY` environment variable to be set with your Honor Platform API key.

Optional environment variables:
- `HONOR_MCP_URL_BASE`: Base URL for the Honor Platform API (default: http://localhost:7075)
- `HONOR_MCP_USER_AGENT`: User agent string for API requests (default: honor-mcp/1.0)

## Usage with Claude Desktop

Add to your Claude Desktop config file (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "honor-mcp": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "honor-mcp",
        "honor-mcp"
      ],
      "env": {
        "HONOR_MCP_API_KEY": "your_api_key_here",
        "HONOR_MCP_URL_BASE": "https://api.honor.education"
      }
    }
  }
}
```

## Available Tools

- `get_courses()`: Get a list of courses created by the user
- `create_course(course_title, course_description, start_date, end_date, course_code)`: Create a new course in Honor Platform

## License

MIT