import base64
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

def load_local_image(rel_path: str):
    """
    Load a local image and return base64 string usable in HTML or st.image
    """
    img_path = BASE_DIR / rel_path
    if not img_path.exists():
        return None

    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def get_crop_image(crop_name: str):
    if not crop_name:
        return None

    crop_name = crop_name.lower().strip()
    return load_local_image(f"assets/crops/{crop_name}.jpg")
