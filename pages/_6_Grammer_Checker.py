import streamlit as st
import google.generativeai as genai

# Configure Gemini API
GOOGLE_API_KEY = "AIzaSyDXbcstn5CucOgm4iKGsVbMGa6QWgvdcic"  # Replace with your actual key
genai.configure(api_key=GOOGLE_API_KEY)

# Set up Gemini model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config={
        "temperature": 0.4,
        "top_p": 1.0,
        "max_output_tokens": 1024
    },
    safety_settings=[
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]
)

# Streamlit App Setup
st.set_page_config(page_title="Grammar Checker", layout="centered")

st.markdown("""
    <div style="text-align: center;">
        <h1 style="color:#4a90e2;">Grammar Checker & Corrector</h1>
        <p>Paste your paragraph or sentence below. We'll fix grammar, spelling, and clarity.</p>
    </div>
""", unsafe_allow_html=True)

# Input from user
user_text = st.text_area("🔍 Enter text to check:", height=200, placeholder="Paste or type a sentence or paragraph...")

if st.button("✅ Correct Grammar"):
    if not user_text.strip():
        st.warning("Please enter some text to check.")
    else:
        with st.spinner("Analyzing and correcting..."):
            prompt = (
                "You are a professional grammar corrector. Fix the grammar, spelling, and clarity of the following text.\n\n"
                f"Text: {user_text}\n\n"
                "Return only the corrected version, without any explanation or comments."
            )
            try:
                response = model.generate_content(prompt)
                corrected_text = response.text.strip()

                st.text_area("orrected Text:", value=corrected_text, height=200)

                st.download_button("Download Corrected Text", corrected_text, file_name="corrected_text.txt")

            except Exception as e:
                st.error("❌ Something went wrong.")
                st.exception(e)
