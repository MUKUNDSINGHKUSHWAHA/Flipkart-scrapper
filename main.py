import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from scraper import start_scraping
import os
from tkinter import ttk
import threading

def upload_file():
    path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
    file_path.set(path)
    if path:
        file_name.set(os.path.basename(path))
        status_label.config(text="File selected. Click 'Start' to begin.")
    else:
        file_name.set("")

def start():
    path = file_path.get()
    if not path:
        messagebox.showwarning("No file", "Please select an Excel file.")
        return
    status_label.config(text="Scraping in progress...")
    progress_bar['value'] = 0
    progress_bar.update()
    root.update()
    def progress_callback(completed, total):
        percent = int((completed / total) * 100)
        progress_bar['value'] = percent
        progress_bar.update()
    def run_scraping():
        success_count, failure_count, output_path = start_scraping(path, progress_callback)
        status_label.config(
            text=f"✅ Done! {success_count} succeeded, {failure_count} failed.\nSaved to:\n{output_path}"
        )
        progress_bar['value'] = 100
        progress_bar.update()
    threading.Thread(target=run_scraping).start()

root = tk.Tk()
root.title("Flipkart FSIN Scraper")

file_path = tk.StringVar()
file_name = tk.StringVar()

tk.Label(root, text="Flipkart FSIN Scraper", font=("Arial", 16)).pack(pady=10)
tk.Button(root, text="Upload Excel File", command=upload_file).pack(pady=5)
tk.Label(root, textvariable=file_name, wraplength=400, fg="green").pack(pady=2)
tk.Label(root, textvariable=file_path, wraplength=400).pack(pady=5)
tk.Button(root, text="Start", command=start).pack(pady=10)
status_label = tk.Label(root, text="", wraplength=400, fg="blue")
status_label.pack(pady=10)

progress_bar = ttk.Progressbar(root, orient='horizontal', length=400, mode='determinate')
progress_bar.pack(pady=5)

root.geometry("500x300")
root.mainloop()
