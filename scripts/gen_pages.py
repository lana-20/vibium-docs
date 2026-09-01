#!/usr/bin/env python3
"""Generate the Vibium command reference from the installed binary.

Every page under docs/commands/ except the curated ones in CURATED is
regenerated from `vibium <cmd> --help`, so the reference can be re-derived
whenever the binary moves.

    python3 scripts/gen_pages.py [--bin vibium] [--out docs/commands]

Curated pages are never touched: they carry examples captured from a live
browser, which help text cannot supply.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

# Pages written by hand against real terminal output. Never overwritten.
CURATED = {"back", "forward", "reload", "url", "title", "map", "find",
           "click", "screenshot", "fill", "wait", "type", "press"}

# Every top-level command, grouped for the sidebar. Checked for drift against
# the binary at run time: an uncategorized command is a hard error, so a new
# command in a future release cannot silently vanish from the sidebar.
CATEGORIES: list[tuple[str, str, list[str]]] = [
    ("navigation", "Navigation",
     ["go", "back", "forward", "reload", "url", "title"]),
    ("mapping", "Mapping & references",
     ["map", "diff"]),
    ("finding", "Finding elements",
     ["find", "frame", "frames", "count"]),
    ("interacting", "Interacting",
     ["click", "dblclick", "fill", "type", "press", "keys", "check",
      "uncheck", "select", "hover", "focus", "drag", "upload", "scroll",
      "mouse", "highlight"]),
    ("reading", "Reading page state",
     ["text", "html", "attr", "value", "a11y-tree", "is", "content"]),
    ("capture", "Capture",
     ["screenshot", "pdf", "eval", "record"]),
    ("waiting", "Waiting",
     ["wait", "sleep"]),
    ("session", "Browser & session",
     ["start", "stop", "daemon", "page", "pages", "viewport", "window",
      "install", "is-installed", "paths", "storage", "cookies", "download",
      "dialog", "geolocation", "media"]),
    ("agent", "Agent integration",
     ["mcp", "add-skill", "pipe", "serve"]),
    ("diagnostics", "Diagnostics",
     ["launch-test", "bidi-test", "ws-test"]),
    ("meta", "Meta",
     ["version", "help", "completion"]),
]

SECTION_RE = re.compile(
    r"^(Usage|Examples|Available Commands|Additional Commands|Flags|Global Flags):\s*$"
)
FLAG_RE = re.compile(r"^\s*(?:(-\w), )?(--[\w-]+)(?:\s+(\S+))?\s{2,}(.+)$")
SUBCMD_RE = re.compile(r"^\s{2,}(\S+)\s+(.+)$")


def run_help(binary: str, path: list[str]) -> str:
    """Capture help for a command path.

    Uses `vibium help <path...>` rather than `<path...> --help`. On v26.8.21
    the latter is broken for fill/type/geolocation/sleep, which set
    DisableFlagParsing and surface `--help` as an arity error instead of help
    (upstream #422/#423). `help` takes a different path through cobra and
    works for every command.
    """
    proc = subprocess.run(
        [binary, "help", *path],
        capture_output=True, text=True, timeout=30,
    )
    out = proc.stdout or proc.stderr
    if out.lstrip().startswith("Error:"):
        raise RuntimeError(
            f"help for {' '.join(path) or '<root>'} returned an error, "
            f"not help text: {out.splitlines()[0]}")
    return out


def yaml_str(s: str) -> str:
    """Quote a frontmatter scalar. Descriptions contain colons."""
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"' 


def parse_help(text: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {"Description": []}
    current = "Description"
    for line in text.splitlines():
        m = SECTION_RE.match(line)
        if m:
            current = m.group(1)
            sections.setdefault(current, [])
            continue
        # The trailing "Use ... for more information" hint is not a section.
        if line.startswith('Use "') and current in ("Flags", "Global Flags"):
            continue
        sections.setdefault(current, []).append(line)
    return {k: [ln.rstrip() for ln in v] for k, v in sections.items()}


def clean(lines: list[str]) -> list[str]:
    """Drop leading/trailing blank lines."""
    out = list(lines)
    while out and not out[0].strip():
        out.pop(0)
    while out and not out[-1].strip():
        out.pop()
    return out


def mdx_escape(s: str) -> str:
    """Make prose safe for MDX.

    `<select>` and `input[type=file]` appear verbatim in vibium's help text;
    unescaped, MDX parses the first as a JSX tag and fails the build. Curly
    braces are MDX expression delimiters and need the same treatment.
    """
    return s.replace("<", "&lt;").replace(">", "&gt;").replace("{", "&#123;").replace("}", "&#125;")


def parse_flags(lines: list[str]) -> list[tuple[str, str, str]]:
    flags = []
    for line in clean(lines):
        m = FLAG_RE.match(line)
        if not m:
            continue
        short, long, argtype, desc = m.groups()
        if long == "--help":
            continue  # every command has it; noise on every page
        name = f"`{long}`" + (f", `{short}`" if short else "")
        flags.append((name, f"`{argtype}`" if argtype else "—", desc.strip()))
    return flags


def parse_subcommands(lines: list[str]) -> list[tuple[str, str]]:
    subs = []
    for line in clean(lines):
        m = SUBCMD_RE.match(line)
        if m:
            subs.append((m.group(1), m.group(2).strip()))
    return subs


def render_sub(cmd: str, sub: str, sections: dict[str, list[str]]) -> list[str]:
    """A subcommand's own synopsis, flags and examples, nested under its parent."""
    desc_lines = clean(sections.get("Description", []))
    summary = desc_lines[0] if desc_lines else ""
    usage = [ln.strip() for ln in clean(sections.get("Usage", []))
             if ln.strip() and not ln.strip().endswith("[command]")]
    usage = [u.replace(" [flags]", "") for u in usage]
    flags = parse_flags(sections.get("Flags", []))
    examples = clean(sections.get("Examples", []))

    out = [f"### `vibium {cmd} {sub}`", ""]
    if summary:
        out += [mdx_escape(summary) + ("." if not summary.endswith(".") else ""), ""]
    out += ["```"] + (usage or [f"vibium {cmd} {sub}"]) + ["```", ""]
    if flags:
        out += ["| Flag | Argument | Description |", "| --- | --- | --- |"]
        out += [f"| {n} | {a} | {mdx_escape(d)} |" for n, a, d in flags]
        out += [""]
    if examples:
        out += ["```sh"] + [ln[2:] if ln.startswith("  ") else ln for ln in examples]
        out += ["```", ""]
    return out


def render(cmd: str, sections: dict[str, list[str]], binary: str,
           version: str, cat_label: str, subhelp: dict[str, dict] | None = None) -> str:
    desc_lines = clean(sections.get("Description", []))
    summary = desc_lines[0] if desc_lines else ""
    body = "\n".join(desc_lines[1:]).strip()

    usage = [ln.strip() for ln in clean(sections.get("Usage", []))
             if ln.strip() and not ln.strip().endswith("[command]")]
    usage = [u.replace(" [flags]", "") for u in usage]

    subs = parse_subcommands(sections.get("Available Commands", []))
    flags = parse_flags(sections.get("Flags", []))
    examples = clean(sections.get("Examples", []))

    out: list[str] = []
    out.append("---")
    out.append(f"title: {yaml_str(f'vibium {cmd}')}")
    out.append(f"sidebar_label: {cmd}")
    out.append(f"description: {yaml_str(summary)}")
    out.append("---")
    out.append("")
    out.append(f"# vibium {cmd}")
    out.append("")
    out.append(mdx_escape(summary) + ("." if summary and not summary.endswith(".") else ""))
    out.append("")
    out.append(":::info[Generated reference]")
    out.append(f"Derived from `vibium help {cmd}` at **{version}**. The examples below are the")
    out.append("command's own built-in samples, not captured terminal output. Pages marked")
    out.append("*Verified* instead carry output from a live browser run.")
    out.append(":::")
    out.append("")

    if body:
        out.append(mdx_escape(body))
        out.append("")

    out.append("## Synopsis")
    out.append("")
    out.append("```")
    out.extend(usage or [f"vibium {cmd}"])
    out.append("```")
    out.append("")

    if flags:
        out.append("## Flags")
        out.append("")
        out.append("| Flag | Argument | Description |")
        out.append("| --- | --- | --- |")
        for name, argtype, fdesc in flags:
            out.append(f"| {name} | {argtype} | {mdx_escape(fdesc)} |")
        out.append("")
        out.append("Global flags apply as well — see [Global flags](/docs/global-flags).")
        out.append("")

    if examples:
        out.append("## Examples")
        out.append("")
        out.append("```sh")
        for line in examples:
            out.append(line[2:] if line.startswith("  ") else line)
        out.append("```")
        out.append("")

    if subs:
        out.append("## Subcommands")
        out.append("")
        out.append("| Subcommand | Description |")
        out.append("| --- | --- |")
        for name, sdesc in subs:
            out.append(f"| [`vibium {cmd} {name}`](#vibium-{cmd}-{name}) | {mdx_escape(sdesc)} |")
        out.append("")
        for name, _ in subs:
            if subhelp and name in subhelp:
                out.extend(render_sub(cmd, name, subhelp[name]))

    out.append("## See also")
    out.append("")
    out.append(f"- [Command reference](/docs/commands) — all commands, grouped by purpose.")
    out.append(f"- [{cat_label}](/docs/commands#{cat_label.lower().replace(' & ', '--').replace(' ', '-')}) — related commands.")
    out.append("")
    return "\n".join(out)


def render_index(summaries: dict[str, str], version: str) -> str:
    out = ["---", "title: \"Command reference\"", "sidebar_label: Overview",
           "sidebar_position: 0",
           "description: Every vibium CLI command, grouped by purpose.",
           "---", "",
           "# Command reference", "",
           f"Every command the vibium binary exposes at **{version}** — "
           f"all {len(summaries)} of them, grouped by purpose.", "",
           ":::note[How this reference is built]",
           "Pages marked *Verified* carry real terminal output captured from a live",
           "browser. The rest are generated from the binary's own `--help` text by",
           "[`scripts/gen_pages.py`](https://github.com/lana-20/vibium-docs), so the",
           "reference can be re-derived whenever vibium ships a new release.",
           ":::", ""]
    for _, label, cmds in CATEGORIES:
        out += [f"## {label}", "", "| Command | Description |", "| --- | --- |"]
        for c in cmds:
            mark = " *(Verified)*" if c in CURATED else ""
            out.append(f"| [`vibium {c}`](/docs/commands/{c}){mark} "
                       f"| {mdx_escape(summaries.get(c, ''))} |")
        out.append("")
    out += ["## Conventions", "",
            "- Arguments shown as `<x>` are required; `[x]` are optional.",
            "- `@eN` always refers to a numeric element reference returned by",
            "  [`map`](/docs/commands/map) or [`find`](/docs/commands/find).",
            "- All commands share a single browser and daemon, so state persists",
            "  across invocations.",
            "- Output is plain text on stdout unless a `-o` flag names a file, or",
            "  the global `--json` flag is set — see [Global flags](/docs/global-flags).",
            "",
            "## Running without installing", "",
            "Every command works through `npx`, with no global install:", "",
            "```sh", "npx -y vibium go https://example.com", "npx -y vibium map",
            "npx -y vibium screenshot -o page.png", "```", "",
            "For a session-wide alias:", "",
            "```sh", "alias vibium='npx -y vibium'", "```", ""]
    return "\n".join(out)


def render_global_flags(root_help: str, version: str) -> str:
    sections = parse_help(root_help)
    flags = parse_flags(sections.get("Flags", []))
    out = ["---", "title: Global flags", "sidebar_position: 2",
           "description: Flags accepted by every vibium command.",
           "---", "", "# Global flags", "",
           f"Accepted by every command at **{version}**. Several are also settable",
           "through the environment, which is usually the better choice in CI.", "",
           "| Flag | Argument | Description |", "| --- | --- | --- |"]
    out += [f"| {n} | {a} | {mdx_escape(d)} |" for n, a, d in flags]
    out += ["", "## Notes", "",
            "- `--json` is honoured by most commands but not all. The gap is tracked",
            "  upstream in [vibium#451](https://github.com/VibiumDev/vibium/issues/451).",
            "- `--headless` is a persistent root flag; `vibium mcp` redeclared it,",
            "  which is tracked in [vibium#452](https://github.com/VibiumDev/vibium/issues/452).",
            "- `--verbose` is accepted everywhere but has no effect on commands that",
            "  delegate to the daemon.", ""]
    return "\n".join(out)


README_BEGIN = "<!-- BEGIN COMMAND STATUS -->"
README_END = "<!-- END COMMAND STATUS -->"


def gh_escape(s: str) -> str:
    """GitHub renders raw tags in README tables as HTML; `<select>` would vanish."""
    return s.replace("<", "&lt;").replace(">", "&gt;")


def render_status_block(summaries: dict[str, str], version: str) -> str:
    """The verified/generated tracker, written into README.md between markers.

    Generated from the same CATEGORIES and CURATED that drive the pages, so the
    tracker cannot drift from what the site actually ships.
    """
    total = len(summaries)
    verified = sorted(CURATED)
    out = [README_BEGIN, "",
           f"**{len(verified)} of {total} verified** — "
           f"{total - len(verified)} still generated from `--help`. "
           f"Measured against `{version}`.", ""]
    for _, label, cmds in CATEGORIES:
        done = sum(1 for c in cmds if c in CURATED)
        out += [f"<details{' open' if done else ''}>",
                f"<summary><strong>{label}</strong> — {done}/{len(cmds)} verified</summary>",
                "", "| | Command | Description |", "| --- | --- | --- |"]
        for c in cmds:
            mark = "x" if c in CURATED else " "
            out.append(f"| [{mark}] | [`{c}`](https://lana-20.github.io/vibium-docs/docs/commands/{c}) "
                       f"| {gh_escape(summaries.get(c, ''))} |")
        out += ["", "</details>", ""]
    out.append(README_END)
    return "\n".join(out)


def update_readme(summaries: dict[str, str], version: str) -> bool:
    readme = Path("README.md")
    if not readme.exists():
        return False
    text = readme.read_text()
    if README_BEGIN not in text or README_END not in text:
        return False
    head, rest = text.split(README_BEGIN, 1)
    _, tail = rest.split(README_END, 1)
    readme.write_text(head + render_status_block(summaries, version) + tail)
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bin", default="vibium")
    ap.add_argument("--out", default="docs/commands")
    args = ap.parse_args()

    version = subprocess.run([args.bin, "--version"], capture_output=True,
                             text=True).stdout.strip() or "unknown"

    root = run_help(args.bin, [])
    listed = []
    in_cmds = False
    for line in root.splitlines():
        if line.startswith("Available Commands:"):
            in_cmds = True
            continue
        if in_cmds:
            if line.startswith("Flags:"):
                break
            if line.strip():
                listed.append(line.split()[0])

    categorized = {c for _, _, cmds in CATEGORIES for c in cmds}
    missing = sorted(set(listed) - categorized)
    stale = sorted(categorized - set(listed))
    if missing:
        print(f"ERROR: uncategorized commands in {version}: {missing}", file=sys.stderr)
        return 1
    if stale:
        print(f"ERROR: categorized but gone from {version}: {stale}", file=sys.stderr)
        return 1

    label_of = {c: label for _, label, cmds in CATEGORIES for c in cmds}
    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)

    written = skipped = 0
    subs_total = [0]
    summaries: dict[str, str] = {}
    for cmd in listed:
        sections = parse_help(run_help(args.bin, [cmd]))
        desc = clean(sections.get("Description", []))
        summaries[cmd] = desc[0] if desc else ""
        if cmd in CURATED:
            skipped += 1
            continue
        subhelp = {
            name: parse_help(run_help(args.bin, [cmd, name]))
            for name, _ in parse_subcommands(sections.get("Available Commands", []))
        }
        subs_total[0] += len(subhelp)
        page = render(cmd, sections, args.bin, version, label_of[cmd], subhelp)
        (outdir / f"{cmd}.mdx").write_text(page)
        written += 1

    (outdir / "index.mdx").write_text(render_index(summaries, version))
    Path(outdir).parent.joinpath("global-flags.mdx").write_text(
        render_global_flags(root, version))

    readme_done = update_readme(summaries, version)

    print(f"{version}: {len(listed)} commands — {written} generated "
          f"({subs_total[0]} subcommands documented inline), "
          f"{skipped} curated left untouched"
          + (", README tracker updated" if readme_done else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
