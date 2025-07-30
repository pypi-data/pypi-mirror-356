# MCP Server for Jira and Confluence

A Model Context Protocol (MCP) server that integrates with Atlassian's Jira and Confluence, enabling AI assistants to interact with these tools directly.

## Features

- **Jira Integration**
  - List recent issues
  - View issue details including comments
  - Get assigned issues with filtering options
  - Create new issues
  - Add comments to issues
  - Transition issues between statuses

- **Confluence Integration**
  - List recent pages
  - View page content
  - Create new pages
  - Update existing pages
  - Add comments to pages

- **AI-Powered Prompts**
  - Summarize Jira issues
  - Create structured Jira issue descriptions
  - Summarize Confluence pages
  - Generate structured Confluence content

## Installation

1. Clone the repository
2. Install dependencies using `uv`:

```bash
pip install uv
uv pip install -e .
```

## Configuration

### Environment Variables

Set the following environment variables to configure the server:

#### Jira Configuration
- `JIRA_URL`: Base URL of your Jira instance
- `JIRA_USERNAME`: Your Jira username
- `JIRA_API_TOKEN`: Your Jira API token or password
- `JIRA_PERSONAL_TOKEN`: Personal access token (alternative to username/API token)

#### Confluence Configuration
- `CONFLUENCE_URL`: Base URL of your Confluence instance
- `CONFLUENCE_USERNAME`: Your Confluence username
- `CONFLUENCE_API_TOKEN`: Your Confluence API token or password
- `CONFLUENCE_PERSONAL_TOKEN`: Personal access token (alternative to username/API token)

## Usage

### Starting the Server

Run the server directly:

```bash
python -m mcp_jira_confluence.server
```

### VSCode MCP Extension

If using with the VSCode MCP extension, the server is configured via `.vscode/mcp.json`:

```json
{
    "servers": [
        {
            "name": "mcp-jira-confluence",
            "command": "python",
            "module": "mcp_jira_confluence",
            "args": [
                "-m", "mcp_jira_confluence"
            ],
            "env": {
                "JIRA_URL": "${env:JIRA_URL}",
                "JIRA_USERNAME": "${env:JIRA_USERNAME}",
                "JIRA_API_TOKEN": "${env:JIRA_API_TOKEN}",
                "JIRA_PERSONAL_TOKEN": "${env:JIRA_PERSONAL_TOKEN}",
                "CONFLUENCE_URL": "${env:CONFLUENCE_URL}",
                "CONFLUENCE_USERNAME": "${env:CONFLUENCE_USERNAME}",
                "CONFLUENCE_API_TOKEN": "${env:CONFLUENCE_API_TOKEN}",
                "CONFLUENCE_PERSONAL_TOKEN": "${env:CONFLUENCE_PERSONAL_TOKEN}"
            },
            "logLevel": "info",
            "enabled": true
        }
    ]
}
```

This configuration:
- Defines the server name as `mcp-jira-confluence`
- Uses Python to run the server module
- Maps all required environment variables from your VS Code environment
- Sets logging level to `info`
- Automatically enables the server

### Claude Desktop

To use with Claude Desktop, add the following configuration:

On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

<details>
  <summary>Development/Unpublished Servers Configuration</summary>
  
```json
"mcpServers": {
  "mcp-jira-confluence": {
    "command": "uv",
    "args": [
      "--directory",
      "/Users/annmariyajoshy/vibecoding/mcp-jira-confluence",
      "run",
      "mcp-jira-confluence"
    ]
    }
  }
  ```
</details>

<details>
  <summary>Published Servers Configuration</summary>
  
```json
"mcpServers": {
  "mcp-jira-confluence": {
    "command": "uvx",
    "args": [
      "mcp-jira-confluence"
    ]
  }
}
```
</details>

## Resources

The server exposes the following types of resources:

- `jira://issue/{ISSUE_KEY}` - Jira issues
- `confluence://page/{PAGE_ID}` - Confluence pages
- `confluence://space/{SPACE_KEY}/page/{PAGE_ID}` - Confluence pages with space key

## Tools and Prompts

The server implements various tools and prompts for interacting with Jira and Confluence:

### Tools
- `create-jira-issue`: Create a new Jira issue
- `comment-jira-issue`: Add a comment to an issue
- `get-assigned-jira-issues`: Get Jira issues assigned to current user with filtering options
- `transition-jira-issue`: Change an issue's status
- `create-confluence-page`: Create a new Confluence page
- `update-confluence-page`: Update an existing page
- `comment-confluence-page`: Add a comment to a page
- `get-confluence-page`: Get a Confluence page by ID or title
- `search-confluence`: Search Confluence pages using CQL (Confluence Query Language)

### Prompts
- `summarize-jira-issue`: Create a summary of a Jira issue
- `create-jira-description`: Generate a structured issue description
- `summarize-confluence-page`: Create a summary of a Confluence page
- `create-confluence-content`: Generate structured Confluence content

## Example Queries

The MCP server responds to natural language queries. Here are some example queries you can use:

### Jira Queries

**Viewing Assigned Issues:**
- "Show my Jira tickets"
- "List my assigned issues"
- "Show my open Jira issues"
- "Get my high priority tickets"
- "Show my tasks in progress"
- "List all bugs assigned to me"
- "What issues are assigned to me?"
- "Find my Jira tickets with high priority"
- "Show my open bugs"

**Issue Management:**
- "Create a new bug report"
- "Add a comment to PROJ-123"
- "Move ticket ABC-456 to Done"
- "Show details of issue XYZ-789"
- "Update the status of PROJ-789"
- "Assign ticket DEV-101 to John"
- "Set priority of PROJ-456 to high"

### Confluence Queries

**Page Management:**
- "Create a new page in TEAM space"
- "Update the Release Notes page"
- "Add comment to the Architecture page"
- "Show content of Project Overview page"
- "Create documentation in DEV space"
- "Edit the meeting notes page"

**Search and Discovery:**
- "Find pages about architecture"
- "Search for release notes in DEV space"
- "Show recently modified pages"
- "Find pages created by John"
- "List pages in the TEAM space"
- "Search Confluence for API documentation"
- "Find pages tagged with 'security'"

Each query can be enhanced with additional parameters for filtering and sorting:
- Add status filters: "Show my open high priority issues"
- Add type filters: "List my bug reports in progress"
- Add date filters: "Show my issues updated this week"
- Add sorting: "Show my tickets sorted by priority"
- Add space filters: "Find pages in TEAM space about security"

## Development

### Building and Publishing

To prepare the package for distribution:

1. Sync dependencies and update lockfile:
```bash
uv sync
```

2. Build package distributions:
```bash
uv build
```

This will create source and wheel distributions in the `dist/` directory.

3. Publish to PyPI:
```bash
uv publish
```

Note: You'll need to set PyPI credentials via environment variables or command flags:
- Token: `--token` or `UV_PUBLISH_TOKEN`
- Or username/password: `--username`/`UV_PUBLISH_USERNAME` and `--password`/`UV_PUBLISH_PASSWORD`

### Debugging

Since MCP servers run over stdio, debugging can be challenging. For the best debugging
experience, we strongly recommend using the [MCP Inspector](https://github.com/modelcontextprotocol/inspector).


You can launch the MCP Inspector via [`npm`](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) with this command:

```bash
npx @modelcontextprotocol/inspector uv --directory /Users/annmariyajoshy/vibecoding/mcp-jira-confluence run mcp-jira-confluence
```


Upon launching, the Inspector will display a URL that you can access in your browser to begin debugging.