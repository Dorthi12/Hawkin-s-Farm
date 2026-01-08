import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

def crop_predict(features: dict):
    url = f"{BASE_URL}/crop/predict"
    payload = {"features": features}
    r = requests.post(url, json=payload)
    r.raise_for_status()
    return r.json()

import requests

BASE_URL = "http://127.0.0.1:8000"

def price_predict(mrp, month, units_sold, category, state):
    payload = {
        "mrp": mrp,
        "month": month,
        "units_sold": units_sold,
        "category": category,
        "state": state,
    }

    r = requests.post(f"{BASE_URL}/price/predict", json=payload)

    if r.status_code != 200:
        raise Exception(r.text)

    return r.json()


def recommend_by_sku(sku: str, k: int = 8):
    url = f"{BASE_URL}/recommend/sku/{sku}?k={k}"
    r = requests.get(url)
    r.raise_for_status()
    return r.json()

def recommend_for_user(user_id: int, k: int = 10):
    url = f"{BASE_URL}/recommend/user/{user_id}?k={k}"
    r = requests.get(url)
    r.raise_for_status()
    return r.json()

def list_products(limit=50, skip=0):
    url = f"{BASE_URL}/products/?limit={limit}&skip={skip}"
    r = requests.get(url)
    r.raise_for_status()
    return r.json()

import requests

BASE_URL = "http://127.0.0.1:8000"

def get_price_categories():
    r = requests.get(f"{BASE_URL}/price/categories")

    if r.status_code != 200:
        raise Exception(r.text)

    return r.json()["categories"]

def get_price_states():
    r = requests.get(f"{BASE_URL}/price/states")

    if r.status_code != 200:
        raise Exception(r.text)

    return r.json()["states"]
