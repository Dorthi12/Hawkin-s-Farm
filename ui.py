import streamlit as st

def lottie_spinner(text="Loading..."):
    st.markdown(
        f"""
        <div style="display:flex; align-items:center;">
            <img src="https://assets9.lottiefiles.com/packages/lf20_j1adxtyb.json" width="60">
            <span style="margin-left:10px;">{text}</span>
        </div>
        """,
        unsafe_allow_html=True
    )
