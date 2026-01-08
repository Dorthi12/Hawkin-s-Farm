import sys, os
sys.path.append(os.getcwd())

import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from pathlib import Path
import base64

from streamlit_app.common.api_client import list_products
from streamlit_app.common.theme import apply_theme

# =====================================================
# PAGE CONFIG (MUST BE FIRST)
# =====================================================
st.set_page_config(
    page_title="Products",
    layout="wide"
)

# =====================================================
# APPLY GLOBAL THEME
# =====================================================
apply_theme("streamlit_app/assets/background/products.avif")

# =====================================================
# CONSTANTS
# =====================================================
CROPS_DIR = Path("streamlit_app/assets/crops")
DEFAULT_IMAGE = "https://via.placeholder.com/600x400?text=No+Image"

# =====================================================
# IMAGE RESOLUTION (LOCAL FIRST)
# =====================================================
def resolve_product_image(row: dict):
    """
    Resolve product image using local assets/crops folder.
    Falls back safely if image missing.
    """
    category = (row.get("category") or row.get("crop") or "").lower().strip()

    if category:
        img_path = CROPS_DIR / f"{category}.jpg"
        if img_path.exists():
            with open(img_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            return f"data:image/jpeg;base64,{b64}"

    return DEFAULT_IMAGE

# =====================================================
# PRODUCT NAME RESOLUTION
# =====================================================
def get_ui_name(row: dict):
    if row.get("display_name"):
        return row["display_name"]
    if row.get("name"):
        return row["name"]
    if row.get("product_name"):
        return row["product_name"]
    if row.get("title"):
        return row["title"]
    if row.get("category"):
        return row["category"].title()
    return "Agricultural Product"

# =====================================================
# HEADER
# =====================================================
st.markdown("## 📦 Farm Products")
st.caption("Explore available agricultural products")

# =====================================================
# LOAD DATA
# =====================================================
products = list_products()
df = pd.DataFrame(products)

if df.empty:
    st.info("No products available.")
    st.stop()

# =====================================================
# FILTERS
# =====================================================
c1, c2 = st.columns(2)

with c1:
    search = st.text_input("🔍 Search by name or category")
    if search:
        df = df[
            df["display_name"].str.contains(search, case=False, na=False)
            | df["category"].str.contains(search, case=False, na=False)
        ]

with c2:
    categories = ["All"] + sorted(df["category"].dropna().unique().tolist())
    selected_category = st.selectbox("Filter by category", categories)
    if selected_category != "All":
        df = df[df["category"] == selected_category]

st.markdown("---")

# =====================================================
# DISPLAY GRID
# =====================================================
cols = st.columns(3)

for i, row in df.iterrows():

    img_src = resolve_product_image(row)
    name = get_ui_name(row)
    sku = row.get("sku", "")
    crop = row.get("category") or row.get("crop") or ""

    with cols[i % 3]:
        components.html(
            f"""
            <div style="
                background:#0B3F43;
                padding:16px;
                border-radius:16px;
                box-shadow:0 8px 22px rgba(11,63,67,0.55);
                margin-bottom:20px;
                color:#ffffff;
                transition:
                    transform 0.25s ease,
                    box-shadow 0.25s ease,
                    filter 0.25s ease;
            "
            onmouseover="
                this.style.transform='scale(1.03)';
                this.style.boxShadow='0 14px 36px rgba(11,63,67,0.75)';
                this.style.filter='brightness(1.05)';
            "
            onmouseout="
                this.style.transform='scale(1)';
                this.style.boxShadow='0 8px 22px rgba(11,63,67,0.55)';
                this.style.filter='brightness(1)';
            "
            >

                <img src="{img_src}"
                     style="
                        width:100%;
                        height:180px;
                        object-fit:cover;
                        border-radius:12px;
                        margin-bottom:12px;
                        background:#083344;
                     "
                />

                <div style="
                    font-size:1.05rem;
                    font-weight:600;
                    color:#D1FAE5;
                    margin-bottom:4px;
                ">
                    {name}
                </div>

                <div style="
                    font-size:0.75rem;
                    color:#B2DFDB;
                    margin-bottom:10px;
                ">
                    Code: {sku}
                </div>

                <span style="
                    display:inline-block;
                    background:#134E4A;
                    color:#ECFEFF;
                    padding:4px 12px;
                    border-radius:999px;
                    font-size:0.75rem;
                ">
                    {crop.title()}
                </span>

            </div>
            """,
            height=340,
        )
