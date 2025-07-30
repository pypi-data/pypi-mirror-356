import os
import subprocess
import webbrowser
from typing import Dict, Any

class SystemController:
    # App mapping dictionary
    APP_MAP = {
        'notepad': 'notepad.exe',
        'calculator': 'calc.exe',
        'chrome': 'chrome.exe',
        'word': 'winword.exe',
        'excel': 'excel.exe'
    }
    
    # Website mapping dictionary
    SITE_MAP = {
        'google': 'https://google.com',
        'youtube': 'https://youtube.com',
        'github': 'https://github.com'
    }

    def execute(self, command: Dict[str, Any]) -> str:
        action = command['action']
        params = command['params']
        
        try:
            if action == 'open_app':
                return self._open_app(params.get('app'))
            elif action == 'open_website':
                return self._open_website(params.get('site'))
            elif action == 'sleep':
                return "Goodbye"
            else:
                return "Command not implemented"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _open_app(self, app_name: str) -> str:
        """Open application with proper mapping"""
        if not app_name:
            return "No application specified"
            
        app_key = app_name.lower()
        executable = self.APP_MAP.get(app_key, app_name)
        
        try:
            subprocess.Popen(executable, shell=True)
            return f"Opening {app_name}"
        except Exception as e:
            return f"Failed to open {app_name}: {str(e)}"
    
    def _open_website(self, site_name: str) -> str:
        """Open website with proper mapping"""
        if not site_name:
            return "No website specified"
            
        site_key = site_name.lower()
        url = self.SITE_MAP.get(site_key, f'https://{site_name}')
        
        try:
            webbrowser.open(url)
            return f"Opening {site_name}"
        except Exception as e:
            return f"Failed to open {site_name}: {str(e)}"