from agentbrief.core import RepoBrief
from agentbrief.render import render_json, render_markdown


def test_render_markdown_includes_agent_guidance() -> None:
    brief = RepoBrief(
        root_name="demo",
        total_files_seen=2,
        languages=["Python"],
        dependency_files=["pyproject.toml"],
        docs=["README.md"],
        ci=[],
        tests=["tests/test_demo.py"],
        notable_files=["src/demo.py"],
    )

    markdown = render_markdown(brief)

    assert "# Agent Brief" in markdown
    assert "`Python`" in markdown
    assert "Suggested Agent Instructions" in markdown


def test_render_json_is_machine_readable() -> None:
    brief = RepoBrief(root_name="demo", total_files_seen=0)

    assert '"root_name": "demo"' in render_json(brief)

