import os
import json
import shutil
from pathlib import Path

class ModRollback:
    def __init__(self, game_dir, backup_dir="backups", manifest_dir="data/manifests"):
        self.game_dir = Path(game_dir)
        self.backup_dir = Path(backup_dir)
        self.manifest_dir = Path(manifest_dir)

    def uninstall_mod(self, mod_name):
        manifest_path = self.manifest_dir / f"{mod_name}_manifest.json"
        
        if not manifest_path.exists():
            return f"Error: No manifest found for {mod_name}"
            
        # Load the manifest
        with open(manifest_path, "r") as f:
            manifest = json.load(f)
            
        mod_backup_dir = self.backup_dir / mod_name
        
        # Reverse the actions logged in the manifest
        for file_record in manifest["files"]:
            rel_path = Path(file_record["path"])
            target_file = self.game_dir / rel_path
            
            if file_record["action"] == "added":
                if target_file.exists():
                    os.remove(target_file)
                    
            elif file_record["action"] == "replaced":
                backup_file = mod_backup_dir / rel_path
                if backup_file.exists():
                    target_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(backup_file, target_file)
                    
        if mod_backup_dir.exists():
            shutil.rmtree(mod_backup_dir)
        os.remove(manifest_path)
        
        return "Uninstalled successfully."