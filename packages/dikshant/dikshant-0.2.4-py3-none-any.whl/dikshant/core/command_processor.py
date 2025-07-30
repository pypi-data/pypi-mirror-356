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
        command_text = text.strip()

        for command in self.commands['commands']:
            for pattern in command['patterns']:
                try:
                    match = re.fullmatch(pattern, command_text, flags=re.IGNORECASE)
                    if match:
                        params = {k: v.strip() for k, v in match.groupdict().items()} if match else {}

                        return {
                            'action': command['action'],
                            'params': params,
                            'response': command.get('response', '').format(**params) if params else command.get('response', '')
                        }
                except re.error:
                    continue

        return {'action': 'unknown'}
