"""
Pensare OS — Vercel Serverless Entry Point

Set env var PENSARE_WORKSPACE to the mounted volume path in Vercel.
Note: the heartbeat daemon and claude CLI are not available in Vercel;
the API serves read-only views of files committed to the repo.
"""

import sys
from pathlib import Path

# Allow importing server.py from dashboard/
sys.path.insert(0, str(Path(__file__).parent.parent / "dashboard"))

from server import app  # noqa: E402 — path must be set first
