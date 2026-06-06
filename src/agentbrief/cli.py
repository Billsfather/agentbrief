from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path
import sys

from .core import scan_repository
from .render import render_json, render_markdown


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog="agent-brief",
        description="Generate a concise repository briefing for AI coding agents.",
    )
    parser.add_argument("path", nargs="?", default=".", help="Repository path to scan.")
    parser.add_argument("--output", "-o", default="AGENTS.md", help="Output file path. Defaults to AGENTS.md.")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown", help="Output format.")
    parser.add_argument("--max-files", type=int, default=120, help="Maximum files to scan.")
    parser.add_argument("--check", action="store_true", help="Exit with an error if the output file is stale.")
    parser.add_argument("--print", dest="print_output", action="store_true", help="Print output to stdout.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        brief = scan_repository(args.path, max_files=args.max_files)
    except (FileNotFoundError, NotADirectoryError) as exc:
        parser.error(str(exc))

    content = render_json(brief) if args.format == "json" else render_markdown(brief)

    if args.print_output:
        sys.stdout.write(content)

    output_path = Path(args.output)
    if args.check:
        try:
            current = output_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            sys.stderr.write(f"{output_path} does not exist.\n")
            return 1
        if current != content:
            sys.stderr.write(f"{output_path} is stale. Run agent-brief {args.path} --output {output_path}.\n")
            return 1
        return 0

    if not args.print_output:
        output_path.write_text(content, encoding="utf-8")
        sys.stdout.write(f"Wrote {output_path}\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

