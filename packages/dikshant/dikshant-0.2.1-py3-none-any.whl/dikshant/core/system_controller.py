import subprocess
import webbrowser
import os
from typing import Dict, Any

class SystemController:
    # All app names in lowercase
    SYSTEM_APPS = {
        'notepad': 'notepad.exe',
        'calculator': 'calc.exe',
        'paint': 'mspaint.exe',
        'wordpad': 'write.exe',
        'cmd': 'cmd.exe',
        'task manager': 'taskmgr.exe',
        'control panel': 'control.exe',
        'edge': 'start msedge',
        'chrome': 'start chrome'
    }

    def execute(self, command: Dict[str, Any]) -> str:
        action = command['action'].lower()
        params = {k:v.lower() for k,v in command.get('params', {}).items()}
        
        try:
            if action == 'open_app':
                return self._open_app(params.get('app', ''))
            elif action == 'open_website':
                return self._open_website(params.get('site', ''))
            elif action == 'sleep':
                return "goodbye"
            return "command not implemented"
        except Exception as e:
            return f"error: {str(e)}".lower()
    
    def _open_app(self, app_name: str) -> str:
        app_name = app_name.lower()
        
        if app_name in self.SYSTEM_APPS:
            os.system(self.SYSTEM_APPS[app_name])
            return f"opening {app_name}"
            
        try:
            subprocess.Popen(app_name.lower(), shell=True)
            return f"opening {app_name}"
        except Exception as e:
            return f"failed to open {app_name}: {str(e)}".lower()
    
    def _open_website(self, site_name: str) -> str:
        site_name = site_name.lower()
        
        if '.' not in site_name:
            site_name = f"{site_name}.com"
        if not site_name.startswith(('http://', 'https://')):
            site_name = f'https://{site_name}'
            
        webbrowser.open(site_name)
        return f"opening {site_name}"