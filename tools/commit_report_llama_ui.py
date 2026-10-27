import sys
import os
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, timedelta
import json
import time
import urllib.request
import urllib.error

SYSTEM_PROMPT = """You are an expert developer and technical lead.
Generate a comprehensive, clear, and professional Git Commit Report summarizing the provided commit logs.

The report must include:
1. Executive Summary: A high-level overview of the main features, bug fixes, and goals achieved during this period.
2. Grouped Changes: Organize individual changes into logical categories (e.g., Features, Bug Fixes, Refactoring, Documentation) with detailed bullet points. Include brief explanations.
3. Impact Analysis: Explain any overall architecture impacts, codebase health changes, or key dependencies introduced.

Use clean Markdown formatting. Do not wrap the output in markdown code blocks. Start directly with the report title '# RELEASE' followed by 3 empty lines."""

# Globals for service loading
llama_service_loading = True
llama_service_error = None

def check_alive():
    url = "http://localhost:9090/v1/chat/completions"
    data = json.dumps({
        "messages": [{"role": "user", "content": "ping"}],
        "max_tokens": 1
    }).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=3) as response:
            if response.getcode() == 200:
                response.read()
                return True
    except Exception:
        pass
    return False

def ensure_llama_service():
    # 1. Check if llamaDS.service is running. If running, stop it first
    print("Checking llamaDS.service status...", flush=True)
    status_ds = subprocess.run(["sudo", "systemctl", "status", "llamaDS.service"], capture_output=True, text=True)
    if status_ds.returncode == 0:
        print("llamaDS.service is running. Stopping llamaDS.service...", flush=True)
        try:
            subprocess.run(["sudo", "systemctl", "stop", "llamaDS.service"], check=True)
            print("llamaDS.service stopped successfully.", flush=True)
        except subprocess.CalledProcessError as e:
            print(f"Warning/Error stopping llamaDS.service: {e}", file=sys.stderr)

    # 2. Validate if llamaJB.service is running using sudo systemctl status llamaJB.service
    print("Checking llamaJB.service status...", flush=True)
    status_res = subprocess.run(["sudo", "systemctl", "status", "llamaJB.service"], capture_output=True, text=True)
    if status_res.returncode != 0:
        print("llamaJB.service is not running. Starting it...", flush=True)
        try:
            subprocess.run(["sudo", "systemctl", "start", "llamaJB.service"], check=True)
            print("llamaJB.service started. Waiting for initialization...", flush=True)
            time.sleep(5)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Error starting llamaJB.service: {e}")
            
    # 3. Validation alive request. If fail, then restart: sudo systemctl restart llamaJB.service
    if not check_alive():
        print("Llama service alive check failed. Restarting llamaJB.service...", flush=True)
        try:
            subprocess.run(["sudo", "systemctl", "restart", "llamaJB.service"], check=True)
            print("llamaJB.service restarted. Waiting for initialization...", flush=True)
            for i in range(15):
                time.sleep(2)
                if check_alive():
                    print("Llama service is alive and ready.", flush=True)
                    return
            raise RuntimeError("Llama service failed alive check after restart.")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Error restarting llamaJB.service: {e}")
    else:
        print("Llama service is alive and ready.", flush=True)

def check_and_warmup_llama_service_bg():
    global llama_service_loading, llama_service_error
    try:
        ensure_llama_service()
        llama_service_loading = False
    except Exception as e:
        llama_service_error = str(e)
        llama_service_loading = False

def run_git(args, cwd):
    try:
        return subprocess.check_output(['git'] + args, cwd=cwd, text=True).strip()
    except subprocess.CalledProcessError:
        return ""

def get_commit_logs(git_dir, since_datetime_str):
    args = [
        'log',
        f'--since={since_datetime_str}',
        '--pretty=format:Commit: %h%nAuthor: %an%nDate: %ad%nSubject: %s%nBody: %b%n---'
    ]
    return run_git(args, git_dir)

