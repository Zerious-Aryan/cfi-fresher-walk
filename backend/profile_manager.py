import json
import os

DATA_PATH = "data/profiles.json"

class ProfileManager:
    def __init__(self):
        self.profiles = []
        self._load_profiles()

    def _load_profiles(self):
        if os.path.exists(DATA_PATH):
            with open(DATA_PATH, 'r') as f:
                self.profiles = json.load(f)
        else:
            self.profiles = []
            self._save_profiles()

    def _save_profiles(self):
        with open(DATA_PATH, 'w') as f:
            json.dump(self.profiles, f, indent=4)

    def add_profile(self, name, image_path, html):
        new_profile = {"name": name, "image": image_path, "HTML": html}
        self.profiles.append(new_profile)
        self._save_profiles()

    def delete_profile(self, name):
        self.profiles = [p for p in self.profiles if p["name"] != name]
        self._save_profiles()

    def get_profiles(self):
        return self.profiles
