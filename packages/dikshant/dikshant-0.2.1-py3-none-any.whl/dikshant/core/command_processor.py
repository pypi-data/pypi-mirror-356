import json
import re
from pathlib import Path
from typing import Dict, Any

class CommandProcessor:
    def __init__(self):
        self.commands = self._load_commands()
        
    def _load_commands(self) -> Dict[str, Any]:
        commands_path = Path(__file__).parent.parent / 'data' / 'commands.json'
        with open(commands_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def process_command(self, text: str) -> Dict[str, Any]:
        # Convert entire input to lowercase immediately
        text = text.lower().strip()
        
        # Strict wake phrase check (also lowercase)
        if not text.startswith("hey friend"):
            return {'action': 'unknown'}
            
        # Extract and clean command
        command_text = text[10:].strip()
        
        for command in self.commands['commands']:
            for pattern in command['patterns']:
                try:
                    # Force lowercase matching
                    if re.fullmatch(pattern.lower(), command_text.lower()):
                        # Extract params (all lowercase)
                        match = re.search(pattern.lower(), command_text.lower())
                        params = {k:v.lower() for k,v in match.groupdict().items()} if match else {}
                        
                        return {
                            'action': command['action'],
                            'params': params,
                            'response': command.get('response', '').lower()
                        }
                except re.error:
                    continue
                
        return {'action': 'unknown'}