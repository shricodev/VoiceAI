import os
import random
import pyttsx3
import datetime
import speedtest
import webbrowser
from requests import get
from time import sleep
from sys import platform
from featuresMain import *
from decouple import config
import speech_recognition as sr

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

# *Reads the lines from listSongs.txt and return a random url of song.


def randomLines():
    lines = open('DataCenter\\listSongs.txt').read().splitlines()
    final = random.choice(lines)
    return final


if __name__ == '__main__':
    wisher()

    while True:
        try:
            outputTakeIn = takeInput()

            if 'search google' in outputTakeIn or 'search in google' in outputTakeIn:
                speak("What do you wanna search?")
                query = takeInput().lower()
                result = googleSearch(query)
                sleep(2)

            elif 'search youtube' in outputTakeIn or 'search in youtube' in outputTakeIn:
                speak("What do you wanna search?")
                query = takeInput().lower()
                result = youtubeSearch(query)
                sleep(2)

            elif outputTakeIn in exitCommands.keys():
                # query = takeInput()
                speak(exitCommands[outputTakeIn])
                exit()

            elif outputTakeIn in greet.keys():
                speak(greet[outputTakeIn])

            elif 'time' in outputTakeIn:
                speak(
                    f"The current time is: {datetime.datetime.now().strftime('%H:%M%p')}")
                sleep(2)

            elif 'set alarm' in outputTakeIn:
                speak("Give me time in TwentyFour Hour Format")
                a = alarmGet(takeInput())
                alarmRing(a)

            elif 'song' in outputTakeIn or 'music' in outputTakeIn:
                try:
                    a = randomLines()
                    webbrowser.open(a)

                except ConnectionError:
                    speak("It seems like you are not connected to the Internet.")
                    sleep(2)

            elif 'owner' in outputTakeIn or 'who is your owner' in outputTakeIn or 'who created you' in outputTakeIn:
                owner()
                sleep(2)

            elif 'change voice' in outputTakeIn or 'change your voice' in outputTakeIn:
                if 'female' in outputTakeIn:
                    engine.setProperty('voice', voices[2].id)
                else:
                    engine.setProperty('voice', voices[0].id)
                speak("Changed my voice, How do you like it?")
                sleep(2)

            elif 'shutdown' in outputTakeIn:
                if platform == 'win32':
                    speak("Shutting down the system..")
                    os.system('shutdown /p /f')
                elif platform == 'linux2' or platform == 'linux' or platform == 'darwin':
                    os.system('poweroff')

            elif 'open cmd' in outputTakeIn or 'open command prompt' in outputTakeIn:
                speak("Opening Command Prompt")
                os.system('start cmd')
                sleep(2)

            elif 'wikipedia' in outputTakeIn:
                speak("What do you wanna search?")
                query = takeInput().lower()
                result = search_on_wikipedia(query)
                speak(f'According to wikipedia, {result}')
                speak("For your convenience I am printing it on the screen.")
                print(result)
                sleep(2)

            elif 'ip' in outputTakeIn or 'ip address' in outputTakeIn:
                ip_addr = get('https://api64.ipify.org/').text
                speak(f"Your IP address is {ip_addr}")
                sleep(2)

            elif 'speedtest' in outputTakeIn or 'speed test' in outputTakeIn:
                speak("Checking the Internet speed. Wait a moment Sir!")
                try:
                    st = speedtest.Speedtest()
                    # down = st.download()
                    # uploadd = st.upload()
                    # roundedspeed = round(down)
                    # finaldown = roundedspeed / 1e+6
                    # roundedup = round(uploadd)
                    # finalup = roundedup / 1e+6
                    # speak(f"Your download speed is: {finaldown} Mbps")
                    # speak(f"Your upload speed is: {finalup} Mbps")
                    # speak("Checking the Download Speed")
                    downres = st.download()/1025/1024
                    # speak("Checking the upload speed")
                    upres = st.upload()/1024/1024
                    # speak("Testing Ping")
                    pingres = st.results.ping
                    speak(
                        f"Your Download speed is: {downres:.2f} megabitpersecond")
                    speak(
                        f"Your Upload speed is: {upres:.2f} megabitpersecond")
                    speak(f"Your Ping is: {pingres} ms")
                    sleep(2)

                except Exception as e:
                    speak(e)
                    sleep(2)

            elif 'my location' in outputTakeIn or 'location' in outputTakeIn:
                loc()

        except Exception as e:
            speak("An error Occured!")
            print(e)
            takeInput()
