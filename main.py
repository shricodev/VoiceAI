from sys import platform
from requests import get
import os
import random
import webbrowser
import pyttsx3
import datetime
import speech_recognition as sr
from featuresMain import *
from decouple import config

# * Initializing the voice engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty("voices")

# * Sets the program voice.
engine.setProperty("voice", voices[1].id)
engine.setProperty("rate", 170)

user = config('USER')
name = config('AI')
# *  Wishes the user based on the current time


def wisher():
    hour = int(datetime.datetime.now().hour)

    if hour > 0 and hour < 12:
        speak(f"Good Morning Sir!")
    elif hour > 12 and hour < 18:
        speak("Good Afternoon Sir!")
    else:
        speak(f"Good Evening {user} Sir!")
    speak(f"I am {name}, Your personal assistant. How can I help you?")

# * Speaks the audio


def speak(text):
    print('')
    print(f"{text}")
    print('')
    engine.say(text)
    engine.runAndWait()

# * Takes the userInput from the microphone and tries to resolve using Google.


def takeInput():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 2
        audio = r.listen(source, timeout=20, phrase_time_limit=10)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query.lower()}\n")

    except Exception as e:
        print("Say that again please!")
        return ""

    try:
        with open("DataCenter\\commands.txt", "a") as f:
            f.write(
                f'[{datetime.datetime.now().strftime("%H:%M:%S%p")}] User said: {query}\n')

    except Exception:
        pass
        print(query)
    return query.lower()

# * Takes the userInput from the microphone in nepali and tries to resolve using Google.

def randomLines():
    lines = open('DataCenter\\listSongs.txt').read().splitlines()
    final =  random.choice(lines)
    return final

if __name__ == '__main__':
    wisher()

    while True:
        try:
            outputTakeIn = takeInput()

            if 'google search' in outputTakeIn:
                speak("What do you wanna search?")
                query = takeInput().lower()
                result = googleSearch(query)

            elif 'youtube search' in outputTakeIn:
                speak("What do you wanna search?")
                query = takeInput().lower()
                result = youtubeSearch(query)

            elif outputTakeIn in exitCommands.keys():
                query = takeInput()
                speak(exitCommands[query])
                exit()

            elif 'time' in outputTakeIn:
                speak(
                    f"The current time is: {datetime.datetime.now().strftime('%H:%M%p')}")

            elif 'set alarm' in outputTakeIn:
                speak("Give me time in TwentyFour Hour Format")
                a = alarmGet(takeInput())
                alarmRing(a)

            elif 'song' in outputTakeIn:
                try:
                    a = randomLines()
                    webbrowser.open(a)

                except ConnectionError:
                    speak("It seems like you are not connected to the Internet.")

            elif 'owner'  in outputTakeIn or 'who is your owner' in outputTakeIn or 'who created you' in outputTakeIn:
                owner()

            elif 'change voice' in outputTakeIn:
                if 'female' in outputTakeIn:
                    engine.setProperty('voice', voices[1].id)
                else:
                    engine.setProperty('voice', voices[0].id)
                speak("Changed my voice, How do you like it?")

            elif 'shutdown' in outputTakeIn:
                if platform == 'win32':
                    speak("Shutting down the system..")
                    os.system('shutdown /p /f')
                elif platform == 'linux2' or platform == 'linux' or platform == 'darwin':
                    os.system('poweroff')

            elif 'open cmd' in outputTakeIn or 'open command prompt' in outputTakeIn:
                os.system('start cmd')

            elif 'wikipedia' in outputTakeIn:
                speak("What do you wanna search?")
                query = takeInput().lower()
                result = search_on_wikipedia(query)
                speak(f'According to wikipedia, {result}')
                speak("For your convenience I am printing it on the screen.")
                print(result)

            elif 'ip' in outputTakeIn  or 'ip address' in outputTakeIn:
                ip_addr = get('https://api64.ipify.org/')
                speak(f"Your IP address is" + {ip_addr}.text)

        except Exception as e:
            speak("An error Occured!")
            print(e)
            takeInput()
