import streamlit as st
import google.generativeai as genai

# Gemini API Configuration
GOOGLE_API_KEY = "AIzaSyDXbcstn5CucOgm4iKGsVbMGa6QWgvdcic"  # Replace with your Gemini API key
genai.configure(api_key=GOOGLE_API_KEY)

# Model Setup
generation_config = {
    "temperature": 0.7,
    "top_p": 0.9,
    "max_output_tokens": 256,
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

# Streamlit Config
st.set_page_config(page_title="Word Enhancer", layout="centered")

st.markdown("""
    <div style="text-align:center;">
        <h1 style="color:#2b7cde;">Word Enhancer</h1>
        <p>Get smarter, better, and more effective word suggestions</p>
    </div>
""", unsafe_allow_html=True)

# UI
with st.form("word_form"):
    word = st.text_input("Enter a word to improve:", placeholder="e.g. good, fast, happy")
    tone = st.selectbox("Enhance for:", ["Formal", "Creative", "Simpler", "More Impactful", "Professional"])
    submit = st.form_submit_button("✨ Enhance Word")

# Generate suggestions
if "enhanced_words" not in st.session_state:
    st.session_state.enhanced_words = ""

if submit:
    if not word:
        st.warning("⚠️ Please enter a word.")
    else:
        with st.spinner("Generating better alternatives..."):
            prompt = (
                f"Suggest 8 to 10 alternative words for '{word}' that sound more {tone.lower()}.\n"
                "Give just the words in a comma-separated list without explanations."
            )
            try:
                response = model.generate_content(prompt)
                st.session_state.enhanced_words = response.text.strip()
                st.success("✅ Here are your enhanced words!")
            except Exception as e:
                st.error("🚫 Error generating suggestions.")
                st.exception(e)

# Show Output
if st.session_state.enhanced_words:
    st.markdown("### 🎯 Suggested Alternatives")
    st.text_area("Copy or tweak your enhanced words:", value=st.session_state.enhanced_words, height=150, key="editable_enhanced")
    st.download_button("📥 Download Suggestions", st.session_state.enhanced_words, file_name="better_words.txt")
