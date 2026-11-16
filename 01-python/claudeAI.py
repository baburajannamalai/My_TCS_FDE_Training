import html
import uuid
import os

import anthropic
import streamlit as st
from anthropic import Anthropic
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

/* Remove default borders from selectbox and chat_input inside the bar */
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
# UI: render one conversation turn
#def render_message(role: str, content: str):
 #   template = user_template if role == "user" else bot_template
    # Escape the text so model output can't break the HTML, and keep its line breaks
  #  message = html.escape(content).replace("\n", "<br>")
   # st.write(template.replace("{{MSG}}", message), unsafe_allow_html=True)

def chatInput():
    with st._bottom:
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


    ##if prompt:
       ## with st.chat_message("user"):
         ##   st.write(f"**({agent_mode},{modelOption})** {prompt}")
    return (agent_mode, modelOption, userPrompt)


#client = anthropic.Client(api_key=st.secrets[""], base_url="https://api.anthropic.com")
client = Anthropic(
    api_key=""# This is the default and can be omitted
)
st.session_state.setdefault("messages", [])
st.session_state.setdefault("thread_id", str(uuid.uuid4()))

agent_mode, modelOption, userPrompt = chatInput()
message = client.messages.create(
    model=agent_mode,
    max_tokens=4096,
    output_config={
        "effort": modelOption
    },
    messages=[
            {
            "role": "user",
                "content": userPrompt
            }
    ]
)

print(message)
if userPrompt:
 st.write(f"**({agent_mode},{modelOption})** {userPrompt}")


#st.session_state.chatHistory += f"**({agent_mode},{modelOption})** {userPrompt}\n"
#for message in st.session_state.messages:
   # render_message(message["role"], message["content"])

#info=chatInput()

#print(info[0], info[1], info[2])