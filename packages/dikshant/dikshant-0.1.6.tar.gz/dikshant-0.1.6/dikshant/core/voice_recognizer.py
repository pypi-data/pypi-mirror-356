import speech_recognition as sr
from typing import Optional

class VoiceRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 0.8  # Faster response
        self.recognizer.energy_threshold = 3000  # Better for quick speech
        self.recognizer.dynamic_energy_threshold = True
        
    def listen(self, timeout: int = 5) -> str:
        """Listen with timeout and quick response"""
        with sr.Microphone() as source:
            print("\nListening...")
            try:
                # Adjust for ambient noise quickly
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=5)
                text = self.recognizer.recognize_google(audio)
                print(f"Recognized: {text}")
                return text
            except sr.WaitTimeoutError:
                return ""
            except sr.UnknownValueError:
                print("Could not understand audio")
                return ""
            except sr.RequestError as e:
                print(f"API error: {e}")
                return ""