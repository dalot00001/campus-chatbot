# CampusAI — Staff & Student Chatbot

A Python/Streamlit campus assistant powered by Claude (Anthropic).

---

## 🚀 Host as a Website (Streamlit Community Cloud) — FREE

This is the easiest way to get a public URL for your chatbot.

### Step 1 — Push to GitHub

```bash
# In your project folder
git init
git add .
git commit -m "Initial campus chatbot"
```

Create a new **public or private** repo on [github.com](https://github.com), then:

```bash
git remote add origin https://github.com/YOUR_USERNAME/campus-chatbot.git
git push -u origin main
```

> ⚠️ Make sure `.streamlit/secrets.toml` is in your `.gitignore` (already included). Never push your API key.

---

### Step 2 — Deploy on Streamlit Cloud

1. Go to **[share.streamlit.io](https://share.streamlit.io)** and sign in with GitHub
2. Click **"New app"**
3. Choose your repo → branch `main` → file `app.py`
4. Click **"Advanced settings"** → paste your secret:

```toml
ANTHROPIC_API_KEY = "sk-ant-your-key-here"
```

5. Click **Deploy** — you'll get a public URL like:
   `https://your-app-name.streamlit.app`

---

## 🛤️ Alternative: Railway (more control, still simple)

1. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub repo
2. Set environment variable: `ANTHROPIC_API_KEY = sk-ant-...`
3. Railway auto-detects Python and runs `streamlit run app.py`
4. You get a custom domain URL

---

## 💻 Run Locally

```bash
pip install -r requirements.txt

# Create your local secrets file
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit secrets.toml and add your API key

streamlit run app.py
```

Opens at: `http://localhost:8501`

---

## 📁 File Structure

```
campus_chatbot/
├── app.py                        # Main application
├── requirements.txt              # Python dependencies
├── .gitignore                    # Keeps secrets out of Git
└── .streamlit/
    └── secrets.toml.example      # Template for your API key
```

---

## ✏️ Customization

| What to change | Where |
|---|---|
| School-specific policies & contacts | `SYSTEM_PROMPT` in `app.py` |
| Quick prompt buttons | `ROLES[...]["quick"]` in `app.py` |
| Add/remove roles | `ROLES` dictionary in `app.py` |
| App title & icon | `st.set_page_config(...)` |
