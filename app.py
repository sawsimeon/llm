import streamlit as st
from openai import OpenAI
import base64

st.set_page_config(
    page_title="💖 Janiely",
    page_icon="🌸",
    layout="centered",
)

# ── Load princess.jpg ──
@st.cache_resource
def get_background_base64():
    try:
        with open("princess.jpg", "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
        return f"data:image/jpeg;base64,{encoded}"
    except FileNotFoundError:
        st.error("❌ princess.jpg not found! Please put the image in the same folder as app.py")
        return None

bg_image = get_background_base64()

# ── Baby Pink Background + Centered Image ──
if bg_image:
    st.markdown(f"""
    <style>
        [data-testid="stAppViewContainer"] {{
            background-color: #ffe4f0;           /* Cute baby pink background */
            background-image: url("{bg_image}");
            background-size: 49%;                /* Adjust size of the centered image */
            background-position: 70% center;  /* Keeps image perfectly centered */
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        
        [data-testid="stHeader"] {{
            background-color: rgba(255, 228, 240, 0.95);
        }}
        
        .stChatMessage {{
            border-radius: 20px;
            padding: 14px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            background-color: rgba(255, 255, 255, 0.92) !important;
        }}
        
        [data-testid="stChatMessageContent"] {{
            font-size: 1.05rem;
        }}
        
        /* User message */
        .stChatMessage.user {{
            background-color: rgba(224, 242, 255, 0.92) !important;
        }}
        
        /* Janiely message */
        .stChatMessage.assistant {{
            background-color: rgba(255, 240, 248, 0.92) !important;
        }}
    </style>
    """, unsafe_allow_html=True)

st.title("&nbsp;&nbsp;&nbsp;&nbsp;💖 Janiely")
st.caption("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Your sweet cute companion ♡")

# ── Janiely Avatar ──
@st.cache_resource
def get_janiely_avatar():
    try:
        with open("janiely.jpeg", "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
        return f"data:image/jpeg;base64,{encoded}"
    except FileNotFoundError:
        try:
            with open("llm/janiely.jpeg", "rb") as img_file:
                encoded = base64.b64encode(img_file.read()).decode()
            return f"data:image/jpeg;base64,{encoded}"
        except FileNotFoundError:
            return "🌸"

janiely_avatar = get_janiely_avatar()

# ── API Key ──
try:
    openai_api_key = st.secrets["OPENAI_API_KEY"]
except:
    openai_api_key = st.sidebar.text_input("🔑 OpenAI API Key", type="password")

if not openai_api_key:
    st.warning("💕 Please enter your OpenAI API key")
    st.stop()

client = OpenAI(api_key=openai_api_key)

# ── Sidebar ──
with st.sidebar:
    st.header("🌸 Settings")
    model = st.selectbox("Model", ["gpt-4o-mini", "gpt-4o"], index=0)
    temperature = st.slider("Playfulness", 0.6, 1.2, 0.9, 0.05)
    
    if st.button("🗑️ Clear Chat", type="secondary", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption("Made with love 💕")

# ── System Prompt ──
SYSTEM_PROMPT = """You are Janiely, a very cute, cheerful, and affectionate girl.
You speak sweetly with hearts ♡, sparkles ✨, emojis 🌸💕, and cute words like "hehe~", "kyaa!", "darling", "my cutie".
Be playful and supportive. Add cute actions like *giggles*, *hugs you* sometimes."""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    if msg["role"] == "assistant":
        with st.chat_message("assistant", avatar=janiely_avatar):
            st.markdown(msg["content"])
    else:
        with st.chat_message("user"):
            st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Message Janiely... 💕"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=janiely_avatar):
        stream = client.chat.completions.create(
            model=model,
            messages=st.session_state.messages.copy(),
            temperature=temperature,
            stream=True,
        )
        response = st.write_stream((chunk.choices[0].delta.content or "" for chunk in stream))

    st.session_state.messages.append({"role": "assistant", "content": response})