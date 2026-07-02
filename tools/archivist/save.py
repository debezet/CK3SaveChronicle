from __future__ import annotations
from pathlib import Path
import zipfile

def load_gamestate(path: str | Path) -> str:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as z:
            if "gamestate" not in z.namelist():
                raise ValueError("No gamestate in save archive")
            data = z.read("gamestate")
    else:
        data = path.read_bytes()
    return data.decode("utf-8-sig", errors="replace")
