import streamlit as st
import google.generativeai as genai

# Configure Gemini API
GOOGLE_API_KEY = "AIzaSyDXbcstn5CucOgm4iKGsVbMGa6QWgvdcic"  # Replace with your actual key
genai.configure(api_key=GOOGLE_API_KEY)

# Gemini model setup
generation_config = {
    "temperature": 0.7,
    "top_p": 0.8,
    "max_output_tokens": 1024,
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
st.set_page_config(page_title="Letter Generator", layout="centered")

# UI Header
st.markdown("""
    <div style="text-align: center;">
        <h1 style="color:#1f77b4;"> AI Letter Generator</h1>
        <p>Create clear and professional letters instantly.</p>
    </div>
""", unsafe_allow_html=True)

# Letter Form
with st.form("letter_form"):
    col1, col2 = st.columns(2)
    with col1:
        recipient = st.text_input("Recipient", placeholder="To the Principal, HR Manager, etc.")
    with col2:
        tone = st.selectbox("Tone", ["Formal", "Polite", "Assertive", "Friendly", "Apologetic"])

    purpose = st.text_input("Subject / Purpose of Letter", placeholder="Leave request, Application, etc.")
    key_points = st.text_area("Key Information", placeholder="State reasons, dates, or any other detail.")
    word_count = st.slider("Desired Word Count", 50, 500, 150, step=10)
    submit = st.form_submit_button("📝 Generate Letter")

# Session State
if "letter_text" not in st.session_state:
    st.session_state.letter_text = ""

# Generate Letter
if submit:
    if not recipient or not purpose or not key_points:
        st.warning("Please fill in all fields.")
    else:
        with st.spinner("Generating your letter..."):
            prompt = (
                f"Write a {tone.lower()} letter of around {word_count} words.\n"
                f"The letter is addressed to: {recipient}.\n"
                f"The subject/purpose of the letter is: {purpose}.\n"
                f"Include the following key points:\n{key_points}\n"
                "The letter should have a proper introduction, main body, and polite closing."
            )
            try:
                response = model.generate_content(prompt)
                st.session_state.letter_text = response.text.strip()
            except Exception as e:
                st.error("Something went wrong.")
                st.exception(e)

# Editable Output
if st.session_state.letter_text:
    st.markdown("### Review & Edit Letter")
    st.session_state.letter_text = st.text_area("Edit the letter below if needed:",
                                                value=st.session_state.letter_text,
                                                height=300)
    st.download_button("📥 Download Letter", st.session_state.letter_text, file_name="generated_letter.txt")
