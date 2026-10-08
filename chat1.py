import streamlit as st
from google import genai

# ==========================================
# 1. API KEY CONFIGURATION
# Direct placement of your Google AI Studio API key
# ==========================================
GEMINI_API_KEY = "AQ.Ab8RN6J3VMAgMpTgYLC0kqzXJH0KFadw3jIWNJgqLnScvmzaIQ"

# Initialize the Gemini Client
client = genai.Client(api_key=GEMINI_API_KEY)

# ==========================================
# 2. STREAMLIT APP & PAGE CONFIGURATION
# ==========================================
st.set_page_config(page_title="Pranasya's Chatbot", page_icon="🌸", layout="centered")

# Custom CSS for Light Pink Theme & Interactive Hover Effects
st.markdown("""
    <style>
    /* Main Background - Light Soft Pink */
    .stApp {
        background-color: #FFF0F5;
    }
    
    /* Header & Titles styling */
    h1, h2, h3, .stCaption {
        color: #4A2E35 !important;
    }

    /* User Chat Bubble Styling & Hover */
    [data-testid="stChatMessage"][data-testid-user="true"],
    div[data-testid="stChatMessage"]:has(div[aria-label="Chat message from user"]) {
        background-color: #FFE4E1 !important;
        border-radius: 12px;
        padding: 10px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    div[data-testid="stChatMessage"]:hover {
        transform: translateY(-2px);
        box-shadow: 0px 4px 12px rgba(219, 112, 147, 0.25);
    }

    /* Chat Input Bar Styling & Focus/Hover Effects */
    div[data-testid="stChatInput"] input {
        background-color: #FFFFFF !important;
        border: 2px solid #FFC0CB !important;
        border-radius: 10px;
        transition: all 0.3s ease;
    }

    div[data-testid="stChatInput"] input:hover {
        border-color: #FF69B4 !important;
        box-shadow: 0 0 8px rgba(255, 105, 180, 0.3);
    }

    div[data-testid="stChatInput"] input:focus {
        border-color: #DB7093 !important;
        box-shadow: 0 0 10px rgba(219, 112, 147, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# Title updated to Pranasya's Chatbot
st.title("🌸 Pranasya's Chatbot")
st.caption("A personalized Streamlit chat application powered by Gemini 3.8")

# ==========================================
# 3. SESSION STATE FOR CHAT HISTORY
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages in the chat UI
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ==========================================
# 4. CHAT INPUT & LLM RESPONSE LOGIC
# ==========================================
user_prompt = st.chat_input("Ask Pranasya's Chatbot anything...")

if user_prompt:
    # 1. Show user message in the chat container
    with st.chat_message("user"):
        st.write(user_prompt)
    
    # 2. Append user message to state history
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    # 3. Call Google Studio (Gemini) API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Format chat history for Gemini
                formatted_contents = [
                    {"role": "user" if msg["role"] == "user" else "model", "parts": [{"text": msg["content"]}]}
                    for msg in st.session_state.messages
                ]

                # Generate content using Gemini 3.8 Flash
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=formatted_contents
                )

                response_text = response.text
                st.write(response_text)

                # Append model response to session state history
                st.session_state.messages.append({"role": "assistant", "content": response_text})

            except Exception as e:
                st.error(f"Error calling Google API: {e}")