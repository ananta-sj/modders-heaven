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

    def check_conflicts(self, payload_root):
        import json
        import os
        from pathlib import Path
        
        conflicts = []
        manifest_dir = Path("data/manifests")
        
        if not manifest_dir.exists():
            return conflicts

        payload_files = set()
        for root, _, files in os.walk(payload_root):
            for file in files:
                full_path = Path(root) / file
                rel_path = str(full_path.relative_to(payload_root))
                payload_files.add(rel_path)

        for manifest_file in manifest_dir.glob("*_manifest.json"):
            mod_name = manifest_file.name.replace("_manifest.json", "")
            
            try:
                with open(manifest_file, "r") as f:
                    manifest_data = json.load(f)
                    
                installed_files = manifest_data.get("files", {})
                
                for p_file in payload_files:
                    if p_file in installed_files:
                        conflicts.append((p_file, mod_name))
            except Exception:
                continue
                
        return conflicts

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