import os

import anthropic
import streamlit as st
from dotenv import load_dotenv 
#from htmlTemplates import css, bot_template, user_template

st.title("Claude AI ChatBot")
#st.markdown(css, unsafe_allow_html=True)

st.markdown("""
<style>
/* Style the bottom container to look like one unified chat input box */
div[data-testid="stBottomBlockContainer"] div[data-testid="stHorizontalBlock"] {
    background-color: #FFFFFF;
    border: 1px solid #4a4b55;
    border-radius: 1.5rem;
    padding: 0.25rem 0.75rem;
    align-items: center;
}

/* Remove default borders from selectbox and chat_input inside the bar */
div[data-testid="stBottomBlockContainer"] div[data-baseweb="select"] > div {
    background-color: transparent !important;
    border: none !important;
}
div[data-testid="stBottomBlockContainer"] div[data-testid="stChatInput"] > div {
    background-color: transparent !important;
    border: none !important;
}
</style>

""", unsafe_allow_html=True)

st.markdown("""
<style>
/* Style the bottom container to look like one unified chat input box */
div[data-testid="selectEffortBlock"] div[data-testid="selectEffortBlock"] {
    background-color: #FFFFFF;
    border: 1px solid #4a4b55;
    border-radius: 1.5rem;
    padding: 0.25rem 0.75rem;
    align-items: center;
}

/*  Remove default borders from selectbox and chat_input inside the bar */
div[data-testid="selectEffortBlock"] div[data-baseweb="select"] > div {
    background-color: transparent !important;
    border: none !important;
}
div[data-testid="selectEffortBlock"] div[data-testid="stChatInput"] > div {
    background-color: transparent !important;
    border: none !important;
}
</style>

""", unsafe_allow_html=True)
def chatInput():
    with st.bottom:
        col1, col2, col3 = st.columns([1.2, 0.8, 3.8], vertical_alignment="center")
        with col1:
            agent_mode = st.selectbox(
                "Agent",
                ["claude-haiku-5-5", "claude-sonnet-5-5", "claude-opus-5-5"],
                label_visibility="collapsed",
            )
        with col2:
            modelOption = st.selectbox(
                "Model",
                ["low", "medium", "high", "xhigh", "max"],
                label_visibility="collapsed",
            )
        with col3:
            userPrompt = st.chat_input("Message...")


    return (agent_mode, modelOption, userPrompt)


st.session_state.setdefault("messages", [])


def get_api_key() -> str | None:
    """Prefer Streamlit secrets, then fall back to the environment."""
    try:
        api_key = st.secrets["ANTHROPIC_API_KEY"]
    except Exception:
        api_key = None

    return api_key or os.getenv("ANTHROPIC_API_KEY")


agent_mode, modelOption, userPrompt = chatInput()
for chat_message in st.session_state.messages:
    with st.chat_message(chat_message["role"]):
        st.markdown(chat_message["content"])

if userPrompt and userPrompt.strip():
    st.session_state.messages.append({"role": "user", "content": userPrompt})
    with st.chat_message("user"):
        st.markdown(userPrompt)

    api_key = get_api_key()
    if not api_key:
        st.error(
            "Set ANTHROPIC_API_KEY in Streamlit secrets or export it as an environment variable."
        )
    else:
        client = anthropic.Anthropic(api_key=api_key)
        try:
            response = client.messages.create(
                model=agent_mode,
                max_tokens=4096,
                output_config={"effort": modelOption},
                messages=st.session_state.messages,
            )
        except anthropic.APIError as exc:
            st.error(f"Anthropic API request failed: {exc}")
        else:
            response_text = "\n".join(
                block.text for block in response.content if block.type == "text"
            )
            if response_text:
                st.session_state.messages.append(
                    {"role": "assistant", "content": response_text}
                )
                with st.chat_message("assistant"):
                    st.markdown(response_text)
            else:
                st.error("Anthropic returned no text response.")
