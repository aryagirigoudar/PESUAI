# from gtts import gTTS
# from playsound import playsound
# from os import remove


# tts = gTTS('hello',lang='en', tld='co.uk')

# tts.save('hello.mp3')
# playsound("./hello.mp3")
# remove("./hello.mp3")
from gtts import gTTS
from io import BytesIO
from pygame import mixer
import time

def speak(text):
    mp3_fp = BytesIO()
    tts = gTTS(text, lang='en', tld='co.uk')
    tts.write_to_fp(mp3_fp)
    return mp3_fp

mixer.init()
sound = speak("This is arya your personal health care")
sound.seek(0)
mixer.music.load(sound, "mp3")
mixer.music.play()
time.sleep(5)