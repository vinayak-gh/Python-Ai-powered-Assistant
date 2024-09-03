import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
from openai import OpenAI

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "d0e1b7f644ac4c0c92fe3fcf38ff4944"

def aiProcess(command):
    client = OpenAI(api_key="sk-6TdAl1Tdj4ctlzsbKT_pNLK3glL-TMs1n7bmn6YlFVT3BlbkFJcm_2i6gCb9AfhcWgM53K6s5puppyax9Qu5EolyLOMA")

    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are a virtual assistant named Jarvis, skilled in general tasks like Alexa and Google Assistant."},
        {"role": "user", "content": command}
     ]
    )

    return completion.choices[0].message['content']

def speak(text):
    engine.say(text)
    engine.runAndWait()

def processCommand(command):
    command = command.lower()
    if "open google" in command:
        webbrowser.open("http://google.com")
    elif "open facebook" in command:
        webbrowser.open("http://facebook.com")
    elif "open youtube" in command:
        webbrowser.open("http://youtube.com")
    elif "open linkedin" in command:
        webbrowser.open("http://linkedin.com")
    elif "news" in command.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            # parse the JSON response
            data = r.json()

            # extract the articles
            articles = data.get('articles', [])

            # speak the headlines
            for article in articles:
                speak(article['title'])
    else:
        response = aiProcess(command)
        speak(response)

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)

            try:
                word = recognizer.recognize_google(audio)
                if word.lower() == "jarvis":
                    speak("Ya")

                    # Listen for the command after the keyword "Jarvis"
                    with sr.Microphone() as source:
                        print("Jarvis is active...")
                        audio = recognizer.listen(source)
                        command = recognizer.recognize_google(audio)

                        processCommand(command)
            except Exception as e:
                print(f"Error: {e}")
