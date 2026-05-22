import customtkinter as ctk
from customtkinter import filedialog
import threading
import traceback

from core.extractor import ModExtractor
from core.installer import ModInstaller
from core.rollback import ModRollback

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ModInstallerGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Universal Mod Installer - v1.0")
        self.geometry("700x650")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # --- TOP FRAME: Inputs ---
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        self.input_frame.grid_columnconfigure(1, weight=1)
        
        # Mod Identifier
        ctk.CTkLabel(self.input_frame, text="Mod Identifier:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=15, pady=(15, 10), sticky="w")
        self.entry_mod_name = ctk.CTkEntry(self.input_frame, placeholder_text="e.g., HD_Textures_V1")
        self.entry_mod_name.grid(row=0, column=1, columnspan=2, padx=15, pady=(15, 10), sticky="ew")
        
        # Zip Selection
        ctk.CTkLabel(self.input_frame, text="Mod Zip File:", font=ctk.CTkFont(weight="bold")).grid(row=1, column=0, padx=15, pady=10, sticky="w")
        self.entry_zip = ctk.CTkEntry(self.input_frame, state="disabled") 
        self.entry_zip.grid(row=1, column=1, padx=(15, 0), pady=10, sticky="ew")
        ctk.CTkButton(self.input_frame, text="Browse", width=80, command=self.browse_zip).grid(row=1, column=2, padx=15, pady=10)
        
        # Game Directory Selection
        ctk.CTkLabel(self.input_frame, text="Game Directory:", font=ctk.CTkFont(weight="bold")).grid(row=2, column=0, padx=15, pady=(10, 15), sticky="w")
        self.entry_game = ctk.CTkEntry(self.input_frame, state="disabled")
        self.entry_game.grid(row=2, column=1, padx=(15, 0), pady=(10, 15), sticky="ew")
        ctk.CTkButton(self.input_frame, text="Browse", width=80, command=self.browse_game).grid(row=2, column=2, padx=15, pady=(10, 15))

        # --- MIDDLE FRAME: Actions ---
        self.action_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.action_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.action_frame.grid_columnconfigure((0, 1), weight=1)
        
        self.btn_install = ctk.CTkButton(self.action_frame, text="Install Mod", fg_color="#238636", hover_color="#2ea043", height=40, font=ctk.CTkFont(weight="bold"), command=self.start_install)
        self.btn_install.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        
        self.btn_uninstall = ctk.CTkButton(self.action_frame, text="Uninstall Mod", fg_color="#da3633", hover_color="#f85149", height=40, font=ctk.CTkFont(weight="bold"), command=self.start_uninstall)
        self.btn_uninstall.grid(row=0, column=1, padx=(10, 0), sticky="ew")

        # --- BOTTOM FRAME: CMD Terminal ---
        cmd_font = ctk.CTkFont(family="Consolas", size=13)
        self.console = ctk.CTkTextbox(
            self, 
            fg_color="#0C0C0C", 
            text_color="#16C60C", 
            font=cmd_font,
            wrap="word"
        )
        self.console.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
        self.log_message("Microsoft Windows [Version 10.0]\n(c) Microsoft Corporation. All rights reserved.\n\nC:\\UniversalModTool> System initialized...")

    def log_message(self, message):
        """Appends text to the terminal and auto-scrolls to the bottom."""
        self.console.insert("end", message + "\n")
        self.console.see("end")

    def browse_zip(self):
        filename = filedialog.askopenfilename(filetypes=[("Zip Archives", "*.zip")])
        if filename:
            self.entry_zip.configure(state="normal")
            self.entry_zip.delete(0, "end")
            self.entry_zip.insert(0, filename)
            self.entry_zip.configure(state="disabled")

    def browse_game(self):
        dirname = filedialog.askdirectory()
        if dirname:
            self.entry_game.configure(state="normal")
            self.entry_game.delete(0, "end")
            self.entry_game.insert(0, dirname)
            self.entry_game.configure(state="disabled")

    def start_install(self):
        mod_name = self.entry_mod_name.get()
        zip_path = self.entry_zip.get()
        game_dir = self.entry_game.get()
        
        if not mod_name or not zip_path or not game_dir:
            self.log_message("C:\\> ERROR: Missing parameters.")
            return
            
        self.btn_install.configure(state="disabled")
        threading.Thread(target=self.run_install_task, args=(zip_path, game_dir, mod_name), daemon=True).start()

    def run_install_task(self, zip_path, game_dir, mod_name):
        try:
            # 1. Initialize Tools
            self.log_message(f"C:\\> Initializing pipeline for '{mod_name}'...")
            extractor = ModExtractor()
            installer = ModInstaller(game_dir=game_dir)
            
            # 2. Extract
            self.log_message("C:\\> Extracting payload to sandbox...")
            sandbox_dir = extractor.extract_zip(zip_path)
            payload_root = extractor.find_payload_root()
            
            # 3. Install
            self.log_message("C:\\> Backing up vanilla files & writing manifest...")
            manifest_path = installer.install_mod(mod_name, payload_root)
            self.log_message(f"C:\\> SUCCESS: Mod committed. Manifest: {manifest_path}")
            
        except Exception as e:
            self.log_message(f"\nFATAL EXCEPTION:\n{traceback.format_exc()}")
            
        finally:
            self.log_message("C:\\> Cleaning up sandbox...")
            extractor.clear_temp()
            self.btn_install.configure(state="normal")

    def start_uninstall(self):
        pass

if __name__ == "__main__":
    app = ModInstallerGUI()
    app.mainloop()