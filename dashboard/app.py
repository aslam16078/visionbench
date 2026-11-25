
import streamlit as st
import httpx

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="VisionBench AI",
    page_icon="🔬",
    layout="wide",
)

st.title("🔬 VisionBench AI")

st.write(
    "Synthetic Visual Data Generation "
    "and Multimodal AI Evaluation Platform"
)

st.divider()

st.subheader("System Status")

if st.button("Check Backend Connection"):
    try:
        response = httpx.get(
            f"{API_URL}/health",
            timeout=5.0,
        )

        response.raise_for_status()

        data = response.json()

        if data["status"] == "healthy":
            st.success("Backend connected successfully!")
            st.json(data)
        else:
            st.warning("Backend returned an unexpected status.")

    except httpx.HTTPError as error:
        st.error(f"Backend connection failed: {error}")

st.divider()

st.subheader("Project Modules")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("Synthetic Data Generator")

with col2:
    st.info("Question Generator")

with col3:
    st.info("AI Model Evaluator")

st.caption("VisionBench AI | Version 0.1.0")
