#!/bin/bash

# Flake8 Performance Patterns - Tmux Workspace Setup
# Usage: ./setup_workspace.sh [project_path] [session_name]

# Configuration
PROJECT_DIR="${1:-$(pwd)/flake8-performance-patterns}"
SESSION_NAME="${2:-flake8-perf}"

# Check if session already exists
if tmux has-session -t $SESSION_NAME 2>/dev/null; then
  echo "Session '$SESSION_NAME' already exists. Attaching..."
  tmux attach-session -t $SESSION_NAME
  exit 0
fi

# Create session and first window
echo "Creating tmux session: $SESSION_NAME"
echo "Project directory: $PROJECT_DIR"

# Create session with first window
tmux new-session -d -s $SESSION_NAME -c "$PROJECT_DIR"

# Window 1: Main Development (dev)
tmux rename-window -t $SESSION_NAME:1 "dev"

# Split vertically (vim top 70%, terminal bottom 30%)
tmux split-window -t $SESSION_NAME:dev -v -p 30 -c "$PROJECT_DIR"

# Start vim in top pane with main plugin file
tmux send-keys -t $SESSION_NAME:dev.0 "vim src/flake8_performance_patterns/__init__.py" Enter

# Bottom pane ready for commands
tmux send-keys -t $SESSION_NAME:dev.1 "# Ready for commands: pytest, flake8, fzf" Enter

# Window 2: Testing & Validation (test)
tmux new-window -t $SESSION_NAME -n "test" -c "$PROJECT_DIR"

# Split horizontally (test files left 50%, test output right 50%)
tmux split-window -t $SESSION_NAME:test -h -p 50 -c "$PROJECT_DIR"

# Left pane: vim in tests directory
tmux send-keys -t $SESSION_NAME:test.0 "vim tests/" Enter

# Right pane: show available test commands
tmux send-keys -t $SESSION_NAME:test.1 "echo 'Test Commands:'" Enter
tmux send-keys -t $SESSION_NAME:test.1 "echo '  pytest -v                    # Run all tests'" Enter
tmux send-keys -t $SESSION_NAME:test.1 "echo '  pytest --cov                 # Run with coverage'" Enter
tmux send-keys -t $SESSION_NAME:test.1 "echo '  flake8 examples/              # Test plugin on examples'" Enter
tmux send-keys -t $SESSION_NAME:test.1 "echo '  python -m pytest tests/      # Explicit test run'" Enter
tmux send-keys -t $SESSION_NAME:test.1 "echo ''" Enter

# Window 3: AI Research & Documentation (ai)
tmux new-window -t $SESSION_NAME -n "ai" -c "$PROJECT_DIR"

# Split horizontally (AI CLI left 60%, docs right 40%)
tmux split-window -t $SESSION_NAME:ai -h -p 40 -c "$PROJECT_DIR"

# Left pane: ready for AI CLI
tmux send-keys -t $SESSION_NAME:ai.0 "echo 'AI CLI Ready:'" Enter
tmux send-keys -t $SESSION_NAME:ai.0 "echo '  claude-cli                    # Code review, architecture'" Enter
tmux send-keys -t $SESSION_NAME:ai.0 "echo '  gemini-cli                    # Pattern research'" Enter
tmux send-keys -t $SESSION_NAME:ai.0 "echo '  # Suggested commit message:'" Enter
tmux send-keys -t $SESSION_NAME:ai.0 "echo '  claude-cli \"suggest commit message for staged changes\"'" Enter
tmux send-keys -t $SESSION_NAME:ai.0 "echo ''" Enter

# Right pane: vim with README
tmux send-keys -t $SESSION_NAME:ai.1 "vim README.md" Enter

# Window 4: Git & Project Management (git)
tmux new-window -t $SESSION_NAME -n "git" -c "$PROJECT_DIR"

# Split horizontally (LazyGit left 75%, project mgmt right 25%)
tmux split-window -t $SESSION_NAME:git -h -p 25 -c "$PROJECT_DIR"

# Left pane: Auto-start LazyGit
tmux send-keys -t $SESSION_NAME:git.0 "lazygit" Enter

# Right pane: Project structure and management commands
tmux send-keys -t $SESSION_NAME:git.1 "echo 'Project Structure:'" Enter
tmux send-keys -t $SESSION_NAME:git.1 "eza --tree --level=3" Enter
tmux send-keys -t $SESSION_NAME:git.1 "echo ''" Enter
tmux send-keys -t $SESSION_NAME:git.1 "echo 'Management Commands:'" Enter
tmux send-keys -t $SESSION_NAME:git.1 "echo '  pip install -e .             # Install in dev mode'" Enter
tmux send-keys -t $SESSION_NAME:git.1 "echo '  pip install -e .[dev]        # Install with dev deps'" Enter
tmux send-keys -t $SESSION_NAME:git.1 "echo '  python setup.py sdist        # Build package'" Enter
tmux send-keys -t $SESSION_NAME:git.1 "echo '  eza --tree                   # Show full structure'" Enter

# Select the first window (dev) and focus on vim
tmux select-window -t $SESSION_NAME:dev
tmux select-pane -t $SESSION_NAME:dev.0

# Attach to session
echo "Workspace ready! Attaching to session..."
tmux attach-session -t $SESSION_NAME
