# Tmux Session Persistence on macOS: Complete Guide

This guide covers all methods to make tmux sessions persist across reboots on macOS, with a focus on maintaining Claude Code sessions.

## Overview

By default, tmux sessions are stored in memory and are lost when you reboot. This guide presents multiple solutions to persist sessions, from simple plugins to custom automation.

## Method 1: tmux-resurrect + tmux-continuum (Recommended)

The most popular and reliable solution for persisting tmux sessions.

### Features
- Saves all sessions, windows, panes, and layouts
- Preserves working directories
- Can restore running programs (with limitations)
- Works seamlessly with Claude Code sessions

### Installation

1. **Install Tmux Plugin Manager (TPM)**:
```bash
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm
```

2. **Add to ~/.tmux.conf**:
```bash
# List of plugins
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-resurrect'
set -g @plugin 'tmux-plugins/tmux-continuum'

# Enable automatic restore
set -g @continuum-restore 'on'

# Save interval (default: 15 minutes)
set -g @continuum-save-interval '15'

# Optional: Restore vim/neovim sessions
set -g @resurrect-strategy-vim 'session'
set -g @resurrect-strategy-nvim 'session'

# Optional: Restore pane contents
set -g @resurrect-capture-pane-contents 'on'

# Initialize TMUX plugin manager (keep at bottom)
run '~/.tmux/plugins/tpm/tpm'
```

3. **Install plugins**:
   - In tmux, press `prefix + I` (default prefix is `Ctrl-b`)

### Usage
- **Manual save**: `prefix + Ctrl-s`
- **Manual restore**: `prefix + Ctrl-r`
- **Automatic**: Sessions save every 15 minutes and restore on tmux start

### macOS Boot Integration
```bash
# Add to ~/.tmux.conf for auto-start on boot
set -g @continuum-boot 'on'
set -g @continuum-boot-options 'iterm'  # or 'terminal' or 'alacritty'
```

## Method 2: LaunchAgent for Auto-Starting Tmux

Create a LaunchAgent to start tmux sessions on login.

### Create LaunchAgent

1. **Create file** `~/Library/LaunchAgents/com.user.tmux-claude.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.tmux-claude</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/tmux</string>
        <string>new-session</string>
        <string>-d</string>
        <string>-s</string>
        <string>claude-code</string>
        <string>-c</string>
        <string>/path/to/working/directory</string>
    </array>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>StandardOutPath</key>
    <string>/tmp/tmux-claude.log</string>
    
    <key>StandardErrorPath</key>
    <string>/tmp/tmux-claude.err</string>
    
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
        <key>HOME</key>
        <string>/Users/yourusername</string>
    </dict>
</dict>
</plist>
```

2. **Load the agent**:
```bash
launchctl load ~/Library/LaunchAgents/com.user.tmux-claude.plist
```

3. **Combine with resurrect** for full restoration after boot.

## Method 3: Shell Configuration Auto-Start

Add to your shell configuration file (`~/.zshrc` or `~/.bash_profile`):

```bash
# Auto-attach to tmux session named 'claude-code'
if [ -z "$TMUX" ]; then
    # Try to attach to existing session, or create new one
    tmux attach-session -t claude-code 2>/dev/null || \
    tmux new-session -s claude-code -c ~/Desktop/markov_github
fi
```

### More sophisticated version:
```bash
# Function to manage Claude Code tmux session
claude_tmux() {
    local session_name="claude-code"
    
    # Check if we're already in tmux
    if [ -n "$TMUX" ]; then
        return
    fi
    
    # Check if session exists
    if tmux has-session -t "$session_name" 2>/dev/null; then
        echo "Attaching to existing Claude Code session..."
        tmux attach-session -t "$session_name"
    else
        echo "Creating new Claude Code session..."
        tmux new-session -s "$session_name" -c ~/Desktop/markov_github/google-mcp
    fi
}

# Optional: auto-run on terminal start
# claude_tmux
```

## Method 4: Custom Session Scripts

Create scripts to save and restore specific session layouts:

### Save script (`~/bin/tmux-save-claude.sh`):
```bash
#!/bin/bash
tmux list-windows -t claude-code -F "#{window_index}:#{window_name}:#{pane_current_path}" > ~/.tmux-claude-session
tmux list-panes -s -t claude-code -F "#{session_name}:#{window_index}.#{pane_index}:#{pane_current_path}:#{pane_current_command}" >> ~/.tmux-claude-session
```

### Restore script (`~/bin/tmux-restore-claude.sh`):
```bash
#!/bin/bash
# Create session
tmux new-session -d -s claude-code -c ~/Desktop/markov_github/google-mcp

# Restore from saved state
while IFS=: read -r window_index window_name path; do
    if [ "$window_index" != "0" ]; then
        tmux new-window -t claude-code:$window_index -n "$window_name" -c "$path"
    fi
done < ~/.tmux-claude-session

# Attach to session
tmux attach-session -t claude-code
```

## Best Practices for Claude Code Sessions

1. **Use tmux-resurrect with continuum** for automatic persistence
2. **Configure restore programs** for Claude-specific tools:
```bash
set -g @resurrect-processes 'claude "~node->node" "~python->python"'
```

3. **Create dedicated session** for Claude Code:
```bash
tmux new-session -s claude-code -n main
```

4. **Set up status bar** to show save status:
```bash
set -g status-right 'Continuum: #{continuum_status}'
```

5. **Regular manual saves** before important changes:
   - Press `prefix + Ctrl-s` before system updates or reboots

## Troubleshooting

### Sessions not restoring automatically
- Ensure tmux-continuum is loaded after other plugins in `.tmux.conf`
- Check that status bar is enabled: `set -g status on`
- Verify saved sessions exist: `ls ~/.tmux/resurrect/`

### Programs not restoring
- Only safe programs restore by default
- Add specific programs to `@resurrect-processes`
- Use tilde (~) for flexible matching: `"~claude->claude"`

### macOS-specific issues
- Grant Terminal/iTerm full disk access in System Preferences
- Ensure correct paths in LaunchAgent
- Check logs: `tail -f /tmp/tmux-*.log`

## Recommended Setup for Claude Code

For the best experience maintaining Claude Code sessions:

1. Install tmux-resurrect and tmux-continuum
2. Configure automatic restore and 5-minute save interval
3. Create a LaunchAgent for boot-time session creation
4. Use the provided respawn scripts for seamless restarts

This combination ensures your Claude Code environment persists across reboots and provides quick recovery options.