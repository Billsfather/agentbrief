# GitHub Action

Use AgentBrief in CI to keep `AGENTS.md` fresh as the repository changes.

## Check Mode

```yaml
name: AgentBrief

on:
  pull_request:
  push:
    branches: [main]

jobs:
  agent-brief:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: Billsfather/agentbrief@v1
        with:
          output: AGENTS.md
          check: true
```

## Generate Mode

Generate a briefing during CI without failing on drift:

```yaml
- uses: Billsfather/agentbrief@v1
  with:
    output: AGENTS.md
    check: false
```

## Inputs

| Input | Default | Description |
| --- | --- | --- |
| `path` | `.` | Repository path to scan. |
| `output` | `AGENTS.md` | Briefing file to generate or check. |
| `format` | `markdown` | Output format: `markdown` or `json`. |
| `max-files` | `120` | Maximum number of files to scan. |
| `check` | `true` | Fail if the committed briefing is stale. |

