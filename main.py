from src import houndify
from src import client_defines
import os

import sys

def play_voice(voice_text):
    voice_lang="-ven-us"
    voice_speed="-s175" # default: 175
    voice_type="m7"     # current: m7
    voice_gap=""
    os.system("espeak "+voice_lang +"+"+voice_type+" "+voice_speed+" "+voice_gap+" \""+voice_text+"\" 2>/dev/null")

if __name__ == '__main__':
  print("client id: "+client_defines.CLIENT_ID+"\nclient key: "+client_defines.CLIENT_KEY)
  voice_text = "Hello. I am fir. Nice to meet you."
  play_voice(voice_text)
  voice_text = "The temperature is sixteen degrees celsius."
  play_voice(voice_text)