# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Autonomous Self-Restart Capability

Claude Code can autonomously restart itself to load MCP servers, test MCP changes, or apply configuration updates. This is particularly powerful for autonomous MCP development where Claude can write, build, and immediately test new MCP server versions.

### Primary Method: TMux Restart (Recommended)

**For testing MCP server changes:**
```bash
/Users/olivierdebeufderijcker/Desktop/markov_github/google-mcp/scripts/claude-tmux-restart.sh
```

This script:
1. Adds the MCP server to Claude's configuration
2. Uses `tmux respawn-pane` to restart Claude in the same terminal
3. Waits 15 seconds for Claude to fully initialize
4. Automatically types "Restart completed, continue" and presses Enter
5. Creates a hands-free restart loop for autonomous operation

Note: Use the full path `/Users/olivierdebeufderijcker/Desktop/markov_github/google-mcp/scripts/claude-tmux-restart.sh` when running this script to ensure it works from any directory.

### Alternative Methods

**Basic auto-restart (requires new terminal):**
```bash
./scripts/claude-auto-restart.sh
```

**Start Claude in tmux (first time setup):**
```bash
./scripts/claude-tmux-start.sh
```

### Autonomous MCP Development Workflow

This restart capability enables Claude to:
1. **Write MCP server code** - Create or modify MCP server implementations
2. **Build the package** - Run `uv build` to package the MCP server
3. **Add to configuration** - Use `claude mcp add` to register the server
4. **Restart and test** - Autonomously restart to load the new MCP version
5. **Verify functionality** - Test the MCP tools are working correctly
6. **Iterate** - Make changes and restart again as needed

Example autonomous development loop:
```bash
# Claude modifies MCP server code
uv build
/Users/olivierdebeufderijcker/Desktop/markov_github/google-mcp/scripts/claude-tmux-restart.sh
# After restart, Claude can test the new MCP tools
```

The restart maintains the same terminal session, preserves context, and requires zero manual intervention - enabling truly autonomous MCP development and testing cycles.

## Overview

This is the mcp-google-workspace MCP server (formerly mcp-gsuite) that provides integration with Google Workspace (Gmail and Google Calendar). It enables AI assistants to interact with Google services through the Model Context Protocol.

Note: This is a fork of the original mcp-gsuite with fixes for JSON Schema compatibility (updated to draft 2020-12) and deployment via PyPI instead of Smithery.

## Development Commands

```bash
# Install dependencies
uv sync

# Run the server locally
uv run mcp-google-workspace

# Run with custom configuration
uv run mcp-google-workspace --gauth-file /path/to/.gauth.json \
                            --accounts-file /path/to/.accounts.json \
                            --credentials-dir /path/to/credentials

# Build package
uv build  # or ./deploy.sh

# Deploy to PyPI
uv publish --config-file .pypirc

# Debug with MCP Inspector
npx @modelcontextprotocol/inspector uv --directory /path/to/google-mcp run mcp-google-workspace

# Monitor logs (macOS)
tail -n 20 -f ~/Library/Logs/Claude/mcp-server-mcp-google-workspace.log
```

## Architecture

The server follows a tool-based architecture:

1. **Entry Points**: `__init__.py` → `server.py` → tool handlers
2. **Authentication**: OAuth2 flow managed by `gauth.py`, stores tokens as `.oauth.{email}.json`
3. **Services**: `gmail.py` and `calendar.py` wrap Google API clients
4. **Tools**: Inherit from `ToolHandler` base class, implement specific operations
5. **Multi-account**: Each tool accepts a `user_id` parameter to select the account

Key architectural decisions:
- Tools are stateless - authentication happens per-request
- HTML email content is parsed with BeautifulSoup
- Attachments are downloaded to temp files
- All dates use ISO 8601 format in UTC

## Important Implementation Notes

When modifying Gmail tools:
- Email body extraction handles both plain text and HTML parts
- The `get_body()` function in `gmail.py` processes multipart messages
- Attachment handling creates temp files that must be cleaned up

When modifying Calendar tools:
- Events use RFC3339 datetime format
- Timezone handling is critical - use pytz for conversions
- Recurring events are not fully supported

Authentication flow:
- First use triggers browser OAuth consent
- Tokens auto-refresh using refresh_token
- Credentials stored in configurable directory

## Testing

Currently no automated tests exist. Test changes by:
1. Using MCP Inspector to verify tool responses
2. Testing with Claude Desktop integration
3. Monitoring server logs for errors

## Deployment Workflow

For deploying improvements to PyPI and testing with Claude Code:

### 1. Development & Testing Cycle
```bash
# Make code changes
# Test locally with uv run mcp-google-workspace

# Build package
uv build

# Test changes via restart
/Users/olivierdebeufderijcker/Desktop/markov_github/google-mcp/scripts/claude-tmux-restart.sh
# Test the new MCP tools in Claude Code
```

### 2. Deploy to PyPI
```bash
# Update version in pyproject.toml (e.g., 0.7.0 -> 0.7.1)
uv build

# Deploy using twine (preferred method)
uv run twine upload dist/mcp_google_workspace-<version>*

# Or use uv publish (experimental)
# uv publish
```

### 3. Update Claude Code Instance
```bash
# Add/Update the MCP server configuration
claude mcp add mcp-google-workspace 'uv run --directory /Users/olivierdebeufderijcker/Desktop/markov_github/google-mcp mcp-google-workspace --gauth-file /Users/olivierdebeufderijcker/Desktop/markov_github/google-mcp/.gauth.json --accounts-file /Users/olivierdebeufderijcker/Desktop/markov_github/google-mcp/.accounts.json'

# Restart Claude to load changes
/Users/olivierdebeufderijcker/Desktop/markov_github/google-mcp/scripts/claude-tmux-restart.sh
```

### 4. Final Testing
After restart, test the new functionality using actual MCP tool calls to verify:
- New tools are available
- Existing tools still work
- Performance improvements are working
- No regressions introduced

### Key Credentials
- PyPI credentials: Uses twine with system ~/.pypirc or project .pypirc
- Note: Package requires Python >=3.13 for deployment