# Complete Professional Setup Guide
## 1Password + Auto-Commit + Backup + Multi-Device Deployment

Last Updated: 2026-02-09

---

## 1. 🔐 1Password Integration (Fix 30x Fingerprint Prompts)

### Problem
You're prompted for fingerprint authentication 30 times per session.

### Solution: Configure Session Duration

#### Step 1: Enable 1Password SSH Agent

1. Open **1Password app**
2. Go to **Settings** (⌘,) → **Developer**
3. Enable **"Use the SSH agent"**
4. Set **"Authorize for"** to **"24 hours"** (instead of "each application")
5. Check **"Integrate with 1Password CLI"**

#### Step 2: Configure SSH to Use 1Password

Add to `~/.ssh/config`:

\`\`\`ssh-config
# 1Password SSH Agent
Host *
    IdentityAgent "~/Library/Group Containers/2BUA8C4S2C.com.1password/t/agent.sock"
    AddKeysToAgent yes
    UseKeychain yes
\`\`\`

#### Step 3: Set Environment Variable

Add to `~/.zshrc` or `~/.bashrc`:

\`\`\`bash
# 1Password SSH Agent
export SSH_AUTH_SOCK=~/Library/Group\ Containers/2BUA8C4S2C.com.1password/t/agent.sock

# 1Password CLI - Keep session alive for 24 hours
export OP_SESSION_TIMEOUT=86400  # 24 hours in seconds
\`\`\`

#### Step 4: Approve for All Applications

Next time 1Password prompts you:
1. Check ✅ **"Approve for all applications"**
2. This reduces prompts from 30x → 1x per 24 hours

#### Step 5: Git Signing with 1Password

Configure git to use 1Password for commit signing:

\`\`\`bash
# Use 1Password SSH key for git signing
git config --global gpg.format ssh
git config --global user.signingkey "ssh-ed25519 AAAA..." # Your 1Password SSH key
git config --global commit.gpgsign true
\`\`\`

---

## 2. 🔄 Auto-Commit for Version Control

### Problem
Manual commits are tedious and easy to forget.

### Solution A: Git Auto-Commit Hook (Recommended)

Create `.git/hooks/post-checkout`:

\`\`\`bash
#!/bin/bash
# Auto-commit after every 10 file changes

CHANGE_COUNT_FILE=".git/auto_commit_counter"

# Initialize counter if doesn't exist
if [ ! -f "$CHANGE_COUNT_FILE" ]; then
    echo "0" > "$CHANGE_COUNT_FILE"
fi

# Increment counter
COUNTER=$(cat "$CHANGE_COUNT_FILE")
COUNTER=$((COUNTER + 1))
echo "$COUNTER" > "$CHANGE_COUNT_FILE"

# Auto-commit every 10 changes
if [ $((COUNTER % 10)) -eq 0 ]; then
    git add -A
    git commit -m "Auto-commit: $COUNTER changes [$(date '+%Y-%m-%d %H:%M:%S')]"
    echo "✅ Auto-committed after $COUNTER changes"
fi
\`\`\`

Make it executable:
\`\`\`bash
chmod +x .git/hooks/post-checkout
\`\`\`

### Solution B: Watchdog Auto-Commit (Time-Based)

Create `.claude/auto_commit_watcher.sh`:

\`\`\`bash
#!/bin/bash
# Auto-commit every 30 minutes if there are changes

INTERVAL=1800  # 30 minutes in seconds
PROJECT_DIR="/Users/jonathanmallinger/Workspace/llm-security-research"

while true; do
    cd "$PROJECT_DIR"

    # Check if there are changes
    if ! git diff-index --quiet HEAD --; then
        TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
        git add -A
        git commit -m "Auto-commit: $TIMESTAMP"
        echo "✅ Auto-committed at $TIMESTAMP"
    fi

    sleep $INTERVAL
done
\`\`\`

Run in background:
\`\`\`bash
nohup ./.claude/auto_commit_watcher.sh > .claude/auto_commit.log 2>&1 &
\`\`\`

### Solution C: Git Autosave (Best for Solo Work)

Install git-autosave:
\`\`\`bash
brew install git-autosave

# Enable for this project
git autosave enable --interval 30m
\`\`\`

---

## 3. 💾 Backup Gitignored Files

### Problem
Files in `.gitignore` aren't backed up and could be lost.

### Solution: Separate Backup Repository

#### Step 1: Create Backup Script

Create `.claude/backup_ignored_files.sh`:

\`\`\`bash
#!/bin/bash
# Backup gitignored files to 1Password or separate repo

PROJECT_NAME="llm-security-research"
BACKUP_DIR="$HOME/.backups/$PROJECT_NAME/$(date +%Y-%m-%d)"
PROJECT_DIR="/Users/jonathanmallinger/Workspace/llm-security-research"

mkdir -p "$BACKUP_DIR"

echo "🔒 Backing up gitignored files..."

# Backup .env files
if [ -f "$PROJECT_DIR/.env" ]; then
    cp "$PROJECT_DIR/.env" "$BACKUP_DIR/.env.backup"
    echo "  ✓ Backed up .env"
fi

# Backup local configs
cp "$PROJECT_DIR/.claude/settings.local.json" "$BACKUP_DIR/" 2>/dev/null

# Backup databases (if not tracked)
find "$PROJECT_DIR" -name "*.db" -size -100M -exec cp {} "$BACKUP_DIR/" \\;

# Store in 1Password
op document create "$BACKUP_DIR/.env.backup" \\
    --title "$PROJECT_NAME .env backup $(date +%Y-%m-%d)" \\
    --vault "Development" 2>/dev/null

echo "✅ Backup complete: $BACKUP_DIR"
\`\`\`

Make executable:
\`\`\`bash
chmod +x .claude/backup_ignored_files.sh
\`\`\`

#### Step 2: Automated Daily Backup (cron)

Add to crontab (`crontab -e`):
\`\`\`cron
# Backup gitignored files daily at 2 AM
0 2 * * * /Users/jonathanmallinger/Workspace/llm-security-research/.claude/backup_ignored_files.sh
\`\`\`

#### Step 3: Alternative - Encrypted Git Repo

Create a separate private repo for sensitive files:
\`\`\`bash
# Create encrypted backup repo
cd "$HOME/.backups"
git init llm-security-research-secrets
cd llm-security-research-secrets

# Enable git-crypt for encryption
git-crypt init
git-crypt export-key ../llm-secrets.key

# Add sensitive files
cp /path/to/.env .
git add .env
git commit -m "Add encrypted .env"
git remote add origin git@github.com:yourusername/secrets-backup.git
git push -u origin main
\`\`\`

---

## 4. 🧠 Serena Memory Filtering

### Problem
Serena creates memories for everything, including non-project setup discussions.

### Solution: Configure Memory Filters

#### Step 1: Update Project Config

Edit `.serena/project.yml` and add:

\`\`\`yaml
# Memory filtering rules
memory_filters:
  # Only create memories for these topics
  include_topics:
    - "attack techniques"
    - "evaluation protocol"
    - "model targeting"
    - "agent coordination"
    - "security research"
    - "code implementation"
    - "bug fixes"

  # Never create memories for these
  exclude_topics:
    - "plugin setup"
    - "configuration"
    - "1password setup"
    - "git configuration"
    - "system setup"
    - "troubleshooting"

  # Exclude conversations shorter than 5 messages
  min_conversation_length: 5

  # Auto-archive memories older than 60 days
  auto_archive_after_days: 60
\`\`\`

#### Step 2: Manual Memory Management

Tell Serena explicitly:
\`\`\`
"Serena, do not create a memory of this setup conversation.
This is one-time configuration, not project knowledge."
\`\`\`

Or request specific memories:
\`\`\`
"Serena, create a memory called 'attack_technique_improvements_2026-02-09'
with only the key decisions we made about evaluation protocols."
\`\`\`

#### Step 3: Automated Memory Cleanup

Add to `.claude/auto_commit_watcher.sh`:

\`\`\`bash
# Clean up Serena memories weekly
if [ $(date +%u) -eq 7 ]; then  # Sunday
    ./.serena/cleanup_old_memories.sh
fi
\`\`\`

---

## 5. 🚀 Deploy to All Devices

### Problem
Need this setup on Linux servers, Windows computers, and mobile devices.

### Solution: Deployment Package

#### Step 1: Create Dotfiles Repository

\`\`\`bash
# Create dotfiles repo
cd ~
mkdir -p dotfiles/.claude
cd dotfiles

# Copy Claude Code configs
cp -r ~/.claude/settings.json .claude/
cp -r /path/to/project/.claude/PLUGIN_SETUP.md .claude/
cp -r /path/to/project/.mcp.json .

# Copy shell configs
cp ~/.zshrc .
cp ~/.gitconfig .
cp ~/.ssh/config ssh_config

# Create installation script
cat > install.sh << 'EOF'
#!/bin/bash
# Claude Code Complete Setup Installer

echo "🚀 Installing Claude Code Complete Setup..."

# 1. Install Claude Code CLI
curl -fsSL https://api.claude.com/install.sh | sh

# 2. Install plugins
claude plugin install superpowers@claude-plugins-official --scope project
claude plugin install serena@claude-plugins-official --scope project
claude plugin marketplace add https://github.com/EveryInc/compound-engineering-plugin
claude plugin install compound-engineering@every-marketplace --scope project

# 3. Copy configs
cp .claude/settings.json ~/.claude/
cp .mcp.json ~/

# 4. Setup 1Password SSH
cat >> ~/.zshrc << 'ZSHRC'
export SSH_AUTH_SOCK=~/Library/Group\\ Containers/2BUA8C4S2C.com.1password/t/agent.sock
export OP_SESSION_TIMEOUT=86400
ZSHRC

# 5. Setup git auto-commit
cp auto_commit_watcher.sh ~/.claude/
chmod +x ~/.claude/auto_commit_watcher.sh

echo "✅ Installation complete!"
echo "Next steps:"
echo "  1. Open 1Password → Settings → Developer"
echo "  2. Enable SSH agent and set to 24 hours"
echo "  3. Restart terminal"
EOF

chmod +x install.sh

# Push to GitHub
git init
git add .
git commit -m "Initial dotfiles setup"
git remote add origin git@github.com:yourusername/dotfiles.git
git push -u origin main
\`\`\`

#### Step 2: Platform-Specific Install Scripts

**For Linux Servers:**

\`\`\`bash
# install_linux.sh
#!/bin/bash

# Install Claude Code
curl -fsSL https://api.claude.com/install.sh | sh

# Clone dotfiles
git clone https://github.com/yourusername/dotfiles.git ~/dotfiles
cd ~/dotfiles

# Run base install
./install.sh

# Linux-specific: Setup systemd for auto-commit
sudo tee /etc/systemd/system/claude-auto-commit.service << EOF
[Unit]
Description=Claude Code Auto-Commit Service
After=network.target

[Service]
Type=simple
User=$USER
ExecStart=/home/$USER/.claude/auto_commit_watcher.sh
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable claude-auto-commit
sudo systemctl start claude-auto-commit
\`\`\`

**For Windows:**

\`\`\`powershell
# install_windows.ps1
# Install Claude Code
iwr https://api.claude.com/install.ps1 -useb | iex

# Clone dotfiles
git clone https://github.com/yourusername/dotfiles.git $HOME\\dotfiles
cd $HOME\\dotfiles

# Install plugins
& "C:\\Program Files\\Claude\\claude.exe" plugin install superpowers@claude-plugins-official --scope project
& "C:\\Program Files\\Claude\\claude.exe" plugin install serena@claude-plugins-official --scope project

# Setup 1Password SSH
$env:SSH_AUTH_SOCK = "$env:LOCALAPPDATA\\1Password\\config\\ssh\\agent.sock"
[Environment]::SetEnvironmentVariable("SSH_AUTH_SOCK", $env:SSH_AUTH_SOCK, "User")
\`\`\`

#### Step 3: One-Command Install

From any device:

\`\`\`bash
# macOS/Linux
curl -fsSL https://raw.githubusercontent.com/yourusername/dotfiles/main/install.sh | bash

# Windows (PowerShell as Admin)
iwr https://raw.githubusercontent.com/yourusername/dotfiles/main/install_windows.ps1 -useb | iex
\`\`\`

---

## 6. 📱 Mobile Setup (Limited)

### iOS/Android
Claude Code is CLI-only (no mobile app), but you can:

1. **Use SSH to your servers:**
   - Install Termius or Blink Shell
   - SSH into your Linux/macOS machine
   - Run Claude Code remotely

2. **Use Claude.ai (web) for mobile:**
   - Not the same as Claude Code
   - But available at https://claude.ai

3. **Setup GitHub Codespaces:**
   - Run Claude Code in browser via Codespaces
   - Access from mobile browser

---

## Quick Start Checklist

### ✅ 1Password (Do Once)
- [ ] Open 1Password → Settings → Developer
- [ ] Enable "Use the SSH agent"
- [ ] Set "Authorize for" to "24 hours"
- [ ] Check "Approve for all applications"
- [ ] Add SSH_AUTH_SOCK to ~/.zshrc

### ✅ Auto-Commit (Do Per Project)
- [ ] Copy `.claude/auto_commit_watcher.sh` to project
- [ ] Run in background: `nohup ./.claude/auto_commit_watcher.sh &`
- [ ] Or install git-autosave: `brew install git-autosave`

### ✅ Backup (Do Once)
- [ ] Copy `.claude/backup_ignored_files.sh` to project
- [ ] Add to crontab: `crontab -e`
- [ ] Test: `./.claude/backup_ignored_files.sh`

### ✅ Serena Memories (Configure Once)
- [ ] Edit `.serena/project.yml` with memory filters
- [ ] Run cleanup: `./.serena/cleanup_old_memories.sh`

### ✅ Deploy Everywhere (Do Once)
- [ ] Create dotfiles repo
- [ ] Add install scripts
- [ ] Push to GitHub
- [ ] Install on each device: `curl -fsSL <url> | bash`

---

## Maintenance Schedule

| Task | Frequency | Command |
|------|-----------|---------|
| Serena memory cleanup | Weekly | `./.serena/cleanup_old_memories.sh` |
| Backup gitignored files | Daily (automated) | Runs via cron |
| Update plugins | Monthly | `claude plugin update --all` |
| Dotfiles sync | After major changes | `cd ~/dotfiles && git push` |

---

## Resources

- [1Password SSH Agent Docs](https://developer.1password.com/docs/ssh/agent/)
- [1Password Session Duration](https://developer.1password.com/docs/ssh/agent/security/)
- [Git Autosave](https://github.com/git-autosave/git-autosave)
- [Dotfiles Best Practices](https://dotfiles.github.io/)

---

## Troubleshooting

### 1Password still prompting frequently
1. Check SSH_AUTH_SOCK is set: `echo $SSH_AUTH_SOCK`
2. Restart 1Password app
3. Verify setting: 1Password → Developer → "24 hours"

### Auto-commit not working
1. Check if script is running: `ps aux | grep auto_commit`
2. Check logs: `cat .claude/auto_commit.log`
3. Make sure script is executable: `chmod +x .claude/auto_commit_watcher.sh`

### Backup failed
1. Check 1Password CLI: `op --version`
2. Sign in: `op signin`
3. Check disk space: `df -h`

---

**Last Updated:** 2026-02-09
**Next Review:** 2026-03-09
