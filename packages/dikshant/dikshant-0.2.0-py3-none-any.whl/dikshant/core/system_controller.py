import subprocess
import webbrowser
import os
from typing import Dict, Any

class SystemController:
    # Enhanced Windows apps mapping
    WIN_APPS = {
        'calculator': 'calc.exe',
        'notepad': 'notepad.exe',
        'paint': 'mspaint.exe',
        'wordpad': 'write.exe',
        'cmd': 'cmd.exe',
        'task manager': 'taskmgr.exe',
        'control panel': 'control.exe',
        'edge': 'start msedge',
        'chrome': 'start chrome',
        'word': 'start winword',
        'excel': 'start excel'
    }

    def execute(self, command: Dict[str, Any]) -> str:
        action = command['action']
        params = command.get('params', {})
        
        try:
            if action == 'open_app':
                return self._open_windows_app(params.get('app', ''))
            elif action == 'open_website':
                return self._open_website(params.get('site', ''))
            elif action == 'create_folder':
                return self._create_folder()
            elif action == 'sleep':
                return "Goodbye"
            return "Command not implemented"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _open_windows_app(self, app_name: str) -> str:
        """Robust Windows app opener"""
        app_name = app_name.lower()
        
        # Handle Microsoft Store apps
        if app_name in self.WIN_APPS:
            os.system(self.WIN_APPS[app_name])
            return f"Opening {app_name}"
            
        # Try direct execution
        try:
            subprocess.Popen(app_name, shell=True)
            return f"Opening {app_name}"
        except Exception as e:
            return f"Failed to open {app_name}: {str(e)}"

    def _open_website(self, site_name: str) -> str:
        """Smart website opener"""
        try:
            if not site_name.startswith(('http://', 'https://')):
                if '.' not in site_name:
                    site_name = f"{site_name}.com"
                site_name = f"https://{site_name}"
            webbrowser.open(site_name)
            return f"Opening {site_name}"
        except Exception as e:
            return f"Failed to open {site_name}: {str(e)}"

    def _create_folder(self) -> str:
        """Desktop folder creator"""
        try:
            desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
            new_folder = os.path.join(desktop, 'New Folder')
            os.makedirs(new_folder, exist_ok=True)
            return "Created new folder on desktop"
        except Exception as e:
            return f"Failed to create folder: {str(e)}"