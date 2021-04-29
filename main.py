import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import pyjokes
from bs4 import BeautifulSoup
import requests
from PyDictionary import PyDictionary
from googletrans import Translator, LANGUAGES
from subprocess import Popen, PIPE, STDOUT
from gtts import gTTS
import os, playsound

bubble_state = True

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
'''
for voice in voices:
  print("Voice:")
  print(" - ID: %s" % voice.id)
  print(" - Name: %s" % voice.name)
  print(" - Languages: %s" % voice.languages)
  print(" - Gender: %s" % voice.gender)
  print(" - Age: %s" % voice.age)
'''
engine.setProperty('voice', voices[1].id)

basic_greetings = ["hello", "hi", "good morning", "love you", "miss you"]
wiki_search = ["search for ", "who is ", "what is "]
basic_questions = {
    "do you love me": "yes, I do",
    "are you awake": "yes, I am",
    "are you listening": "yes, I am",
    "are you single": "sorry, I'm in relationship with wifi",
    "are you mad": "oh! i'm not",
    "do you hate me": "i love you my dear",
    "how are you": "i'm fine. thank you.",
    "i am bored": "Do you want me to tell some jokes?"
}

def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            voice = listener.listen(source, timeout=7)
            command = listener.recognize_google(voice).lower()
            print(command)
            if 'bubble' in command:
                command = command.replace("bubble", "")
            return command
    except Exception as e:
        print(e)
    return ''

def google_assistant(data):
    try:
        ga_subprocess = Popen(
            "python -m googlesamples.assistant.grpc.textinput --device-id 'helpful-scion-300015' --device-model-id 'ABCD2'",
            shell=True, stdout=PIPE, stdin=PIPE, stderr=PIPE)
        stdout_data = ga_subprocess.communicate(input=data.encode("utf-8"))[0]
        print(stdout_data)
        ga_reply = str(stdout_data).split("\\r\\n")[1].replace("<@assistant>", "")
        return bytes((ga_reply).encode("utf-8"))
    except Exception as e:
        print(e)


def run_bubble():
    global bubble_state, engine
    order = take_command()
    keyword = order.replace("translate", "")
    while keyword == "":
        talk("Go ahead!")
        keyword = take_command()
    if "translate" in order:
        talk("To which language?")
        lang = take_command()
        while lang == "":
            talk("Can you repeat that?")
            lang = take_command()
        for code, language in LANGUAGES.items():
            if language == lang:
                dest_lang = code
        keyword = order.replace("translate", "")
        translation = Translator().translate(keyword, dest=dest_lang)
        talk("Translating "+ keyword + " to " +lang)
        speak = gTTS(text=translation.text, lang=dest_lang, slow=False)
        speak.save("captured_voice.mp3")
        playsound.playsound("captured_voice.mp3")
        os.remove("captured_voice.mp3")
        print(translation.text)
    elif 'play' in order:
        song = order.replace('play', '')
        print("Playing...")
        talk("Enjoy the song! bye for now!")
        pywhatkit.playonyt(song)
        bubble_state = False
    elif ('time' in order) or ('weather') in order:
        #time = datetime.datetime.now().strftime("%H:%M")
        #time = datetime.datetime.now().strftime("%I:%M %p")
        #talk("the current time is " + time)
        talk(google_assistant(order))
    elif any(word in order for word in wiki_search ):
        for x in wiki_search:
            if x in order:
                keyword = order.replace(x, "")
        print(keyword)
        info = wikipedia.summary(keyword, 1)
        talk(info)
    elif any(word in order for word in basic_questions.keys()):
        for x in basic_questions.keys():
            if x in order:
                talk(basic_questions[x])
    elif "joke" in order:
            talk(pyjokes.get_joke())
    elif "meaning" in order:
        keyword = order.replace("meaning of", "")
        talk(PyDictionary().meaning(keyword))
    elif "ok bye" in order:
        talk("Nice talking to you!")
        bubble_state = False
    elif any(word in order for word in basic_greetings):
        talk(order + " dear")
    else:
        if order=='':
            talk("Did you say something?")
        else:
            talk("Sorry! I'm not trained to help you on that")



if __name__ == '__main__':
    talk("Hello! I'm bubble your personal assistant ")
    while bubble_state:
        run_bubble()