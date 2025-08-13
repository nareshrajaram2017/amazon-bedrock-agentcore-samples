import os
import streamlit as st
from chat import ChatManager
import uuid
from streamlit_cognito_auth import CognitoAuthenticator
import json


import os
import sys

# Get the current file's directory and add the project root to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(project_root)

from utils import get_ssm_parameter, get_customer_support_secret

secret = get_customer_support_secret()
secret = json.loads(secret)

authenticator = CognitoAuthenticator(
    pool_id=secret['pool_id'],
    app_client_id=secret['client_id'],
    app_client_secret=secret['client_secret'],
    use_cookies=False
)

is_logged_in = authenticator.login()
if not is_logged_in:
    st.stop()


def logout():
    print("Logout in example")
    authenticator.logout()


with st.sidebar:
    st.text(f"Welcome,\n{authenticator.get_username()}")
    st.button("Logout", "logout_btn", on_click=logout)

st.title("Customer Support Agent")
st.write(st.session_state)

chat_manager = ChatManager("default")

if "session_id" not in st.session_state:
    st.session_state["session_id"] = uuid.uuidv4()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    payload=json.dumps({"prompt": prompt, "actor_id": st.session_state["auth_username"]})

    with st.chat_message("assistant"):
        accumulated_response = chat_manager.invoke_endpoint_nostreaming( agent_arn=st.session_state["agent_arn"],
            payload=payload,
            bearer_token=st.session_state["auth_access_token"],
            session_id=st.session_state["session_id"]
        )
        # accumulated_response = ""
        # for chunk in chat_manager.invoke_endpoint(
        #             agent_arn=st.session_state["agent_arn"],
        #             payload=json.dumps(
        #                 {"prompt": prompt, "actor_id": st.session_state["auth_username"]}
        #             ),
        #             bearer_token=st.session_state["auth_access_token"],
        #             session_id=st.session_state["session_id"],
        #         ):
        #     chunk = str(chunk)
        #     if chunk.strip():
        #         accumulated_response += chunk
        #         chunk_count += 1

        #         if chunk_count % 3 == 0:
        #             accumulated_response += ""


        #         time.sleep(0.02)

        # st.write(accumulated_response)

        print(f"Response: {accumulated_response}")
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": accumulated_response})

