from pathlib import Path

from agentbrief.cli import main


def test_cli_writes_default_markdown(workspace_tmp: Path, monkeypatch) -> None:
    tmp_path = workspace_tmp
    (tmp_path / "hello.py").write_text("print('hello')\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    exit_code = main([".", "--output", "AGENTS.md"])

    assert exit_code == 0
    assert (tmp_path / "AGENTS.md").exists()


def test_cli_check_fails_when_output_is_stale(workspace_tmp: Path) -> None:
    tmp_path = workspace_tmp
    (tmp_path / "hello.py").write_text("print('hello')\n", encoding="utf-8")
    output = tmp_path / "AGENTS.md"
    output.write_text("stale\n", encoding="utf-8")

    exit_code = main([str(tmp_path), "--output", str(output), "--check"])

    assert exit_code == 1
