
import threading
import time
import sys
from .core.voice_recognizer import VoiceRecognizer
from .core.command_processor import CommandProcessor
from .core.system_controller import SystemController
from .core.text_to_speech import TextToSpeech

class Dikshant:
    def __init__(self):
        self._stop_event = threading.Event()
        self.recognizer = VoiceRecognizer()
        self.processor = CommandProcessor()
        self.controller = SystemController()
        self.tts = TextToSpeech()
        self.wake_phrase = "hey friend"
        self.sleep_phrase = "take rest"

    def start(self):
        self.tts.speak("I'm ready to help")
        try:
            self._run()
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self._stop_event.set()
        self.tts.speak("Goodbye")
        sys.exit(0)

    def _run(self):
        while not self._stop_event.is_set():
            try:
                print("\nListening...")
                text = self.recognizer.listen()
                
                if not text:
                    continue
                    
                text_lower = text.lower()
                
                if self.sleep_phrase in text_lower:
                    self.stop()
                
                elif self.wake_phrase in text_lower:
                    command = text_lower.split(self.wake_phrase, 1)[1].strip()
                    self._process_command(command)
                    
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(1)
            finally:
                time.sleep(0.1)

    def _process_command(self, command_text):
        command = self.processor.process_command(command_text)
        if command['action'] == 'unknown':
            self.tts.speak("I didn't understand that")
            return
            
        result = self.controller.execute(command)
        self.tts.speak(command.get('response', result))
