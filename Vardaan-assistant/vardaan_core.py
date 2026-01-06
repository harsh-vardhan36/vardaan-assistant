import requests
import time
import re
import random
from datetime import datetime
import os
from dotenv import load_dotenv

# ================= ENV =================
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ================= CASUAL CHAT =================
chat_responses = {
    "how are you": [
        "I'm great, thanks for asking!",
        "All systems running perfectly 🚀",
        "Doing awesome 😄"
    ],
    "hello": [
        "Hello! How can I help you today?",
        "Hi there! 👋"
    ],
    "thank you": [
        "You're welcome 😊",
        "Happy to help!"
    ],
    "who created you": [
        "I was created by team Dragon."
    ]
}

def casual_chat(command: str):
    for key in chat_responses:
        if key in command:
            return random.choice(chat_responses[key])
    return None

# ================= WEATHER =================
def get_weather(city: str) -> str:
    api_key = "234613d877a4fcb4069bcea137035bc4"  # your OpenWeather key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        res = requests.get(url, timeout=10)
        data = res.json()

        if data.get("cod") != 200:
            return "City not found."

        return (
            f"🌤 Weather in {city.title()}:\n"
            f"Temperature: {data['main']['temp']}°C\n"
            f"Humidity: {data['main']['humidity']}%\n"
            f"Condition: {data['weather'][0]['description'].title()}"
        )
    except Exception as e:
        return f"Weather error: {e}"

# ================= JOKE =================
def tell_joke():
    try:
        res = requests.get("https://v2.jokeapi.dev/joke/Any?type=single", timeout=10)
        return res.json().get("joke", "Couldn't fetch a joke.")
    except:
        return "Couldn't fetch a joke."

# ================= YOUTUBE =================
def search_youtube(query: str):
    return f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"

# ================= CURRENCY =================
def parse_conversion_request(command: str):
    match = re.search(r"convert (\d+(\.\d+)?) (\w+) to (\w+)", command)
    if match:
        return float(match.group(1)), match.group(3).upper(), match.group(4).upper()
    return None, None, None

def convert_currency(amount, base, target):
    api_key = "fca_live_AmcdFYuscbhyAhRLaRTx48dZ1kSvCSuyRd57ekU1"
    url = f"https://api.freecurrencyapi.com/v1/latest?apikey={api_key}&base_currency={base}"
    try:
        res = requests.get(url, timeout=10).json()
        rate = res["data"][target]
        return f"{amount} {base} = {amount * rate:.2f} {target}"
    except:
        return "Currency conversion failed."

# ================= LLAMA (GROQ) =================
def llama_answer(question: str) -> str:
    if not GROQ_API_KEY:
        return " API key missing. Please add GROQ_API_KEY in .env"

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "You are Vardaan, a helpful AI assistant."},
            {"role": "user", "content": question}
        ],
        "temperature": 0.7,
        "max_tokens": 400
    }

    try:
        res = requests.post(url, headers=headers, json=payload, timeout=20)
        res.raise_for_status()
        return "" + res.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"error: {e}"

# ================= MAIN BRAIN =================
def process_command(command: str) -> str:
    original = command
    command = command.lower().strip()

    # Casual chat
    chat = casual_chat(command)
    if chat:
        return chat

    # Time / Date
    if "time" in command:
        return time.ctime()
    if "date" in command:
        return datetime.now().strftime("%Y-%m-%d")

    # Weather
    if "weather in" in command:
        city = command.replace("weather in", "").strip()
        return get_weather(city)

    # Joke
    if "joke" in command:
        return tell_joke()

    # YouTube
    if "youtube" in command:
        q = original.replace("youtube", "").strip()
        return search_youtube(q)

    # Currency
    if "convert" in command:
        amount, base, target = parse_conversion_request(command)
        if amount:
            return convert_currency(amount, base, target)
        return "Try: convert 100 usd to inr"

    # Exit
    if "exit" in command or "quit" in command:
        return "Goodbye! 👋"

    # 👉 FALLBACK: LLaMA for general questions
    return llama_answer(original)
