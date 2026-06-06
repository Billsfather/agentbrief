from pathlib import Path

from agentbrief.core import scan_repository


def test_scan_repository_detects_common_project_signals(workspace_tmp: Path) -> None:
    tmp_path = workspace_tmp
    (tmp_path / "src").mkdir()
    (tmp_path / "tests").mkdir()
    (tmp_path / ".github" / "workflows").mkdir(parents=True)
    (tmp_path / "src" / "app.py").write_text("print('hello')\n", encoding="utf-8")
    (tmp_path / "tests" / "test_app.py").write_text("def test_ok(): assert True\n", encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")
    (tmp_path / ".github" / "workflows" / "ci.yml").write_text("name: ci\n", encoding="utf-8")

    brief = scan_repository(tmp_path)

    assert brief.root_name == tmp_path.name
    assert brief.languages == ["Python"]
    assert brief.dependency_files == ["pyproject.toml"]
    assert brief.docs == ["README.md"]
    assert brief.ci == [".github/workflows/ci.yml"]
    assert brief.tests == ["tests/test_app.py"]
    assert "src/app.py" in brief.notable_files


def test_scan_repository_ignores_dependency_directories(workspace_tmp: Path) -> None:
    tmp_path = workspace_tmp
    (tmp_path / "node_modules").mkdir()
    (tmp_path / "node_modules" / "ignored.js").write_text("console.log('skip')\n", encoding="utf-8")
    (tmp_path / "app.ts").write_text("export const ok = true\n", encoding="utf-8")

    brief = scan_repository(tmp_path)

    assert brief.languages == ["TypeScript"]
    assert brief.total_files_seen == 1
