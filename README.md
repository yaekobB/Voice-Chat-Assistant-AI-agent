# Voice-Chat-Assistant-AI-agent
# 🎙️ Voice Chat Assistant

A browser-based conversational voice assistant built with Python and Flask that enables natural spoken interaction using STT, LLM, and TTS components. Developed as part of my Master’s in Artificial Intelligence and Computer Science.

---

## 🚀 Features

- 🔁 Looped conversation until user stops
- 🗣️ Real-time Speech-to-Text (STT) using Whisper
- 🤖 LLM-generated replies with Groq API (LLaMA3-8B)
- 🔊 Offline Text-to-Speech (TTS) using pyttsx3
- 🌐 Clean browser interface with live interaction and audio playback
- 🔄 Reset and stop chat functionality
- 🎧 Greeting message at start

---

## 🧠 Tech Stack

| Component      | Library/Tool            |
|----------------|--------------------------|
| Backend        | Python, Flask            |
| STT            | OpenAI Whisper           |
| LLM            | Groq API (LLaMA3-8B)     |
| TTS            | pyttsx3 (offline TTS)    |
| UI             | HTML, CSS, JavaScript    |
| Audio Handling | sounddevice, scipy       |

---

## 📁 Project Structure

```
voice-chat-assistant/
│
├── app.py                 # Main Flask backend
├── templates/
│   └── index.html         # Frontend HTML interface
├── static/
│   └── audio/             # TTS-generated .wav files
├── .env                   # Environment variables (not pushed)
├── requirements.txt       # Python dependencies
└── README.md              # Project overview
```

---

## ⚙️ Setup Instructions

### 1. Clone this repo

```bash
git clone https://github.com/your-username/voice-chat-assistant.git
cd voice-chat-assistant
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add environment variables

Create a `.env` file in the root directory with:

```
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Run the application

```bash
python app.py
```

Visit [http://localhost:5000](http://localhost:5000) in your browser.

---

## 🧪 Demo Workflow

1. Press **Start Voice**.
2. Assistant greets you and starts listening.
3. Speak your query (e.g., “What’s the weather like?”).
4. Assistant replies with text and voice.
5. Loop continues until you say: _stop_, _exit_, or press **Stop Voice**.

---

## 📚 Academic Context

This assistant is part of my hands-on learning and academic exploration during my Master’s degree in Artificial Intelligence and Computer Science. It demonstrates practical integration of speech and language technologies for interactive interfaces.

---

## 🔮 Roadmap

- [ ] Real-time VAD (voice activity detection)
- [ ] Voice interrupt using Web Audio API
- [ ] Replace pyttsx3 with more natural TTS (e.g., ElevenLabs, Google, Azure)
- [ ] Live transcription and streaming using WebSocket

---

## 📄 License

This project is for academic and educational purposes. Feel free to fork and expand it with credit.

---

## 👨‍💻 Author

**Yaekob Beyene**  
_MSc Artificial Intelligence and Computer Science_  
🔗 [LinkedIn](#) &nbsp;&nbsp;&nbsp; 📧 [Email](#)

