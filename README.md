A conversational AI bot written in Python, running on a Raspberry Pi.

Dependencies:
* snowboy
* houndify
* espeak
* gTTs

A video of the bot can be found here:
https://www.youtube.com/watch?v=BxX-n9olvWw&feature=youtu.be

To run FIR on your own Raspberry Pi, connect a speaker and microphone to the system and clone the respository.
Create src/client_defines.py containing your client key and client ID from Houndify to perform the voice request (you
will first have to create an account first) surrounded by quotation marks:

```python
CLIENT_ID = "YOUR CLIENT ID FROM HOUNDIFY"
CLIENT_KEY = "YOUR CLIENT KEY FROM HOUNDIFY"
```

After creating this file, just run python3 main.py, and say FIR's name. You will hear a ding sound indicating the start
of the voice request.

Note that this is just a prototype for a future voice-controlled room-automation project, _Pascal_.
