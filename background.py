import base64
from pathlib import Path

def get_base64_bg(path: str):
    bg_file = Path(path)
    with open(bg_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()
