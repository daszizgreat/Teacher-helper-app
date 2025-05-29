import streamlit as st
import google.generativeai as genai

# Gemini API Configuration
GOOGLE_API_KEY = "AIzaSyDXbcstn5CucOgm4iKGsVbMGa6QWgvdcic"  # Replace with your actual key
genai.configure(api_key=GOOGLE_API_KEY)

# Gemini model setup
generation_config = {
    "temperature": 0.6,
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

# Page Config
st.set_page_config(page_title="Reply Message Crafter", layout="centered")

# App Header
st.markdown("""
    <div style="text-align: center;">
        <h1 style="color:#6c63ff;">✉️ Precision Reply Generator</h1>
        <p style="font-size:18px;">Generate short, sharp, professional replies with custom signature.</p>
    </div>
""", unsafe_allow_html=True)

# Input Form
with st.form("reply_form"):
    st.markdown("#### 🧾 Reply Details")
    name = st.text_input("Recipient Name", placeholder="John")
    context = st.text_area("Purpose / Context of Reply", placeholder="Explain what you're replying to and your position.")
    signature = st.text_input("Signature (your name + title)", placeholder="Jane Doe\nHead of Communications")

    submit = st.form_submit_button("🔁 Generate Reply")

# Session State for Output
if "reply_text" not in st.session_state:
    st.session_state.reply_text = ""

# Handle Submission
if submit:
    if not name or not context or not signature:
        st.warning("⚠️ All fields are required.")
    else:
        with st.spinner("Formulating your reply..."):
            prompt = (
                f"Write a short, professional reply message.\n"
                f"- Begin with: 'Dead {name},'\n"
                f"- Be direct, courteous, and to the point.\n"
                f"- Context: {context}\n"
                f"- Close with the following signature:\n{signature}\n"
                "Keep the reply between 40 and 100 words, very professional and formal."
            )

            try:
                response = model.generate_content(prompt)
                st.session_state.reply_text = response.text.strip()
                st.success("✅ Reply generated successfully.")
            except Exception as e:
                st.error("🚫 Something went wrong.")
                st.exception(e)

# Editable Reply Output
if st.session_state.reply_text:
    st.markdown("### ✏️ Your Editable Reply Message")
    st.session_state.reply_text = st.text_area(
        "You can edit the reply here before copying or downloading:",
        value=st.session_state.reply_text,
        height=200,
        key="editable_reply"
    )

    st.download_button("📥 Download Reply", st.session_state.reply_text, file_name="professional_reply.txt")
