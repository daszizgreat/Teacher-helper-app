import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(page_title="Teacher  Dashboard", layout="wide")

st.markdown("""
    <style>
        .tool-card {
            background-color: #f0f2f6;
            border-radius: 12px;
            padding: 20px;
            margin: 10px 0;
            text-align: center;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
            transition: 0.3s;
        }
        .tool-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        }
        .tool-button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 18px;
            font-size: 16px;
            border: none;
            border-radius: 8px;
            text-decoration: none;
            display: inline-block;
            margin-top: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Teacher Dashboard")
st.markdown("A centralized taskbar for all your AI-powered tools. Click a tool to open it in a new tab.")

# Define tools
tools = [
    {"name": "📧 Email Generator", "url": "http://localhost:8501/1_Email_Generator"},
    {"name": "📢 Notice Generator", "url": "http://localhost:8501/2_NOTICE_Generator"},
    {"name": "✉️ Letter Generator", "url": "http://localhost:8501/3_Letter_Generator"},
    {"name": "💬 Message Maker", "url": "http://localhost:8501/4_Message_Maker"},
    {"name": "📝 Minutes of Meeting Generator", "url": "http://localhost:8501/5_Minuites_of_Meeting_Generator"},
    {"name": "🔍 Grammar Checker", "url": "http://localhost:8501/6_Grammer_Checker"},
    {"name": "🧾 Word Generator", "url": "http://localhost:8501/7_Word_Generator"},
    {"name": "📰 Summariser", "url": "http://localhost:8501/8_Summariser"},
    {"name": "♻️ Text Paraphraser", "url": "http://localhost:8501/9_Text_Paraphraser"},
]

# Display in rows of 3
cols = st.columns(3)
for i, tool in enumerate(tools):
    with cols[i % 3]:
        st.markdown(f"""
            <div class='tool-card'>
                <h3>{tool['name']}</h3>
                <a href="{tool['url']}" target="_blank" class="tool-button">Open Tool</a>
            </div>
        """, unsafe_allow_html=True)
