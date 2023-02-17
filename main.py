
#pip install speechrecognition/openai/pyttsx3/pipwin/pyaudio
#video tutorial followed: https://www.youtube.com/watch?v=cRSLxePDmbA
#Importing 
import speech_recognition as sr
import pyttsx3
import openai


#openai key - Generate and use your own

openai.api_key = "YOUR API KEY HERE FOUND AT OPENAI"

#speech to text engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
#voice id
engine.setProperty('voices',voices[1].id)

#mic as input source
r = sr.Recognizer()
mic = sr.Microphone(device_index = 1)

#variables
conversation = ""
user_name = "Human"
bot_name = "AI"

#mic activation
while True:
    with mic as source:
        print("\n Listening...")
        r.adjust_for_ambient_noise(source,duration = 0.2)
        audio = r.listen(source)
    print("Thinking...")

    try: 
        user_input = r.recognize_google(audio)
    except:
        continue
    #formatting
    prompt = user_name + ":" + user_input + "\n" + bot_name + ":"
    conversation += prompt

    #openai playground code
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=conversation,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )

    #response
    response_str = response["choices"][0]["text"].replace("\n", "")
    response_str = response_str.split(
        user_name + ":",1)[0].split(bot_name + ":",1)[0]
    conversation += response_str + "\n"
    print(response_str)

    engine.say(response_str)
    engine.runAndWait()
