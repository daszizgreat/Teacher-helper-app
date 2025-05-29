import streamlit as st
import google.generativeai as genai

# Configure Gemini API
GOOGLE_API_KEY = "AIzaSyDXbcstn5CucOgm4iKGsVbMGa6QWgvdcic"  # Replace with your actual key
genai.configure(api_key=GOOGLE_API_KEY)
# Setup Gemini model
generation_config = {
    "temperature": 0.5,
    "top_p": 0.8,
    "max_output_tokens": 512,
    "top_k": 40,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    safety_settings=safety_settings
)

# Streamlit UI setup
st.set_page_config(page_title="AI Summarizer", layout="centered")

st.markdown(
    """
    <div style="text-align: center;">
        <h1 style="color:#6c63ff;">📄 AI Text Summarizer</h1>
        <p>Paste or upload text, preview it, and get a smart editable summary.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# File Upload and Manual Input
uploaded_file = st.file_uploader("📤 Upload a Text File", type=["txt"])
manual_text = st.text_area("✍️ Or Paste Your Text Below", height=200)

# State for content preview
if "preview_text" not in st.session_state:
    st.session_state.preview_text = ""

if "show_preview" not in st.session_state:
    st.session_state.show_preview = False

# Extract text
if uploaded_file:
    st.session_state.preview_text = uploaded_file.read().decode("utf-8")
elif manual_text.strip():
    st.session_state.preview_text = manual_text.strip()

# Preview toggle button
if st.session_state.preview_text:
    if st.button("👁️ Preview Uploaded/Pasted Text"):
        st.session_state.show_preview = not st.session_state.show_preview

# Show preview if toggled
if st.session_state.show_preview:
    st.markdown("#### 📃 Preview Text")
    st.text_area("Text Preview", value=st.session_state.preview_text, height=250, disabled=True)

# Summarize Button
if st.session_state.preview_text:
    if st.button("🧠 Summarize Text"):
        with st.spinner("Generating summary..."):
            try:
                prompt = f"Please summarize the following text clearly and concisely:\n\n{st.session_state.preview_text}"
                response = model.generate_content(prompt)
                st.session_state.summary_text = response.text.strip()
                st.success("✅ Summary generated successfully!")
            except Exception as e:
                st.error("⚠️ Error while summarizing.")
                st.exception(e)

# Editable summary output
if "summary_text" in st.session_state and st.session_state.summary_text:
    st.markdown("### 📝 Your Summary (Editable)")
    edited_summary = st.text_area("Make changes if needed before downloading:",
                                  value=st.session_state.summary_text, height=250)
    st.download_button("📥 Download Summary", edited_summary, file_name="summary.txt")