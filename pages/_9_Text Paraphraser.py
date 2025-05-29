import streamlit as st
import google.generativeai as genai

# Configure Gemini API
GOOGLE_API_KEY = "AIzaSyDXbcstn5CucOgm4iKGsVbMGa6QWgvdcic"  # Replace with your actual key
genai.configure(api_key=GOOGLE_API_KEY)

# Setup Gemini model
generation_config = {
    "temperature": 0.7,
    "top_p": 0.9,
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

# Streamlit Page Config
st.set_page_config(page_title="AI Text Rephraser", layout="centered")

st.markdown("""
    <div style="text-align: center;">
        <h1 style="color:#6c63ff;">AI Text Rephraser</h1>
        <p>Paste or upload text, select a style & tone, and get reworded versions instantly.</p>
    </div>
""", unsafe_allow_html=True)

# File Upload / Text Input
uploaded_file = st.file_uploader("Upload a Text File", type=["txt"])
manual_text = st.text_area(" OR Paste Text to Rephrase", height=200)

# Extract text
text_input = ""
if uploaded_file:
    text_input = uploaded_file.read().decode("utf-8")
elif manual_text.strip():
    text_input = manual_text.strip()

# Rephrasing options
st.markdown("####  Rephrase Settings")
styles = ["Professional", "Casual", "Simplified", "Creative", "Concise"]
tone_options = ["Neutral", "Formal", "Informal", "Polite", "Assertive", "Friendly"]

col1, col2 = st.columns(2)
with col1:
    style = st.selectbox("✏️ Rephrase Style", styles)
with col2:
    tone = st.selectbox("🎯 Tone", tone_options)

# Rephrase Button
if text_input:
    if st.button("🔁 Rephrase Text"):
        with st.spinner("Rephrasing your text..."):
            prompt = (
                f"Rephrase the following text in a {style.lower()} style and {tone.lower()} tone. "
                f"Preserve the original meaning while improving clarity or engagement:\n\n{text_input}"
            )

            try:
                response = model.generate_content(prompt)
                rephrased_text = response.text.strip()
                st.session_state.rephrased = rephrased_text
            except Exception as e:
                st.error("⚠️ Error generating rephrased text.")
                st.exception(e)

# Show result
if "rephrased" in st.session_state and st.session_state.rephrased:
    st.markdown("### ✨ Rephrased Text (Editable)")
    edited_text = st.text_area("You can make final edits below:", value=st.session_state.rephrased, height=250)
    st.download_button("📥 Download Rephrased Text", edited_text, file_name="rephrased.txt")
else:
    st.info("Please upload or enter text to get started.")
