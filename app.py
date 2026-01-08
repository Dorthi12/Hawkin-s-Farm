import streamlit as st

st.set_page_config(
    page_title="Hawkins Farm 🌱",
    layout="wide"
)

st.title("🌾 Hawkins Farm – Smart Agriculture Platform")

st.markdown("""
Welcome to **Hawkins Farm**  

Use the sidebar to:
- Predict crops  
- Estimate prices  
- Get product recommendations  
- Browse products  
""")

st.info("Make sure FastAPI backend is running on port 8000.")
