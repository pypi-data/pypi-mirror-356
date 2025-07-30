#!/usr/bin/env bash
# claude-trigger-restart.sh - Trigger restart when running under wrapper

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Check if we're running under the wrapper
if [ -z "${CLAUDE_CONTROL_FILE:-}" ]; then
    echo "❌ Not running under claude-wrapper.sh"
    echo "   Start Claude with: ./scripts/claude-wrapper.sh"
    exit 1
fi

if [ ! -f "$CLAUDE_CONTROL_FILE" ]; then
    echo "❌ Control file not found: $CLAUDE_CONTROL_FILE"
    exit 1
fi

echo "🔄 Triggering Claude restart..."

# Add MCP server before restart
echo "📦 Adding mcp-google-workspace..."
claude mcp add mcp-google-workspace -- uv --directory "$PROJECT_DIR" run mcp-google-workspace \
    --gauth-file "$PROJECT_DIR/.gauth.json" \
    --accounts-file "$PROJECT_DIR/.accounts.json"

echo "✅ MCP server added!"

# Trigger restart
echo "RESTART" > "$CLAUDE_CONTROL_FILE"

echo "✅ Restart triggered!"
echo "   Claude will restart momentarily in this terminal..."

# This script will exit, Claude will exit, and the wrapper will restart it
exit 0