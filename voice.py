import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import requests
import wolframalpha
import os
import subprocess

# Initialize the speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# WolframAlpha client
client = wolframalpha.Client('Here, Enter your id ')

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query

def greet_user():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your assistant. How can I help you today?")

def search_wikipedia(query):
    speak('Searching Wikipedia...')
    query = query.replace("wikipedia", "")
    results = wikipedia.summary(query, sentences=2)
    speak("According to Wikipedia")
    print(results)
    speak(results)
    return results

def open_website(query):
    speak("Opening website")
    webbrowser.open(query)
    return "Opening website: " + query

def get_weather(city):
    api_key = "Here, Enter your API Key"
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(base_url)
    data = response.json()
    if data["cod"] != "404":
        main = data["main"]
        weather = data["weather"][0]["description"]
        temp = main["temp"] - 273.15 
        response_text = f"The temperature in {city} is {temp:.2f} degrees Celsius with {weather}."
        speak(response_text)
        return response_text
    else:
        speak("City not found")
        return "City not found"

def answer_query(query):
    res = client.query(query)
    try:
        answer = next(res.results).text
        speak(answer)
        return answer
    except StopIteration:
        speak("I don't know the answer to that question.")
        return "I don't know the answer to that question."

# OS Functions
def execute_command(command):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        speak("Command executed successfully.")
        return output
    except subprocess.CalledProcessError as e:
        speak("Sorry, there was an error executing the command.")
        return str(e.output)

# GUI Functions
def on_start_clicked():
    greet_user()
    start_button.config(state=tk.DISABLED)
    entry.config(state=tk.NORMAL)
    mic_button.config(state=tk.NORMAL)

def on_enter_pressed(event=None):
    user_input = entry.get()
    chat_window.insert(tk.END, "You: " + user_input + "\n", "user")
    entry.delete(0, tk.END)
    process_query(user_input)

def on_mic_clicked():
    user_input = take_command()
    if user_input != "None":
        chat_window.insert(tk.END, "You: " + user_input + "\n", "user")
        process_query(user_input)

def process_query(query):
    if 'wikipedia' in query:
        response = search_wikipedia(query)
    elif 'whatsapp' in query:
        response = open_website("https://web.whatsapp.com/")
    elif 'open' in query:
        response = open_website(query.replace("open ", ""))
    elif 'weather' in query:
        city = query.split("in")[-1].strip()
        response = get_weather(city)
    elif 'exit' in query or 'quit' in query:
        speak("Goodbye!")
        window.quit()
    elif 'execute' in query:
        command = query.replace("execute ", "")
        response = execute_command(command)
    else:
        response = answer_query(query)
    
    chat_window.insert(tk.END, "Assistant: " + response + "\n", "assistant")

# Create the main window
window = tk.Tk()
window.title("AI Command Interface")
window.geometry("600x600")
window.resizable(False, False)
window.configure(bg="#2C3E50")

# Create the chat window
chat_window = scrolledtext.ScrolledText(window, wrap=tk.WORD, bg="#ECF0F1", fg="#2C3E50", font=("Arial", 12))
chat_window.tag_configure("user", foreground="#2980B9", font=("Arial", 12, "bold"))
chat_window.tag_configure("assistant", foreground="#E74C3C", font=("Arial", 12, "italic"))
chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Create the entry box for user input
entry = tk.Entry(window, width=80, state=tk.DISABLED, font=("Arial", 14))
entry.pack(padx=10, pady=10, fill=tk.X)
entry.bind("<Return>", on_enter_pressed)

# Create a frame for the buttons
button_frame = tk.Frame(window, bg="#2C3E50")
button_frame.pack(pady=10)

# Create the start button
start_button = tk.Button(button_frame, text="Start Assistant", command=on_start_clicked, bg="#27AE60", fg="white", font=("Arial", 12, "bold"))
start_button.pack(side=tk.LEFT, padx=5)

# Create the microphone button
mic_button = tk.Button(button_frame, text="🎤 Speak", command=on_mic_clicked, state=tk.DISABLED, bg="#2980B9", fg="white", font=("Arial", 12, "bold"))
mic_button.pack(side=tk.RIGHT, padx=5)

# Run the main event loop
window.mainloop()
