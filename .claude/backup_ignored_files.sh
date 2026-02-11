#!/bin/bash
# Backup gitignored files to 1Password and local storage

PROJECT_NAME="models"
BACKUP_DIR="$HOME/.backups/$PROJECT_NAME/$(date +%Y-%m-%d)"
PROJECT_DIR="/Users/jonathanmallinger/models"
LOG_FILE="$HOME/.backups/$PROJECT_NAME/backup.log"

mkdir -p "$BACKUP_DIR"
mkdir -p "$(dirname "$LOG_FILE")"

echo "🔒 Backing up gitignored files at $(date)" | tee -a "$LOG_FILE"
echo "   Backup directory: $BACKUP_DIR" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

BACKUP_COUNT=0

# Backup .env files
if [ -f "$PROJECT_DIR/.env" ]; then
    cp "$PROJECT_DIR/.env" "$BACKUP_DIR/.env.backup"
    echo "  ✓ Backed up .env" | tee -a "$LOG_FILE"
    ((BACKUP_COUNT++))

    # Store in 1Password (if CLI available and signed in)
    if command -v op &> /dev/null; then
        op document create "$BACKUP_DIR/.env.backup" \
            --title "$PROJECT_NAME .env backup $(date +%Y-%m-%d)" \
            --vault "Development" 2>/dev/null && \
            echo "  ✓ Uploaded .env to 1Password" | tee -a "$LOG_FILE"
    fi
fi

# Backup .env.local files
if [ -f "$PROJECT_DIR/.env.local" ]; then
    cp "$PROJECT_DIR/.env.local" "$BACKUP_DIR/.env.local.backup"
    echo "  ✓ Backed up .env.local" | tee -a "$LOG_FILE"
    ((BACKUP_COUNT++))
fi

# Backup local Claude settings
if [ -f "$PROJECT_DIR/.claude/settings.local.json" ]; then
    cp "$PROJECT_DIR/.claude/settings.local.json" "$BACKUP_DIR/settings.local.json"
    echo "  ✓ Backed up .claude/settings.local.json" | tee -a "$LOG_FILE"
    ((BACKUP_COUNT++))
fi

# Backup small databases (< 100MB)
DB_COUNT=0
while IFS= read -r -d '' db_file; do
    cp "$db_file" "$BACKUP_DIR/"
    ((DB_COUNT++))
    ((BACKUP_COUNT++))
done < <(find "$PROJECT_DIR" -name "*.db" -size -100M -print0 2>/dev/null)

if [ $DB_COUNT -gt 0 ]; then
    echo "  ✓ Backed up $DB_COUNT database files" | tee -a "$LOG_FILE"
fi

# Backup any .key or .pem files
KEY_COUNT=0
while IFS= read -r -d '' key_file; do
    cp "$key_file" "$BACKUP_DIR/"
    ((KEY_COUNT++))
    ((BACKUP_COUNT++))
done < <(find "$PROJECT_DIR" -name "*.key" -o -name "*.pem" -print0 2>/dev/null)

if [ $KEY_COUNT -gt 0 ]; then
    echo "  ✓ Backed up $KEY_COUNT key/certificate files" | tee -a "$LOG_FILE"
fi

# Create backup archive
cd "$BACKUP_DIR/.."
ARCHIVE_NAME="$PROJECT_NAME-backup-$(date +%Y-%m-%d).tar.gz"
tar -czf "$ARCHIVE_NAME" "$(date +%Y-%m-%d)" 2>/dev/null
ARCHIVE_SIZE=$(du -h "$ARCHIVE_NAME" | cut -f1)

echo "" | tee -a "$LOG_FILE"
echo "✅ Backup complete!" | tee -a "$LOG_FILE"
echo "   Files backed up: $BACKUP_COUNT" | tee -a "$LOG_FILE"
echo "   Archive: $ARCHIVE_NAME ($ARCHIVE_SIZE)" | tee -a "$LOG_FILE"
echo "   Location: $BACKUP_DIR" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# Clean up backups older than 30 days
find "$HOME/.backups/$PROJECT_NAME" -name "*.tar.gz" -mtime +30 -delete 2>/dev/null
