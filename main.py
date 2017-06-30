from src import houndify
from src import client_defines
from gtts import gTTS
import RPi.GPIO as GPIO
import os
import sys
import wave
import random

voice_lang="-ven-us"
voice_speed="-s175" # default: 175
voice_type="m7"     # current: m7
voice_gap=""        # default: -g10

BUFFER_SIZE = 512

def play_random_error():
    error_reponses =    [
                            "I'm sorry. I didn't catch that.",
                            "Could you repeat that please?",
                            "You what. Mate?",
                            "I'm sorry. I didn't understand that.",
                        ]
    play_voice(random.choice(error_reponses))

class MyListener(houndify.HoundListener):
    def onPartialTranscript(self, transcript):
        print("Partial transcript: " + transcript)
    def onFinalResponse(self, response):
        print("Final response: " + str(response))
        if len(response["AllResults"]) > 0:
            spokenResponseLong = response["AllResults"][0]["WrittenResponseLong"]
            if spokenResponseLong != "Didn't get that!":
                play_voice(spokenResponseLong)
            else:
                play_random_error()
        else:
            play_random_error()
    def onError(self, err):
        print("Error: " + str(err))

def play_voice(voice_text):
    os.system("espeak "+voice_lang +"+"+voice_type+" "+voice_speed+" "+voice_gap+" \""+voice_text+"\" 2>/dev/null")
    # tts = gTTS(text=voice_text, lang='en-uk')
    # tts.save("response.mp3")
    # os.system("play response.mp3")
    # os.remove("response.mp3")


def test_voice():
    voice_text = "Hello. I am fir. Nice to meet you."
    play_voice(voice_text)
    voice_text = "The temperature is sixteen degrees celsius."
    play_voice(voice_text)
    voice_text = "I am sorry to hear that, but I am just a robot."
    play_voice(voice_text)

if __name__ == '__main__':
    print("client id: "+client_defines.CLIENT_ID+"\nclient key: "+client_defines.CLIENT_KEY)

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(18,GPIO.OUT)

    client = houndify.StreamingHoundClient(client_defines.CLIENT_ID, client_defines.CLIENT_KEY, "fir_robot")
    client.setLocation(51.654022,-0.038691)
    clientMatches = [ {
        "Expression" : '"what" . "is" . "your" . "name"',
        "Result" : { "Intent" : "NAME" },
        "SpokenResponse" : "I am fir",
        "SpokenResponseLong" : "My name is fir. Nice to meet you.",
        "WrittenResponse" : "I am fir.",
        "WrittenResponseLong" : "My name is fir. Nice to meet you."
    } ]
    client.setHoundRequestInfo('ClientMatches', clientMatches)
    client.setHoundRequestInfo('UnitPreference', 'METRIC')
    client.setHoundRequestInfo('FirstPersonSelf', 'Fir')

    client.setSampleRate(16000)
    
    i = 0
    finished = False
    GPIO.output(18,GPIO.HIGH)
    try:
        client.start(MyListener())
        print("Starting voice control")
        while not finished and i<5:
            os.system("arecord temp"+str(i)+".wav -D sysdefault:CARD=1 -r 16000 -f S16_LE -d 1")
            audio = wave.open("temp"+str(i)+".wav")
            samples = audio.readframes(BUFFER_SIZE)
            while len(samples) != 0 and not finished:
                finished = client.fill(samples)
                samples = audio.readframes(BUFFER_SIZE)
            audio.close()
            os.remove("temp"+str(i)+".wav")
            i+=1

        client.finish()
        GPIO.output(18,GPIO.LOW)
        print("Finished voice control")
    except:
        GPIO.output(18,GPIO.LOW)