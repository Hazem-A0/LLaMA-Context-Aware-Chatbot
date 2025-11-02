import os
import streamlit as st
from agent.agent_runner import ask_agent
import time
from datetime import datetime
import base64

# ---------- CONFIG ----------
PDF_STORE = "uploaded_pdfs"
os.makedirs(PDF_STORE, exist_ok=True)

# ---------- PAGE SETTINGS ----------
st.set_page_config(
    page_title="🦙 LLaMA Context Chatbot", 
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://docs.streamlit.io/',
        'Report a bug': None,
        'About': "# LLaMA Context-Aware Chatbot\nBuilt with LangChain, Streamlit, and LLaMA"
    }
)

# ---------- CUSTOM CSS ----------
def load_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Custom header */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin: 0.5rem 0 0 0;
    }
    
    /* PDF Upload Area */
    .upload-container {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border: 2px dashed #cbd5e1;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .upload-container:hover {
        border-color: #6366f1;
        background: linear-gradient(135deg, #eef2ff 0%, #e0e7ff 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.15);
    }
    
    /* PDF List Styling */
    .pdf-item {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #6366f1;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: all 0.2s ease;
    }
    
    .pdf-item:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.15);
    }
    
    .pdf-item.selected {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border-left-color: #fff;
    }
    
    .pdf-name {
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .pdf-size {
        font-size: 0.8rem;
        opacity: 0.7;
        margin-top: 0.25rem;
    }
    
    /* Chat Container */
    .chat-container {
        background: white;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        overflow: hidden;
        height: 600px;
        display: flex;
        flex-direction: column;
    }
    
    /* Chat Header */
    .chat-header {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        padding: 1.5rem;
        text-align: center;
        position: relative;
    }
    
    .chat-header h3 {
        margin: 0;
        font-weight: 600;
        font-size: 1.2rem;
    }
    
    .context-badge {
        position: absolute;
        top: 1rem;
        right: 1rem;
        background: rgba(255,255,255,0.2);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        backdrop-filter: blur(10px);
    }
    
    /* Chat Messages */
    .chat-messages {
        flex: 1;
        overflow-y: auto;
        padding: 1.5rem;
        background: #f8fafc;
    }
    
    .message {
        margin-bottom: 1rem;
        animation: slideUp 0.3s ease;
    }
    
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .user-message {
        display: flex;
        justify-content: flex-end;
    }
    
    .bot-message {
        display: flex;
        justify-content: flex-start;
    }
    
    .message-content {
        max-width: 70%;
        padding: 1rem 1.25rem;
        border-radius: 18px;
        position: relative;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .user-message .message-content {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        margin-left: 2rem;
    }
    
    .bot-message .message-content {
        background: white;
        color: #1f2937;
        margin-right: 2rem;
        border: 1px solid #e5e7eb;
    }
    
    .message-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        margin: 0 0.5rem;
        flex-shrink: 0;
    }
    
    .user-avatar {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        order: 2;
    }
    
    .bot-avatar {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
    }
    
    .message-time {
        font-size: 0.7rem;
        opacity: 0.6;
        margin-top: 0.25rem;
    }
    
    /* Input Area */
    .input-container {
        padding: 1.5rem;
        background: transparent;
        border-top: none;
    }
    
    /* Custom buttons */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.2s ease;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
    }
    
    .secondary-button {
        background: rgba(239, 68, 68, 0.1) !important;
        color: #ef4444 !important;
        border: 1px solid rgba(239, 68, 68, 0.2) !important;
    }
    
    .secondary-button:hover {
        background: rgba(239, 68, 68, 0.2) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Metrics styling */
    .metric-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #6366f1;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #6b7280;
        margin-top: 0.25rem;
    }
    
    /* Status indicators */
    .status-online {
        color: #10b981;
        font-weight: 600;
    }
    
    .status-offline {
        color: #6b7280;
        font-weight: 600;
    }
    
    /* Loading animation */
    .typing-indicator {
        display: flex;
        align-items: center;
        padding: 1rem;
        background: white;
        border-radius: 18px;
        margin-right: 2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .typing-dots {
        display: flex;
        gap: 4px;
    }
    
    .dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #6b7280;
        animation: bounce 1.4s infinite ease-in-out;
    }
    
    .dot:nth-child(1) { animation-delay: -0.32s; }
    .dot:nth-child(2) { animation-delay: -0.16s; }
    .dot:nth-child(3) { animation-delay: 0s; }
    
    @keyframes bounce {
        0%, 80%, 100% {
            transform: scale(0.8);
            opacity: 0.5;
        }
        40% {
            transform: scale(1);
            opacity: 1;
        }
    }
    
    /* Scrollbar styling */
    .chat-messages::-webkit-scrollbar {
        width: 6px;
    }
    
    .chat-messages::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 3px;
    }
    
    .chat-messages::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 3px;
    }
    
    .chat-messages::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }
    
    /* Empty state */
    .empty-state {
        text-align: center;
        padding: 3rem 2rem;
        color: #6b7280;
    }
    
    .empty-state-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        opacity: 0.3;
    }
    
    .empty-state h3 {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #374151;
    }
    
    .empty-state p {
        font-size: 1rem;
        line-height: 1.6;
        max-width: 400px;
        margin: 0 auto;
    }
    
    /* Permanent toggle button for sidebar - always visible */
    .sidebar-toggle-fixed {
        position: fixed;
        top: 20px;
        left: 20px;
        z-index: 99999;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
        transition: all 0.2s ease;
        font-size: 0.85rem;
        font-weight: 600;
        white-space: nowrap;
    }
    
    .sidebar-toggle-fixed:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 1.8rem;
        }
        
        .chat-container {
            height: 500px;
        }
        
        .message-content {
            max-width: 85%;
        }
        
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        .sidebar-toggle {
            width: 45px;
            height: 45px;
            top: 15px;
            left: 15px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# ---------- HELPER FUNCTIONS ----------
def format_file_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0B"
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024
        i += 1
    return f"{size_bytes:.1f}{size_names[i]}"

def get_pdf_info(pdf_path):
    """Get PDF file information"""
    if os.path.exists(pdf_path):
        size = os.path.getsize(pdf_path)
        return {
            'size': format_file_size(size),
            'exists': True
        }
    return {'exists': False}

# ---------- INITIALIZE SESSION STATE ----------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "selected_pdf" not in st.session_state:
    st.session_state.selected_pdf = None

if "typing" not in st.session_state:
    st.session_state.typing = False

# ---------- LOAD CUSTOM CSS ----------
load_css()

# Add a permanent toggle button using HTML/JS that actually works
st.markdown("""
<button class="sidebar-toggle-fixed" onclick="toggleSidebar()" id="sidebarToggleBtn">
    📂 Document     
</button>

<script>
function toggleSidebar() {
    // Try multiple methods to find and click the sidebar toggle
    const selectors = [
        '[data-testid="collapsedControl"]',
        '[data-testid="stSidebarNav"] button',
        '.css-1cypcdb',
        'button[kind="header"]',
        '[title*="navigation"]',
        '[aria-label*="navigation"]'
    ];
    
    let found = false;
    for (let selector of selectors) {
        const element = document.querySelector(selector);
        if (element && element.offsetParent !== null) {
            element.click();
            found = true;
            break;
        }
    }
    
    // If no toggle found, try to find any button in the header area
    if (!found) {
        const headerButtons = document.querySelectorAll('header button, .stApp > header button');
        for (let btn of headerButtons) {
            if (btn.offsetParent !== null) {
                btn.click();
                break;
            }
        }
    }
}

// Update button text based on sidebar state
function updateToggleButton() {
    const btn = document.getElementById('sidebarToggleBtn');
    const sidebar = document.querySelector('[data-testid="stSidebar"]');
    const collapsedControl = document.querySelector('[data-testid="collapsedControl"]');
    
    if (btn) {
        if (collapsedControl && collapsedControl.offsetParent !== null) {
            btn.textContent = '📂 Show Sidebar';
        } else if (sidebar && sidebar.offsetParent !== null) {
            btn.textContent = '📁 Hide Sidebar';
        } else {
            btn.textContent = '📂 Document Manager';
        }
    }
}

// Watch for changes and update button
const observer = new MutationObserver(updateToggleButton);
if (document.body) {
    observer.observe(document.body, {
        childList: true,
        subtree: true,
        attributes: true,
        attributeFilter: ['style', 'class']
    });
}

// Initial update
setTimeout(updateToggleButton, 500);
setInterval(updateToggleButton, 1000);
</script>
""", unsafe_allow_html=True)

# ---------- MAIN HEADER ----------
st.markdown("""
<div class="main-header">
    <h1>🦙 LLaMA Context-Aware Chatbot</h1>
    <p>Upload documents and ask intelligent questions with context awareness</p>
</div>
""", unsafe_allow_html=True)

# ---------- SIDEBAR: PDF MANAGEMENT ----------
with st.sidebar:
    st.markdown("### 📂 Document Manager")
    
    # Upload section
    st.markdown("""
    <div class="upload-container">
        <h4>📤 Upload Documents</h4>
        <p>Drag & drop or browse for PDF files</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(
        "Choose PDF files", 
        type=["pdf"], 
        accept_multiple_files=True,
        help="Upload one or more PDF files to provide context for your questions"
    )
    
    # Handle file uploads
    if uploaded_files:
        for uploaded_file in uploaded_files:
            pdf_path = os.path.join(PDF_STORE, uploaded_file.name)
            
            # Save file if it doesn't exist
            if not os.path.exists(pdf_path):
                with open(pdf_path, "wb") as f:
                    f.write(uploaded_file.read())
                st.success(f"✅ Saved: {uploaded_file.name}")
    
    # Display uploaded PDFs
    pdf_files = [f for f in os.listdir(PDF_STORE) if f.endswith('.pdf')]
    
    if pdf_files:
        st.markdown("### 📚 Available Documents")
        
        for pdf_file in pdf_files:
            pdf_path = os.path.join(PDF_STORE, pdf_file)
            pdf_info = get_pdf_info(pdf_path)
            
            is_selected = st.session_state.selected_pdf == pdf_file
            
            # Create columns for PDF item
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                if st.button(
                    f"📄 {pdf_file[:20]}..." if len(pdf_file) > 20 else f"📄 {pdf_file}",
                    key=f"select_{pdf_file}",
                    help=f"Click to select for context\nSize: {pdf_info['size']}",
                    type="primary" if is_selected else "secondary"
                ):
                    st.session_state.selected_pdf = pdf_file
                    st.rerun()
            
            with col2:
                st.markdown(f"<small>{pdf_info['size']}</small>", unsafe_allow_html=True)
            
            with col3:
                if st.button("🗑️", key=f"delete_{pdf_file}", help="Delete file"):
                    os.remove(pdf_path)
                    if st.session_state.selected_pdf == pdf_file:
                        st.session_state.selected_pdf = None
                    st.rerun()
    
    else:
        st.info("📝 No documents uploaded yet. Upload a PDF to get started!")
    
    # Statistics
    st.markdown("---")
    st.markdown("### 📊 Statistics")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{len(pdf_files)}</div>
            <div class="metric-label">Documents</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{len(st.session_state.chat_history)}</div>
            <div class="metric-label">Messages</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Context status
    if st.session_state.selected_pdf:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
                    color: white; padding: 1rem; border-radius: 8px; text-align: center; margin-top: 1rem;">
            <strong>🎯 Context Active</strong><br>
            <small>{st.session_state.selected_pdf}</small>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: #f3f4f6; color: #6b7280; padding: 1rem; border-radius: 8px; text-align: center; margin-top: 1rem;">
            <strong>⚪ No Context</strong><br>
            <small>Select a document for context-aware responses</small>
        </div>
        """, unsafe_allow_html=True)

# ---------- MAIN CHAT INTERFACE ----------
chat_col1, chat_col2 = st.columns([3, 1])

with chat_col1:
    # Chat header with context indicator
    context_badge = ""
    if st.session_state.selected_pdf:
        context_badge = f'<div class="context-badge">📄 {st.session_state.selected_pdf[:15]}...</div>'
    
    st.markdown(f"""
    <div class="chat-header">
        <h3>💬 Intelligent Assistant</h3>
        {context_badge}
    </div>
    """, unsafe_allow_html=True)
    
    # Chat messages container
    chat_container = st.container()
    
    with chat_container:
        if st.session_state.chat_history:
            # Display chat messages
            for i, (speaker, message) in enumerate(st.session_state.chat_history):
                timestamp = datetime.now().strftime("%H:%M")
                
                if speaker == "user":
                    st.markdown(f"""
                    <div class="message user-message">
                        <div class="message-content">
                            {message}
                            <div class="message-time">{timestamp}</div>
                        </div>
                        <div class="message-avatar user-avatar">🧑</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="message bot-message">
                        <div class="message-avatar bot-avatar">🤖</div>
                        <div class="message-content">
                            {message}
                            <div class="message-time">{timestamp}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Show typing indicator
            if st.session_state.typing:
                st.markdown("""
                <div class="message bot-message">
                    <div class="message-avatar bot-avatar">🤖</div>
                    <div class="typing-indicator">
                        <span>Assistant is typing</span>
                        <div class="typing-dots">
                            <div class="dot"></div>
                            <div class="dot"></div>
                            <div class="dot"></div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        else:
            # Empty state
            st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">💬</div>
                <h3>Start a Conversation</h3>
                <p>Upload a document and ask me anything! I'll provide context-aware responses based on your uploaded materials.</p>
            </div>
            """, unsafe_allow_html=True)

# ---------- INPUT AREA ----------
# Remove the white container div and apply dark styling
st.markdown("""
<style>
.stTextArea > div > div > textarea {
    background-color: #374151 !important;
    color: white !important;
    border: 2px solid #4b5563 !important;
    border-radius: 12px !important;
}
.stTextArea > div > div > textarea:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
}
.stTextArea label {
    color: white !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

input_col1, input_col2, input_col3 = st.columns([4, 1, 1])

with input_col1:
    user_input = st.text_area(
        "Your question:",
        placeholder="Ask me anything about your documents...",
        height=100,
        key="message_input"
    )

with input_col2:
    send_button = st.button("🚀 Send", type="primary", use_container_width=True)

with input_col3:
    clear_button = st.button("🗑️ Clear", type="secondary", use_container_width=True)

# Remove the closing div since we removed the opening one

# ---------- HANDLE USER INPUT ----------
def send_message():
    if user_input.strip():
        # Add user message to history
        st.session_state.chat_history.append(("user", user_input.strip()))
        
        # Show typing indicator
        st.session_state.typing = True
        st.rerun()

def process_message():
    if st.session_state.typing and st.session_state.chat_history:
        last_message = st.session_state.chat_history[-1]
        if last_message[0] == "user":
            # Get PDF bytes if selected
            pdf_bytes = None
            if st.session_state.selected_pdf:
                pdf_path = os.path.join(PDF_STORE, st.session_state.selected_pdf)
                try:
                    with open(pdf_path, "rb") as f:
                        pdf_bytes = f.read()
                except Exception as e:
                    st.error(f"Error reading PDF: {e}")
            
            # Get response from agent
            try:
                with st.spinner("Processing your question..."):
                    response = ask_agent(last_message[1], pdf_bytes=pdf_bytes)
                
                # Add bot response to history
                st.session_state.chat_history.append(("assistant", response))
                
            except Exception as e:
                error_msg = f"I apologize, but I encountered an error while processing your request: {str(e)}"
                st.session_state.chat_history.append(("assistant", error_msg))
            
            finally:
                st.session_state.typing = False
                st.rerun()

# Handle button clicks
if send_button and user_input.strip():
    send_message()

if clear_button and st.session_state.chat_history:
    st.session_state.chat_history = []
    st.session_state.typing = False
    st.rerun()

# Process pending messages
if st.session_state.typing:
    process_message()

# ---------- FOOTER ----------
with st.sidebar:
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6b7280; font-size: 0.8rem;">
        <p>Built with ❤️ using</p>
        <p><strong>LangChain • Streamlit • LLaMA</strong></p>
        <p>v2.0 - Enhanced UI/UX</p>
    </div>
    """, unsafe_allow_html=True)