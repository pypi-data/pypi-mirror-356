import subprocess
import webbrowser
from typing import Dict, Any

class SystemController:
    def execute(self, command: Dict[str, Any]) -> str:
        action = command['action']
        params = command.get('params', {})
        
        try:
            if action == 'open_app':
                return self._open_any_app(params.get('app', ''))
            elif action == 'open_website':
                return self._open_website(params.get('site', ''))
            elif action == 'sleep':
                return "Goodbye"
            else:
                return "Command not implemented"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _open_any_app(self, app_name: str) -> str:
        """Universal app opener using system shell"""
        try:
            subprocess.Popen(app_name, shell=True)
            return f"Opening {app_name}"
        except Exception as e:
            return f"Failed to open {app_name}: {str(e)}"
    
    def _open_website(self, site_name: str) -> str:
        """Universal website opener"""
        try:
            url = f'https://{site_name}' if not site_name.startswith(('http://', 'https://')) else site_name
            webbrowser.open(url)
            return f"Opening {site_name}"
        except Exception as e:
            return f"Failed to open {site_name}: {str(e)}"