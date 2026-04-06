import streamlit as st
import anthropic

# ── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CampusAI",
    page_icon="🎓",
    layout="centered",
)

# ── Styling ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
h1, h2, h3 { font-family: 'Playfair Display', serif !important; }

.stApp { background: linear-gradient(135deg, #f5f3ef 0%, #e8e4dc 100%); }

[data-testid="stChatMessage"] {
    background: white;
    border-radius: 16px;
    padding: 4px 8px;
    margin-bottom: 6px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

[data-testid="stSidebar"] { background: #1a1a2e !important; }
[data-testid="stSidebar"] * { color: #e5e7eb !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: white !important; }

div[data-testid="column"] > div > div > div > button {
    width: 100%;
    border-radius: 14px !important;
    border: 1.5px solid rgba(255,255,255,0.15) !important;
    background: rgba(255,255,255,0.07) !important;
    color: white !important;
    font-size: 15px !important;
    padding: 14px !important;
    transition: all 0.2s ease;
}
div[data-testid="column"] > div > div > div > button:hover {
    background: rgba(255,255,255,0.15) !important;
}

.status-badge {
    display: inline-block;
    background: #dcfce7;
    color: #166534;
    font-size: 12px;
    padding: 3px 10px;
    border-radius: 12px;
    margin-top: 4px;
}

hr { border-color: rgba(255,255,255,0.1) !important; }
</style>
""", unsafe_allow_html=True)


# ── API key resolution (secrets → env → sidebar input) ───────────────────────
def get_hosted_key():
    """Check Streamlit secrets first, then environment variable."""
    try:
        return st.secrets["ANTHROPIC_API_KEY"]
    except Exception:
        pass
    import os
    return os.environ.get("ANTHROPIC_API_KEY", None)


HOSTED_KEY = get_hosted_key()


# ── Constants ─────────────────────────────────────────────────────────────────
ROLES = {
    "🎓 Student": {
        "key": "student",
        "quick": [
            "How do I register for courses?",
            "When is the next exam period?",
            "How do I get my transcript?",
            "Where is the student health center?",
        ],
    },
    "🏛️ Staff": {
        "key": "staff",
        "quick": [
            "How do I submit a leave request?",
            "Where are the HR policies?",
            "How do I book a meeting room?",
            "IT support contact info?",
        ],
    },
    "📚 Faculty": {
        "key": "faculty",
        "quick": [
            "How do I submit final grades?",
            "What's the research grant deadline?",
            "How do I access the LMS?",
            "Academic calendar for this term?",
        ],
    },
}

SYSTEM_PROMPT = """You are CampusAI, a helpful and warm assistant for university staff, students, and faculty.

You assist with:
- Academic queries: course registration, schedules, grades, transcripts, deadlines
- Campus services: library, health center, IT support, housing, cafeteria
- Administrative tasks: forms, policies, procedures, official contacts
- Staff/HR support: leave requests, payroll, facilities, departmental processes
- Faculty support: grading systems, LMS, research grants, academic calendar
- General campus life: events, clubs, security, campus transport

Guidelines:
- Be warm, professional, and concise
- Use bullet points for multi-step instructions
- If you don't know a specific policy or date, advise the user to verify with the relevant department
- Never fabricate specific deadlines, fees, or names
- Always end complex answers by suggesting who to contact for official confirmation

The current user role is: {role}
"""


# ── Session state ─────────────────────────────────────────────────────────────
if "role" not in st.session_state:
    st.session_state.role = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "manual_api_key" not in st.session_state:
    st.session_state.manual_api_key = ""


def get_client():
    key = HOSTED_KEY or st.session_state.manual_api_key
    if key:
        return anthropic.Anthropic(api_key=key)
    return None


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎓 CampusAI")
    st.markdown("*Your campus assistant*")
    st.markdown('<span class="status-badge">● Online</span>', unsafe_allow_html=True)
    st.divider()

    if not HOSTED_KEY:
        st.markdown("### Setup")
        manual_key = st.text_input(
            "Anthropic API Key",
            type="password",
            placeholder="sk-ant-...",
            help="Get your key at console.anthropic.com",
        )
        if manual_key:
            st.session_state.manual_api_key = manual_key
            st.success("API key set ✓")
        st.divider()

    st.markdown("### Select Role")
    for label, info in ROLES.items():
        if st.button(label, key=f"role_{info['key']}", use_container_width=True):
            st.session_state.role = label
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "Welcome! 👋 I'm **CampusAI**, your campus assistant. What can I help you with today?",
                }
            ]
            st.rerun()

    if st.session_state.role:
        st.divider()
        st.markdown(f"**Active:** {st.session_state.role}")
        if st.button("🔄 Switch Role", use_container_width=True):
            st.session_state.role = None
            st.session_state.messages = []
            st.rerun()

    st.divider()
    st.caption("AI-generated responses — verify important details with the relevant office.")


# ── Main area ─────────────────────────────────────────────────────────────────
if not st.session_state.role:
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("# CampusAI")
        st.markdown("#### Your intelligent university assistant")
        st.markdown("""
Get instant answers about campus life, academics, administration, and more.

**To get started:**
1. Select your role in the sidebar 👈
2. Start chatting!
        """)
else:
    role_info = ROLES[st.session_state.role]
    st.markdown(f"## {st.session_state.role} Portal")
    st.markdown('<span class="status-badge">● Live</span>', unsafe_allow_html=True)

    if len(st.session_state.messages) <= 1:
        st.markdown("**Quick questions:**")
        cols = st.columns(2)
        for i, prompt in enumerate(role_info["quick"]):
            with cols[i % 2]:
                if st.button(prompt, key=f"quick_{i}", use_container_width=True):
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    st.rerun()
        st.divider()

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar="🎓" if msg["role"] == "assistant" else "👤"):
            st.markdown(msg["content"])

    if user_input := st.chat_input("Ask anything about campus..."):
        client = get_client()
        if not client:
            st.error("⚠️ Please enter your Anthropic API key in the sidebar.")
        else:
            st.session_state.messages.append({"role": "user", "content": user_input})

            with st.chat_message("user", avatar="👤"):
                st.markdown(user_input)

            with st.chat_message("assistant", avatar="🎓"):
                placeholder = st.empty()
                full_response = ""

                with client.messages.stream(
                    model="claude-sonnet-4-20250514",
                    max_tokens=1024,
                    system=SYSTEM_PROMPT.format(role=st.session_state.role),
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                ) as stream:
                    for text in stream.text_stream:
                        full_response += text
                        placeholder.markdown(full_response + "▌")

                placeholder.markdown(full_response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response}
                )
