#!/usr/bin/env bash
# claude-tmux-start.sh - Start Claude in a tmux session for autonomous restart

set -euo pipefail

SESSION_NAME="claude-mcp"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "🤖 Claude Tmux Session Manager"
echo "=============================="
echo ""

# Check if tmux is installed
if ! command -v tmux &> /dev/null; then
    echo "❌ tmux is not installed!"
    echo "   Install with: brew install tmux"
    exit 1
fi

# Check if reattach-to-user-namespace is installed (needed for clipboard support)
if ! command -v reattach-to-user-namespace &> /dev/null; then
    echo "⚠️  reattach-to-user-namespace is not installed!"
    echo "   This is needed for Command+V paste support in tmux"
    echo "   Install with: brew install reattach-to-user-namespace"
    echo ""
    echo "   Continuing without full clipboard support..."
    echo ""
fi

# Create/update tmux config for macOS-like experience
TMUX_CONFIG="$HOME/.tmux.conf"
if ! grep -q "# Claude MCP Settings" "$TMUX_CONFIG" 2>/dev/null; then
    echo "📝 Configuring tmux for macOS-like experience..."
    cat >> "$TMUX_CONFIG" << 'EOF'

# Claude MCP Settings
# Enable mouse support (scroll, select, resize panes)
set -g mouse on

# macOS clipboard integration
set -g set-clipboard on

# Use reattach-to-user-namespace for proper clipboard support on macOS
set-option -g default-command "reattach-to-user-namespace -l $SHELL"

# Enable native macOS clipboard operations
bind-key -T copy-mode-vi Enter send-keys -X copy-pipe-and-cancel "pbcopy"
bind-key -T copy-mode-vi MouseDragEnd1Pane send-keys -X copy-pipe-and-cancel "pbcopy"
bind-key -T copy-mode MouseDragEnd1Pane send-keys -X copy-pipe-and-cancel "pbcopy"

# Allow terminal app to handle Command+V for paste
set -g terminal-overrides 'xterm*:smcup@:rmcup@'

# Better scrolling
set -g history-limit 50000

# More intuitive split commands
bind | split-window -h
bind - split-window -v

# Start windows and panes at 1, not 0
set -g base-index 1
setw -g pane-base-index 1
EOF
    echo "✅ Tmux config updated!"
fi

# Check if session already exists
if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
    echo "✅ Session '$SESSION_NAME' already exists"
    echo "   Attaching to existing session..."
    echo ""
    echo "💡 Tip: To detach properly, use Ctrl+B, then D"
    echo "   If you exit with Ctrl+C, run this script again to reattach"
    echo ""
    
    # Reload config in case it was just updated
    tmux source-file "$TMUX_CONFIG" 2>/dev/null || true
    
    exec tmux attach-session -t "$SESSION_NAME"
else
    echo "📦 Creating new tmux session: $SESSION_NAME"
    
    # Create new tmux session with config and start Claude
    tmux new-session -d -s "$SESSION_NAME" -c "$PWD" \
        "echo '🚀 Starting Claude in tmux session...'; echo ''; echo '🖱️  Mouse scrolling enabled!'; echo '📋 Copy text by selecting with mouse'; echo ''; claude --dangerously-skip-permissions -c"
    
    # Source the config for the new session
    tmux source-file "$TMUX_CONFIG" 2>/dev/null || true
    
    echo "✅ Session created!"
    echo ""
    echo "📝 Tmux commands:"
    echo "   Scroll: Use mouse wheel or trackpad"
    echo "   Copy: Select text with mouse (auto-copies to clipboard)"
    echo "   Paste: Command+V (requires reattach-to-user-namespace)"
    echo "   Detach: Ctrl+B, then D (recommended)"
    echo "   List sessions: tmux ls"
    echo ""
    echo "⚠️  Important: If you exit with Ctrl+C, use this to reattach:"
    echo "   ./scripts/claude-tmux-attach.sh"
    echo ""
    echo "🔄 Claude can restart itself using:"
    echo "   ./scripts/claude-tmux-restart.sh"
    echo ""
    
    # Attach to the session
    exec tmux attach-session -t "$SESSION_NAME"
fi