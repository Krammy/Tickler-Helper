import os, json
from pathlib import Path

class Settings:
    def __init__(self):
        # Step 1: Get the current directory path of your Python script
        # Step 2: Combine the script directory path with the filename 'settings.json'
        script_directory = Path(__file__).resolve().parent
        settings_file_path = script_directory.joinpath('settings.json')
        with open(settings_file_path, 'r') as settings_file:
            settings = json.load(settings_file)
        ztk_path = settings['ztk_path']
        self.tickler_path = os.path.join(ztk_path, settings['tickler_path'])
        self.inbox_path = os.path.join(ztk_path, settings['inbox_path'])

settings = Settings()
