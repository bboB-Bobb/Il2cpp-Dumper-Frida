import tkinter as tk
from tkinter import ttk
import subprocess
import threading
import sys
import os
import csv

class DumperApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Il2Cpp Dumper")
        self.window.geometry("500x420")
        self.window.configure(bg="#0d1117")
        self.window.resizable(False, False)

        # Style Combobox dropdown listbox
        self.window.option_add('*TCombobox*Listbox.background', '#161b22')
        self.window.option_add('*TCombobox*Listbox.foreground', '#c9d1d9')
        self.window.option_add('*TCombobox*Listbox.selectBackground', '#3182ce')
        self.window.option_add('*TCombobox*Listbox.selectForeground', '#ffffff')

        self.setup_styles()
        self.build_ui()
        
        self.frida_process = None
        self.refresh_process_list()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure("TFrame", background="#0d1117")
        style.configure("TLabel", background="#0d1117", foreground="#c9d1d9", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground="#58a6ff")
        style.configure("Desc.TLabel", font=("Segoe UI", 9), foreground="#8b949e")
        
        style.configure("TCombobox", fieldbackground="#161b22", background="#30363d", foreground="#c9d1d9", borderwidth=1, arrowcolor="#c9d1d9")
        
        style.configure("Primary.TButton", background="#238636", foreground="white", font=("Segoe UI", 10, "bold"), borderwidth=0, padding=8)
        style.map("Primary.TButton", background=[("active", "#2ea043"), ("disabled", "#30363d")])

        style.configure("Secondary.TButton", background="#30363d", foreground="#c9d1d9", font=("Segoe UI", 10, "bold"), padding=8)
        style.map("Secondary.TButton", background=[("active", "#4b5563"), ("disabled", "#21262d")])

        style.configure("Refresh.TButton", background="#30363d", foreground="#c9d1d9", font=("Segoe UI", 12, "bold"), padding=2)
        style.map("Refresh.TButton", background=[("active", "#4b5563")])

    def build_ui(self):
        main_layout = ttk.Frame(self.window, padding=25)
        main_layout.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_layout, text="Il2Cpp Dumper", style="Header.TLabel").pack(pady=(0, 2))
        ttk.Label(main_layout, text="Attach Frida and dump assemblies", style="Desc.TLabel").pack(pady=(0, 20))

        selection_frame = ttk.Frame(main_layout)
        selection_frame.pack(fill=tk.X, pady=(0, 20))
        ttk.Label(selection_frame, text="Target Process:").pack(anchor=tk.W, pady=(0, 5))
        
        combo_container = ttk.Frame(selection_frame)
        combo_container.pack(fill=tk.X)
        
        self.selected_process = tk.StringVar()
        self.combo_box = ttk.Combobox(combo_container, textvariable=self.selected_process, font=("Segoe UI", 10), style="TCombobox")
        self.combo_box.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.refresh_btn = ttk.Button(combo_container, text="↻", style="Refresh.TButton", width=3, command=self.refresh_process_list)
        self.refresh_btn.pack(side=tk.LEFT, padx=(8, 0))

        button_row = ttk.Frame(main_layout)
        button_row.pack(fill=tk.X, pady=(0, 20))

        self.inject_btn = ttk.Button(button_row, text="Inject & Dump", style="Primary.TButton", command=self.trigger_dump)
        self.inject_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        self.open_folder_btn = ttk.Button(button_row, text="Open Output", command=self.open_output_folder, style="Secondary.TButton")
        self.open_folder_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))

        self.console_view = tk.Text(main_layout, bg="#161b22", fg="#8b949e", font=("Consolas", 9), height=10, relief=tk.FLAT, padx=10, pady=10, wrap=tk.WORD)
        self.console_view.pack(fill=tk.BOTH, expand=True)
        
        self.console_view.tag_config("sys", foreground="#58a6ff")
        self.console_view.tag_config("err", foreground="#f85149")
        self.console_view.tag_config("success", foreground="#2ea043")
        self.console_view.tag_config("std", foreground="#8b949e")

        self.print_sys("Ready. Waiting for input.")

    def open_output_folder(self):
        folder_path = os.path.join(os.getcwd(), "Dumped")
        os.makedirs(folder_path, exist_ok=True)
        if os.name == 'nt':
            os.startfile(folder_path)

    def refresh_process_list(self):
        self.combo_box.set("Scanning...")
        self.window.update()
        
        active_processes = self.fetch_windows_processes()
        self.combo_box['values'] = active_processes
        
        if active_processes:
            self.combo_box.set(active_processes[0])
        else:
            self.combo_box.set("")

    def fetch_windows_processes(self):
        try:
            hide_window_flag = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            raw_output = subprocess.check_output('tasklist /fo csv /nh', shell=True, text=True, creationflags=hide_window_flag)
            
            found_exes = set()
            for line in csv.reader(raw_output.splitlines()):
                if line and len(line) > 0:
                    proc_name = line[0]
                    if proc_name.lower().endswith('.exe'):
                        found_exes.add(proc_name)
            
            system_processes = {"svchost.exe", "conhost.exe", "RuntimeBroker.exe", "cmd.exe", "taskhostw.exe", 
                                "dllhost.exe", "SearchIndexer.exe", "csrss.exe", "lsass.exe", "smss.exe", 
                                "winlogon.exe", "services.exe", "fontdrvhost.exe", "explorer.exe", "ctfmon.exe"}
            
            clean_list = [p for p in found_exes if p not in system_processes]
            return sorted(clean_list, key=lambda x: x.lower())
        except Exception as e:
            self.print_err(f"Failed to fetch processes: {str(e)}")
            return []

    def _push_log(self, text, style="std"):
        self.console_view.configure(state=tk.NORMAL)
        self.console_view.insert(tk.END, text + "\n", style)
        self.console_view.see(tk.END)
        self.console_view.configure(state=tk.DISABLED)

    def print_sys(self, msg): self._push_log(f"[System] {msg}", "sys")
    def print_err(self, msg): self._push_log(f"[Error] {msg}", "err")
    def print_success(self, msg): self._push_log(msg, "success")
    def print_std(self, msg): self._push_log(msg, "std")

    def trigger_dump(self):
        target_exe = self.selected_process.get().strip()
        if not target_exe:
            self.print_err("No process selected.")
            return

        self.inject_btn.config(state=tk.DISABLED, text="Running...")
        self.refresh_btn.config(state=tk.DISABLED)
        self.open_folder_btn.config(state=tk.DISABLED)
        
        self.console_view.configure(state=tk.NORMAL)
        self.console_view.delete(1.0, tk.END)
        self.console_view.configure(state=tk.DISABLED)
        
        self.print_sys(f"Initializing dump for target: {target_exe}")
        
        threading.Thread(target=self.run_background_tasks, args=(target_exe,), daemon=True).start()

    def run_background_tasks(self, target_exe):
        npm = "npm.cmd" if os.name == 'nt' else "npm"
        hide_window_flag = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0

        if not os.path.exists("node_modules"):
            self.print_sys("node_modules not found. Installing dependencies...")
            try:
                installer = subprocess.Popen([npm, "install"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=hide_window_flag)
                for line in iter(installer.stdout.readline, ''):
                    if line: self.window.after(0, self.print_std, line.strip())
                installer.wait()
                
                if installer.returncode != 0:
                    self.window.after(0, self.print_err, "Dependency installation failed.")
                    self.window.after(0, self.unlock_ui)
                    return
                self.window.after(0, self.print_success, "Dependencies installed successfully.")
            except Exception as e:
                self.window.after(0, self.print_err, f"npm install error: {str(e)}")
                self.window.after(0, self.unlock_ui)
                return

        self.print_sys("Generating agent.ts...")
        
        game_clean_name = target_exe[:-4] if target_exe.lower().endswith(".exe") else target_exe
        final_filename = f"{game_clean_name}_Dump.cs"
        
        dump_folder = os.path.join(os.getcwd(), "Dumped").replace('\\', '/')
        os.makedirs("Dumped", exist_ok=True)
        
        agent_script = f"""import "frida-il2cpp-bridge";

Il2Cpp.perform(() => {{
    console.log("[+] Il2Cpp dumping initialized.");
    console.log("[+] Unity version: " + Il2Cpp.unityVersion);

    Il2Cpp.dump("{final_filename}", "{dump_folder}");

    console.log("[+] Dump complete: {dump_folder}/{final_filename}");
}});
"""
        try:
            with open("agent.ts", "w", encoding="utf-8") as f:
                f.write(agent_script)
        except Exception as e:
            self.window.after(0, self.print_err, f"File write error: {str(e)}")
            self.window.after(0, self.unlock_ui)
            return

        self.print_sys("Compiling agent script...")
        try:
            builder = subprocess.Popen([npm, "run", "build"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=hide_window_flag)
            for line in iter(builder.stdout.readline, ''):
                if line: self.window.after(0, self.print_std, line.strip())
            
            builder.wait()
            if builder.returncode != 0:
                self.window.after(0, self.print_err, "Build process failed.")
                self.window.after(0, self.unlock_ui)
                return
                
            self.window.after(0, self.print_sys, "Compilation successful. Injecting Frida agent...")
            
            self.frida_process = subprocess.Popen(["frida", "-n", target_exe, "-l", "agent.js"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=hide_window_flag)
            
            for line in iter(self.frida_process.stdout.readline, ''):
                if line:
                    lower_line = line.lower()
                    if "error" in lower_line or "exception" in lower_line or "failed" in lower_line:
                        self.window.after(0, self.print_err, line.strip())
                    elif "complete" in lower_line or "success" in lower_line or "initialized" in lower_line:
                        self.window.after(0, self.print_success, line.strip())
                        if "complete" in lower_line:
                            self.window.after(0, self.open_output_folder)
                    else:
                        self.window.after(0, self.print_std, line.strip())
                        
            self.frida_process.wait()
            self.window.after(0, self.print_sys, "Frida process terminated.")
            
        except FileNotFoundError as e:
            self.window.after(0, self.print_err, f"Executable not found: {e.filename}.")
        except Exception as e:
            self.window.after(0, self.print_err, f"Execution error: {str(e)}")
        finally:
            self.window.after(0, self.unlock_ui)

    def unlock_ui(self):
        self.inject_btn.config(state=tk.NORMAL, text="Inject & Dump")
        self.refresh_btn.config(state=tk.NORMAL)
        self.open_folder_btn.config(state=tk.NORMAL)

if __name__ == "__main__":
    app_window = tk.Tk()
    app = DumperApp(app_window)
    app_window.mainloop()
