import os
import shutil
import json
from pathlib import Path

class ModInstaller:
    def __init__(self, game_dir, backup_dir="backups", manifest_dir="data/manifests"):
        self.game_dir = Path(game_dir)
        self.backup_dir = Path(backup_dir)
        self.manifest_dir = Path(manifest_dir)
        
        # Ensure our storage directories exist
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.manifest_dir.mkdir(parents=True, exist_ok=True)

    def install_mod(self, mod_name, payload_root):
        payload_path = Path(payload_root)
        manifest = {"mod_name": mod_name, "files": []}
        mod_backup_dir = self.backup_dir / mod_name
        
        # Walk through every file in the unzipped mod
        for root, _, files in os.walk(payload_path):
            for file in files:
                source_file = Path(root) / file
                
                # Calculate the exact path relative to the game directory
                rel_path = source_file.relative_to(payload_path)
                target_file = self.game_dir / rel_path
                
                # 1. Handle Backup & Manifest Logging
                if target_file.exists():
                    # The game already has this file. Back it up!
                    backup_file = mod_backup_dir / rel_path
                    backup_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(target_file, backup_file)
                    
                    manifest["files"].append({
                        "path": str(rel_path),
                        "action": "replaced"
                    })
                else:
                    # This is a brand new file added by the mod
                    manifest["files"].append({
                        "path": str(rel_path),
                        "action": "added"
                    })
                    
                # 2. Copy the mod file into the live game directory
                target_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source_file, target_file)

        # 3. Save the Manifest to disk
        manifest_path = self.manifest_dir / f"{mod_name}_manifest.json"
        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=4)
            
        return manifest_path