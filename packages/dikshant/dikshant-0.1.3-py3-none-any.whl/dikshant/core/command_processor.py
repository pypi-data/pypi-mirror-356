import json
import sys
from pathlib import Path
from typing import Dict, Any

try:
    # Modern Python (3.9+) resource API
    from importlib.resources import files
except ImportError:
    # Fallback for older Python versions
    from importlib.resources import read_text

class CommandProcessor:
    def __init__(self):
        """
        Initialize command processor and load command definitions.
        Raises RuntimeError if commands cannot be loaded.
        """
        self.commands = self._load_commands()
        
    def _load_commands(self) -> Dict[str, Any]:
        """Load commands from package data with fallback mechanisms."""
        try:
            # Attempt modern resource API first
            if 'files' in globals():
                data = files('dikshant.data').joinpath('commands.json')
                with data.open('r', encoding='utf-8') as f:
                    return json.load(f)
            
            # Fallback for Python 3.7-3.8
            if 'read_text' in globals():
                return json.loads(read_text('dikshant.data', 'commands.json'))
            
            # Final fallback to direct file access
            data_path = Path(__file__).parent.parent / 'data' / 'commands.json'
            with open(data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
                
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Invalid JSON in commands file: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Failed to load commands: {str(e)}")

    def process_command(self, text: str) -> Dict[str, Any]:
        """
        Process voice input text and return command dictionary.
        
        Args:
            text: Input voice command text
            
        Returns:
            Dictionary with:
            - 'action': Command to execute
            - 'params': Extracted parameters
            - 'response': Optional response template
        """
        text = text.lower().strip()
        
        for command in self.commands.get('commands', []):
            for pattern in command.get('patterns', []):
                try:
                    if re.fullmatch(pattern, text):
                        return {
                            'action': command['action'],
                            'params': self._extract_params(pattern, text),
                            'response': command.get('response', '')
                        }
                except re.error:
                    continue
                
        return {'action': 'unknown'}

    def _extract_params(self, pattern: str, text: str) -> Dict[str, str]:
        """
        Extract named parameters from command using regex groups.
        
        Args:
            pattern: Regex pattern with named groups
            text: Input text to match
            
        Returns:
            Dictionary of parameter names to values
        """
        match = re.search(pattern, text)
        return match.groupdict() if match else {}