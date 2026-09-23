#!/usr/bin/env python3
"""A small GUI for playing and saving media from supported URLs."""

import shutil
import subprocess
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from urllib.parse import urlparse


APP_DIR = Path(__file__).resolve().parent
DOWNLOAD_DIR = Path.home() / "Videos"


class LinkPlayer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LinkPlayer")
        self.geometry("620x440")
        self.minsize(520, 390)
        self.configure(bg="#101319")
        self.process = None

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background="#101319")
        style.configure("TLabel", background="#101319", foreground="#e8edf5", font=("Sans", 10))
        style.configure("Title.TLabel", font=("Sans", 22, "bold"), foreground="#ffffff")
        style.configure("Muted.TLabel", foreground="#9aa7b7")
        style.configure("TButton", padding=(13, 9), font=("Sans", 10, "bold"))
        style.configure("Accent.TButton", background="#69d4bb", foreground="#101319")
        style.map("Accent.TButton", background=[("active", "#84e2cc")])
        style.configure("TEntry", fieldbackground="#1b222c", foreground="#ffffff", padding=10)
        style.configure("TCombobox", fieldbackground="#1b222c", foreground="#ffffff", padding=7)

        root = ttk.Frame(self, padding=28)
        root.pack(fill="both", expand=True)
        ttk.Label(root, text="LINKPLAYER", style="Title.TLabel").pack(anchor="w")
        ttk.Label(root, text="Play a link or save a video for later.", style="Muted.TLabel").pack(anchor="w", pady=(3, 24))

        ttk.Label(root, text="VIDEO LINK").pack(anchor="w", pady=(0, 7))
        url_row = ttk.Frame(root)
        url_row.pack(fill="x")
        self.url = tk.StringVar()
        self.url_entry = ttk.Entry(url_row, textvariable=self.url)
        self.url_entry.pack(side="left", fill="x", expand=True)
        ttk.Button(url_row, text="Paste", command=self.paste).pack(side="left", padx=(8, 0))

        options = ttk.Frame(root)
        options.pack(fill="x", pady=(20, 16))
        ttk.Label(options, text="Quality").pack(side="left")
        self.quality = tk.StringVar(value="Best available")
        ttk.Combobox(options, textvariable=self.quality, values=("Best available", "Up to 1080p", "Up to 720p"), state="readonly", width=17).pack(side="left", padx=(10, 26))
        ttk.Label(options, text="Save to").pack(side="left")
        self.folder = tk.StringVar(value=str(DOWNLOAD_DIR))
        ttk.Button(options, text="Choose folder", command=self.choose_folder).pack(side="left", padx=10)

        buttons = ttk.Frame(root)
        buttons.pack(fill="x", pady=(2, 20))
        ttk.Button(buttons, text="▶  Play link", style="Accent.TButton", command=self.play).pack(side="left")
        self.download_button = ttk.Button(buttons, text="↓  Download", command=self.download)
        self.download_button.pack(side="left", padx=10)

        ttk.Separator(root).pack(fill="x", pady=(2, 16))
        ttk.Label(root, text="ACTIVITY").pack(anchor="w", pady=(0, 7))
        self.status = tk.StringVar(value="Ready. Paste a video link to get started.")
        ttk.Label(root, textvariable=self.status, style="Muted.TLabel", wraplength=550).pack(anchor="w")
        self.progress = ttk.Progressbar(root, mode="indeterminate")
        self.progress.pack(fill="x", pady=(12, 0))
        ttk.Label(root, text="Works with public links supported by yt-dlp. DRM protected streams cannot be downloaded.", style="Muted.TLabel", wraplength=550).pack(anchor="w", side="bottom", pady=(22, 0))

    def paste(self):
        try:
            self.url.set(self.clipboard_get().strip())
        except tk.TclError:
            self.status.set("Clipboard is empty.")

    def choose_folder(self):
        chosen = filedialog.askdirectory(initialdir=self.folder.get())
        if chosen:
            self.folder.set(chosen)

    def get_url(self):
        value = self.url.get().strip()
        parsed = urlparse(value)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            messagebox.showerror("Invalid link", "Paste a complete http:// or https:// video link.")
            return None
        return value

    def dependency(self, name):
        if shutil.which(name):
            return True
        messagebox.showerror("Missing program", f"{name} is not installed. On Arch Linux, install it with:\n\nsudo pacman -S {name}")
        return False

    def play(self):
        url = self.get_url()
        if not url:
            return
        if not self.dependency("mpv"):
            return
        if not self.dependency("yt-dlp"):
            return
        try:
            subprocess.Popen(["mpv", "--ytdl-format=" + self.format_spec(), url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
            self.status.set("Opened in mpv. Playback quality depends on the source and your connection.")
        except OSError as exc:
            messagebox.showerror("Could not start playback", str(exc))

    def format_spec(self):
        quality = self.quality.get()
        if quality == "Up to 1080p":
            return "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best"
        if quality == "Up to 720p":
            return "bestvideo[height<=720]+bestaudio/best[height<=720]/best"
        return "bestvideo+bestaudio/best"

    def download(self):
        url = self.get_url()
        if not url:
            return
        if not self.dependency("yt-dlp"):
            return
        if not self.dependency("ffmpeg"):
            return
        target = Path(self.folder.get()).expanduser()
        try:
            target.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            messagebox.showerror("Folder error", str(exc))
            return
        self.download_button.configure(state="disabled")
        self.progress.start(12)
        self.status.set("Starting download…")
        threading.Thread(target=self.run_download, args=(url, target), daemon=True).start()

    def run_download(self, url, target):
        command = ["yt-dlp", "--newline", "--progress", "-f", self.format_spec(), "--merge-output-format", "mkv", "-o", str(target / "%(title)s.%(ext)s"), url]
        try:
            self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
            last_line = ""
            for line in self.process.stdout:
                line = line.strip()
                if line:
                    last_line = line
                    self.after(0, self.status.set, line[:105])
            code = self.process.wait()
            result = (code, last_line)
        except OSError as exc:
            result = (1, str(exc))
        self.after(0, self.finish_download, *result)

    def finish_download(self, code, detail):
        self.progress.stop()
        self.download_button.configure(state="normal")
        if code == 0:
            self.status.set("Download complete. " + detail[:90])
        else:
            self.status.set("Download failed. " + detail[:130])
            messagebox.showerror("Download failed", detail or "yt-dlp returned an error. Check that the link is supported and accessible.")


if __name__ == "__main__":
    LinkPlayer().mainloop()
