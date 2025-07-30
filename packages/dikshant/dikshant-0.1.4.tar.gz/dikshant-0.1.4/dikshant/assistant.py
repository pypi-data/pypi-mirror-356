import threading
from .core.voice_recognizer import VoiceRecognizer
from .core.command_processor import CommandProcessor
from .core.system_controller import SystemController
from .core.text_to_speech import TextToSpeech

class Dikshant:
    def __init__(self):
        self.is_active = False
        self.recognizer = VoiceRecognizer()
        self.processor = CommandProcessor()
        self.controller = SystemController()
        self.tts = TextToSpeech()
        self.wake_phrase = "hey friend"
        self.sleep_phrase = "take rest"
        
    def start(self):
        """Start the assistant in background"""
        self.is_active = True
        self.tts.speak("I'm ready to help")
        thread = threading.Thread(target=self._run, daemon=True)
        thread.start()
        
    def _run(self):
        """Main listening loop"""
        while self.is_active:
            text = self.recognizer.listen()
            if not text:
                continue
                
            if self.wake_phrase in text.lower():
                command = text.lower().split(self.wake_phrase)[1].strip()
                self._process_command(command)
            elif self.sleep_phrase in text.lower():
                self.is_active = False
                self.tts.speak("Going to rest now")
                
    def _process_command(self, command_text):
        """Process and execute commands"""
        command = self.processor.process_command(command_text)
        if command['action'] == 'unknown':
            self.tts.speak("I didn't understand that")
            return
            
        result = self.controller.execute(command)
        self.tts.speak(command.get('response', result)) 
