import sys
import os
sys.path.append(os.getcwd())

import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt


from streamlit_app.common.theme import apply_theme
from streamlit_app.common.api_client import crop_predict
from streamlit_app.common.image_utils import get_crop_image


# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Crop Prediction",
    layout="wide"
)

# =====================================================
# APPLY GLOBAL THEME
# =====================================================
apply_theme("streamlit_app/assets/background/crop_pred.webp")


# =====================================================
# SESSION STATE INIT
# =====================================================
if "predicted_crop" not in st.session_state:
    st.session_state.predicted_crop = None

if "proba_list" not in st.session_state:
    st.session_state.proba_list = None


# =====================================================
# HEADER
# =====================================================
st.title("🌱 Smart Crop Prediction")
st.write(
    "Enter soil and weather parameters to predict the most suitable crop."
)


# =====================================================
# INPUTS — SOIL
# =====================================================
st.subheader("🧪 Soil Nutrients")

c1, c2, c3 = st.columns(3)
with c1:
    nitrogen = st.slider("Nitrogen (N)", 0, 150, 90)
with c2:
    phosphorus = st.slider("Phosphorus (P)", 0, 150, 40)
with c3:
    potassium = st.slider("Potassium (K)", 0, 150, 40)


# =====================================================
# INPUTS — WEATHER
# =====================================================
st.subheader("🌦️ Weather Conditions")

c4, c5, c6, c7 = st.columns(4)
with c4:
    temperature = st.slider("Temperature (°C)", 0.0, 50.0, 25.0)
with c5:
    humidity = st.slider("Humidity (%)", 0.0, 100.0, 80.0)
with c6:
    ph = st.slider("Soil pH", 0.0, 14.0, 6.5)
with c7:
    rainfall = st.slider("Rainfall (mm)", 0.0, 300.0, 120.0)

st.markdown("---")


# =====================================================
# SOIL HEALTH INSIGHT
# =====================================================
st.subheader("🧠 Soil Health Insight")

if nitrogen < 30:
    st.warning("Low Nitrogen: Leaf growth may be poor")
elif nitrogen > 120:
    st.info("High Nitrogen: Risk of excessive vegetative growth")
else:
    st.success("Nitrogen level looks balanced")

if ph < 5.5:
    st.warning("Soil is acidic")
elif ph > 7.5:
    st.warning("Soil is alkaline")
else:
    st.success("Soil pH is optimal")


# =====================================================
# PREDICTION
# =====================================================
if st.button("🚜 Predict Best Crop", use_container_width=True):

    features = {
        "nitrogen": nitrogen,
        "phosphorus": phosphorus,
        "potassium": potassium,
        "temperature": temperature,
        "humidity": humidity,
        "ph": ph,
        "rainfall": rainfall,
    }

    with st.spinner("Analyzing soil & climate data..."):
        result = crop_predict(features)

        st.session_state.predicted_crop = result["predicted_label"]
        st.session_state.proba_list = result.get("predicted_proba")


# =====================================================
# RESULTS
# =====================================================
if st.session_state.predicted_crop and st.session_state.proba_list:

    crop = st.session_state.predicted_crop
    proba_list = st.session_state.proba_list

    st.success(f"🌾 **Recommended Crop: {crop.upper()}**")

    # ---- Crop Image ----
    img_b64 = get_crop_image(crop)
    if img_b64:
        st.markdown(
            f"""
            <div style="text-align:center; margin-top:20px;">
                <img src="data:image/jpeg;base64,{img_b64}"
                     style="width:320px; border-radius:16px;
                            box-shadow:0 8px 24px rgba(0,0,0,0.25);"/>
            </div>
            """,
            unsafe_allow_html=True
        )

    # =================================================
    # ANIMATED PROBABILITY CHART
    # =================================================
    st.subheader("📊 Prediction Confidence")

    # ⚠️ Replace this with your actual crop labels if available
    crop_labels = [f"Crop {i+1}" for i in range(len(proba_list))]

    df = pd.DataFrame({
        "Crop": crop_labels,
        "Probability": proba_list
    }).sort_values("Probability", ascending=False)

    import matplotlib.pyplot as plt
    import numpy as np

    # =========================
    # TOP 4 PROBABILITY GRAPH
    # =========================
    st.subheader("📊 Top 4 Crop Prediction Confidence")

    proba_list = st.session_state.proba_list

    # ⚠️ Replace with real crop names if your backend provides them
    crop_labels = [f"Crop {i + 1}" for i in range(len(proba_list))]

    # Create dataframe
    df = pd.DataFrame({
        "Crop": crop_labels,
        "Probability": proba_list
    })

    # Take top 4
    df_top4 = df.sort_values("Probability", ascending=False).head(4)

    # Plot
    fig, ax = plt.subplots(figsize=(7, 4))

    # Pale blue background
    fig.patch.set_facecolor("#e6f2ff")
    ax.set_facecolor("#e6f2ff")

    # Dark green bars
    bars = ax.bar(
        df_top4["Crop"],
        df_top4["Probability"],
        color="#14532d"  # dark green
    )

    # Percentage labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{height:.1%}",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
            color="#0f172a"
        )

    # Axis styling
    ax.set_ylim(0, 1)
    ax.set_ylabel("Probability", fontsize=11)
    ax.set_xlabel("Crop", fontsize=11)
    ax.set_title("Top 4 Most Likely Crops", fontsize=13, fontweight="bold")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    st.pyplot(fig)

    # =================================================
    # EXPLANATION
    # =================================================
    with st.expander("🤔 Why was this crop recommended?"):
        st.write(
            f"""
            **{crop.upper()}** is recommended because:
            - Soil nutrients align with its growth needs
            - Temperature ({temperature}°C) is favorable
            - Rainfall ({rainfall} mm) supports healthy yield
            - Soil pH ({ph}) is within optimal range
            """
        )

else:
    st.info("👆 Enter values and click **Predict Best Crop** to see recommendations.")
