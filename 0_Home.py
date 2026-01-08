import streamlit as st
from streamlit_app.common.theme import apply_theme

# =====================================================
# PAGE CONFIG (MUST BE FIRST)
# =====================================================
st.set_page_config(
    page_title="Hawkins Farm",
    layout="wide"
)

# =====================================================
# APPLY GLOBAL THEME
# =====================================================
apply_theme("streamlit_app/assets/background/bg.jpg")

# =====================================================
# HOME PAGE CSS
# =====================================================
st.markdown(
    """
    <style>
    /* =========================
       HERO SECTION
       ========================= */
    .home-hero {
        position: relative;
        z-index: 2;
        background: linear-gradient(
            to right,
            rgba(0,0,0,0.60),
            rgba(0,0,0,0.30)
        );
        padding: 3rem 3.2rem;
        border-radius: 24px;
        margin-bottom: 3rem;
    }

    .home-hero h1 {
        color: #ffffff !important;
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 0.75rem;
    }

    .home-hero p {
        color: #e5e7eb !important;
        font-size: 1.1rem;
        max-width: 900px;
        line-height: 1.7;
    }

    /* =========================
       METRIC VISIBILITY (FINAL)
       ========================= */
    div[data-testid="metric-container"] {
        background: rgba(0, 0, 0, 0.45) !important;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.15) !important;
        padding: 1.2rem;
    }

    [data-testid="stMetricLabel"] {
        color: #e5e7eb !important;
        font-weight: 600 !important;
        opacity: 1 !important;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        opacity: 1 !important;
    }

    [data-testid="stMetricDelta"] {
        color: #22c55e !important;
        font-weight: 600 !important;
        opacity: 1 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================
# HERO CONTENT (TITLE IS HERE — NOT GONE)
# =====================================================
st.markdown(
    """
    <div class="home-hero">
        <h1>🌾 Hawkins Farm – Smart Agriculture Platform</h1>
        <p>
            AI-powered platform to help farmers make informed decisions
            using data and machine learning.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# =====================================================
# METRICS
# =====================================================
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🌱 Crop Recommendation", "ML-based", "Active")

with col2:
    st.metric("💰 Price Estimation", "AI-powered", "Active")

with col3:
    st.metric("📦 Product Insights", "Data-driven", "Active")

st.markdown("---")

# =====================================================
# FEATURES
# =====================================================
st.subheader("🚀 What you can do")

st.markdown(
    """
    - Predict the best crop based on soil & weather  
    - Estimate market price of agricultural products  
    - Get product recommendations using ML  
    - Explore farm products database  
    """
)

st.info("Use the sidebar to navigate through features.")
