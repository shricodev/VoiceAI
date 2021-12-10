import sys
import random
import webbrowser
import pyttsx3
import datetime
import speech_recognition as sr
from featuresMain import owner, googleSearch, youtubeSearch, exitCommands, alarmRing, alarmGet

# * Initializing the voice engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty("voices")

# * Sets the program voice.
engine.setProperty("voice", voices[1].id)
engine.setProperty("rate", 170)

# *  Wishes the user based on the current time


def wisher():
    hour = int(datetime.datetime.now().hour)

    if hour > 0 and hour < 12:
        speak(f"Good Morning Sir!")
    elif hour > 12 and hour < 18:
        speak("Good Afternoon Sir!")
    else:
        speak("Good Evening Piyush Sir!")
    speak("I am JARVIS, Your personal assistant. How can I help you?")

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


# def takeInputNep():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening...")
#         r.pause_threshold = 2
#         audio = r.listen(source, timeout=20, phrase_time_limit=10)

#     try:
#         print("Recognizing...")
#         query = r.recognize_google(audio, language="hi")
#         print(f"User said: {query}\n")

#     except Exception as e:
#         speak("Say that again please!")
#         return ""
#     try:
#         with open("DataCenter\\command_Nep.txt", "a") as f:
#             a = f'[{datetime.datetime.now().strftime("%H:%M:%S%p")}] User said: {query}\n'
#             f.write(a)
#     except Exception:
#         pass
#     return query.lower()


def randomLines():
    lines = open('DataCenter\\listSongs.txt').read().splitlines()
    return random.choice(lines)

if __name__ == '__main__':
    wisher()

    while True:
        try:
            outputTakeIn = takeInput()

            if 'google search' in outputTakeIn:
                speak("What do you wanna search?")
                googleSearch(takeInput())

            elif 'youtube search' in outputTakeIn:
                speak("What do you wanna search?")
                youtubeSearch(takeInput())

            elif outputTakeIn in exitCommands.keys():
                speak(exitCommands[takeInput()])
                sys.exit()

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

            elif ('owner' or 'who created you' or 'who is your owner') in outputTakeIn:
                owner()

            
        except Exception as e:
            speak("An error Occured!")
            print(e)
            takeInput()
