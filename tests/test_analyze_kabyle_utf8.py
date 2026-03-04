import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_analyze_kabyle_survives_cp1252_console() -> None:
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "cp1252"

    proc = subprocess.run(
        [sys.executable, str(ROOT / "analyze_kabyle.py")],
        cwd=str(ROOT),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert proc.returncode == 0, proc.stderr.decode("utf-8", errors="replace")
    output = proc.stdout.decode("utf-8", errors="replace")
    assert "CORPUS:" in output

