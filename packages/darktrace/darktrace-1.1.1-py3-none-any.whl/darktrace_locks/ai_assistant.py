# darktrace_locks/ai_assistant.py
from dotenv import load_dotenv
load_dotenv()
import os
import openai
import pyttsx3
import threading
from langdetect import detect

# Load API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

engine = pyttsx3.init()
engine.setProperty("rate", 180)

# Change voice to female with Indian accent (if available)
voices = engine.getProperty("voices")
for voice in voices:
    if "female" in voice.name.lower() and "english" in voice.name.lower():
        engine.setProperty("voice", voice.id)
        break

def speak(text):
    print("🗣️ " + text)
    engine.say(text)
    engine.runAndWait()

def detect_language(text):
    try:
        return detect(text)
    except:
        return "en"

def ask_anuj(prompt, language="en"):
    try:
        print("💡 Thinking...")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can change to gpt-4 if available
            messages=[
                {"role": "system", "content": "You are Anuj, a helpful AI assistant with a Ghibli-style tone."},
                {"role": "user", "content": prompt}
            ]
        )

        reply = response.choices[0].message.content.strip()

        # Speak asynchronously
        threading.Thread(target=speak, args=(reply,), daemon=True).start()

        return reply

    except Exception as e:
        return f"⚠️ Error: {str(e)}"
