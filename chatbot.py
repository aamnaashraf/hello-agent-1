# chatbot.py
import os
import chainlit as cl
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

# Memory for chat history
chat_history = []

@cl.on_message
async def main(message: cl.Message):
    # Append user message to chat history
    chat_history.append({"role": "user", "parts": [message.content]})
    
    # Send the message to Gemini
    try:
        response = model.generate_content(chat_history)
        # Get bot_reply
        bot_reply = response.text
        # Add bot response to history
        chat_history.append({"role": "model", "parts": [bot_reply]})
        # Send response to UI
        await cl.Message(content=bot_reply).send()
    except Exception as e:
        await cl.Message(content=f"Error: {str(e)}").send()

