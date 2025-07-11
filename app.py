import streamlit as st
from summarizer import summarize_text
from utils import extract_text_from_file, get_readability, get_word_count, extract_keywords, format_as_study_notes
import tempfile

# Config
st.set_page_config(page_title="AI Writer Pro", page_icon="🧠", layout="wide")

# Toggle Theme
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

col1, col2 = st.columns([1, 9])
with col1:
    if st.button("🌙 Toggle Theme"):
        st.session_state.dark_mode = not st.session_state.dark_mode

# Theme Settings
dark = st.session_state.dark_mode
bg_gradient = "linear-gradient(135deg, #1e1e1e, #000000)" if dark else "linear-gradient(135deg, #e0c3fc, #8ec5fc)"
text_color = "#ffffff" if dark else "#000000"
card_color = "#2a2a2a" if dark else "#ffffffcc"
primary_btn = "#3f51b5" if dark else "#6a1b9a"
header_color = "#ff8a80" if dark else "#4e148c"

# Custom CSS
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap');

    html, body, [data-testid="stAppViewContainer"] {{
        font-family: 'Poppins', sans-serif;
        background: {bg_gradient};
        color: {text_color};
    }}

    .title {{
        text-align: center;
        font-size: 50px;
        font-weight: 700;
        color: {header_color};
        margin-top: 20px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
    }}

    label, .css-16idsys p, .css-1cpxqw2, .stSelectbox label, .stTextArea label {{
        color: {text_color} !important;
        font-weight: bold;
    }}

    .summary-box {{
        background-color: {card_color};
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        margin-top: 30px;
        color: {text_color};
    }}

    .stButton>button {{
        background-color: {primary_btn};
        color: white !important;
        border-radius: 25px;
        padding: 10px 30px;
        font-weight: bold;
        font-size: 16px;
        transition: 0.3s ease;
        box-shadow: 0 0 15px {primary_btn};
    }}

    .stButton>button:hover {{
        background-color: white !important;
        color: {primary_btn} !important;
        border: 2px solid {primary_btn};
    }}

    .stDownloadButton>button {{
        background-color: #2e7d32;
        color: white;
        padding: 10px 25px;
        border-radius: 25px;
        font-weight: bold;
        margin-top: 10px;
    }}
    </style>
""", unsafe_allow_html=True)

# Title with Black Brain Icon
st.markdown(f'''
    <div class="title">
        <img src="https://cdn-icons-png.flaticon.com/512/3877/3877424.png" width="50" style="margin-bottom: -10px;" />
        <span style="vertical-align: middle;">AI Writer Pro</span>
    </div>
''', unsafe_allow_html=True)

# Input Section
uploaded_file = st.file_uploader("📂 Upload a file (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])
text_input = st.text_area("✍️ Or paste your text here", height=250)
format_option = st.selectbox("🧾 Choose summary format", ["Paragraph", "Smart Notes"])

# Generate Summary
if st.button("🧠 Generate Summary"):
    if uploaded_file:
        ext = f".{uploaded_file.name.split('.')[-1]}"
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            tmp.write(uploaded_file.read())
            input_text = extract_text_from_file(tmp.name, ext)
    else:
        input_text = text_input

    if not input_text.strip():
        st.error("❌ No input provided!")
    else:
        summary = summarize_text(input_text)
        word_count = get_word_count(input_text)
        summary_wc = get_word_count(summary)
        readability = get_readability(summary)
        keywords = extract_keywords(input_text)

        formatted = format_as_study_notes(summary) if format_option == "Smart Notes" else summary

        st.success("✅ Summary Generated!")
        st.markdown('<div class="summary-box">', unsafe_allow_html=True)
        st.markdown(f"**🧠 Summary:**\n\n{formatted}")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(f"- 📊 **Original Word Count:** `{word_count}`")
        st.markdown(f"- 📉 **Summary Word Count:** `{summary_wc}`")
        st.markdown(f"- 📈 **Readability Score:** `{readability:.2f}`")
        st.markdown(f"- 🔑 **Keywords:** `{', '.join(keywords)}`")

        st.download_button("⬇ Download Summary", data=formatted, file_name="summary.txt", mime="text/plain")
