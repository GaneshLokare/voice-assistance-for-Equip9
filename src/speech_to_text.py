import speech_recognition as sr
import pyttsx3
from gtts import gTTS
import pyaudio
import sys
from src.exception import equip9_Exception

class SpeechRecognition:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def recognize_speech(self, duration=0.2):
        try:
            # Initialize the engine
            engine = pyttsx3.init()

            # Convert text to speech
            text = "Welcome to Equip 9, please tell us your requirement"
            engine.say(text)

            # Speak the text
            engine.runAndWait()
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=duration)

                audio = self.recognizer.listen(source)

                # convert spoken sentence into text
                text = self.recognizer.recognize_google(audio)
                text = text.lower()

            return text
        
        except  Exception as e:
                raise  equip9_Exception(e,sys)

