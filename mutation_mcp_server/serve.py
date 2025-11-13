# mutation_mcp_server/serve.py
# pip install fastmcp uvicorn fastapi

from pathlib import Path
import subprocess, json
from fastmcp import FastMCP
import os, sys, shlex, platform, time
from datetime import datetime
import html
import re
import yaml
from fastapi.staticfiles import StaticFiles  # works with Starlette/FastAPI under the hood

APP_NAME = "mutation-tester"

ROOT = Path(__file__).resolve().parents[1]
PYTESTER = ROOT / "PythonTester" / "Main.py"
RUNS_DIR = ROOT / ".mutant_runs"

# This will be the base used in the link we return to Agent Mode
# On the VM, set this env var:
#   export BASE_EXTERNAL_URL="http://mut-capstone.csse.rose-hulman.edu:8000"
BASE_EXTERNAL_URL = os.environ.get("BASE_EXTERNAL_URL", "http://localhost:8000")

mcp = FastMCP(APP_NAME)

# Let FastMCP build the HTTP MCP app (this exposes /mcp correctly)
app = mcp.http_app()

# Make sure the runs directory exists
RUNS_DIR.mkdir(parents=True, exist_ok=True)

# Serve files from the project root so that
#   http://<host>:8000/files/.mutant_runs/<run_id>/stdout.html
# can be opened in a browser.
app.mount("/files", StaticFiles(directory=ROOT), name="files-root")

ANSI_RE = re.compile(r"\x1b\[(?P<codes>[\d;]*)m")

# Map SGR codes to CSS
COLOR_MAP = {
    "31": "color:#800000",  # red (ERROR)
    "32": "color:#008000",  # green (Correct)
    "33": "color:#B8860B",  # yellow (Timeout)
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
        out = []
        open_span = False
        pos = 0

        for m in ANSI_RE.finditer(s):
            # write text before this match
            if m.start() > pos:
                out.append(s[pos:m.start()])

            codes = [c for c in m.group("codes").split(";") if c] or ["0"]

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
                else:
                    continue

            if applied_style is not None:
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


def update_config_yaml(root: Path, file_source: str, test_source: str) -> bool:
    """Update config.yaml with the provided file and test directories."""
    config_path = root / "PythonTester" / "config.yaml"

    try:
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f) or {}
        else:
            config = {}

        config["file_source"] = file_source
        config["test_source"] = test_source

        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump(config, f, sort_keys=False)

        print(f"Updated {config_path} with new file/test directories.")
        return True
    except Exception as e:
        print(f"Error updating config.yaml: {e}")
        return False


@mcp.tool
def run_mutation_tests(args: str = "", cwd: str = "PythonTester", timeout_seconds: int = 1000) -> dict:
    """
    Run PythonTester/Main.py with raw CLI args; save HTML on the VM and return a browser-viewable link.
    """
    # Normalize timeout
    try:
        timeout_s = int(float(timeout_seconds))
    except Exception:
        timeout_s = 5

    ROOT = Path(__file__).resolve().parents[1]
    PYTESTER = ROOT / "PythonTester" / "Main.py"
    RUNS_DIR = ROOT / ".mutant_runs"

    # Parse args for -f / -t so we can keep config.yaml in sync
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
        # ensure we can kill the whole group on timeout
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

    # This is the link you can click in a browser
    view_url = f"{BASE_EXTERNAL_URL}/files/.mutant_runs/{run_id}/stdout.html"

    summary = {
        "run_id": run_id,
        "returncode": rc,
        "stdout_path": str(stdout_html_path.resolve()),
        "stderr_path": str(stderr_path.resolve()),
        "view_url": view_url,
        "timestamp_end": time.time(),
    }

    (out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    # Agent Mode can show this text, and the link will be clickable in the UI
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

