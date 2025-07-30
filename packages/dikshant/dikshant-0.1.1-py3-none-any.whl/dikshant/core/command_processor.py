 
import json
import re
from pathlib import Path

class CommandProcessor:
    def __init__(self):
        self.commands = self._load_commands()
        
    def _load_commands(self):
        # Modern Python package-relative path handling
        data = files('dikshant').joinpath('data/commands.json')
        with data.open('r', encoding='utf-8') as f:
            return json.load(f)
    
    def process_command(self, text: str):
        text = text.lower().strip()
        
        for command in self.commands['commands']:
            for pattern in command['patterns']:
                if re.fullmatch(pattern, text):
                    return {
                        'action': command['action'],
                        'params': self._extract_params(pattern, text),
                        'response': command.get('response', '')
                    }
        
        return {'action': 'unknown'}