# Claude Marketplace

A custom [Claude Code](https://code.claude.com) plugin marketplace hosting reusable skills.

## Install

### 1. Add this marketplace to Claude Code

```
/plugin marketplace add akshanshkmr/claude-marketplace
```

### 2. Install a plugin

```
/plugin install git-workflow@claude-marketplace
/plugin install code-quality@claude-marketplace
```

### 3. Use the skills

```
/git-workflow:smart-commit
/git-workflow:pr-summary
/code-quality:review src/my-file.ts
```

---

## Available plugins

### `git-workflow`

Git workflow automation.

| Skill | Invocation | Description |
|---|---|---|
| `smart-commit` | `/git-workflow:smart-commit` | Stage and commit with an auto-generated conventional commit message |
| `pr-summary` | `/git-workflow:pr-summary` | Write a pull request description from the current branch diff |

### `code-quality`

Code review and quality checks.

| Skill | Invocation | Description |
|---|---|---|
| `review` | `/code-quality:review [file]` | Review code for bugs, security issues, and best practices |

---

## Add your own skill

1. Create a plugin directory under `plugins/`:

```
plugins/
└── my-plugin/
    ├── .claude-plugin/
    │   └── plugin.json
    └── skills/
        └── my-skill/
            └── SKILL.md
```

2. Add it to `.claude-plugin/marketplace.json`:

```json
{
  "name": "my-plugin",
  "source": "./plugins/my-plugin",
  "description": "What this plugin does"
}
```

3. Push and install:

```
/plugin marketplace update claude-marketplace
/plugin install my-plugin@claude-marketplace
```

See the [Claude Code skills docs](https://code.claude.com/docs/en/skills) for full `SKILL.md` authoring guidance.
