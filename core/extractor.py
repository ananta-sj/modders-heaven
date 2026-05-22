import os
import zipfile
import shutil

class ModExtractor:
    def __init__(self, temp_dir="temp_extract"):
        self.temp_dir = temp_dir

    def clear_temp(self):
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        os.makedirs(self.temp_dir, exist_ok=True)

    def extract_zip(self, zip_path):
        self.clear_temp()
        
        if not zipfile.is_zipfile(zip_path):
            raise ValueError(f"The file {zip_path} is not a valid zip archive.")

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.temp_dir)
            
        return self.temp_dir

    def find_payload_root(self):
        current_root = self.temp_dir
        
        while True:
            items = [i for i in os.listdir(current_root) if not i.startswith('.')]
            
            if len(items) == 1 and os.path.isdir(os.path.join(current_root, items[0])):
                current_root = os.path.join(current_root, items[0])
            else:
                break
                
        return current_root