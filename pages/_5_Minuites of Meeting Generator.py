import streamlit as st
import google.generativeai as genai
from datetime import date

# Configure Gemini API
GOOGLE_API_KEY = "AIzaSyDXbcstn5CucOgm4iKGsVbMGa6QWgvdcic"  # Replace with your real key
genai.configure(api_key=GOOGLE_API_KEY)

# Gemini model setup
generation_config = {
    "temperature": 0.5,
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

# Page setup
st.set_page_config(page_title="Minutes of Meeting Generator", layout="centered")

# Header
st.markdown("""
    <div style="text-align: center;">
        <h1 style="color:#4CAF50;">Minutes of Meeting Generator</h1>
        <p style="font-size:17px;">Capture, generate, and track MoM documents effortlessly.</p>
    </div>
""", unsafe_allow_html=True)

# Form
with st.form("mom_form"):
    st.markdown("#### 📝 Meeting Details")

    meeting_title = st.text_input("Meeting Title", placeholder="Project Kickoff / Weekly Sync")
    meeting_date = st.date_input("Date", value=date.today())
    participants = st.text_area("Participants", placeholder="John, Lisa, Mark...")
    agenda = st.text_area("Agenda", placeholder="What were the main objectives of the meeting?")
    discussion = st.text_area("Discussion Summary", placeholder="Summarize key discussion points...")
    action_items = st.text_area("Action Items", placeholder="List the tasks assigned, responsible persons, and deadlines.")
    recorder = st.text_input("Minutes Prepared By", placeholder="Your name")

    submit = st.form_submit_button("🧾 Generate Minutes")

# Output session state
if "mom_text" not in st.session_state:
    st.session_state.mom_text = ""

# Generate MoM
if submit:
    if not meeting_title or not participants or not agenda or not discussion:
        st.warning("⚠️ Please fill in all required fields.")
    else:
        with st.spinner("Generating structured Minutes of Meeting..."):
            prompt = (
                f"Create formal and structured Minutes of Meeting with the following:\n"
                f"- Title: {meeting_title}\n"
                f"- Date: {meeting_date.strftime('%B %d, %Y')}\n"
                f"- Participants: {participants}\n"
                f"- Agenda: {agenda}\n"
                f"- Discussion Summary: {discussion}\n"
                f"- Action Items: {action_items}\n"
                f"- Recorded By: {recorder}\n\n"
                "Include proper formatting with headings like Title, Date, Participants, Agenda, Discussion Summary, Action Items, and Recorder."
            )

            try:
                response = model.generate_content(prompt)
                st.session_state.mom_text = response.text.strip()
                st.success("✅ Minutes generated successfully.")
            except Exception as e:
                st.error("🚫 Failed to generate Minutes.")
                st.exception(e)

# Display + Edit
if st.session_state.mom_text:
    st.markdown("### 🧾 Your Editable Minutes of Meeting")
    st.session_state.mom_text = st.text_area(
        "You can edit the generated minutes here:",
        value=st.session_state.mom_text,
        height=400,
        key="editable_mom"
    )

    st.download_button("📥 Download MoM", st.session_state.mom_text, file_name="minutes_of_meeting.txt")
