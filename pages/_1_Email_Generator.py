import streamlit as st
import google.generativeai as genai
from email.mime.text import MIMEText
import smtplib

# ==== CONFIGURATION ====
GOOGLE_API_KEY = "AIzaSyDXbcstn5CucOgm4iKGsVbMGa6QWgvdcic"
genai.configure(api_key=GOOGLE_API_KEY)

# ==== GEMINI MODEL SETUP ====
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

# ==== PAGE CONFIG ====
st.set_page_config(page_title="Email Crafter", layout="centered")

# ==== CUSTOM CSS ====
st.markdown("""
<style>
body {
    font-family: 'Segoe UI', sans-serif;
    background-color: #fdfdfd;
}
h1, h2, h3, h4 {
    font-weight: 600;
    color: #333333;
}
h1, h2, h3 {
    text-align: center;
}
section.main > div {
    background-color: #ffffff;
    border-radius: 12px;
    padding: 2rem;
    margin-top: 1rem;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.05);
}
input, textarea, .stTextInput, .stTextArea {
    border: 1px solid #d1d1d1;
    border-radius: 10px !important;
    padding: 0.75rem;
    background-color: #fafafa;
}
label {
    font-weight: 500 !important;
    margin-bottom: 0.25rem;
    color: #444444;
}
.stSlider > div {
    padding-top: 0.5rem;
}
button[kind="primary"] {
    background-color: #f9634f !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 0.5rem 1.25rem !important;
    font-weight: bold;
    transition: background-color 0.3s ease;
}
button[kind="primary"]:hover {
    background-color: #e4563c !important;
}
button[title="Download"] {
    margin-top: 10px;
    background-color: #2e86de !important;
    color: white !important;
}
.stAlert > div {
    border-radius: 10px;
    padding: 0.75rem 1rem;
}
.stAlert-success {
    background-color: #e6f9f0;
    color: #167e56;
}
.stAlert-error {
    background-color: #fdecea;
    color: #a94442;
}
.stCheckbox > label > div {
    margin-left: 5px;
    font-weight: 500;
}
footer, #MainMenu, header {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# ==== HEADER ====
st.markdown("""
<div style="text-align: center;">
    <h1 style="color:#f9634f;">Email Crafter</h1>
    <p>Create, review, and polish professional emails in seconds!</p>
</div>
""", unsafe_allow_html=True)

# ==== FORM ====
with st.form("email_form"):
    st.markdown("#### 🧾 Email Inputs")

    col1, col2 = st.columns(2)
    with col1:
        honorific = st.text_input("Honorific", placeholder="Dr., Mr., Ms., Team")
    with col2:
        recipient_name = st.text_input("Recipient's Name", placeholder="John Smith")

    subject = st.text_input("📌 Email Subject", placeholder="Request for Project Update")
    important_info = st.text_area("🗒️ Key Information", placeholder="Describe what the email should cover.")
    word_count = st.slider("✍️ Desired Word Count", 50, 500, 150, 10)

    send_option = st.checkbox("📤 Send this email to recipient")
    receiver_email = st.text_input("✉️ Recipient Email", placeholder="someone@example.com") if send_option else None

    submit = st.form_submit_button("🚀 Generate Email")

# ==== SESSION STATE ====
if "email_text" not in st.session_state:
    st.session_state.email_text = ""

# ==== EMAIL GENERATION ====
if submit:
    if not important_info or not subject:
        st.warning("⚠️ Please fill in both the subject and the key information.")
    else:
        with st.spinner("Crafting your professional email..."):
            prompt = (
                f"Write a full professional email of about {word_count} words.\n"
                f"Start with a greeting using '{honorific} {recipient_name}'.\n"
                f"The subject is: {subject}.\n"
                f"The email should include the following key points:\n{important_info}\n"
                "Ensure a polite tone and a proper closing signature. Use formal and clear language."
            )

            try:
                response = model.generate_content(prompt)
                st.session_state.email_text = response.text.strip()
            except Exception as e:
                st.error("🚫 Oops! Something went wrong.")
                st.exception(e)

# ==== OUTPUT ====
if st.session_state.email_text:
    st.markdown("### Your Email")
    st.session_state.email_text = st.text_area(
        label="Edit your email below before sending or downloading:",
        value=st.session_state.email_text,
        height=300,
        key="editable_email"
    )

    st.download_button("📥 Download Edited Email", st.session_state.email_text, file_name="edited_email.txt")

    # SEND EMAIL OPTION
    if send_option and receiver_email:
        def send_otp_via_email(email_id, user_name, email_text):
            sender_email = 'teamnexusofficial25@gmail.com'
            sender_password = 'qkmm yqcq vqtm vmoq'
            subject = "Your Auto-Generated Email from Email Crafter"

            message = MIMEText(email_text)
            message["Subject"] = subject
            message["From"] = sender_email
            message["To"] = email_id

            try:
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                    server.login(sender_email, sender_password)
                    server.sendmail(sender_email, email_id, message.as_string())
                return True
            except Exception as e:
                st.error(f"❌ Failed to send email: {e}")
                return False

        if st.button("📧 Send Email"):
            success = send_otp_via_email(receiver_email, recipient_name, st.session_state.email_text)
            if success:
                st.success("✅ Email sent successfully!")
