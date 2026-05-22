import os
import zipfile
import shutil

class ModExtractor:
    def __init__(self, temp_dir="temp_extract"):
        self.temp_dir = temp_dir

    def clear_temp(self):
        """Safely cleans up the temporary extraction folder."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        os.makedirs(self.temp_dir, exist_ok=True)

    def extract_zip(self, zip_path):
        """Extracts the entire zip file into the sandbox directory."""
        self.clear_temp()
        
        if not zipfile.is_zipfile(zip_path):
            raise ValueError(f"The file {zip_path} is not a valid zip archive.")

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.temp_dir)
            
        return self.temp_dir

    def find_payload_root(self):
        """
        Scans the temp directory to find where the actual mod files begin.
        Fixes the issue where modders wrap everything inside an extra folder.
        """
        current_root = self.temp_dir
        
        while True:
            # List everything inside the current directory, ignoring hidden files
            items = [i for i in os.listdir(current_root) if not i.startswith('.')]
            
            # If there's exactly ONE item and it happens to be a folder, 
            # the mod files are nested deeper. Step inside it.
            if len(items) == 1 and os.path.isdir(os.path.join(current_root, items[0])):
                current_root = os.path.join(current_root, items[0])
            else:
                # We found the floor where the multiple loose files/folders exist
                break
                
        return current_root