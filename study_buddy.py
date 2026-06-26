import streamlit as st
from groq import Groq
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .main {
        background: linear-gradient(180deg, #f8f9ff 0%, #f0f4ff 100%);
    }
    
    /* Header Styling */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
        text-align: center;
    }
    
    .header-container h1 {
        font-size: 3rem;
        font-weight: 900;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .header-container p {
        font-size: 1.2rem;
        opacity: 0.95;
        font-weight: 300;
    }
    
    /* Feature Cards */
    .feature-card {
        background: white;
        border-radius: 15px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.1);
        border: 2px solid transparent;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.2);
        border-color: #667eea;
    }
    
    .feature-header {
        font-size: 1.8rem;
        font-weight: 800;
        margin-bottom: 1rem;
        color: #333;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .feature-description {
        color: #666;
        font-size: 1rem;
        margin-bottom: 1.5rem;
        line-height: 1.6;
    }
    
    /* Input Styling */
    .stTextInput input {
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 0.75rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .stTextArea textarea {
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        font-family: 'Segoe UI', sans-serif;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.8rem 2rem;
        font-weight: 700;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        cursor: pointer;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
    }
    
    /* Messages */
    .stSuccess {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        border-left: 5px solid #00d26a;
        border-radius: 10px;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        border-left: 5px solid #ff6b6b;
        border-radius: 10px;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-left: 5px solid #667eea;
        border-radius: 10px;
        color: white;
    }
    
    /* Saved Items Container */
    .saved-item-wrapper {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border-left: 5px solid #667eea;
        box-shadow: 0 3px 15px rgba(102, 126, 234, 0.08);
        transition: all 0.3s ease;
    }
    
    .saved-item-wrapper:hover {
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
    }
    
    .saved-item-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #333;
        margin-bottom: 0.5rem;
    }
    
    .saved-item-time {
        font-size: 0.85rem;
        color: #999;
        margin-bottom: 1rem;
    }
    
    /* Metrics */
    .metric-box {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
    }
    
    .metric-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.15);
    }
    
    .metric-number {
        font-size: 2.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        margin-top: 0.5rem;
        font-weight: 600;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 1rem;
    }
    
    /* Sidebar */
    .sidebar-section {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 3px 15px rgba(102, 126, 234, 0.1);
        border-left: 5px solid #667eea;
    }
    
    .sidebar-section h3 {
        color: #667eea;
        margin-bottom: 1rem;
        font-size: 1.2rem;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        margin: 2rem 0;
        border-radius: 2px;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #666;
        margin-top: 3rem;
    }
    
    .footer-text {
        font-size: 1rem;
        font-weight: 600;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Groq
from dotenv import load_dotenv
load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
# Session state
if "saved_summary" not in st.session_state:
    st.session_state.saved_summary = None
if "saved_quiz" not in st.session_state:
    st.session_state.saved_quiz = None
if "saved_flashcards" not in st.session_state:
    st.session_state.saved_flashcards = None

# Data functions
DATA_FILE = "study_buddy_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            return {"notes": [], "quizzes": [], "flashcards": []}
    return {"notes": [], "quizzes": [], "flashcards": []}

def save_data(data):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)
        return True
    except:
        return False

def add_item(item_type, content, title=""):
    data = load_data()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    item = {
        "id": len(data[item_type]),
        "title": title,
        "content": content,
        "timestamp": timestamp
    }
    data[item_type].append(item)
    return save_data(data)

def delete_item(item_type, item_id):
    data = load_data()
    data[item_type] = [item for item in data[item_type] if item["id"] != item_id]
    save_data(data)

# SIDEBAR
with st.sidebar:
    st.markdown("""
    <div class="sidebar-section">
        <h3>📖 How to Use</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    **🔍 Explain Topics**
    
    Enter any topic and get clear explanations in simple terms.
    """)
    
    st.markdown("""
    **📝 Summarize Notes**
    
    Paste your notes and convert them to organized summaries.
    """)
    
    st.markdown("""
    **❓ Generate Quizzes**
    
    Create quiz questions to test your knowledge.
    """)
    
    st.markdown("""
    **📇 Create Flashcards**
    
    Make Q&A cards for better memorization.
    """)
    
    st.markdown("""
    **💾 Save Everything**
    
    Keep all your work organized and accessible.
    """)
    
    st.divider()
    
    st.markdown("<h3 style='color: #667eea;'>📊 Your Progress</h3>", unsafe_allow_html=True)
    
    data = load_data()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Notes", len(data["notes"]), "📝")
    with col2:
        st.metric("Quizzes", len(data["quizzes"]), "❓")
    with col3:
        st.metric("Cards", len(data["flashcards"]), "📇")

