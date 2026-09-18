#!/usr/bin/env python3
"""
Auto Preview - Antigravity Kit
==============================
Manages (start/stop/status) the local development server for previewing the application.

Usage:
    python .agent/scripts/auto_preview.py start [port]
    python .agent/scripts/auto_preview.py stop
    python .agent/scripts/auto_preview.py status
"""

import os
import sys
import time
import json
import signal
import argparse
import subprocess
from pathlib import Path

AGENT_DIR = Path(".agent")
PID_FILE = AGENT_DIR / "preview.pid"
LOG_FILE = AGENT_DIR / "preview.log"

def get_project_root():
    return Path(".").resolve()

IS_WINDOWS = sys.platform == "win32"

def is_running(pid):
    # On Windows os.kill(pid, 0) does not probe: it terminates the process.
    if IS_WINDOWS:
        out = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"],
                             capture_output=True, text=True).stdout
        return str(pid) in out
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False

def read_pid_file():
    """preview.pid holds "<pid> <port>" (older versions wrote only the pid)."""
    parts = PID_FILE.read_text().split()
    pid = int(parts[0])
    port = int(parts[1]) if len(parts) > 1 else 3000
    return pid, port

def get_start_command(root):
    pkg_file = root / "package.json"
    if not pkg_file.exists():
        return None
    
    with open(pkg_file, 'r') as f:
        data = json.load(f)
    
    scripts = data.get("scripts", {})
    if "dev" in scripts:
        return ["npm", "run", "dev"]
    elif "start" in scripts:
        return ["npm", "start"]
    return None

def start_server(port=3000):
    if PID_FILE.exists():
        try:
            pid, _ = read_pid_file()
            if is_running(pid):
                print(f"⚠️  Preview already running (PID: {pid})")
                return
        except:
            pass # Invalid PID file

    root = get_project_root()
    cmd = get_start_command(root)
    
    if not cmd:
        print("❌ No 'dev' or 'start' script found in package.json")
        sys.exit(1)
    
    # Add port env var if needed (simple heuristic)
    env = os.environ.copy()
    env["PORT"] = str(port)
    
    print(f"🚀 Starting preview on port {port}...")
    
    AGENT_DIR.mkdir(exist_ok=True)
    with open(LOG_FILE, "w") as log:
        process = subprocess.Popen(
            cmd,
            cwd=str(root),
            stdout=log,
            stderr=log,
            env=env,
            # npm is npm.cmd on Windows and needs the shell there. On macOS/Linux
            # shell=True with a list would run only "npm", without its arguments.
            shell=IS_WINDOWS,
            # own process group, so stop can kill npm together with the dev server it spawned
            start_new_session=not IS_WINDOWS,
        )
    
    PID_FILE.write_text(f"{process.pid} {port}")
    print(f"✅ Preview started! (PID: {process.pid})")
    print(f"   Logs: {LOG_FILE}")
    print(f"   URL: http://localhost:{port}")

def stop_server():
    if not PID_FILE.exists():
        print("ℹ️  No preview server found.")
        return

    try:
        pid, _ = read_pid_file()
        if is_running(pid):
            if IS_WINDOWS:
                subprocess.call(['taskkill', '/F', '/T', '/PID', str(pid)])
            else:
                os.killpg(pid, signal.SIGTERM)  # the whole group: npm and the dev server
            print(f"🛑 Preview stopped (PID: {pid})")
        else:
            print("ℹ️  Process was not running.")
    except Exception as e:
        print(f"❌ Error stopping server: {e}")
    finally:
        if PID_FILE.exists():
            PID_FILE.unlink()

def status_server():
    running = False
    pid = None
    url = "Unknown"
    
    if PID_FILE.exists():
        try:
            pid, port = read_pid_file()
            if is_running(pid):
                running = True
                url = f"http://localhost:{port}"
        except:
            pass
            
    print("\n=== Preview Status ===")
    if running:
        print(f"✅ Status: Running")
        print(f"🔢 PID: {pid}")
        print(f"🌐 URL: {url}")
        print(f"📝 Logs: {LOG_FILE}")
    else:
        print("⚪ Status: Stopped")
    print("===================\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["start", "stop", "status"])
    parser.add_argument("port", nargs="?", default="3000")
    
    args = parser.parse_args()
    
    if args.action == "start":
        start_server(int(args.port))
    elif args.action == "stop":
        stop_server()
    elif args.action == "status":
        status_server()

if __name__ == "__main__":
    main()
