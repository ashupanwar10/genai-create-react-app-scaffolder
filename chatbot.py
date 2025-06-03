import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import re
from prompt import message_prompt
from helper_func import generate_system_message, format_message
from create_react_app import create_react_app

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(page_title="React App Scaffolder",
                   page_icon=":rocket:")


# Title aligned to top-left
st.markdown("<h1>React App Scaffolder</h1>", unsafe_allow_html=True)

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

# Session state initialization
if "messages" not in st.session_state:
    st.session_state.messages = [
        format_message(generate_system_message(), "assistant")
    ]

if "model" not in st.session_state:
    st.session_state.model = "gpt-4"

if "zip_path" not in st.session_state:
    st.session_state.zip_path = None

if "zip_filename" not in st.session_state:
    st.session_state.zip_filename = None

# Function to extract JSON payload from AI response


def extract_json_payload(text):
    # Look for JSON pattern in the text
    json_pattern = r'\{[\s\S]*"project_name"[\s\S]*\}'
    match = re.search(json_pattern, text)
    if match:
        try:
            json_str = match.group(0)
            # Clean up any possible markdown formatting
            json_str = json_str.replace('```json', '').replace('```', '')
            return json_str
        except:
            return None
    return None


# Display previous messages
for message in st.session_state.messages:
    st.chat_message(message["role"]).markdown(message["content"])

# Display download button if zip is available
if st.session_state.zip_path and os.path.exists(st.session_state.zip_path):
    with open(st.session_state.zip_path, "rb") as file:
        st.download_button(
            label="Download React App",
            data=file,
            file_name=st.session_state.zip_filename,
            mime="application/zip"
        )

# User input
if user_prompt := st.chat_input("Ask me about creating a React app..."):
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        stream = client.chat.completions.create(
            model=st.session_state.model,
            messages=[{"role": "system", "content": message_prompt}] +
            [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True
        )

        for chunk in stream:
            token = chunk.choices[0].delta.content
            if token:
                full_response += token
                message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response})

        # Check if the response contains a JSON payload for creating a React app
        json_payload = extract_json_payload(full_response)
        if json_payload:
            st.info("Creating your React app... Please wait.")
            zip_path, message = create_react_app(json_payload)

            if zip_path and os.path.exists(zip_path):
                st.session_state.zip_path = zip_path
                st.session_state.zip_filename = os.path.basename(zip_path)
                st.success(message)
                st.rerun()  # Trigger rerun to show download button
            else:
                st.error(message)
