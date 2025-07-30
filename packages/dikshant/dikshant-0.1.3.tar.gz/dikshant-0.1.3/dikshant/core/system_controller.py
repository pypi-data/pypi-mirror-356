 
import os
import subprocess
import webbrowser

class SystemController:
    def execute(self, command):
        action = command['action']
        
        if action == 'open_app':
            return self._open_app(command['params']['app'])
        elif action == 'open_website':
            return self._open_website(command['params']['site'])
        # Add more actions here
        else:
            return "Command not implemented"
    
    def _open_app(self, app_name):
        try:
            app_map = {
                'youtube': 'chrome.exe',
                'chrome': 'chrome.exe',
                'notepad': 'notepad.exe'
            }
            subprocess.Popen(app_map.get(app_name.lower(), app_name))
            return f"Opening {app_name}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _open_website(self, site):
        try:
            site_map = {
                'youtube': 'https://youtube.com',
                'google': 'https://google.com'
            }
            webbrowser.open(site_map.get(site.lower(), f'https://{site}'))
            return f"Opening {site}"
        except Exception as e:
            return f"Error: {str(e)}"