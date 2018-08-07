A conversational AI bot written in Python, running on a Raspberry Pi.

Dependencies:
* snowboy
* houndify
* espeak
* gTTs

A video of the bot can be found here:
https://www.youtube.com/watch?v=BxX-n9olvWw&feature=youtu.be

To run this bot on your own Raspberry Pi, perform the following:

Connect a speaker and microphone to the Raspberry Pi system and clone the respository.

This bot requires a snowboy wake-word model to initiate a voice request (similar to "Hi Siri" or "Ok, Google", etc.). A wake-word model has already been created for the name, "FIR", and is used by default. You can create your own wake-word at https://snowboy.kitt.ai. Once you have created a UMDL file, change line 144 of `main.py` to use your model (you can have several), as below:

```python
models = ["my_wake_word.umdl"]
```

You will need to create an account on Houndify (the free version should be fine) and enable the Client Matches domain. Feel
free to enable other domains such as weather, sports, etc. Once you have an account, create `src/client_defines.py` containing your client key and client ID from Houndify surrounded by quotation marks, as below:

```python
CLIENT_ID = "YOUR CLIENT ID FROM HOUNDIFY"
CLIENT_KEY = "YOUR CLIENT KEY FROM HOUNDIFY"
```

After creating this file, just run `python3 main.py`, and say "FIR" or whatever wake-word phrase you have used. You will hear a ding sound indicating the start of the voice request. You can then give commands such as, "how are you" or "i don't like you", and the bot should respond.

Note that this was originally a prototype for a future voice-controlled room-automation project, _Pascal_.
