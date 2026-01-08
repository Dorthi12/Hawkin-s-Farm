import sys
import os
sys.path.append(os.getcwd())

import streamlit as st
import streamlit.components.v1 as components

from streamlit_app.common.theme import apply_theme
from streamlit_app.common.api_client import recommend_by_sku, list_products

from pathlib import Path
import base64

CROPS_DIR = Path("streamlit_app/assets/crops")

def get_product_image(product: dict):
    """
    Resolve product image from local assets/crops folder
    using product category.
    """
    category = product.get("category", "").lower().strip()

    if not category:
        return None

    # Expected filename: banana.jpg, groundnuts.jpg, etc.
    img_path = CROPS_DIR / f"{category}.jpg"

    if not img_path.exists():
        return None

    with open(img_path, "rb") as f:
        img_bytes = f.read()

    b64 = base64.b64encode(img_bytes).decode()

    return f"data:image/jpeg;base64,{b64}"

# =====================================================
# PAGE CONFIG (MUST BE FIRST)
# =====================================================
st.set_page_config(
    page_title="Recommendations",
    layout="wide"
)

# =====================================================
# APPLY GLOBAL THEME
# =====================================================
apply_theme("streamlit_app/assets/background/recommendation.avif")


# =====================================================
# HEADER
# =====================================================
st.title("🧠 Smart Product Recommendations")
st.caption("ML-powered similarity-based recommendations")


# =====================================================
# LOAD PRODUCTS
# =====================================================
products = list_products()
sku_map = {p["sku"]: p["display_name"] for p in products}


# =====================================================
# PRODUCT SELECTION
# =====================================================
selected_sku = st.selectbox(
    "📦 Select a product",
    list(sku_map.keys()),
    format_func=lambda x: sku_map[x]
)


# =====================================================
# RECOMMEND
# =====================================================
if st.button("🔍 Get Recommendations", use_container_width=True):

    with st.spinner("Finding similar products..."):
        try:
            result = recommend_by_sku(selected_sku)
            recs = result.get("recommendations", [])

            st.subheader("🔗 Recommended Products")

            if not recs:
                st.info("No similar products found.")
            else:
                for r in recs:
                    p = r.get("product")
                    if not p:
                        continue

                    score = r.get("score", 0.0)

                    # ---------------- CARD (SAFE HTML) ----------------
                    img = get_product_image(p)

                    img = get_product_image(p)

                    components.html(
                        f"""
                        <div style="
                            background:#0B3F43;
                            padding:16px 18px;
                            border-radius:16px;
                            box-shadow:0 10px 26px rgba(11,63,67,0.55);
                            margin-bottom:18px;
                            color:#ECFEFF;
                            display:flex;
                            align-items:center;
                            gap:14px;
                            transition: transform 0.25s ease, box-shadow 0.25s ease;
                        "
                        onmouseover="
                            this.style.transform='scale(1.04)';
                            this.style.boxShadow='0 16px 36px rgba(11,63,67,0.75)';
                        "
                        onmouseout="
                            this.style.transform='scale(1)';
                            this.style.boxShadow='0 10px 26px rgba(11,63,67,0.55)';
                        "
                        >

                            <!-- IMAGE -->
                            <img src="{img}"
                                 style="
                                    width:56px;
                                    height:56px;
                                    border-radius:12px;
                                    object-fit:cover;
                                    flex-shrink:0;
                                    box-shadow:0 4px 12px rgba(0,0,0,0.35);
                                 " />

                            <!-- TEXT -->
                            <div>
                                <div style="
                                    font-size:1.05rem;
                                    font-weight:600;
                                    color:#D1FAF5;
                                    margin-bottom:4px;
                                ">
                                    {p['display_name']}
                                </div>

                                <div style="font-size:0.9rem;">
                                    Category: {p.get('category', 'N/A')}
                                </div>

                                <div style="font-size:0.9rem;">
                                    Similarity Score: {score:.2f}
                                </div>
                            </div>

                        </div>
                        """,
                        height=110
                    )

        except Exception as e:
            st.error(f"Recommendation failed: {e}")


# =====================================================
# INFO FOOTER
# =====================================================
components.html(
    """
    <div style="
        background:#0A2540;
        padding:16px 20px;
        border-radius:14px;
        margin-top:40px;
        color:#E5EDFF;
        font-size:0.95rem;
        text-align:center;
        line-height:1.6;
        max-width:900px;
        margin-left:auto;
        margin-right:auto;
    ">
        ℹ️ This page provides AI-driven product recommendations based on similarity
        and historical interaction patterns.<br>
        Products are ranked to highlight relevant alternatives and support
        informed decision-making.
    </div>
    """,
    height=120
)
