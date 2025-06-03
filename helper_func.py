"""
Helper functions for the Streamlit chatbot app.
This module contains utility functions to enhance the chatbot's functionality,
such as generating a system message, formatting messages, and managing session state.
"""


def generate_system_message(message_prompt=None):
    """
    Generates a system message for the chatbot.
    This message provides context and instructions for the chatbot's behavior.
    Args:

        message_prompt (str): A custom message prompt to guide the chatbot's responses.
    Returns:
        str: The generated system message.
    """
    if not message_prompt:
        # Default message prompt if none is provided
        message_prompt = (
            "Hello! I'm your AI assistant, here to help you scaffold a new React application. "
            "Before we begin, please ensure that Node.js is installed on your system. "
            "Let me know the features or requirements you'd like in your app, "
            "and I'll guide you through the setup process.\n\n"
            "For example, you can say:\n"
            "- I want to create a new React app.\n"
            "- Can you help me set up a React project with TypeScript?\n"
        )

    return message_prompt


def format_message(content, role="assistant"):
    """
    Formats a message for the chatbot.

    Args:
        role (str): The role of the message sender (e.g., 'user', 'assistant'), defaulting to 'assistant'.
        content (str): The content of the message.

    Returns:
        dict: A dictionary representing the formatted message.
    """
    return {
        "role": role,
        "content": content
    }
