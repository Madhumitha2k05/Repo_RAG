import streamlit as st
import requests

# ============================================
# BACKEND URLS
# ============================================
ASK_API = "http://127.0.0.1:8000/ask"
LOAD_REPO_API = "http://127.0.0.1:8000/load_repo"

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="Repo_RAG",
    page_icon="🤖",
    layout="centered"
)

# ============================================
# BEAUTIFUL CSS
# ============================================
creative_design = """
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"]  {
    font-family: 'Poppins', sans-serif !important;
}

/* Animated Background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(-45deg,
        #ffc8dd,
        #a2d2ff,
        #cdb4db,
        #bde0fe,
        #fde4cf);
    background-size: 400% 400%;
    animation: gradient 12s ease infinite;
}

/* Animation */
@keyframes gradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Transparent Header */
[data-testid="stHeader"] {
    background: transparent;
}

/* Main Title */
.main-title {
    text-align: center;
    font-size: 50px;
    font-weight: 700;
    color: white;
    margin-top: 10px;
    text-shadow: 2px 2px 10px rgba(0,0,0,0.2);
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: white;
    font-size: 16px;
    margin-bottom: 30px;
}

/* Glass Box */
.glass-box {
    background: rgba(255,255,255,0.18);
    border-radius: 20px;
    padding: 20px;
    backdrop-filter: blur(14px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.10);
    border: 1px solid rgba(255,255,255,0.2);
    margin-bottom: 20px;
}

/* Text Input */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.4) !important;
    border: 1px solid rgba(255,255,255,0.5) !important;
    border-radius: 12px !important;
    color: #333 !important;
    padding: 12px !important;
    font-size: 15px !important;
}

/* Buttons */
div.stButton > button:first-child {
    width: 100%;
    border-radius: 12px !important;
    height: 45px;
    border: none;
    font-size: 15px;
    font-weight: 600;
    color: white;
    background: linear-gradient(to right, #ff758c, #ff7eb3);
    transition: 0.3s;
}

div.stButton > button:first-child:hover {
    transform: scale(1.02);
    box-shadow: 0 5px 15px rgba(0,0,0,0.15);
}

/* Chat Bubbles */
.user-msg {
    background: rgba(255,255,255,0.4);
    padding: 12px 16px;
    border-radius: 15px 15px 0px 15px;
    margin-bottom: 10px;
    color: #222;
    text-align: right;
    width: fit-content;
    float: right;
    clear: both;
}

.bot-msg {
    background: rgba(255,255,255,0.2);
    padding: 12px 16px;
    border-radius: 15px 15px 15px 0px;
    margin-bottom: 15px;
    color: #222;
    text-align: left;
    width: fit-content;
    float: left;
    clear: both;
}

/* Clearfix for chat bubbles */
.chat-container::after {
    content: "";
    clear: both;
    display: table;
}

/* Styling Streamlit Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 20px;
    justify-content: center;
}
.stTabs [data-baseweb="tab"] {
    background-color: rgba(255, 255, 255, 0.2);
    border-radius: 10px 10px 0px 0px;
    padding: 10px 20px;
}
.stTabs [aria-selected="true"] {
    background-color: rgba(255, 255, 255, 0.4);
    border-bottom-color: transparent !important;
}

</style>
"""

st.markdown(creative_design, unsafe_allow_html=True)

# ============================================
# TITLE
# ============================================
st.markdown("<div class='main-title'>🤖 Repo RAG</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>AI Powered Repository Assistant 🚀</div>", unsafe_allow_html=True)

# ============================================
# SESSION STATE (Separate memory for tabs)
# ============================================
if "general_msgs" not in st.session_state:
    st.session_state.general_msgs = []
if "repo_msgs" not in st.session_state:
    st.session_state.repo_msgs = []

# ============================================
# NAVIGATION TABS
# ============================================
tab1, tab2 = st.tabs(["💬 General Chatbot", "📂 Repocode Assistant"])

# --------------------------------------------
# TAB 1: GENERAL CHATBOT
# --------------------------------------------
with tab1:
    st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
    st.subheader("💬 Ask Anything")
    
    # Display Chat History (General)
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for msg in st.session_state.general_msgs:
        if msg["role"] == "user":
            st.markdown(f"<div class='user-msg'><b>You:</b><br>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-msg'>🤖 <b>Repocode:</b><br>{msg['content']}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Input and Buttons
    general_input = st.text_input("", placeholder="Ask a general coding question...", key="gen_input")
    
    col1, col2 = st.columns(2)
    with col1:
        ask_gen = st.button("💬 Ask Bot", key="btn_ask_gen")
    with col2:
        clear_gen = st.button("🗑 Clear Chat", key="btn_clear_gen")

    # Ask Logic (General)
    if ask_gen:
        if general_input:
            st.session_state.general_msgs.append({"role": "user", "content": general_input})
            try:
                with st.spinner("Thinking... 🤔"):
                    response = requests.post(ASK_API, json={"question": general_input}, timeout=60)
                    if response.status_code == 200:
                        answer = response.json().get("response", "No response from AI")
                        st.session_state.general_msgs.append({"role": "assistant", "content": answer})
                        st.rerun()
                    else:
                        st.error("Server Error")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Enter a question first")

    # Clear Logic (General)
    if clear_gen:
        st.session_state.general_msgs = []
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


# --------------------------------------------
# TAB 2: REPOCODE ASSISTANT (Load + Chat)
# --------------------------------------------
with tab2:
    # 1. Load Repo Section
    st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
    st.subheader("📂 Load GitHub Repository")
    
    repo_url = st.text_input("Paste Repository URL", placeholder="https://github.com/user/repository.git", key="repo_url")
    
    if st.button("🚀 Load Repository", key="btn_load_repo"):
        if repo_url:
            try:
                with st.spinner("Loading repository..."):
                    response = requests.post(LOAD_REPO_API, json={"repo_url": repo_url}, timeout=60)
                    if response.status_code == 200:
                        st.success("✅ Repository Loaded Successfully!")
                    else:
                        st.error("❌ Failed to load repository")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter repository URL")
    st.markdown("</div>", unsafe_allow_html=True)

    # 2. Repo Chat Section
    st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
    st.subheader("💬 Ask about the Repository")

    # Display Chat History (Repo)
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for msg in st.session_state.repo_msgs:
        if msg["role"] == "user":
            st.markdown(f"<div class='user-msg'><b>You:</b><br>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-msg'>🤖 <b>Repocode:</b><br>{msg['content']}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Input and Buttons
    repo_input = st.text_input("", placeholder="Ask about the loaded code...", key="rep_input")
    
    col3, col4 = st.columns(2)
    with col3:
        ask_repo = st.button("💬 Ask Repocode", key="btn_ask_repo")
    with col4:
        clear_repo = st.button("🗑 Clear Chat", key="btn_clear_repo")

    # Ask Logic (Repo)
    if ask_repo:
        if repo_input:
            st.session_state.repo_msgs.append({"role": "user", "content": repo_input})
            try:
                with st.spinner("Searching repository... 🔍"):
                    response = requests.post(ASK_API, json={"question": repo_input}, timeout=60)
                    if response.status_code == 200:
                        answer = response.json().get("response", "No response from AI")
                        st.session_state.repo_msgs.append({"role": "assistant", "content": answer})
                        st.rerun()
                    else:
                        st.error("Server Error")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Enter a question first")

    # Clear Logic (Repo)
    if clear_repo:
        st.session_state.repo_msgs = []
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)