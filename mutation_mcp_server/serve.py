# mutation_mcp_server/serve.py
# pip install fastmcp

from pathlib import Path
import subprocess, uuid, json
from fastmcp import FastMCP   
import os, sys, shlex, platform, time
from datetime import datetime
import html
import re

APP_NAME = "mutation-tester"
ROOT = Path(__file__).resolve().parents[1]
PYTESTER = ROOT / "PythonTester" / "Main.py"
RUNS_DIR = ROOT / ".mutant_runs"

mcp = FastMCP(APP_NAME)   

ANSI_RE = re.compile(r"\x1b\[(?P<codes>[\d;]*)m")

# Map SGR codes to CSS
COLOR_MAP = {
    "31": "color:#800000",  # red (ERROR)
    "32": "color:#008000",  # green (Correct)
    "33": "color:#B8860B", # yellow (Timeout)
}

def ansi_to_html_basic(ansi_text: str, out_path: Path) -> bool:
    """
    Convert ANSI-colored text to standalone HTML using <pre> with exact newlines.
    """
    try:
        # Normalize line endings
        s = ansi_text.replace("\r\n", "\n").replace("\r", "\n")

        # Escape HTML so raw text is safe
        s = html.escape(s)

        # Replace ANSI SGR sequences with <span> and </span>
        #    We keep at most one open span at a time.
        out = []
        open_span = False

        pos = 0
        for m in ANSI_RE.finditer(s):
            # write text before this match
            if m.start() > pos:
                out.append(s[pos:m.start()])

            codes = [c for c in m.group("codes").split(";") if c] or ["0"]

            # handle only first meaningful code in the group
            applied_style = None
            for code in codes:
                if code == "0":  # reset
                    if open_span:
                        out.append("</span>")
                        open_span = False
                    applied_style = None
                    break
                elif code in COLOR_MAP:
                    applied_style = COLOR_MAP[code]
                    # keep scanning in case a later "0" exists in same sequence
                else:
                    # ignore other codes (bold, etc) — extend as needed
                    continue

            if applied_style is not None:
                # close any previous open span
                if open_span:
                    out.append("</span>")
                    open_span = False
                out.append(f'<span style="{applied_style}">')
                open_span = True

            pos = m.end()

        # tail
        if pos < len(s):
            out.append(s[pos:])

        if open_span:
            out.append("</span>")

        # Wrap in a <pre> that preserves newlines/spacing exactly
        html_doc = (
            "<!doctype html><meta charset='utf-8'>"
            "<pre style=\"font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;"
            "font-size: 12px; line-height: 1.35; white-space: pre; margin: 0\">"
            + "".join(out) +
            "</pre>"
        )

        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html_doc, encoding="utf-8")
        return True
    except Exception:
        return False


@mcp.tool                       
def run_mutation_tests(args: str = "", cwd: str = "PythonTester", timeout_seconds: int = 1000) -> dict:
    """Run PythonTester/Main.py with raw CLI args; returns paths & metadata."""
    # Normalize timeout (handles strings like "5")
    try:
        timeout_s = int(float(timeout_seconds))
    except Exception:
        timeout_s = 5

    ROOT = Path(__file__).resolve().parents[1]
    PYTESTER = ROOT / "PythonTester" / "Main.py"
    RUNS_DIR = ROOT / ".mutant_runs"

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    out = RUNS_DIR / f"run_{timestamp}"
    out.mkdir(parents=True, exist_ok=True)
    run_id = out.name

    cmd = [sys.executable, "-u", str(PYTESTER)] + shlex.split(args)
    env = os.environ.copy()
    env.setdefault("PYTHONIOENCODING", "utf-8")
    env.setdefault("PYTHONUNBUFFERED", "1")

    # Breadcrumb for debugging
    (out / "debug.json").write_text(json.dumps({
        "cmd": cmd,
        "cwd": str((ROOT / cwd).resolve()),
        "python": sys.executable,
        "timeout_seconds": timeout_s,
        "timestamp_start": time.time()
    }, indent=2))

    stdout_html_path = out / "stdout.html"
    stderr_path = out / "stderr.txt"
    summary_path = out / "summary.json"

    # Launch without shell to avoid Windows hangs; capture output; deny stdin
    creation = subprocess.CREATE_NEW_PROCESS_GROUP if platform.system() == "Windows" else 0
    proc = subprocess.Popen(
        cmd,
        cwd=(ROOT / cwd),
        env=env,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=False,
        creationflags=creation
    )

    try:
        stdout, stderr = proc.communicate(timeout=timeout_s)
        rc = proc.returncode
    except subprocess.TimeoutExpired:
        # Kill the whole process tree on timeout, windows was causing me issues here
        if platform.system() == "Windows":
            subprocess.run(
                ["taskkill", "/PID", str(proc.pid), "/T", "/F"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
        else:
            try:
                os.killpg(os.getpgid(proc.pid), 9)
            except Exception:
                proc.kill()
        rc = -1
        stdout, stderr = "", f"[Timed out after {timeout_s}s]\n"
    # writes output to .mutantruns folder with debug info too
    ansi_to_html_basic(stdout or "", stdout_html_path)
    stderr_path.write_text(stderr or "")

    summary = {
        "run_id": run_id,
        "returncode": rc,
        "stdout_path": str(stdout_html_path.resolve()),
        "stderr_path": str(stderr_path.resolve()),
        "timestamp_end": time.time()
    }
    summary_path.write_text(json.dumps(summary, indent=2))
    return summary

if __name__ == "__main__":
    # runs an HTTP MCP server on port 8000 at /mcp/
    mcp.run(transport="http", host="0.0.0.0", port=8000)           
