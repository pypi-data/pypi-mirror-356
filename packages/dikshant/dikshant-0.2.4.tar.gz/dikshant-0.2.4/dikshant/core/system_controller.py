import subprocess
import webbrowser
import os
from typing import Dict, Any
import pyautogui

class SystemController:
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
        params = command.get('params', {})

        try:
            if action == 'open_app':
                return self._open_app(params.get('app', ''))
            elif action == 'open_website':
                return self._open_website(params.get('site', ''))
            elif action == 'search_google':
                return self._search_google(params.get('query', ''))
            elif action == 'volume_up':
                pyautogui.press('volumeup')
                return "volume increased"
            elif action == 'volume_down':
                pyautogui.press('volumedown')
                return "volume decreased"
            elif action == 'mute':
                pyautogui.press('volumemute')
                return "volume muted"
            elif action == 'shutdown':
                os.system('shutdown /s /t 5')
                return "shutting down"
            elif action == 'create_folder':
                return self._create_folder(params.get('foldername', 'NewFolder'))
            elif action == 'create_file':
                return self._create_file(params.get('filename', 'NewFile.txt'))
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
        subprocess.Popen(app_name, shell=True)
        return f"opening {app_name}"

    def _open_website(self, site_name: str) -> str:
        if '.' not in site_name:
            site_name = f"{site_name}.com"
        if not site_name.startswith(('http://', 'https://')):
            site_name = f'https://{site_name}'
        webbrowser.open(site_name)
        return f"opening {site_name}"

    def _search_google(self, query: str) -> str:
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(url)
        return f"searching for {query}"

    def _create_folder(self, foldername: str) -> str:
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        folder_path = os.path.join(desktop, foldername)
        os.makedirs(folder_path, exist_ok=True)
        return f"folder '{foldername}' created"

    def _create_file(self, filename: str) -> str:
        if not filename.lower().endswith('.txt'):
            filename += '.txt'
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        file_path = os.path.join(desktop, filename)
        with open(file_path, 'w') as f:
            f.write("Created by Dikshant Assistant\\n")
        return f"file '{filename}' created"