# MAIN HEADER
st.markdown("""
<div class="header-container">
    <h1>📚 AI Study Buddy</h1>
    <p>Your Personal AI-Powered Learning Assistant</p>
</div>
""", unsafe_allow_html=True)

# FEATURE 1: EXPLAIN
st.markdown('<div class="feature-card">', unsafe_allow_html=True)
st.markdown('<div class="feature-header">🔍 Explain Any Topic</div>', unsafe_allow_html=True)
st.markdown('<div class="feature-description">Get instant explanations of any topic in simple, easy-to-understand language</div>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    topic = st.text_input("What topic do you want to understand?", placeholder="e.g., Photosynthesis, AI, Economics...")
with col2:
    st.write("")
    explain_btn = st.button("✨ Explain", key="explain", use_container_width=True)

if explain_btn:
    if topic:
        with st.spinner("🤔 Thinking..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": f"Explain '{topic}' in very simple terms a school student can understand. Keep it short and clear."}]
            )
            st.success("✅ Here's your explanation:")
            st.write(response.choices[0].message.content)
    else:
        st.warning("⚠️ Please enter a topic!")

st.markdown('</div>', unsafe_allow_html=True)

# FEATURE 2: SUMMARIZE
st.markdown('<div class="feature-card">', unsafe_allow_html=True)
st.markdown('<div class="feature-header">📝 Summarize Notes</div>', unsafe_allow_html=True)
st.markdown('<div class="feature-description">Convert your long notes into clear, organized bullet-point summaries</div>', unsafe_allow_html=True)

notes = st.text_area("Paste your study notes:", height=150, key="notes_input", placeholder="Paste your notes here...")

col1, col2 = st.columns([1, 1])
with col1:
    sum_btn = st.button("📋 Summarize", key="summarize")

if sum_btn:
    if notes:
        with st.spinner("⏳ Creating summary..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": f"Summarize these notes in clear bullet points:\n\n{notes}"}]
            )
            st.session_state.saved_summary = response.choices[0].message.content
            st.success("✅ Summary created!")
            st.write(st.session_state.saved_summary)
    else:
        st.warning("⚠️ Please paste notes!")

if st.session_state.saved_summary:
    if st.button("💾 Save Summary", key="save_summary"):
        add_item("notes", st.session_state.saved_summary, f"Summary - {datetime.now().strftime('%H:%M:%S')}")
        st.success("✅ Saved to your collection!")
        st.session_state.saved_summary = None

st.markdown('</div>', unsafe_allow_html=True)

# FEATURE 3: QUIZ
st.markdown('<div class="feature-card">', unsafe_allow_html=True)
st.markdown('<div class="feature-header">❓ Generate Quiz</div>', unsafe_allow_html=True)
st.markdown('<div class="feature-description">Create multiple-choice quiz questions to test your understanding</div>', unsafe_allow_html=True)

quiz_notes = st.text_area("Paste notes for quiz:", height=150, key="quiz_input", placeholder="Paste your notes here...")

col1, col2 = st.columns([1, 1])
with col1:
    quiz_btn = st.button("🎯 Generate Quiz", key="quiz")

if quiz_btn:
    if quiz_notes:
        with st.spinner("⏳ Creating quiz..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": f"Generate 5 multiple choice quiz questions with answers:\n\n{quiz_notes}"}]
            )
            st.session_state.saved_quiz = response.choices[0].message.content
            st.success("✅ Quiz created!")
            st.write(st.session_state.saved_quiz)
    else:
        st.warning("⚠️ Please paste notes!")

if st.session_state.saved_quiz:
    if st.button("💾 Save Quiz", key="save_quiz"):
        add_item("quizzes", st.session_state.saved_quiz, f"Quiz - {datetime.now().strftime('%H:%M:%S')}")
        st.success("✅ Saved to your collection!")
        st.session_state.saved_quiz = None

st.markdown('</div>', unsafe_allow_html=True)

# FEATURE 4: FLASHCARDS
st.markdown('<div class="feature-card">', unsafe_allow_html=True)
st.markdown('<div class="feature-header">📇 Generate Flashcards</div>', unsafe_allow_html=True)
st.markdown('<div class="feature-description">Create Q&A flashcards for efficient memorization and learning</div>', unsafe_allow_html=True)

flash_notes = st.text_area("Paste notes for flashcards:", height=150, key="flash_input", placeholder="Paste your notes here...")

