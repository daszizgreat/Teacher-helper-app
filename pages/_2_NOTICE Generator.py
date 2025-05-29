import streamlit as st
import google.generativeai as genai

# Configure Gemini API
GOOGLE_API_KEY = "AIzaSyDXbcstn5CucOgm4iKGsVbMGa6QWgvdcic"  # Replace with your actual API key
genai.configure(api_key=GOOGLE_API_KEY)

# Gemini model setup
generation_config = {
    "temperature": 0.6,
    "top_p": 0.9,
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
st.set_page_config(page_title="Notice Generator", layout="centered")

# App Header
st.markdown(
    """
    <div style="text-align: center;">
        <h1 style="color:#2b7cde;">Notice Generator</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Form Inputs
with st.form("notice_form"):
    st.markdown("####  Notice Details")

    title = st.text_input("Notice Title", placeholder="Annual General Meeting")
    purpose = st.text_area("Purpose of the Notice", placeholder="Why is this notice being issued?")
    audience = st.text_input("Intended Audience", placeholder="All Employees / Students / Members")
    organizer = st.text_input("Issued By", placeholder="HR Department / Principal / Event Committee")
    date = st.date_input("Date of Notice")

    word_count = st.slider("Approximate Word Count", 50, 400, 120, 10)

    submit = st.form_submit_button("📄 Generate Notice")

# Store state
if "notice_text" not in st.session_state:
    st.session_state.notice_text = ""

# Generate notice
if submit:
    if not title or not purpose or not audience or not organizer:
        st.warning("⚠️ Please fill out all the required fields.")
    else:
        with st.spinner("Generating your notice..."):
            prompt = (
                f"Create a formal notice of about {word_count} words with the following details:\n"
                f"- Title: {title}\n"
                f"- Purpose: {purpose}\n"
                f"- Audience: {audience}\n"
                f"- Issued By: {organizer}\n"
                f"- Date: {date.strftime('%B %d, %Y')}\n"
                "Use a clear and formal tone. Begin with 'NOTICE' as the heading. Include all the above elements in a structured way."
            )

            try:
                response = model.generate_content(prompt)
                st.session_state.notice_text = response.text.strip()
                st.success("✅ Notice generated! You can now review or edit it.")
            except Exception as e:
                st.error("🚫 Something went wrong.")
                st.exception(e)

# Editable Notice Section
if st.session_state.notice_text:
    st.markdown("### ✏️ Your Editable Notice")
    st.session_state.notice_text = st.text_area(
        "Edit the notice before downloading or publishing:",
        value=st.session_state.notice_text,
        height=300,
        key="editable_notice"
    )

    st.download_button("📥 Download Notice", st.session_state.notice_text, file_name="generated_notice.txt")
