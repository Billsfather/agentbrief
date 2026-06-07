# AgentBrief

Generate a short, useful repository briefing for AI coding agents.

AgentBrief scans a project locally and creates an `AGENTS.md`-style briefing that tells tools like Codex, Claude Code, Cursor, and GitHub Copilot where the important files are, how the project is built, and what conventions an agent should respect before editing.

```bash
pipx install agentbrief
agent-brief .
```

Or keep `AGENTS.md` fresh in GitHub Actions:

```yaml
- uses: Billsfather/agentbrief@v1
  with:
    output: AGENTS.md
    check: true
```

No API keys. No network calls. No source upload.

## Why this exists

AI coding agents work better when they have a compact map of the repo before they start changing files. Most projects either have no agent instructions or have a stale hand-written note. AgentBrief gives maintainers a fast baseline they can commit, review, and customize.

## Features

- Generates Markdown or JSON summaries from local files.
- Detects languages, dependency manifests, scripts, tests, CI, docs, and notable source files.
- Respects `.gitignore`-style common directories such as `.git`, `node_modules`, `dist`, `.venv`, and build caches.
- Supports `--check` for CI so committed briefings stay fresh.
- Ships as a GitHub Action for pull request checks.
- Uses only the Python standard library.

## Quick Start

Create or refresh `AGENTS.md`:

```bash
agent-brief . --output AGENTS.md
```

Print the briefing without writing a file:

```bash
agent-brief . --print
```

Fail CI when the committed briefing is stale:

```bash
agent-brief . --output AGENTS.md --check
```

Emit machine-readable JSON:

```bash
agent-brief . --format json --print
```

## GitHub Action

Add AgentBrief to CI:

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

See [docs/github-action.md](docs/github-action.md) for all inputs.

## Example Output

```markdown
# Agent Brief

Generated for `my-project`.

## Project Signals

- Languages: TypeScript, Python
- Dependency files: package.json, pyproject.toml
- CI: .github/workflows/ci.yml
- Tests: tests/, src/example.test.ts

## Suggested Agent Instructions

- Read the dependency and test sections before editing shared code.
- Prefer existing scripts from package.json or pyproject.toml.
- Keep generated files and dependency directories out of edits.
```

## CLI Reference

```text
usage: agent-brief [path] [--output AGENTS.md] [--format markdown|json]
                   [--max-files 120] [--check] [--print]
```

## What Makes This Star-Worthy

High-star projects usually combine a timely problem, a tiny install path, a clear demo, and a maintainer-friendly contribution surface. AgentBrief is intentionally scoped around those traits:

- The problem is current: coding agents need reliable repo context.
- The tool is safe by default: local scan only, no credentials.
- The value is visible in one command.
- The output can be committed, reviewed, and improved by humans.

## Roadmap

- Framework-specific detectors for Next.js, FastAPI, Django, Rails, Rust, Go, and Java.
- Optional token-budgeted output for different agent context windows.
- Framework-specific GitHub Action presets.
- `AGENTS.md` merge mode that preserves hand-written maintainer notes.
- Repository health score with actionable fixes.

## Development

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e . pytest
python -m pytest
```

## License

MIT
