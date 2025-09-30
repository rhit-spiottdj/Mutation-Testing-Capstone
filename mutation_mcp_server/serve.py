# mutation_mcp_server/serve.py
# pip install fastmcp

from pathlib import Path
import subprocess, uuid, json
from fastmcp import FastMCP   
import os, sys, shlex, platform, time

APP_NAME = "mutation-tester"
ROOT = Path(__file__).resolve().parents[1]
PYTESTER = ROOT / "PythonTester" / "Main.py"
RUNS_DIR = ROOT / ".mutant_runs"

mcp = FastMCP(APP_NAME)       

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

    RUNS_DIR.mkdir(exist_ok=True)
    run_id = str(uuid.uuid4())
    out = RUNS_DIR / run_id
    out.mkdir(parents=True, exist_ok=True)

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

    stdout_path = out / "stdout.txt"
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
    stdout_path.write_text(stdout or "")
    stderr_path.write_text(stderr or "")

    summary = {
        "run_id": run_id,
        "returncode": rc,
        "stdout_path": str(stdout_path.resolve()),
        "stderr_path": str(stderr_path.resolve()),
        "timestamp_end": time.time()
    }
    summary_path.write_text(json.dumps(summary, indent=2))
    return summary

if __name__ == "__main__":
    mcp.run()                   
