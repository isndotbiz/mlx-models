#!/bin/bash
# Auto-commit watcher - commits changes every 30 minutes if there are any

INTERVAL=1800  # 30 minutes in seconds
PROJECT_DIR="/Users/jonathanmallinger/models"
LOG_FILE=".claude/auto_commit.log"

echo "🔄 Auto-commit watcher started at $(date)" >> "$LOG_FILE"
echo "   Interval: $INTERVAL seconds ($(($INTERVAL / 60)) minutes)" >> "$LOG_FILE"
echo "   Project: $PROJECT_DIR" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

while true; do
    cd "$PROJECT_DIR"

    # Check if there are changes
    if ! git diff-index --quiet HEAD -- 2>/dev/null; then
        TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

        # Get changed files count
        CHANGED_COUNT=$(git status --porcelain | wc -l | tr -d ' ')

        # Add all changes
        git add -A

        # Create commit
        git commit -m "Auto-commit: $CHANGED_COUNT files changed at $TIMESTAMP

Co-Authored-By: Claude Sonnet 4.5 (1M context) <noreply@anthropic.com>" >> "$LOG_FILE" 2>&1

        echo "✅ Auto-committed $CHANGED_COUNT files at $TIMESTAMP" | tee -a "$LOG_FILE"
    else
        echo "  No changes at $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
    fi

    # Clean up Serena memories on Sundays
    if [ $(date +%u) -eq 7 ]; then
        if [ -f ".serena/cleanup_old_memories.sh" ]; then
            echo "🧹 Running weekly memory cleanup..." >> "$LOG_FILE"
            ./.serena/cleanup_old_memories.sh >> "$LOG_FILE" 2>&1
        fi
    fi

    sleep $INTERVAL
done
