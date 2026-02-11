# Claude Code Setup for models

This project uses the complete Claude Code professional setup.

## What's Included

- ✅ Superpowers plugin (development methodologies)
- ✅ Compound Engineering plugin (full automation workflow)
- ✅ Serena plugin (AI coding assistant)
- ✅ GitHub MCP server (native GitHub integration)
- ✅ Auto-commit watcher (commits every 30 minutes)
- ✅ Backup system (daily backups of sensitive files)
- ✅ Serena memory filtering (project-relevant only)

## Quick Start

### 1. Verify Plugins

```bash
claude plugin list
claude mcp list
```

All plugins should show as "enabled" and all MCP servers should be "Connected".

### 2. Start Auto-Commit Watcher

```bash
nohup ./.claude/auto_commit_watcher.sh > /dev/null 2>&1 &
```

Verify it's running:
```bash
pgrep -fl auto_commit_watcher
```

### 3. Setup Backup (Optional)

Add to crontab for daily backups:
```bash
crontab -e
```

Add this line:
```
0 2 * * * /Users/jonathanmallinger/models/.claude/backup_ignored_files.sh
```

## Documentation

- **COMPLETE_SETUP_GUIDE.md** - Full setup instructions
- **PLUGIN_SETUP.md** - Plugin configuration reference
- **.serena/memory_management.md** - Serena memory management guide

## Maintenance

### Check Auto-Commit Status
```bash
pgrep -fl auto_commit_watcher
tail -f .claude/auto_commit.log
```

### Clean Up Old Memories
```bash
./.serena/cleanup_old_memories.sh
```

### Run Manual Backup
```bash
./.claude/backup_ignored_files.sh
```

## Troubleshooting

See `.claude/COMPLETE_SETUP_GUIDE.md` for detailed troubleshooting.

---

Deployed on: Mon Feb  9 22:41:23 PST 2026
From: /Users/jonathanmallinger/Workspace/llm-security-research
