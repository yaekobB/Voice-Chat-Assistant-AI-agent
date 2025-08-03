
import os
import whisper
import sounddevice as sd
import numpy as np
import pyttsx3
from scipy.io.wavfile import write
from flask import Flask, render_template, request, jsonify
from groq import Groq
from contextlib import contextmanager
import tempfile
import logging
from dotenv import load_dotenv
import time
import uuid
import shutil
import re


logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
dotenv_path = os.path.join(os.path.dirname(__file__), ".", ".env")
load_dotenv(dotenv_path)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("Missing GROQ_API_KEY")

SAMPLE_RATE = 22050
RECORD_DURATION = 12  # seconds
WHISPER_MODEL = whisper.load_model("small")
groq_client = Groq(api_key=GROQ_API_KEY)
STOP_COMMANDS = {"stop", "exit", "quit", "byebye", "stop conversation", "end conversation"}

# Ensure the audio directory exists
os.makedirs("static/audio", exist_ok=True)


def speak_text(text, output_path):
    engine = pyttsx3.init()
    engine.setProperty("rate", 160)
    engine.setProperty("volume", 1.0)
    engine.save_to_file(text, output_path)
    engine.runAndWait()
    engine.stop()

    # 🔁 Wait up to 5 seconds for file to actually appear
    for _ in range(10):
        if os.path.exists(output_path):
            return
        time.sleep(0.5)



# Initialize conversation history with a system message
conversation_history = [
    {
        "role": "system",
        "content": (
            "You are a voice-based AI assistant. "
            "Always speak in plain, natural English. "
            "Your responses should be a summary, concise, clear, and easy to understand. "
            "Avoid complex vocabulary, jargon, or technical terms. "
            "Never use markdown, symbols like *, punctuation-based formatting, emojis, lists, or special characters like *, -, :, etc. "
            "Respond as if you're speaking clearly to a human through voice, not writing."
        )
    }
]

@contextmanager
def temp_audio_file():
    path = tempfile.mktemp(suffix=".wav")
    yield path
    try:
        os.remove(path)
    except FileNotFoundError:
        pass



def is_valid_text(text):
    words = re.findall(r'\b\w+\b', text)
    return len(words) >= 2  # Reject one-word or garbage input

def clean_for_tts(text):
    """Remove markdown symbols and formatting characters for better TTS experience."""
    return re.sub(r"[*_`~•\-–—#@^+=>✓✔️❌🔹🔸🎯🚀🤖🧠😊😂❤️🔥💡👉]", "", text).strip()


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/loop_conversation", methods=["POST"])
def loop_conversation():
    try:
        with temp_audio_file() as input_audio:
            logging.info("Recording audio")
            recording = sd.rec(int(RECORD_DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype=np.float32)
            sd.wait()
            write(input_audio, SAMPLE_RATE, recording)

            logging.info("Transcribing audio")
            result = WHISPER_MODEL.transcribe(input_audio, fp16=False, language="en")
            user_text = result["text"].strip().lower()
            logging.info(f"Transcribed text: {user_text}")

            if not user_text or not is_valid_text(user_text):
                return jsonify({
                    "reply": "I didn't hear anything clear. Please try again.",
                    "user_text": "[unrecognized input]",
                    "should_stop": False
                })

            if any(cmd in user_text for cmd in STOP_COMMANDS):
                return jsonify({"reply": "Conversation stopped.", "user_text": user_text, "should_stop": True})

            conversation_history.append({"role": "user", "content": user_text})
            response = groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=conversation_history[-6:],
                temperature=0.7,
                max_tokens=100
            )
            reply = response.choices[0].message.content.strip()
            logging.info(f"LLM reply: {reply}")
            conversation_history.append({"role": "assistant", "content": reply})
            
            # Clean * like characters of the reply for TTS
            cleaned_reply = clean_for_tts(reply)
            
            with temp_audio_file() as temp_output:
                speak_text(cleaned_reply, temp_output)
                audio_name = f"response_{uuid.uuid4().hex}.wav"
                final_path = os.path.join("static/audio", audio_name)
                shutil.copy(temp_output, final_path)

            return jsonify({
                "reply": reply,
                "user_text": user_text,
                "audio_url": f"/static/audio/{audio_name}",
                "should_stop": False
            })

    except Exception as e:
        logging.exception("Error in loop_conversation")
        return jsonify({"error": str(e), "should_stop": False}), 500

# Clean up audio directory on server start
def clear_audio_folder():
    folder = os.path.join("static", "audio")
    for filename in os.listdir(folder):
        if filename.endswith(".wav"):
            try:
                os.remove(os.path.join(folder, filename))
            except Exception as e:
                logging.warning(f"Could not delete {filename}: {e}")

clear_audio_folder()

@app.route("/reset_chat", methods=["POST"])
def reset_chat():
    global conversation_history
    conversation_history = [
        {
            "role": "system",
            "content": (
                "You are a voice-based AI assistant. "
                "Always speak in plain, natural English. "
                "Your responses should be a summary, concise, clear, and easy to understand. "
                "Avoid complex vocabulary, jargon, or technical terms. "
                "Never use markdown, symbols like *, punctuation-based formatting, emojis, lists, or special characters like *, -, :, etc. "
                "Respond as if you're speaking clearly to a human through voice, not writing."
            )
        }
    ]
    return jsonify({"status": "reset"}), 200

@app.route("/greeting", methods=["GET"])
def greeting():
    try:
        greeting_text = "Hello dear, how can I assist you?"
        cleaned_text = clean_for_tts(greeting_text)

        with temp_audio_file() as temp_output:
            speak_text(cleaned_text, temp_output)
            audio_name = f"greeting_{uuid.uuid4().hex}.wav"
            final_path = os.path.join("static/audio", audio_name)
            shutil.copy(temp_output, final_path)

        return jsonify({
            "reply": greeting_text,
            "audio_url": f"/static/audio/{audio_name}"
        })
    except Exception as e:
        logging.exception("Error generating greeting")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
