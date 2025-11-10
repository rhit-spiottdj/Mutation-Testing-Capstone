# mutation_mcp_server/serve.py
# pip install fastmcp fastapi uvicorn pyyaml

from pathlib import Path
import subprocess, json
from fastmcp import FastMCP
import os, sys, shlex, platform, time
from datetime import datetime
import html
import re
import base64
import yaml

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import socket

APP_NAME = "mutation-tester"
ROOT = Path(__file__).resolve().parents[1]
PYTESTER = ROOT / "PythonTester" / "Main.py"
RUNS_DIR = ROOT / ".mutant_runs"

# Public URL used for links returned to clients (set this in the VM env)
# e.g. export BASE_EXTERNAL_URL="http://mut-capstone.csse.rose-hulman.edu:8000"
BASE_EXTERNAL_URL = os.environ.get("BASE_EXTERNAL_URL", f"http://{socket.getfqdn()}:8000")

mcp = FastMCP(APP_NAME)

ANSI_RE = re.compile(r"\x1b\[(?P<codes>[\d;]*)m")
COLOR_MAP = {
    "31": "color:#800000",  # red (ERROR)
    "32": "color:#008000",  # green (Correct)
    "33": "color:#B8860B",  # yellow (Timeout)
}

def ansi_to_html_basic(ansi_text: str, out_path: Path) -> bool:
    try:
        s = ansi_text.replace("\r\n", "\n").replace("\r", "\n")
        s = html.escape(s)

        out = []
        open_span = False
        pos = 0
        for m in ANSI_RE.finditer(s):
            if m.start() > pos:
                out.append(s[pos:m.start()])
            codes = [c for c in m.group("codes").split(";") if c] or ["0"]
            applied_style = None
            for code in codes:
                if code == "0":
                    if open_span:
                        out.append("</span>")
                        open_span = False
                    applied_style = None
                    break
                elif code in COLOR_MAP:
                    applied_style = COLOR_MAP[code]
            if applied_style is not None:
                if open_span:
                    out.append("</span>")
                    open_span = False
                out.append(f'<span style="{applied_style}">')
                open_span = True
            pos = m.end()
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
    """Run mutation tests, save HTML on VM, and return a browser-viewable link."""
    try:
        timeout_s = int(float(timeout_seconds))
    except Exception:
        timeout_s = 5

    # Parse optional -f/--files and -t/--tests and persist to config.yaml
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

    cmd = [sys.executable, "-u", str(PYTESTER)] + args_list
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
    stderr_url = f"{BASE_EXTERNAL_URL}/files/.mutant_runs/{run_id}/stderr.txt"

    summary = {
        "run_id": run_id,
        "returncode": rc,
        "stdout_path": str(stdout_html_path.resolve()),
        "stderr_path": str(stderr_path.resolve()),
        "view_url": view_url,
        "stderr_url": stderr_url,
        "timestamp_end": time.time(),
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    # Return structured content so Agent Mode can show the link
    return {
        "run_id": run_id,
        "returncode": rc,
        "stdout_path": summary["stdout_path"],
        "stderr_path": summary["stderr_path"],
        "view_url": view_url,
        "structured_content": {
            "type": "text",
            "text": f"Mutation test finished (rc={rc}).\nOpen results:\n{view_url}",
        },
    }

# ---------- ASGI app that serves both MCP and static files ----------
app = FastAPI()

# Serve the entire repo at /files so .mutant_runs is browsable
app.mount("/files", StaticFiles(directory=str(ROOT), html=False), name="files")

# Mount the MCP server under /mcp (requires fastmcp >= 0.3 providing asgi_app)
try:
    asgi_mcp = mcp.asgi_app()
    app.mount("/mcp", asgi_mcp)
except AttributeError:
    # If your fastmcp version lacks asgi_app(), you can still run MCP only by
    # calling mcp.run(...) in __main__, but then /files won't be available.
    asgi_mcp = None

@app.get("/health")
def health():
    return {"ok": True, "base_external_url": BASE_EXTERNAL_URL}

if __name__ == "__main__":
    # IMPORTANT: run the unified ASGI app so /files works.
    # If asgi_mcp is unavailable, fall back to MCP-only (no static files).
    if asgi_mcp is not None:
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)
    else:
        mcp.run(transport="http", host="0.0.0.0", port=8000)
