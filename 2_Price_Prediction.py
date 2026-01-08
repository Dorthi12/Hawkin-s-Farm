import sys
import os
sys.path.append(os.getcwd())

import streamlit as st
import streamlit.components.v1 as components

from streamlit_app.common.theme import apply_theme
from streamlit_app.common.api_client import (
    price_predict,
    get_price_categories,
    get_price_states
)

# =====================================================
# PAGE CONFIG (MUST BE FIRST)
# =====================================================
st.set_page_config(
    page_title="Price Prediction",
    layout="wide"
)

# =====================================================
# APPLY GLOBAL THEME
# =====================================================
apply_theme("streamlit_app/assets/background/price_pred.jpg")

# =====================================================
# HEADER
# =====================================================
st.title("💰 Smart Price Prediction")
st.caption("Estimate market price using AI-based demand & seasonality model")

# =====================================================
# INPUTS
# =====================================================
c1, c2, c3 = st.columns(3)

with c1:
    mrp = st.number_input("Base MRP (₹)", 0.0, 5000.0, 100.0)

with c2:
    units = st.number_input("Units Sold", 0.0, 10000.0, 200.0)

with c3:
    month = st.selectbox("Month", list(range(1, 13)))

c4, c5 = st.columns(2)

with c4:
    category = st.selectbox(
        "Category",
        get_price_categories()
    )

with c5:
    state = st.selectbox(
        "State",
        get_price_states()
    )

st.markdown("---")

# =====================================================
# PREDICT
# =====================================================
if st.button("📈 Predict Price", use_container_width=True):
    with st.spinner("Running price model..."):
        try:
            result = price_predict(mrp, month, units, category, state)
            price = result["predicted_price"]

            price = round(price, 2)
            min_price = round(price * 0.92, 2)
            max_price = round(price * 1.08, 2)

            components.html(
                f"""
                <style>
                    #price-card {{
                        background:#014760;
                        padding:28px;
                        border-radius:22px;
                        text-align:center;
                        box-shadow:0 10px 28px rgba(1,71,96,0.55);
                        max-width:420px;
                        margin-top:24px;
                        color:#f8fafc;
                        font-family: Inter, system-ui;
                        transition: 
                            transform 0.25s ease,
                            box-shadow 0.25s ease,
                            filter 0.25s ease;
                    }}

                    #price-card:hover {{
                        transform: translateY(-6px) scale(1.01);
                        box-shadow:
                            0 0 0 1px rgba(34,197,94,0.25),
                            0 14px 40px rgba(34,197,94,0.45);
                        filter: brightness(1.08);
                    }}

                    #price {{
                        font-size:2.8rem;
                        font-weight:700;
                        margin-bottom:6px;
                        transition: text-shadow 0.25s ease;
                    }}

                    #price-card:hover #price {{
                        text-shadow: 0 0 18px rgba(34,197,94,0.65);
                    }}

                    .download-btn {{
                        background:#22c55e;
                        color:white;
                        border:none;
                        padding:10px 18px;
                        border-radius:12px;
                        font-weight:600;
                        cursor:pointer;
                        transition:
                            transform 0.2s ease,
                            box-shadow 0.2s ease,
                            background 0.2s ease;
                    }}

                    .download-btn:hover {{
                        background:#16a34a;
                        transform: scale(1.05);
                        box-shadow: 0 0 16px rgba(34,197,94,0.7);
                    }}
                </style>

                <div id="price-card">
                    <div style="font-size:1.1rem; margin-bottom:8px;">
                        💸 Estimated Market Price
                    </div>

                    <div id="price">₹ 0.00</div>

                    <div style="font-size:0.95rem; opacity:0.9; margin-bottom:14px;">
                        Expected range: ₹ {min_price} – ₹ {max_price}
                    </div>

                    <button class="download-btn" onclick="downloadCard()">
                        📥 Download as Image
                    </button>
                </div>

                <script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js"></script>

                <script>
                    // Count-up animation
                    let target = {price};
                    let current = 0;
                    let step = target / 60;

                    let el = document.getElementById("price");
                    let interval = setInterval(() => {{
                        current += step;
                        if (current >= target) {{
                            current = target;
                            clearInterval(interval);
                        }}
                        el.innerText = "₹ " + current.toFixed(2);
                    }}, 16);

                    function downloadCard() {{
                        html2canvas(document.getElementById("price-card")).then(canvas => {{
                            let link = document.createElement("a");
                            link.download = "price_prediction.png";
                            link.href = canvas.toDataURL();
                            link.click();
                        }});
                    }}
                </script>
                """,
                height=280
            )



        except Exception as e:
            st.error(f"Prediction failed: {e}")
