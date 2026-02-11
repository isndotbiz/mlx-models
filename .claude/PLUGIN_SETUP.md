# Claude Code Plugin Configuration

## Project-Scoped Plugins (All Enabled)

All plugins are installed at **project scope** so every team member gets the same configuration.

### 🚀 Active Plugins

1. **Superpowers** (`superpowers@claude-plugins-official`)
   - Version: 4.2.0
   - 20+ development methodology skills
   - TDD, systematic debugging, planning, code review
   - Commands: `/superpowers:*` (see full list with `/superpowers:using-superpowers`)

2. **Compound Engineering** (`compound-engineering@every-marketplace`)
   - Version: 2.31.1
   - 24 specialized AI agents + 13 commands + 11 skills
   - Includes Context7 MCP server for codebase context
   - Full autonomous workflow: Plan → Work → Review → Compound
   - Commands: `/plan`, `/delegate`, `/assess`, `/codify`
   - GitHub: https://github.com/EveryInc/compound-engineering-plugin

3. **Serena** (`serena@claude-plugins-official`)
   - Version: 96276205880a
   - AI coding assistant
   - MCP Server: ✅ Connected
   - Source: https://github.com/oraios/serena

### GitHub Integration

GitHub functionality is provided via **GitHub MCP Server** (official):
- ✅ MCP Server: Connected
- ✅ Authenticated as: isndotbiz
- ✅ Native GitHub tools available to Claude
- ✅ Fallback: `gh` CLI also available for manual commands

## MCP Server Status

Run `claude mcp list` to check status:

```
✓ Serena                        - Connected
✓ Context7 (via Compound Eng.)  - Connected
✓ GitHub (official MCP)         - Connected
```

All MCP servers are connected and operational!

### MCP Configuration

The project uses `.mcp.json` for MCP server configuration:
- **GitHub MCP**: Official @modelcontextprotocol/server-github
- **Authentication**: Uses GITHUB_TOKEN environment variable
- **Scope**: Project-level (tracked in git)

## Compound Engineering Workflow

The Compound Engineering plugin provides a complete development workflow:

### Core Commands

1. **`/plan`** - Turn feature ideas into detailed GitHub issues
   - Creates structured implementation plans
   - Breaks down into bite-sized tasks
   - Generates GitHub issues automatically

2. **`/delegate`** - Execute work systematically
   - Implements the plan with tracked progress
   - Uses git worktrees for isolation
   - Follows test-driven development

3. **`/assess`** - Multi-agent code review
   - 12 specialized review agents in parallel
   - Checks security, performance, architecture
   - Generates comprehensive review reports

4. **`/codify`** - Document learnings
   - Records insights and patterns
   - Updates team documentation
   - Makes future work easier

### Philosophy

**Compound Engineering** means each unit of work should make subsequent units easier, not harder. Every command generates documentation that helps future work.

## Configuration Files

- `.claude/settings.json` - Project plugin configuration (tracked in git)
- `.claude/settings.local.json` - Personal overrides (gitignored)
- `.claude/CLAUDE.md` - Project instructions (tracked in git)
- `.claude/PLUGIN_SETUP.md` - This file (tracked in git)

## Marketplaces

Configured marketplaces:

```bash
# Official Anthropic marketplace
claude-plugins-official

# Every Inc. marketplace (Compound Engineering)
every-marketplace
```

## Adding More Plugins

```bash
# From official marketplace
claude plugin install <plugin-name>@claude-plugins-official --scope project

# From Every marketplace
claude plugin install <plugin-name>@every-marketplace --scope project

# Add a new marketplace
claude plugin marketplace add https://github.com/owner/repo.git

# Update settings.json to enable it
# Edit .claude/settings.json and add to enabledPlugins
```

## Troubleshooting

### GitHub Operations

GitHub functionality is available via the `gh` CLI tool, which is already authenticated:
```bash
gh auth status        # Check authentication
gh pr create          # Create pull request
gh issue list         # List issues
gh repo view          # View repository
```

### Personal Overrides

Create `.claude/settings.local.json` for personal preferences:

```json
{
  "enabledPlugins": {
    "my-personal-plugin@marketplace": true
  }
}
```

This won't affect team members and is gitignored.

## Quick Commands

```bash
# List installed plugins
claude plugin list

# Check MCP server health
claude mcp list

# View available superpowers skills
/superpowers:using-superpowers

# Compound Engineering workflow
/plan       # Create implementation plan
/delegate   # Execute the plan
/assess     # Review the code
/codify     # Document learnings

# Access plugin tools
/plugin
```

## Resources

- [Compound Engineering GitHub](https://github.com/EveryInc/compound-engineering-plugin)
- [Compound Engineering Philosophy](https://every.to/guides/compound-engineering)
- [Superpowers Documentation](https://github.com/obra/superpowers)

## Last Updated

2026-02-09 - Added Compound Engineering plugin with integrated Context7
