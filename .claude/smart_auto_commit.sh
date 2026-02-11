#!/bin/bash
# Smart Auto-Commit - Only runs when you're actively working
# Prevents duplicates, auto-starts on directory entry

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOCK_FILE="$PROJECT_DIR/.claude/.watcher.lock"
LOG_FILE="$PROJECT_DIR/.claude/auto_commit.log"
INACTIVITY_TIMEOUT=3600  # Stop after 1 hour of no git activity

# Check if watcher is already running for this project
if [ -f "$LOCK_FILE" ]; then
    PID=$(cat "$LOCK_FILE" 2>/dev/null)
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "✓ Auto-commit watcher already running for $(basename "$PROJECT_DIR") (PID: $PID)"
        exit 0
    else
        # Stale lock file, remove it
        rm -f "$LOCK_FILE"
    fi
fi

# Write our PID to lock file
echo $$ > "$LOCK_FILE"

echo "🔄 Auto-commit watcher started for $(basename "$PROJECT_DIR") at $(date)" | tee -a "$LOG_FILE"
echo "   PID: $$" | tee -a "$LOG_FILE"
echo "   Will auto-stop after $((INACTIVITY_TIMEOUT / 60)) minutes of inactivity" | tee -a "$LOG_FILE"
echo "" >> "$LOG_FILE"

# Cleanup function
cleanup() {
    rm -f "$LOCK_FILE"
    echo "⏹  Auto-commit watcher stopped for $(basename "$PROJECT_DIR") at $(date)" >> "$LOG_FILE"
    exit 0
}

trap cleanup EXIT INT TERM

LAST_ACTIVITY=$(date +%s)
CHECK_INTERVAL=300  # Check every 5 minutes

while true; do
    cd "$PROJECT_DIR"

    # Check for inactivity
    CURRENT_TIME=$(date +%s)
    TIME_SINCE_ACTIVITY=$((CURRENT_TIME - LAST_ACTIVITY))

    if [ $TIME_SINCE_ACTIVITY -gt $INACTIVITY_TIMEOUT ]; then
        echo "⏸  No activity for $((INACTIVITY_TIMEOUT / 60)) minutes, stopping watcher" >> "$LOG_FILE"
        cleanup
    fi

    # Check if there are changes
    if ! git diff-index --quiet HEAD -- 2>/dev/null; then
        TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
        CHANGED_COUNT=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')

        if [ "$CHANGED_COUNT" -gt 0 ]; then
            # Reset inactivity timer
            LAST_ACTIVITY=$(date +%s)

            # Add and commit
            git add -A
            git commit -m "Auto-commit: $CHANGED_COUNT files changed at $TIMESTAMP

Co-Authored-By: Claude Sonnet 4.5 (1M context) <noreply@anthropic.com>" >> "$LOG_FILE" 2>&1

            echo "✅ Auto-committed $CHANGED_COUNT files at $TIMESTAMP" | tee -a "$LOG_FILE"
        fi
    fi

    sleep $CHECK_INTERVAL
done