def truncate_prompt_if_needed(prompt, max_tokens=14000):
    max_chars = max_tokens * 4
    if len(prompt) > max_chars:
        return prompt[:max_chars] + "\n\n... [LOGS TRUNCATED DUE TO MODEL LIMITS] ..."
    return prompt

# Set up main window styling colors (Catppuccin Mocha theme)
BG_COLOR = "#1e1e2e"       # Catppuccin Mocha Base
FRAME_BG = "#252538"       # Slightly lighter
TEXT_COLOR = "#cdd6f4"     # Text
DIM_TEXT = "#a6adc8"       # Subtext
ACCENT_COLOR = "#89b4fa"   # Blue
GREEN_COLOR = "#a6e3a1"    # Green
RED_COLOR = "#f38ba8"      # Red
DARK_BLACK = "#11111b"     # Crust

def main():
    global llama_service_loading, llama_service_error
    
    # Start checking/starting model service in background thread
    threading.Thread(target=check_and_warmup_llama_service_bg, daemon=True).start()
    
    # Parse git root path
    git_dir = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()
    if not os.path.isdir(git_dir):
        print(f"Error: {git_dir} is not a directory.")
        sys.exit(1)
        
    toplevel = run_git(['rev-parse', '--show-toplevel'], git_dir)
    if not toplevel:
        print(f"Error: {git_dir} is not a git repository.")
        sys.exit(1)
        
    git_dir = toplevel
    
    # Create main window
    root = tk.Tk()
    root.title("Git Commit Report Generator (Llama)")
    root.geometry("1100x750")
    root.minsize(980, 600)
    root.configure(bg=BG_COLOR)
    
    # Setup themed styles
    style = ttk.Style()
    style.theme_use('default')
    
    style.configure(".", background=BG_COLOR, foreground=TEXT_COLOR)
    style.configure("TFrame", background=BG_COLOR)
    style.configure("Card.TFrame", background=FRAME_BG, relief="flat")
    
    style.configure("TLabel", background=BG_COLOR, foreground=TEXT_COLOR, font=("Helvetica", 11))
    style.configure("Title.TLabel", background=BG_COLOR, foreground=ACCENT_COLOR, font=("Helvetica", 16, "bold"))
    style.configure("Sub.TLabel", background=BG_COLOR, foreground=DIM_TEXT, font=("Helvetica", 10, "italic"))
    style.configure("Header.TLabel", background=FRAME_BG, foreground=TEXT_COLOR, font=("Helvetica", 12, "bold"))
    style.configure("CardLabel.TLabel", background=FRAME_BG, foreground=DIM_TEXT, font=("Helvetica", 9, "bold"))
    
    # Buttons
    style.configure("TButton", 
                    background=FRAME_BG, 
                    foreground=TEXT_COLOR, 
                    font=("Helvetica", 11, "bold"), 
                    borderwidth=0, 
                    focuscolor=ACCENT_COLOR,
                    padding=(10, 5))
    style.map("TButton",
              background=[("active", ACCENT_COLOR), ("disabled", "#313244")],
              foreground=[("active", DARK_BLACK), ("disabled", "#585b70")])
              
    style.configure("Accent.TButton", 
                    background=ACCENT_COLOR, 
                    foreground=DARK_BLACK, 
                    font=("Helvetica", 11, "bold"), 
                    borderwidth=0,
                    padding=(10, 5))
    style.map("Accent.TButton",
              background=[("active", "#b4befe"), ("disabled", "#313244")],
              foreground=[("active", DARK_BLACK), ("disabled", "#585b70")])
 
    style.configure("Success.TButton", 
                    background=GREEN_COLOR, 
                    foreground=DARK_BLACK, 
                    font=("Helvetica", 11, "bold"), 
                    borderwidth=0,
                    padding=(10, 5))
    style.map("Success.TButton",
              background=[("active", GREEN_COLOR)])
 
    # Header Frame
    header_frame = ttk.Frame(root, style="TFrame", padding=15)
    header_frame.pack(fill=tk.X)
    
    title_label = ttk.Label(header_frame, text="Git Commit Report Generator (Llama)", style="Title.TLabel")
    title_label.pack(anchor=tk.W)
    
    path_label = ttk.Label(header_frame, text=f"Repository: {git_dir}", style="Sub.TLabel")
    path_label.pack(anchor=tk.W, pady=(5, 0))
    
    # DateTime Picker Card (Secondary Frame background)
    card_frame = ttk.Frame(root, style="Card.TFrame", padding=15)
    card_frame.pack(fill=tk.X, padx=15, pady=5)
    
    # Left grid for spinbox inputs
    inputs_frame = ttk.Frame(card_frame, style="Card.TFrame")
    inputs_frame.pack(side=tk.LEFT, fill=tk.Y)
    
    # Labels row
    labels = ["Year", "Month", "Day", "Hour", "Minute", "Second"]
    for idx, text in enumerate(labels):
        lbl = ttk.Label(inputs_frame, text=text, style="CardLabel.TLabel")
        lbl.grid(row=0, column=idx, padx=5, pady=(0, 2), sticky=tk.W)
        
    # Spinbox variables initialized to 24 hours ago
    default_init = datetime.now() - timedelta(days=1)
    year_var = tk.StringVar(value=str(default_init.year))
    month_var = tk.StringVar(value=f"{default_init.month:02d}")
    day_var = tk.StringVar(value=f"{default_init.day:02d}")
    hour_var = tk.StringVar(value=f"{default_init.hour:02d}")
    minute_var = tk.StringVar(value=f"{default_init.minute:02d}")
    second_var = tk.StringVar(value=f"{default_init.second:02d}")
    
    # Spinbox styles and creation
    spin_opts = {
        "bg": DARK_BLACK,
        "fg": TEXT_COLOR,
        "buttonbackground": FRAME_BG,
        "selectbackground": ACCENT_COLOR,
        "selectforeground": DARK_BLACK,
        "bd": 1,
        "relief": "flat",
        "insertbackground": TEXT_COLOR,
        "font": ("Helvetica", 11),
        "justify": "center"
    }
    
    year_spin = tk.Spinbox(inputs_frame, from_=2000, to=2100, textvariable=year_var, width=6, **spin_opts)
    month_spin = tk.Spinbox(inputs_frame, values=[f"{i:02d}" for i in range(1, 13)], textvariable=month_var, width=4, **spin_opts)
    day_spin = tk.Spinbox(inputs_frame, values=[f"{i:02d}" for i in range(1, 32)], textvariable=day_var, width=4, **spin_opts)
    hour_spin = tk.Spinbox(inputs_frame, values=[f"{i:02d}" for i in range(0, 24)], textvariable=hour_var, width=4, **spin_opts)
    minute_spin = tk.Spinbox(inputs_frame, values=[f"{i:02d}" for i in range(0, 60)], textvariable=minute_var, width=4, **spin_opts)
    second_spin = tk.Spinbox(inputs_frame, values=[f"{i:02d}" for i in range(0, 60)], textvariable=second_var, width=4, **spin_opts)
    
    year_spin.grid(row=1, column=0, padx=5)
    month_spin.grid(row=1, column=1, padx=5)
    day_spin.grid(row=1, column=2, padx=5)
    hour_spin.grid(row=1, column=3, padx=5)
    minute_spin.grid(row=1, column=4, padx=5)
    second_spin.grid(row=1, column=5, padx=5)
    
    # Right preset buttons frame
    presets_frame = ttk.Frame(card_frame, style="Card.TFrame")
    presets_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(20, 0))
    
    preset_title = ttk.Label(presets_frame, text="Quick Presets", style="CardLabel.TLabel")
    preset_title.pack(anchor=tk.W, pady=(0, 2))
    
    buttons_subframe = ttk.Frame(presets_frame, style="Card.TFrame")
    buttons_subframe.pack(fill=tk.X)
    
    def set_presets(delta_type):
        now = datetime.now()
        if delta_type == "24h":
            target = now - timedelta(days=1)
        elif delta_type == "7d":
            target = now - timedelta(days=7)
        elif delta_type == "today":
            target = now.replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            target = now
            
        year_var.set(str(target.year))
        month_var.set(f"{target.month:02d}")
        day_var.set(f"{target.day:02d}")
        hour_var.set(f"{target.hour:02d}")
        minute_var.set(f"{target.minute:02d}")
        second_var.set(f"{target.second:02d}")

    def set_date_by_revision():
        revision = simpledialog.askstring(
            "Date by Revision", 
            "Enter commit hash, branch name, or relative ref (e.g. HEAD~3):",
            parent=root
        )
        if not revision:
            return
            
        revision = revision.strip()
        if not revision:
            return
            
        date_str = run_git(['log', '-1', '--format=%ci', revision], git_dir)
        if not date_str:
            messagebox.showerror("Error", f"Could not find revision '{revision}' or retrieve its date.", parent=root)
            return
            
        try:
            parts = date_str.split(' ')
            if len(parts) >= 2:
                date_part = parts[0]
                time_part = parts[1]
                
                y, m, d = date_part.split('-')
                hr, mnt, sec = time_part.split(':')
                
                commit_dt = datetime(int(y), int(m), int(d), int(hr), int(mnt), int(sec))
                target_dt = commit_dt + timedelta(minutes=1)
                
                year_var.set(str(target_dt.year))
                month_var.set(f"{target_dt.month:02d}")
                day_var.set(f"{target_dt.day:02d}")
                hour_var.set(f"{target_dt.hour:02d}")
                minute_var.set(f"{target_dt.minute:02d}")
                second_var.set(f"{target_dt.second:02d}")
                
                status_label.config(
                    text=f"Status: Date set to {revision} + 1m ({target_dt.strftime('%Y-%m-%d %H:%M:%S')})",
                    foreground=GREEN_COLOR
                )
            else:
                raise ValueError("Unexpected date format")
        except Exception as e:
            messagebox.showerror("Parsing Error", f"Failed to parse date string '{date_str}':\n{str(e)}", parent=root)
        
    btn_24h = ttk.Button(buttons_subframe, text="Last 24h", command=lambda: set_presets("24h"), width=10)
    btn_24h.pack(side=tk.LEFT, padx=2)
    
    btn_7d = ttk.Button(buttons_subframe, text="Last 7d", command=lambda: set_presets("7d"), width=10)
    btn_7d.pack(side=tk.LEFT, padx=2)
    
    btn_today = ttk.Button(buttons_subframe, text="Today", command=lambda: set_presets("today"), width=10)
    btn_today.pack(side=tk.LEFT, padx=2)
 
    rev_subframe = ttk.Frame(presets_frame, style="Card.TFrame")
    rev_subframe.pack(fill=tk.X, pady=(5, 0))
 
    btn_rev = ttk.Button(rev_subframe, text="📅 Date by Revision Num.", command=set_date_by_revision)
    btn_rev.pack(fill=tk.X, padx=2)
    
    # Action & Status Frame
    action_frame = ttk.Frame(root, style="TFrame", padding=15)
    action_frame.pack(fill=tk.X)
    
    # Text Area Frame
    text_frame = ttk.Frame(root, style="TFrame", padding=(15, 0, 15, 15))
    text_frame.pack(fill=tk.BOTH, expand=True)
    
    report_text = tk.Text(
        text_frame, 
        bg=DARK_BLACK, 
        fg=TEXT_COLOR, 
        insertbackground=TEXT_COLOR,
        selectbackground="#585b70",
        font=("DejaVu Sans Mono", 11),
        padx=15,
        pady=15,
        relief="flat",
        wrap=tk.WORD,
        state=tk.DISABLED
    )
    
    scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=report_text.yview)
    report_text.configure(yscrollcommand=scrollbar.set)
    
    report_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Clipboard Copy
    def copy_to_clipboard():
        content = report_text.get("1.0", tk.END).strip()
        if content:
            root.clipboard_clear()
            root.clipboard_append(content)
            root.update()
            
            copy_btn.config(text="✓ Copied!", style="Success.TButton")
            root.after(2000, lambda: copy_btn.config(text="📋 Copy to Clipboard", style="Accent.TButton"))
            
    # Generation logic thread wrapper
    def start_generation():
        generate_btn.config(state=tk.DISABLED)
        copy_btn.config(state=tk.DISABLED)
        auto_ver_btn.config(state=tk.DISABLED)
        status_label.config(text="Status: Preparing...", foreground=DIM_TEXT)
        report_text.config(state=tk.NORMAL)
        report_text.delete("1.0", tk.END)
        report_text.config(state=tk.DISABLED)
        
        try:
            y = int(year_var.get())
            m = int(month_var.get())
            d = int(day_var.get())
            hr = int(hour_var.get())
            mnt = int(minute_var.get())
            sec = int(second_var.get())
            selected_dt = datetime(y, m, d, hr, mnt, sec)
        except Exception as e:
            messagebox.showerror("Invalid Date/Time", f"Please enter valid date and time values.\nError: {str(e)}")
            generate_btn.config(state=tk.NORMAL)
            auto_ver_btn.config(state=tk.NORMAL)
            return
            
        since_str = selected_dt.strftime("%Y-%m-%d %H:%M:%S")
        
        thread = threading.Thread(target=generate_report_thread, args=(since_str,))
        thread.daemon = True
        thread.start()
        
    def generate_report_thread(since_str):
        global llama_service_loading, llama_service_error
        
        def update_status(text, color=DIM_TEXT):
            root.after(0, lambda: status_label.config(text=f"Status: {text}", foreground=color))
            
        update_status("Extracting git log...")
        logs = get_commit_logs(git_dir, since_str)
        if not logs:
            update_status("No commits found since selected date-time.", RED_COLOR)
            root.after(0, lambda: generate_btn.config(state=tk.NORMAL))
            root.after(0, lambda: auto_ver_btn.config(state=tk.NORMAL))
            return
            
        update_status("Warming up llamaJB.service...")
        while llama_service_loading:
            time.sleep(0.1)
            
        if llama_service_error:
            update_status("Service Load Error", RED_COLOR)
            root.after(0, lambda: messagebox.showerror("Service Load Error", f"Failed to verify llamaJB.service:\n{llama_service_error}"))
            root.after(0, lambda: generate_btn.config(state=tk.NORMAL))
            root.after(0, lambda: auto_ver_btn.config(state=tk.NORMAL))
            return
            
        update_status("Generating report...", ACCENT_COLOR)
        
        # Prepare text area
        root.after(0, lambda: report_text.config(state=tk.NORMAL))
        
        def append_chunk(chunk_text):
            report_text.insert(tk.END, chunk_text)
            report_text.see(tk.END)
            
        try:
            prompt = f"Here are the git commit logs since {since_str}:\n\n{logs}"
            truncated_prompt = truncate_prompt_if_needed(prompt)
            
            url = "http://localhost:9090/v1/chat/completions"
            headers = {
                "Content-Type": "application/json"
            }
            payload = {
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": truncated_prompt}
                ],
                "temperature": 0.4,
                "top_p": 0.95,
                "stream": True
            }
            
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers=headers,
                method="POST"
            )
            
            with urllib.request.urlopen(req) as response:
                for line in response:
                    line = line.decode('utf-8').strip()
                    if not line:
                        continue
                    if line.startswith("data: "):
                        data_str = line[len("data: "):]
                        if data_str == "[DONE]":
                            break
                        try:
                            chunk = json.loads(data_str)
                            choices = chunk.get("choices", [])
                            if choices:
                                delta = choices[0].get("delta", {})
                                content = delta.get("content", "")
                                if content:
                                    root.after(0, append_chunk, content)
                        except json.JSONDecodeError:
                            pass
                            
            root.after(0, append_chunk, "\n\n***AI release commit***\n")
            update_status("Success!", GREEN_COLOR)
            root.after(0, lambda: copy_btn.config(state=tk.NORMAL))
        except urllib.error.HTTPError as e:
            update_status("Generation failed", RED_COLOR)
            try:
                body = e.read().decode("utf-8")
                err_msg = f"{e}\n\nResponse body:\n{body}"
            except Exception:
                err_msg = str(e)
            root.after(0, lambda msg=err_msg: messagebox.showerror("Generation Failed", f"HTTP error during inference:\n{msg}"))
        except Exception as e:
            update_status("Generation failed", RED_COLOR)
            err_msg = str(e)
            root.after(0, lambda msg=err_msg: messagebox.showerror("Generation Failed", f"An error occurred during inference:\n{msg}"))
        finally:
            root.after(0, lambda: report_text.config(state=tk.DISABLED))
            root.after(0, lambda: generate_btn.config(state=tk.NORMAL))
            root.after(0, lambda: auto_ver_btn.config(state=tk.NORMAL))
 
    def set_date_by_auto_version():
        if generate_btn['state'] == tk.DISABLED:
            return
            
        output = run_git(['log', '-1', '--fixed-strings', '--grep=***AI release commit***', '--format=%H %ci'], git_dir)
        if not output:
            messagebox.showwarning("Not Found", "No commit containing '***AI release commit***' was found.", parent=root)
            return
            
        try:
            parts = output.split(' ')
            if len(parts) >= 3:
                commit_hash = parts[0]
                date_part = parts[1]
                time_part = parts[2]
                
                y, m, d = date_part.split('-')
                hr, mnt, sec = time_part.split(':')
                
                commit_dt = datetime(int(y), int(m), int(d), int(hr), int(mnt), int(sec))
                target_dt = commit_dt + timedelta(minutes=1)
                
                year_var.set(str(target_dt.year))
                month_var.set(f"{target_dt.month:02d}")
                day_var.set(f"{target_dt.day:02d}")
                hour_var.set(f"{target_dt.hour:02d}")
                minute_var.set(f"{target_dt.minute:02d}")
                second_var.set(f"{target_dt.second:02d}")
                
                status_label.config(
                    text=f"Status: Auto version {commit_hash[:8]} + 1m ({target_dt.strftime('%Y-%m-%d %H:%M:%S')})",
                    foreground=GREEN_COLOR
                )
                start_generation()
            else:
                raise ValueError("Unexpected date format")
        except Exception as e:
            messagebox.showerror("Parsing Error", f"Failed to parse git log output '{output}':\n{str(e)}", parent=root)

    generate_btn = ttk.Button(action_frame, text="⚡ Generate Report", command=start_generation)
    generate_btn.pack(side=tk.LEFT, padx=(0, 10))
    
    copy_btn = ttk.Button(action_frame, text="📋 Copy to Clipboard", style="Accent.TButton", command=copy_to_clipboard, state=tk.DISABLED)
    copy_btn.pack(side=tk.LEFT)
    
    auto_ver_btn = ttk.Button(action_frame, text="🔄 Auto -Version", command=set_date_by_auto_version)
    auto_ver_btn.pack(side=tk.LEFT, padx=(10, 0))
    
    status_label = ttk.Label(action_frame, text="Status: Ready", font=("Helvetica", 10, "italic"))
    status_label.pack(side=tk.RIGHT, padx=10)
    
    root.mainloop()

if __name__ == "__main__":
    main()
