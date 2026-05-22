import os
import shutil
import json
from pathlib import Path

class ModInstaller:
    def __init__(self, game_dir, backup_dir="backups", manifest_dir="data/manifests"):
        self.game_dir = Path(game_dir)
        self.backup_dir = Path(backup_dir)
        self.manifest_dir = Path(manifest_dir)
        
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.manifest_dir.mkdir(parents=True, exist_ok=True)

    def install_mod(self, mod_name, payload_root):
        payload_path = Path(payload_root)
        manifest = {"mod_name": mod_name, "files": []}
        mod_backup_dir = self.backup_dir / mod_name
        
        for root, _, files in os.walk(payload_path):
            for file in files:
                source_file = Path(root) / file
                
                rel_path = source_file.relative_to(payload_path)
                target_file = self.game_dir / rel_path
                
                if target_file.exists():
                    backup_file = mod_backup_dir / rel_path
                    backup_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(target_file, backup_file)
                    
                    manifest["files"].append({
                        "path": str(rel_path),
                        "action": "replaced"
                    })
                else:
                    manifest["files"].append({
                        "path": str(rel_path),
                        "action": "added"
                    })
                    
                target_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source_file, target_file)

        manifest_path = self.manifest_dir / f"{mod_name}_manifest.json"
        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=4)
            
        return manifest_path