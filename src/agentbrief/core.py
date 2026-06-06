from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable
import json


IGNORED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    ".pytest_cache",
    ".tmp",
    ".mypy_cache",
    ".ruff_cache",
    ".next",
    ".nuxt",
    ".turbo",
    ".cache",
    "node_modules",
    "bower_components",
    "target",
    "build",
    "dist",
    "coverage",
    ".idea",
    ".vscode",
}

LANGUAGE_BY_EXTENSION = {
    ".py": "Python",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".mjs": "JavaScript",
    ".cjs": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".go": "Go",
    ".rs": "Rust",
    ".java": "Java",
    ".kt": "Kotlin",
    ".kts": "Kotlin",
    ".rb": "Ruby",
    ".php": "PHP",
    ".cs": "C#",
    ".cpp": "C++",
    ".cc": "C++",
    ".cxx": "C++",
    ".c": "C",
    ".h": "C/C++",
    ".hpp": "C++",
    ".swift": "Swift",
    ".scala": "Scala",
    ".sh": "Shell",
    ".ps1": "PowerShell",
    ".r": "R",
    ".lua": "Lua",
    ".ex": "Elixir",
    ".exs": "Elixir",
    ".erl": "Erlang",
    ".fs": "F#",
    ".fsx": "F#",
    ".clj": "Clojure",
    ".dart": "Dart",
    ".sql": "SQL",
}

DEPENDENCY_FILES = {
    "package.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "package-lock.json",
    "pyproject.toml",
    "requirements.txt",
    "poetry.lock",
    "Pipfile",
    "Pipfile.lock",
    "Cargo.toml",
    "Cargo.lock",
    "go.mod",
    "go.sum",
    "Gemfile",
    "Gemfile.lock",
    "composer.json",
    "composer.lock",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "Makefile",
    "Dockerfile",
}

DOC_NAMES = {"README.md", "CONTRIBUTING.md", "CHANGELOG.md", "SECURITY.md", "CODE_OF_CONDUCT.md"}
CI_PARTS = (".github/workflows", ".gitlab-ci.yml", "azure-pipelines.yml", "circle.yml")
TEST_HINTS = ("test", "tests", "spec", "__tests__")


@dataclass(frozen=True)
class RepoBrief:
    root_name: str
    total_files_seen: int
    languages: list[str] = field(default_factory=list)
    dependency_files: list[str] = field(default_factory=list)
    docs: list[str] = field(default_factory=list)
    ci: list[str] = field(default_factory=list)
    tests: list[str] = field(default_factory=list)
    notable_files: list[str] = field(default_factory=list)
    package_scripts: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        return {
            "root_name": self.root_name,
            "total_files_seen": self.total_files_seen,
            "languages": self.languages,
            "dependency_files": self.dependency_files,
            "docs": self.docs,
            "ci": self.ci,
            "tests": self.tests,
            "notable_files": self.notable_files,
            "package_scripts": self.package_scripts,
        }


def scan_repository(path: str | Path, max_files: int = 120) -> RepoBrief:
    root = Path(path).resolve()
    if not root.exists():
        raise FileNotFoundError(f"Repository path does not exist: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"Repository path is not a directory: {root}")

    files = list(_iter_files(root, max_files=max_files))
    language_names = _detect_languages(files)
    rel_files = [_relative(root, file) for file in files]

    dependency_files = sorted(rel for rel in rel_files if Path(rel).name in DEPENDENCY_FILES)
    docs = sorted(rel for rel in rel_files if Path(rel).name in DOC_NAMES)
    ci = sorted(rel for rel in rel_files if _is_ci_file(rel))
    tests = sorted(rel for rel in rel_files if _is_test_file(rel))[:20]
    notable_files = _notable_files(rel_files)
    package_scripts = _read_package_scripts(root / "package.json")

    return RepoBrief(
        root_name=root.name,
        total_files_seen=len(files),
        languages=language_names,
        dependency_files=dependency_files,
        docs=docs,
        ci=ci,
        tests=tests,
        notable_files=notable_files,
        package_scripts=package_scripts,
    )


def _iter_files(root: Path, max_files: int) -> Iterable[Path]:
    count = 0
    for path in sorted(root.rglob("*")):
        if count >= max_files:
            break
        if not path.is_file():
            continue
        if _has_ignored_part(root, path):
            continue
        count += 1
        yield path


def _has_ignored_part(root: Path, path: Path) -> bool:
    try:
        relative = path.relative_to(root)
    except ValueError:
        return True
    return any(part in IGNORED_DIRS for part in relative.parts)


def _detect_languages(files: list[Path]) -> list[str]:
    languages = {LANGUAGE_BY_EXTENSION[path.suffix.lower()] for path in files if path.suffix.lower() in LANGUAGE_BY_EXTENSION}
    return sorted(languages)


def _relative(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def _is_ci_file(rel_path: str) -> bool:
    return any(rel_path == part or rel_path.startswith(f"{part}/") for part in CI_PARTS)


def _is_test_file(rel_path: str) -> bool:
    parts = [part.lower() for part in Path(rel_path).parts]
    name = Path(rel_path).name.lower()
    return any(part in TEST_HINTS for part in parts) or name.startswith("test_") or name.endswith(("_test.py", ".test.ts", ".test.tsx", ".spec.ts", ".spec.tsx"))


def _notable_files(rel_files: list[str]) -> list[str]:
    priority_names = {
        "AGENTS.md",
        "CLAUDE.md",
        "CODEX.md",
        "README.md",
        "pyproject.toml",
        "package.json",
        "Cargo.toml",
        "go.mod",
        "Dockerfile",
        "docker-compose.yml",
        "Makefile",
    }
    selected = [rel for rel in rel_files if Path(rel).name in priority_names]
    selected.extend(rel for rel in rel_files if rel.startswith(("src/", "app/", "lib/", "packages/")) and rel not in selected)
    return selected[:30]


def _read_package_scripts(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        return {}
    scripts = data.get("scripts")
    if not isinstance(scripts, dict):
        return {}
    return {str(key): str(value) for key, value in sorted(scripts.items())}
