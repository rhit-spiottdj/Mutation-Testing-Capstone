# mutation_mcp_server/serve.py
# pip install fastmcp

from pathlib import Path
import subprocess, uuid, json
from fastmcp import FastMCP   
import os, sys, shlex, platform, time
from datetime import datetime
import html
import re
import base64, mimetypes
import yaml
# --- add these imports near the top with your others ---
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles


APP_NAME = "mutation-tester"
ROOT = Path(__file__).resolve().parents[1]
PYTESTER = ROOT / "PythonTester" / "Main.py"
RUNS_DIR = ROOT / ".mutant_runs"
BASE_EXTERNAL_URL = os.environ.get("BASE_EXTERNAL_URL", "http://localhost:8000")

app = FastAPI()

results_dir = ROOT / ".mutant_runs"
results_dir.mkdir(parents=True, exist_ok=True)

# Mount at /files (to match your existing link) and also /results as an alias
app.mount("/files", StaticFiles(directory=ROOT), name="files-root")
app.mount("/results", StaticFiles(directory=results_dir), name="results")

mcp = FastMCP(APP_NAME)   

ANSI_RE = re.compile(r"\x1b\[(?P<codes>[\d;]*)m")

# Map SGR codes to CSS
COLOR_MAP = {
    "31": "color:#800000",  # red (ERROR)
    "32": "color:#008000",  # green (Correct)
    "33": "color:#B8860B", # yellow (Timeout)
}

def _b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


def ansi_to_html_str(ansi_text: str) -> str:
    s = ansi_text.replace("\r\n", "\n").replace("\r", "\n")
    s = html.escape(s)
    out, open_span, pos = [], False, 0
    for m in ANSI_RE.finditer(s):
        if m.start() > pos:
            out.append(s[pos:m.start()])
        codes = [c for c in m.group("codes").split(";") if c] or ["0"]
        applied = None
        for code in codes:
            if code == "0":
                if open_span:
                    out.append("</span>")
                    open_span = False
                applied = None
                break
            elif code in COLOR_MAP:
                applied = COLOR_MAP[code]
        if applied is not None:
            if open_span:
                out.append("</span>")
                open_span = False
            out.append(f'<span style="{applied}">')
            open_span = True
        pos = m.end()
    if pos < len(s): out.append(s[pos:])
    if open_span: out.append("</span>")
    return (
        "<!doctype html><meta charset='utf-8'>"
        "<pre style=\"font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;"
        "font-size: 12px; line-height: 1.35; white-space: pre; margin: 0\">"
        + "".join(out) + "</pre>"
    )


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

def update_config_yaml(root: Path, file_source: str, test_source: str):
    """Update config.yaml with the provided file and test directories."""

    config_path = root / "PythonTester" / "config.yaml"

    try:
        # Load existing config
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f) or {}
        else:
            config = {}

        # Update or create keys
        config["file_source"] = file_source
        config["test_source"] = test_source

        # Write it back
        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump(config, f, sort_keys=False)

        print(f"Updated {config_path} with new file/test directories.")
        return True
    except Exception as e:
        print(f"Error updating config.yaml: {e}")
        return False


@mcp.tool
def run_mutation_tests(args: str = "", cwd: str = "PythonTester", timeout_seconds: int = 1000) -> dict:
    """Run mutation tests, save HTML on VM, and return a browser-viewable link."""
    try:
        timeout_s = int(float(timeout_seconds))
    except Exception:
        timeout_s = 5

    ROOT = Path(__file__).resolve().parents[1]
    PYTESTER = ROOT / "PythonTester" / "Main.py"
    RUNS_DIR = ROOT / ".mutant_runs"

    # Parse args for file/test sources
    args_list = shlex.split(args)
    file_dir, test_dir = None, None
    for i, a in enumerate(args_list):
        if a in ("-f", "--files") and i + 1 < len(args_list):
            file_dir = args_list[i + 1]
        elif a in ("-t", "--tests") and i + 1 < len(args_list):
            test_dir = args_list[i + 1]
    if file_dir and test_dir:
        update_config_yaml(ROOT, file_dir, test_dir)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    out = RUNS_DIR / f"run_{timestamp}"
    out.mkdir(parents=True, exist_ok=True)
    run_id = out.name

    cmd = [sys.executable, "-u", str(PYTESTER)] + shlex.split(args)
    env = os.environ.copy()
    env.setdefault("PYTHONIOENCODING", "utf-8")
    env.setdefault("PYTHONUNBUFFERED", "1")

    popen_kwargs = dict(
        cwd=(ROOT / cwd),
        env=env,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=False,
    )
    if platform.system() != "Windows":
        popen_kwargs["preexec_fn"] = os.setsid

    proc = subprocess.Popen(cmd, **popen_kwargs)

    try:
        stdout, stderr = proc.communicate(timeout=timeout_s)
        rc = proc.returncode
    except subprocess.TimeoutExpired:
        if platform.system() != "Windows":
            try:
                os.killpg(os.getpgid(proc.pid), 9)
            except Exception:
                proc.kill()
        rc = -1
        stdout, stderr = "", f"[Timed out after {timeout_s}s]\n"

    stdout_html_path = out / "stdout.html"
    stderr_path = out / "stderr.txt"
    ansi_to_html_basic(stdout or "", stdout_html_path)
    stderr_path.write_text(stderr or "", encoding="utf-8")

    view_url = f"{BASE_EXTERNAL_URL}/files/.mutant_runs/{run_id}/stdout.html"

    summary = {
        "run_id": run_id,
        "returncode": rc,
        "stdout_path": str(stdout_html_path.resolve()),
        "stderr_path": str(stderr_path.resolve()),
        "view_url": view_url,
        "timestamp_end": time.time()
    }

    # Save JSON summary file
    (out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    # --- Return a structured Agent Mode object with the link visible ---
    return {
        "run_id": run_id,
        "returncode": rc,
        "stdout_path": summary["stdout_path"],
        "stderr_path": summary["stderr_path"],
        "view_url": view_url,
        "structured_content": {
            "type": "text",
            "text": f"Mutation test finished.\n\nOpen results here:\n{view_url}",
        },
    }



if __name__ == "__main__":
    # runs an HTTP MCP server on port 8000 at /mcp/
    mcp.run(transport="http", host="0.0.0.0", port=8000)           
