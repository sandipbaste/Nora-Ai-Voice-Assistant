import threading
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import uuid
import requests
import webbrowser
import speech_recognition as sr
import pygame
import google.generativeai as genai
from gtts import gTTS
from dotenv import load_dotenv

# Local modules
import musicLibrary  # create musicLibrary.py with a dict of songs

# === SETUP ===
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
newsapi = os.getenv("NEWS_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

recognizer = sr.Recognizer()

# Create audio folder if not exists
AUDIO_DIR = "audio_files"
os.makedirs(AUDIO_DIR, exist_ok=True)

# === SPEAK FUNCTION ===
def speak(text, save_file=False):
    """Convert text to speech. If save_file=True, return filename in audio_files/"""
    tts = gTTS(text)
    if save_file:
        filename = f"audio_{uuid.uuid4().hex}.mp3"
        file_path = os.path.join(AUDIO_DIR, filename)
        tts.save(file_path)
        return filename
    else:
        temp_path = os.path.join(AUDIO_DIR, "temp.mp3")
        tts.save(temp_path)
        pygame.mixer.init()
        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.music.unload()
        os.remove(temp_path)
        return None

# === AI PROCESS ===
def aiProcess(command: str):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([
        {"role": "user", "parts": ["You are a virtual assistant named Nora skilled in general tasks like Alexa and Google Cloud."]},
        {"role": "user", "parts": [command]}
    ])
    return response.text

# === TIMER FUNCTION ===
def start_timer(minutes: int, reminder: str = "Time’s up! Take a break."):
    def timer_thread():
        time.sleep(minutes * 60)
        speak(reminder)
    threading.Thread(target=timer_thread, daemon=True).start()
    return f"Timer set for {minutes} minutes."

# === PROCESS COMMANDS ===
def processCommand(c: str):
    c = c.lower()

    if "open google" in c:
        speak("Opening Google")
        webbrowser.open("https://google.com")
        return "Opened Google"

    elif "open facebook" in c:
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")
        return "Opened Facebook"

    elif "open youtube" in c:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
        return "Opened YouTube"

    elif "open linkedin" in c:
        speak("Opening LinkedIn")
        webbrowser.open("https://linkedin.com")
        return "Opened LinkedIn"

    elif c.startswith("play"):
        song = c.split(" ")[1]
        link = musicLibrary.music.get(song, None)
        if link:
            speak(f"Playing {song}")
            webbrowser.open(link)
            return f"Playing {song}"
        else:
            speak("Song not found.")
            return "Song not found."

    elif "news" in c:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code == 200:
            articles = r.json().get("articles", [])
            headlines = [article["title"] for article in articles[:5]]
            for title in headlines:
                speak(title)
            return " | ".join(headlines)
        else:
            speak("Sorry, couldn't fetch news right now.")
            return "News fetch failed."

    elif "timer" in c or "remind me" in c:
        import re
        match = re.search(r"(\d+)\s*minute", c)
        if match:
            minutes = int(match.group(1))
            reminder = "Time’s up! Take a short break." if "break" in c else "Time’s up!"
            speak(start_timer(minutes, reminder))
            return f"Timer started for {minutes} minutes."
        else:
            speak("Please specify the timer duration in minutes.")
            return "No duration found."

    else:
        output = aiProcess(c)
        speak(output)
        return output

# === FASTAPI ENDPOINT (Frontend) ===
@app.post("/ask/")
async def ask_question(data: dict):
    question = data.get("question", "")
    if not question:
        return {"error": "No question provided"}

    answer = processCommand(question)
    filename = speak(answer, save_file=True)

    return {
        "answer": answer,
        "audio_url": f"/audio/{filename}" if filename else None
    }

@app.get("/audio/{filename}")
async def get_audio(filename: str):
    file_path = os.path.join(AUDIO_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/mpeg")
    return {"error": "File not found"}


# === LOCAL MODE ===
if __name__ == "__main__":
    speak("Initializing Nora....")
    activated = False

    try:
        while True:
            if not activated:
                print("Listening for wake word...")
                with sr.Microphone() as source:
                    audio = recognizer.listen(source, timeout=4, phrase_time_limit=2)
                try:
                    word = recognizer.recognize_google(audio)
                    if word.lower() in ["nora", "hello nora", "noraa"]:
                        activated = True
                        speak("Yes, how can I help you?")
                except Exception:
                    pass
            else:
                print("Nora Active...")
                with sr.Microphone() as source:
                    audio = recognizer.listen(source)
                try:
                    command = recognizer.recognize_google(audio)
                    if "stop nora" in command.lower():
                        speak("Goodbye, shutting down.")
                        break
                    processCommand(command)
                except Exception:
                    pass
    except KeyboardInterrupt:
        print("\nNora stopped by user.")
        speak("Goodbye, shutting down.")
