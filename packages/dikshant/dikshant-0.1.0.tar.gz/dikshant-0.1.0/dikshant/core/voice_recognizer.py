 
import speech_recognition as sr
from typing import Optional

class VoiceRecognizer:
    def __init__(self, api_key: Optional[str] = None):
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 0.8
        self.recognizer.energy_threshold = 4000
        
    def listen(self) -> str:
        """Listen to microphone and return transcribed text"""
        with sr.Microphone() as source:
            print("Listening...")
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                text = self.recognizer.recognize_google(audio)
                print(f"Recognized: {text}")
                return text
            except sr.WaitTimeoutError:
                return ""
            except sr.UnknownValueError:
                print("Could not understand audio")
                return ""
            except sr.RequestError as e:
                print(f"API error; {e}")
                return ""