col1, col2 = st.columns([1, 1])
with col1:
    flash_btn = st.button("⚡ Generate Cards", key="flash")

if flash_btn:
    if flash_notes:
        with st.spinner("⏳ Creating flashcards..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": f"Create 8 flashcards. Format: Q: [question] | A: [answer]\n\n{flash_notes}"}]
            )
            st.session_state.saved_flashcards = response.choices[0].message.content
            st.success("✅ Flashcards created!")
            st.write(st.session_state.saved_flashcards)
    else:
        st.warning("⚠️ Please paste notes!")

if st.session_state.saved_flashcards:
    if st.button("💾 Save Flashcards", key="save_flash"):
        add_item("flashcards", st.session_state.saved_flashcards, f"Flashcards - {datetime.now().strftime('%H:%M:%S')}")
        st.success("✅ Saved to your collection!")
        st.session_state.saved_flashcards = None

st.markdown('</div>', unsafe_allow_html=True)

# SAVED ITEMS SECTION
st.markdown("---")
st.markdown("<h2 style='text-align: center; font-size: 2.2rem; color: #333; margin: 2rem 0;'>📋 Your Saved Items</h2>", unsafe_allow_html=True)

data = load_data()
total = len(data["notes"]) + len(data["quizzes"]) + len(data["flashcards"])

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""
    <div class="metric-box">
        <div class="metric-number">""" + str(total) + """</div>
        <div class="metric-label">Total Items</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="metric-box">
        <div class="metric-number">""" + str(len(data["notes"])) + """</div>
        <div class="metric-label">Summaries</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="metric-box">
        <div class="metric-number">""" + str(len(data["quizzes"])) + """</div>
        <div class="metric-label">Quizzes</div>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown("""
    <div class="metric-box">
        <div class="metric-number">""" + str(len(data["flashcards"])) + """</div>
        <div class="metric-label">Flashcards</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# TABS
tab1, tab2, tab3 = st.tabs(["📝 Summaries", "❓ Quizzes", "📇 Flashcards"])

# TAB 1: NOTES
with tab1:
    if data["notes"]:
        for i, note in enumerate(data["notes"]):
            st.markdown(f"""
            <div class="saved-item-wrapper">
                <div class="saved-item-title">{note['title']}</div>
                <div class="saved-item-time">📅 {note['timestamp']}</div>
            </div>
            """, unsafe_allow_html=True)
            col1, col2 = st.columns([5, 1])
            with col1:
                with st.expander("👁️ View Content"):
                    st.write(note["content"])
            with col2:
                if st.button("🗑️", key=f"del_note_{i}"):
                    delete_item("notes", note["id"])
                    st.rerun()
    else:
        st.info("📌 No summaries yet. Create one and save it!")

# TAB 2: QUIZZES
with tab2:
    if data["quizzes"]:
        for i, quiz in enumerate(data["quizzes"]):
            st.markdown(f"""
            <div class="saved-item-wrapper">
                <div class="saved-item-title">{quiz['title']}</div>
                <div class="saved-item-time">📅 {quiz['timestamp']}</div>
            </div>
            """, unsafe_allow_html=True)
            col1, col2 = st.columns([5, 1])
            with col1:
                with st.expander("👁️ View Quiz"):
                    st.write(quiz["content"])
            with col2:
                if st.button("🗑️", key=f"del_quiz_{i}"):
                    delete_item("quizzes", quiz["id"])
                    st.rerun()
    else:
        st.info("📌 No quizzes yet. Create one and save it!")

# TAB 3: FLASHCARDS
with tab3:
    if data["flashcards"]:
        for i, flashcard in enumerate(data["flashcards"]):
            st.markdown(f"""
            <div class="saved-item-wrapper">
                <div class="saved-item-title">{flashcard['title']}</div>
                <div class="saved-item-time">📅 {flashcard['timestamp']}</div>
            </div>
            """, unsafe_allow_html=True)
            col1, col2 = st.columns([5, 1])
            with col1:
                with st.expander("👁️ View Flashcards"):
                    st.write(flashcard["content"])
            with col2:
                if st.button("🗑️", key=f"del_flash_{i}"):
                    delete_item("flashcards", flashcard["id"])
                    st.rerun()
    else:
        st.info("📌 No flashcards yet. Create some and save them!")

# FOOTER
st.markdown("""
<div class="footer">
    <p class="footer-text">✨ AI Study Buddy ✨</p>
    <p style="color: #999; font-size: 0.9rem; margin-top: 1rem;">Making learning smarter, faster, and more enjoyable</p>
</div>
""", unsafe_allow_html=True)