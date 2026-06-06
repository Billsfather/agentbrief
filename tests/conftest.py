from __future__ import annotations

from pathlib import Path
import re
import shutil

import pytest


@pytest.fixture
def workspace_tmp(request) -> Path:
    safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", request.node.name)
    path = Path.cwd() / "pytest_tmp" / safe_name
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)
    return path

