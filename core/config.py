import json
import os
from pathlib import Path

class ConfigManager:
    def __init__(self, config_path="data/config.json"):
        self.config_path = Path(config_path)
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.config = self.load_config()

    def load_config(self):
        if not self.config_path.exists():
            return {"game_dir": ""}
            
        try:
            with open(self.config_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {"game_dir": ""}

    def save_config(self):
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=4)
            
    def get_game_dir(self):
        return self.config.get("game_dir", "")
        
    def set_game_dir(self, path):
        self.config["game_dir"] = path
        self.save_config()