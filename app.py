import customtkinter as ctk
from customtkinter import filedialog
import threading
import traceback
import os
from pathlib import Path
from tkinterdnd2 import TkinterDnD, DND_FILES

from core.extractor import ModExtractor
from core.installer import ModInstaller
from core.rollback import ModRollback
from core.config import ConfigManager

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class TkinterDnD_CTk(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

class ModInstallerGUI(TkinterDnD_CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)
        
        self.title("Modder's Heaven - v2.0")
        self.geometry("1000x680")
        self.iconbitmap("logo.ico")
        
        # Pure void background
        self.configure(fg_color="#030305") 
        self.config = ConfigManager()
        
        # --- CYBERPUNK FONTS ---
        ui_font = ctk.CTkFont(family="Courier New", size=14, weight="bold")
        title_font = ctk.CTkFont(family="Courier New", size=20, weight="bold")
        cmd_font = ctk.CTkFont(family="Consolas", size=13)
        
        # --- NEON PALETTE ---
        neon_cyan = "#00f3ff"
        neon_pink = "#ff007f"
        neon_yellow = "#fcee0a"
        panel_bg = "#08080c"
        
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # ==========================================
        # LEFT COLUMN: MAIN ACTION AREA
        # ==========================================
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_rowconfigure(2, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # --- TOP FRAME: Inputs (Neon Cyan Borders) ---
        self.input_frame = ctk.CTkFrame(self.main_frame, fg_color=panel_bg, border_width=2, border_color=neon_cyan, corner_radius=0)
        self.input_frame.grid(row=0, column=0, pady=(0, 15), sticky="ew")
        self.input_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(self.input_frame, text="MOD_ID:", text_color=neon_pink, font=ui_font).grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        self.entry_mod_name = ctk.CTkEntry(self.input_frame, font=ui_font, placeholder_text="AWAITING_INPUT...", fg_color="#000000", border_color=neon_pink, text_color=neon_cyan, corner_radius=0)
        self.entry_mod_name.grid(row=0, column=1, columnspan=2, padx=20, pady=(20, 10), sticky="ew")
        
        ctk.CTkLabel(self.input_frame, text="ZIP_PAYLOAD:", text_color=neon_pink, font=ui_font).grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.entry_zip = ctk.CTkEntry(self.input_frame, font=ui_font, fg_color="#000000", border_color=neon_pink, text_color=neon_cyan, corner_radius=0) 
        self.entry_zip.grid(row=1, column=1, padx=(20, 5), pady=10, sticky="ew")
        
        # Hollow "Ghost" buttons for browsing
        self.btn_browse_zip = ctk.CTkButton(self.input_frame, text="[SEARCH]", width=80, font=ui_font, fg_color="transparent", border_width=1, border_color=neon_cyan, text_color=neon_cyan, hover_color="#003333", corner_radius=0, command=self.browse_zip)
        self.btn_browse_zip.grid(row=1, column=2, padx=(5, 20), pady=10)
        
        ctk.CTkLabel(self.input_frame, text="TARGET_DIR:", text_color=neon_pink, font=ui_font).grid(row=2, column=0, padx=20, pady=(10, 20), sticky="w")
        self.entry_game = ctk.CTkEntry(self.input_frame, font=ui_font, fg_color="#000000", border_color=neon_pink, text_color=neon_cyan, corner_radius=0)
        self.entry_game.grid(row=2, column=1, padx=(20, 5), pady=(10, 20), sticky="ew")
        
        saved_dir = self.config.get_game_dir()
        if saved_dir:
            self.entry_game.insert(0, saved_dir)
        self.entry_game.configure(state="disabled")
            
        self.btn_browse_game = ctk.CTkButton(self.input_frame, text="[SEARCH]", width=80, font=ui_font, fg_color="transparent", border_width=1, border_color=neon_cyan, text_color=neon_cyan, hover_color="#003333", corner_radius=0, command=self.browse_game)
        self.btn_browse_game.grid(row=2, column=2, padx=(5, 20), pady=(10, 20))

        # --- MIDDLE FRAME: Cyber Yellow Action Button ---
        self.btn_install = ctk.CTkButton(
            self.main_frame, text="> EXECUTE_INJECTION <", 
            fg_color="transparent", border_width=2, border_color=neon_yellow,
            hover_color="#333300", text_color=neon_yellow,
            height=45, corner_radius=0, font=ctk.CTkFont(family="Courier New", size=18, weight="bold"),
            command=self.start_install
        )
        self.btn_install.grid(row=1, column=0, pady=(0, 15), sticky="ew")

        # --- BOTTOM FRAME: Hacker Terminal ---
        self.console = ctk.CTkTextbox(
            self.main_frame, fg_color="#000000", text_color="#00ff41", # Classic Matrix Green text 
            border_width=2, border_color=neon_pink, corner_radius=0,
            font=cmd_font, wrap="word"
        )
        self.console.grid(row=2, column=0, sticky="nsew")
        
        self.log_message("SYS_OS [Version 2077.0]\n(c) Night City Corp. Unauthorized access logged.\n\nC:\\> AWAITING_PAYLOAD...")

        # ==========================================
        # RIGHT COLUMN: INSTALLED MODS SIDEBAR
        # ==========================================
        self.sidebar_frame = ctk.CTkFrame(self, fg_color=panel_bg, border_width=2, border_color=neon_cyan, corner_radius=0) 
        self.sidebar_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 20), pady=20)
        self.sidebar_frame.grid_rowconfigure(1, weight=1)
        
        self.lbl_sidebar = ctk.CTkLabel(self.sidebar_frame, text="// ACTIVE_MODS", text_color=neon_yellow, font=title_font)
        self.lbl_sidebar.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        self.mod_list_scroll = ctk.CTkScrollableFrame(self.sidebar_frame, fg_color="transparent")
        self.mod_list_scroll.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        
        self.refresh_mod_list()

        # --- DRAG AND DROP SETUP ---
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.handle_drop)

    def log_message(self, message):
        self.console.insert("end", message + "\n")
        self.console.see("end")

    def browse_zip(self):
        filename = filedialog.askopenfilename(filetypes=[("Zip Archives", "*.zip")])
        if filename:
            self.entry_zip.configure(state="normal")
            self.entry_zip.delete(0, "end")
            self.entry_zip.insert(0, filename)
            self.entry_zip.configure(state="disabled")
    
    def handle_drop(self, event):
        file_path = event.data
        
        file_path = file_path.strip('{}')
        
        if file_path.lower().endswith(".zip"):
            self.entry_zip.configure(state="normal")
            self.entry_zip.delete(0, "end")
            self.entry_zip.insert(0, file_path)
            self.entry_zip.configure(state="disabled")
            
            mod_name = os.path.basename(file_path).replace(".zip", "")
            self.entry_mod_name.delete(0, "end")
            self.entry_mod_name.insert(0, mod_name)
            
            self.log_message(f"C:\\> Zip file loaded via Drag & Drop: {mod_name}")
        else:
            self.log_message("C:\\> ERROR: Only .zip files can be dropped here!")

    def browse_game(self):
        dirname = filedialog.askdirectory()
        if dirname:
            self.entry_game.configure(state="normal")
            self.entry_game.delete(0, "end")
            self.entry_game.insert(0, dirname)
            self.entry_game.configure(state="disabled")
            self.config.set_game_dir(dirname)

    def refresh_mod_list(self):
        for widget in self.mod_list_scroll.winfo_children():
            widget.destroy()

        manifest_dir = Path("data/manifests")
        if not manifest_dir.exists():
            return

        mods_found = False
        for manifest_file in manifest_dir.glob("*_manifest.json"):
            mods_found = True
            mod_name = manifest_file.name.replace("_manifest.json", "")
            
            # Create a mini container for the row (Hollow Neon Border)
            row_frame = ctk.CTkFrame(self.mod_list_scroll, fg_color="#000000", border_width=1, border_color="#00f3ff", corner_radius=0)
            row_frame.pack(fill="x", pady=4, padx=4)
            
            # Mod Name Label
            lbl = ctk.CTkLabel(row_frame, text=mod_name, text_color="#00f3ff", anchor="w", font=ctk.CTkFont(family="Courier New", weight="bold"))
            lbl.pack(side="left", padx=10, pady=5, fill="x", expand=True)
            
            # Uninstall "X" Button (Neon Red/Pink warning)
            btn = ctk.CTkButton(row_frame, text="[X]", width=30, height=24, fg_color="transparent", border_width=1, border_color="#ff007f", text_color="#ff007f", hover_color="#33001a", corner_radius=0, command=lambda m=mod_name: self.start_uninstall(m))
            btn.pack(side="right", padx=10, pady=5)
            
        if not mods_found:
            lbl = ctk.CTkLabel(self.mod_list_scroll, text="No mods installed.", text_color="gray")
            lbl.pack(pady=20)

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
            self.log_message(f"C:\\> Initializing pipeline for '{mod_name}'...")
            extractor = ModExtractor()
            installer = ModInstaller(game_dir=game_dir)
            
            self.log_message("C:\\> Extracting payload to sandbox...")
            sandbox_dir = extractor.extract_zip(zip_path)
            payload_root = extractor.find_payload_root()
            
            # --- NEW: CONFLICT DETECTION ENGINE ---
            self.log_message("C:\\> Scanning for file conflicts...")
            conflicts = installer.check_conflicts(payload_root)
            
            if conflicts:
                self.log_message("\n[!] FATAL: FILE CONFLICT DETECTED [!]")
                for file_path, conflicting_mod in conflicts:
                    self.log_message(f"  -> File: {file_path}")
                    self.log_message(f"  -> Controlled by: '{conflicting_mod}'")
                
                self.log_message("\nC:\\> INSTALLATION ABORTED. Uninstall the conflicting mod first to protect game integrity.")
                
                extractor.clear_temp()
                self.btn_install.configure(state="normal")
                return
            # ---------------------------------------
            
            self.log_message("C:\\> Backing up vanilla files & writing manifest...")
            manifest_path = installer.install_mod(mod_name, payload_root)
            self.log_message(f"C:\\> SUCCESS: Mod committed. Manifest: {manifest_path}")
            
        except Exception as e:
            self.log_message(f"\nFATAL EXCEPTION:\n{traceback.format_exc()}")
            
        finally:
            if 'extractor' in locals():
                self.log_message("C:\\> Cleaning up sandbox...")
                extractor.clear_temp()
            self.btn_install.configure(state="normal")
            
            self.refresh_mod_list()

    def start_uninstall(self, mod_name):
        game_dir = self.entry_game.get()
        if not game_dir:
            self.log_message("C:\\> ERROR: Game directory not set.")
            return
            
        self.log_message(f"\nC:\\> Starting Uninstall for: {mod_name}...")
        rollback = ModRollback(game_dir=game_dir)
        result = rollback.uninstall_mod(mod_name)
        
        self.log_message(f"C:\\> {result}")
        
        self.refresh_mod_list()

if __name__ == "__main__":
    app = ModInstallerGUI()
    app.mainloop()