import streamlit as st
from groq import Groq

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CampusAI",
    page_icon="🎓",
    layout="centered",
)

# ── Styling ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Outfit:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
}

/* ── Deep navy + electric teal background ── */
.stApp {
    background: linear-gradient(145deg, #0a0e1a 0%, #0d1b2a 40%, #0a1628 70%, #071020 100%);
    min-height: 100vh;
}

/* Animated background dots */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image:
        radial-gradient(circle at 20% 20%, rgba(0, 212, 255, 0.07) 0%, transparent 50%),
        radial-gradient(circle at 80% 80%, rgba(99, 102, 241, 0.07) 0%, transparent 50%),
        radial-gradient(circle at 50% 50%, rgba(16, 185, 129, 0.04) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
}

/* ── All text white by default ── */
.stApp, .stApp p, .stApp li, .stApp span, .stApp label {
    color: #e2e8f0 !important;
}

h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
    color: #ffffff !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #060d1a 0%, #0a1628 100%) !important;
    border-right: 1px solid rgba(0, 212, 255, 0.15) !important;
}
[data-testid="stSidebar"] * { color: #cbd5e1 !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
    font-family: 'Syne', sans-serif !important;
}

/* ── Role buttons in sidebar ── */
div[data-testid="column"] > div > div > div > button,
[data-testid="stSidebar"] button {
    width: 100%;
    border-radius: 12px !important;
    border: 1px solid rgba(0, 212, 255, 0.25) !important;
    background: rgba(0, 212, 255, 0.06) !important;
    color: #e2e8f0 !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 14px !important;
    padding: 12px 16px !important;
    transition: all 0.2s ease !important;
}
div[data-testid="column"] > div > div > div > button:hover,
[data-testid="stSidebar"] button:hover {
    background: rgba(0, 212, 255, 0.15) !important;
    border-color: rgba(0, 212, 255, 0.5) !important;
    transform: translateY(-1px) !important;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 16px !important;
    padding: 6px 12px !important;
    margin-bottom: 8px !important;
    backdrop-filter: blur(10px) !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(0, 212, 255, 0.3) !important;
    border-radius: 24px !important;
}
[data-testid="stChatInputTextArea"] {
    color: #e2e8f0 !important;
    font-family: 'Outfit', sans-serif !important;
    background: transparent !important;
}

/* ── Quick prompt buttons ── */
.stButton > button {
    background: rgba(0, 212, 255, 0.06) !important;
    border: 1px solid rgba(0, 212, 255, 0.2) !important;
    color: #94d8e8 !important;
    border-radius: 24px !important;
    font-size: 13px !important;
    font-family: 'Outfit', sans-serif !important;
    padding: 8px 16px !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: rgba(0, 212, 255, 0.15) !important;
    border-color: rgba(0, 212, 255, 0.5) !important;
    color: #ffffff !important;
}

/* ── Status badge ── */
.status-online {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(16, 185, 129, 0.15);
    color: #6ee7b7;
    font-size: 12px;
    padding: 4px 12px;
    border-radius: 20px;
    border: 1px solid rgba(16, 185, 129, 0.3);
    font-family: 'Outfit', sans-serif;
}

/* ── Role badge ── */
.role-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(0, 212, 255, 0.1);
    color: #67e8f9;
    font-size: 13px;
    padding: 6px 14px;
    border-radius: 20px;
    border: 1px solid rgba(0, 212, 255, 0.25);
    font-family: 'Outfit', sans-serif;
    margin-bottom: 8px;
}

/* ── Hero section ── */
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 52px;
    font-weight: 800;
    background: linear-gradient(135deg, #00d4ff, #6366f1, #10b981);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    margin-bottom: 12px;
}

.hero-sub {
    color: #94a3b8;
    font-size: 16px;
    line-height: 1.7;
    font-weight: 300;
}

/* ── Divider ── */
hr {
    border-color: rgba(0, 212, 255, 0.15) !important;
    margin: 16px 0 !important;
}

/* ── Info box ── */
.stAlert {
    background: rgba(0, 212, 255, 0.08) !important;
    border: 1px solid rgba(0, 212, 255, 0.2) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
}

