import subprocess
import webbrowser
import os
from typing import Dict, Any

class SystemController:
    # Windows app mappings
    WIN_APPS = {
        'calculator': 'calc.exe',
        'notepad': 'notepad.exe',
        'paint': 'mspaint.exe',
        'wordpad': 'write.exe',
        'cmd': 'cmd.exe',
        'task manager': 'taskmgr.exe',
        'control panel': 'control.exe',
        'edge': 'msedge.exe',
        'chrome': 'chrome.exe'
    }

    def execute(self, command: Dict[str, Any]) -> str:
        action = command['action']
        params = command.get('params', {})
        
        try:
            if action == 'open_app':
                return self._open_any_app(params.get('app', ''))
            elif action == 'open_website':
                return self._open_website(params.get('site', ''))
            elif action == 'create_folder':
                return self._create_folder()
            elif action == 'sleep':
                return "Goodbye"
            else:
                return "Command not implemented"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _open_any_app(self, app_name: str) -> str:
        """Improved Windows app handling"""
        try:
            # Check mapped apps first
            app_key = app_name.lower()
            if app_key in self.WIN_APPS:
                subprocess.Popen(self.WIN_APPS[app_key])
                return f"Opening {app_name}"
            
            # Try direct execution
            subprocess.Popen(app_name, shell=True)
            return f"Opening {app_name}"
        except Exception as e:
            return f"Failed to open {app_name}: {str(e)}"

    def _open_website(self, site_name: str) -> str:
        """Improved website handling"""
        try:
            # Add .com if no domain specified
            if '.' not in site_name:
                site_name = f"{site_name}.com"
            
            # Ensure https protocol
            if not site_name.startswith(('http://', 'https://')):
                site_name = f'https://{site_name}'
                
            webbrowser.open(site_name)
            return f"Opening {site_name}"
        except Exception as e:
            return f"Failed to open {site_name}: {str(e)}"

    def _create_folder(self) -> str:
        """Create folder on desktop"""
        try:
            desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
            new_folder = os.path.join(desktop, 'New Folder')
            os.makedirs(new_folder, exist_ok=True)
            return "Created new folder on desktop"
        except Exception as e:
            return f"Failed to create folder: {str(e)}"