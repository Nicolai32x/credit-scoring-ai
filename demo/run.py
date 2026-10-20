"""Start Streamlit with shared code on PYTHONPATH so updates are reloaded."""

import os
from pathlib import Path
import subprocess
import sys


def main():
    root = Path(__file__).resolve().parents[1]
    environment = os.environ.copy()
    existing = environment.get("PYTHONPATH", "")
    environment["PYTHONPATH"] = str(root / "code") + (os.pathsep + existing if existing else "")
    return subprocess.call([
        sys.executable, "-m", "streamlit", "run", str(root / "demo" / "app.py"),
        "--server.address", "127.0.0.1", "--server.headless", "true",
        "--browser.gatherUsageStats", "false", *sys.argv[1:],
    ], cwd=root, env=environment)


if __name__ == "__main__":
    raise SystemExit(main())
