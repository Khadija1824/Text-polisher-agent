"""Streamlit UI for the Text Polisher Agent."""
import os
import streamlit as st
from dotenv import load_dotenv
from agent import TextPolisher

load_dotenv()

st.set_page_config(
    page_title="Text Polisher Agent",
    page_icon="✍️",
    layout="centered",
)

API_KEY = os.getenv("GOOGLE_API_KEY")

# ---------------- Sidebar ----------------
with st.sidebar:
    st.title("✍️ Text Polisher")
    st.caption("Any input -> clean, correct English.")

    if not API_KEY:
        API_KEY = st.text_input("Gemini API Key", type="password",
                                help="Or set GOOGLE_API_KEY in .env")

    model = st.selectbox(
        "Model",
        ["gemini-2.5-flash", "gemini-2.5-pro"],
        index=0,
    )
    tone = st.selectbox(
        "Target tone",
        ["professional", "formal", "neutral", "friendly", "casual"],
        index=0,
    )
    variety = st.selectbox(
        "English variety",
        ["Standard English", "American English", "British English", "Simple/Plain English"],
    )

# ---------------- Header ----------------
st.title("✍️ Universal Text Polisher")
st.caption(
    "Paste broken English, Hinglish, Roman Urdu, SMS-speak, or any messy text - "
    "get clean, correct English back with the meaning preserved."
)

if not API_KEY:
    st.warning("Please provide a Gemini API key in the sidebar or .env file.")
    st.stop()


# ---------------- Agent (cached) ----------------
@st.cache_resource(show_spinner=False)
def get_polisher(api_key: str, model: str) -> TextPolisher:
    return TextPolisher(api_key=api_key, model=model)

polisher = get_polisher(API_KEY, model)


# ---------------- Input ----------------
input_text = st.text_area(
    "Your text",
    height=220,
    placeholder="e.g., yaar tmrw meeting 3pm ok?",
)

polish_btn = st.button("✨ Polish", type="primary", use_container_width=True)


# ---------------- Output ----------------
if polish_btn:
    if not input_text.strip():
        st.error("Please enter some text.")
    else:
        with st.spinner("Polishing..."):
            result = polisher.polish(input_text, tone=tone, variety=variety)

        if result.get("error"):
            st.error(f"Failed: {result['error']}")
        else:
            st.subheader("Polished English")
            st.text_area("", result["polished"], height=180, key="out")

            st.divider()
            c1, c2, c3 = st.columns(3)
            c1.metric("Detected", result.get("detected_language", "-"))
            c2.metric("Tone", result.get("tone_applied", "-"))
            c3.metric("Confidence", f"{result.get('confidence', 0):.0%}")

            changes = result.get("changes_summary", [])
            if changes:
                st.subheader("What changed")
                for c in changes:
                    st.write(f"- {c}")