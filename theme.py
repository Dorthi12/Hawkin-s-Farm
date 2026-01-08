import streamlit as st
from streamlit_app.common.background import get_base64_bg


def apply_theme(bg_path: str | None = None):
    """
    Applies the global Hawkins Farm theme.
    Optional bg_path: path to background image
    """

    bg_img = ""
    if bg_path:
        bg_img = get_base64_bg(bg_path)

    st.markdown(
        f"""
        <style>
        /* =========================
           PAGE BACKGROUND
           ========================= */
        .stApp {{
            {"background-image: url('data:image/webp;base64," + bg_img + "');" if bg_img else ""}
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        

        /* =========================
           REMOVE STREAMLIT HEADER
           ========================= */
        header[data-testid="stHeader"] {{
            background: transparent !important;
            height: 0px;
        }}

        div[data-testid="stToolbar"] {{
            display: none !important;
        }}

        /* =========================
           SIDEBAR (GLOBAL)
           ========================= */
        section[data-testid="stSidebar"] {{
            background: rgba(15, 23, 42, 0.95) !important;
        }}

        section[data-testid="stSidebar"] * {{
            color: #e5e7eb !important;
        }}

        section[data-testid="stSidebar"] a[aria-current="page"] {{
            background: rgba(34, 197, 94, 0.18) !important;
            border-radius: 8px;
        }}

        /* =========================
           MAIN CONTENT GLASS PANEL
           ========================= */
        section[data-testid="stMain"] {{
            background: rgba(0, 0, 0, 0.30);
            border-radius: 22px;
            padding: 3rem;
            margin: 1.5rem auto;
            max-width: 95%;
        }}

        section[data-testid="stMain"] > div {{
            background: transparent !important;
        }}

        /* =========================
           TYPOGRAPHY
           ========================= */
        section[data-testid="stMain"] h1,
        section[data-testid="stMain"] h2,
        section[data-testid="stMain"] h3,
        section[data-testid="stMain"] h4 {{
            color: #ffffff !important;
            font-weight: 700;
        }}

        section[data-testid="stMain"] p,
        section[data-testid="stMain"] span,
        section[data-testid="stMain"] label,
        section[data-testid="stMain"] li,
        section[data-testid="stMain"] small {{
            color: #f1f5f9 !important;
        }}

        /* =========================
           SLIDERS
           ========================= */
        section[data-testid="stMain"] div[data-testid="stSlider"] label {{
            color: #e5e7eb !important;
            font-weight: 500;
        }}

        section[data-testid="stMain"] div[data-testid="stSlider"] span {{
            color: #ffffff !important;
            font-weight: 600;
        }}

        section[data-testid="stMain"] div[data-testid="stSlider"] > div {{
            color: #22c55e !important;
        }}

        /* =========================
           METRICS
           ========================= */
        div[data-testid="metric-container"] {{
            background: rgba(0, 0, 0, 0.35);
            border-radius: 16px;
            padding: 1rem;
            border: 1px solid rgba(255,255,255,0.08);
        }}

        div[data-testid="metric-container"] * {{
            color: #ffffff !important;
        }}

        /* =========================
           ALERTS
           ========================= */
        .stAlert {{
            background: rgba(13, 42, 67, 0.85) !important;
            color: #ffffff !important;
            border-radius: 14px;
            border: none;
        }}

        /* =========================
           BUTTONS
           ========================= */
        button {{
            background: linear-gradient(135deg, #16a34a, #22c55e) !important;
            color: #ffffff !important;
            border-radius: 14px !important;
            font-weight: 600 !important;
        }}

        /* =========================
           DIVIDER
           ========================= */
        hr {{
            border: none;
            height: 1px;
            background: linear-gradient(
                to right,
                transparent,
                rgba(255,255,255,0.25),
                transparent
            );
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
