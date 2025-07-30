import json
import re
import sys
from pathlib import Path
from typing import Dict, Any

try:
    from importlib.resources import files
except ImportError:
    from importlib.resources import read_text

class CommandProcessor:
    def __init__(self):
        self.commands = self._load_commands()
        
    def _load_commands(self) -> Dict[str, Any]:
        try:
            if 'files' in globals():
                data = files('dikshant.data').joinpath('commands.json')
                with data.open('r', encoding='utf-8') as f:
                    return json.load(f)
            
            if 'read_text' in globals():
                return json.loads(read_text('dikshant.data', 'commands.json'))
            
            data_path = Path(__file__).parent.parent / 'data' / 'commands.json'
            with open(data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
                
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Invalid JSON: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Failed to load commands: {str(e)}")

    def process_command(self, text: str) -> Dict[str, Any]:
        text = text.lower().strip()
        
        # Strict wake phrase enforcement
        if not text.startswith("hey friend"):
            return {'action': 'unknown'}
            
        command_text = text[10:].strip()  # Remove "hey friend"
        
        for command in self.commands['commands']:
            for pattern in command['patterns']:
                try:
                    if re.fullmatch(pattern, command_text):
                        return {
                            'action': command['action'],
                            'params': self._extract_params(pattern, command_text),
                            'response': command.get('response', '')
                        }
                except re.error:
                    continue
                
        return {'action': 'unknown'}

    def _extract_params(self, pattern: str, text: str) -> Dict[str, str]:
        match = re.search(pattern, text)
        return match.groupdict() if match else {}