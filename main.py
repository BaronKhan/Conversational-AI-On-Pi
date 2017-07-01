from src import houndify
from src import client_defines
from gtts import gTTS
import RPi.GPIO as GPIO
import os
import sys
import wave
import random
import signal
import snowboydecoder

voice_lang="-ven-us"
voice_speed="-s175" # default: 175
voice_type="m7"     # current: m7
voice_gap=""        # default: -g10

BUFFER_SIZE = 512

interrupted = False

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
        play_voice("I'm very sorry, but I've had enough for today. Goodbye.")

def play_voice(voice_text):
    # espeak
    os.system("espeak "+voice_lang +"+"+voice_type+" "+voice_speed+" "+voice_gap+" \""+voice_text+"\" 2>/dev/null")
    
    # gTTS
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

def run_voice_request(client):
    snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING)
    i = 0
    finished = False
    GPIO.output(18,GPIO.HIGH)
    os.system("amixer sset PCM mute")
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
        os.system("amixer sset PCM unmute")
        client.finish()
        GPIO.output(18,GPIO.LOW)
        print("Finished voice control")
    except:
        GPIO.output(18,GPIO.LOW)
        os.system("amixer sset PCM unmute")

def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

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

    signal.signal(signal.SIGINT, signal_handler)

    models = ["fir_model.umdl", "hello_model.umdl", "hi_model.umdl", "hey_fir_model.umdl"]
    sensitivity = [0.5, 0.2, 0.2, 0.5]

    if not len(models) == len(sensitivity):
        raise AssertionError()

    detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)
    callbacks = [lambda: snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING),
                 lambda: snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING),
                 lambda: snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING),
                 lambda: snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING)]
    print('Listening... Press Ctrl+C to exit')

    detector.start(detected_callback=callbacks,
                   interrupt_check=interrupt_callback,
                   sleep_time=0.03)

    detector.terminate()