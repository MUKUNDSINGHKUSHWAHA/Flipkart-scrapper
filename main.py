import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from scraper import start_scraping

def upload_file():
    file_path.set(filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")]))
    status_label.config(text="File selected. Click 'Start' to begin.")

def start():
    path = file_path.get()
    if not path:
        messagebox.showwarning("No file", "Please select an Excel file.")
        return
    status_label.config(text="Scraping in progress...")
    root.update()
    success_count, failure_count, output_path = start_scraping(path)
    status_label.config(
        text=f"✅ Done! {success_count} succeeded, {failure_count} failed.\nSaved to:\n{output_path}"
    )

root = tk.Tk()
root.title("Flipkart FSIN Scraper")

file_path = tk.StringVar()

tk.Label(root, text="Flipkart FSIN Scraper", font=("Arial", 16)).pack(pady=10)
tk.Button(root, text="Upload Excel File", command=upload_file).pack(pady=5)
tk.Label(root, textvariable=file_path, wraplength=400).pack(pady=5)
tk.Button(root, text="Start", command=start).pack(pady=10)
status_label = tk.Label(root, text="", wraplength=400, fg="blue")
status_label.pack(pady=10)

root.geometry("500x300")
root.mainloop()