/* ── Input label ── */
.stTextInput label { color: #94a3b8 !important; }

/* ── Success message ── */
.stSuccess {
    background: rgba(16, 185, 129, 0.1) !important;
    border: 1px solid rgba(16, 185, 129, 0.3) !important;
    border-radius: 10px !important;
    color: #6ee7b7 !important;
}

/* ── Error message ── */
.stError {
    background: rgba(239, 68, 68, 0.1) !important;
    border: 1px solid rgba(239, 68, 68, 0.3) !important;
    border-radius: 10px !important;
}

/* ── Caption ── */
.stCaption { color: #475569 !important; font-size: 11px !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: rgba(255,255,255,0.02); }
::-webkit-scrollbar-thumb { background: rgba(0, 212, 255, 0.2); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(0, 212, 255, 0.4); }
</style>
""", unsafe_allow_html=True)


# ── API key resolution ────────────────────────────────────────────────────────
def get_hosted_key():
    try:
        return st.secrets["GROQ_API_KEY"]
    except Exception:
        pass
    import os
    return os.environ.get("GROQ_API_KEY", None)

HOSTED_KEY = get_hosted_key()


# ── Constants ─────────────────────────────────────────────────────────────────
ROLES = {
    "🎓 Student": {
        "key": "student",
        "color": "#00d4ff",
        "quick": [
            "How do I register for courses?",
            "When is the next exam period?",
            "How do I get my transcript?",
            "Where is the student health center?",
        ],
    },
    "🏛️ Staff": {
        "key": "staff",
        "color": "#6366f1",
        "quick": [
            "How do I submit a leave request?",
            "Where are the HR policies?",
            "How do I book a meeting room?",
            "IT support contact info?",
        ],
    },
    "📚 Faculty": {
        "key": "faculty",
        "color": "#10b981",
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
        return Groq(api_key=key)
    return None


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎓 CampusAI")
    st.markdown('<span class="status-online">● Live</span>', unsafe_allow_html=True)
    st.divider()

    if not HOSTED_KEY:
        st.markdown("### Setup")
        manual_key = st.text_input(
            "Groq API Key",
            type="password",
            placeholder="gsk_...",
            help="Get your free key at console.groq.com",
        )
        if manual_key:
            st.session_state.manual_api_key = manual_key
            st.success("API key set ✓")
        st.caption("🔗 [Get free key →](https://console.groq.com)")
        st.divider()

    st.markdown("### Select Your Role")
    for label, info in ROLES.items():
        if st.button(label, key=f"role_{info['key']}", use_container_width=True):
            st.session_state.role = label
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": f"Welcome! 👋 I'm **CampusAI**, your intelligent campus assistant. I'm here to help with anything — academics, services, admin, and more. What can I do for you today?",
                }
            ]
            st.rerun()

    if st.session_state.role:
        st.divider()
        role_info = ROLES[st.session_state.role]
        st.markdown(f'<span class="role-badge">{st.session_state.role}</span>', unsafe_allow_html=True)
        if st.button("🔄 Switch Role", use_container_width=True):
            st.session_state.role = None
            st.session_state.messages = []
            st.rerun()

    st.divider()
    st.caption("Powered by Groq · Responses are AI-generated")
    st.caption("Verify important info with your campus office.")


# ── Main area ─────────────────────────────────────────────────────────────────
if not st.session_state.role:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown('<div class="hero-title">CampusAI</div>', unsafe_allow_html=True)
        st.markdown('<p class="hero-sub">Your intelligent university assistant — get instant answers about academics, campus services, administration, and more.</p>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("👈 Select your role in the sidebar to get started")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**Available for:**")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("🎓 **Students**\nCourses, grades, transcripts")
        with c2:
            st.markdown("🏛️ **Staff**\nHR, facilities, admin")
        with c3:
            st.markdown("📚 **Faculty**\nGrading, LMS, research")

else:
    role_info = ROLES[st.session_state.role]

    st.markdown(f"## {st.session_state.role} Portal")
    st.markdown('<span class="status-online">● Online</span>', unsafe_allow_html=True)

    # Quick prompts
    if len(st.session_state.messages) <= 1:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**Quick questions to get you started:**")
        cols = st.columns(2)
        for i, prompt in enumerate(role_info["quick"]):
            with cols[i % 2]:
                if st.button(prompt, key=f"quick_{i}", use_container_width=True):
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    st.rerun()
        st.divider()

    # Render message history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar="🎓" if msg["role"] == "assistant" else "👤"):
            st.markdown(msg["content"])

    # Chat input
    if user_input := st.chat_input("Ask anything about campus..."):
        client = get_client()
        if not client:
            st.error("⚠️ Please enter your Groq API key in the sidebar.")
        else:
            st.session_state.messages.append({"role": "user", "content": user_input})

            with st.chat_message("user", avatar="👤"):
                st.markdown(user_input)

            with st.chat_message("assistant", avatar="🎓"):
                placeholder = st.empty()
                full_response = ""

                groq_messages = [
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT.format(role=st.session_state.role),
                    }
                ] + [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]

                stream = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=groq_messages,
                    stream=True,
                    max_tokens=1024,
                )

                for chunk in stream:
                    delta = chunk.choices[0].delta.content or ""
                    full_response += delta
                    placeholder.markdown(full_response + "▌")

                placeholder.markdown(full_response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response}
                )
