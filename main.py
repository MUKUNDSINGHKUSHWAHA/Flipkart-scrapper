import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import threading
from tkinterdnd2 import TkinterDnD, DND_FILES  # For drag and drop functionality
from scraper import start_scraping

class FlipkartScraperApp:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        
    def setup_ui(self):
        # Color scheme
        self.BG_COLOR = "#F4F4F9"
        self.FRAME_BG = "#F4F4F9"
        self.FRAME_BORDER = "#BDC3C7"
        self.HEADER_BG = "#34495E"
        self.HEADER_FG = "#ECF0F1"
        self.BUTTON_BG = "#2980B9"  # Primary blue
        self.BUTTON_FG = "#FFFFFF"
        self.BUTTON_BORDER = "#1C5980"
        self.BUTTON_HOVER = "#2471A3"  # Darker blue
        self.ACCENT_COLOR = "#3498DB"  # Lighter blue for start button
        self.ACCENT_HOVER = "#2874A6"  # Darker blue for hover
        self.STATUS_FG = "#2C3E50"
        self.FOOTER_BG = "#D6DBDF"
        self.FONT_FAMILY = "Calibri"
        self.SUCCESS_COLOR = "#2980B9"
        
        # Configure root window
        self.root.title("Flipkart FSIN Scraper")
        self.root.geometry("600x550")
        self.root.configure(bg=self.BG_COLOR)
        self.root.resizable(False, False)
        
        # Header Frame
        header_frame = tk.Frame(self.root, bg=self.HEADER_BG, height=80)
        header_frame.pack(fill=tk.X)
        
        tk.Label(
            header_frame,
            text="Flipkart FSIN Scraper",
            font=(self.FONT_FAMILY, 20, "bold"),
            bg=self.HEADER_BG,
            fg=self.HEADER_FG
        ).pack(pady=20)
        
        # Main Content Frame
        main_frame = tk.Frame(self.root, bg=self.FRAME_BG, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # File Selection Section - Now with drag and drop
        file_frame = tk.LabelFrame(
            main_frame,
            text=" File Selection ",
            font=(self.FONT_FAMILY, 12),
            bg=self.FRAME_BG,
            fg=self.STATUS_FG,
            bd=2,
            relief=tk.GROOVE
        )
        file_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Configure drag and drop
        file_frame.drop_target_register(DND_FILES)
        file_frame.dnd_bind('<<Drop>>', self.on_drop)
        file_frame.dnd_bind('<<DragEnter>>', lambda e: self.on_drag_enter(e, file_frame))
        file_frame.dnd_bind('<<DragLeave>>', lambda e: self.on_drag_leave(e, file_frame))
        
        # File path variables
        self.file_path = tk.StringVar()
        self.file_name = tk.StringVar()
        
        # Upload Button
        upload_btn = tk.Button(
            file_frame,
            text="📁 Upload Excel File",
            command=self.upload_file,
            bg=self.BUTTON_BG,
            fg=self.BUTTON_FG,
            font=(self.FONT_FAMILY, 11, "bold"),
            bd=1,
            relief=tk.RAISED,
            padx=15,
            pady=5,
            activebackground=self.BUTTON_HOVER,
            activeforeground=self.BUTTON_FG
        )
        upload_btn.pack(pady=10)
        
        # Drag and drop hint
        tk.Label(
            file_frame,
            text="--- or drag & drop Excel file here ---",
            fg="#7F8C8D",
            bg=self.FRAME_BG,
            font=(self.FONT_FAMILY, 9, "italic")
        ).pack(pady=(0, 10))
        
        # File info display
        self.file_info_label = tk.Label(
            file_frame,
            textvariable=self.file_name,
            wraplength=500,
            fg=self.SUCCESS_COLOR,
            bg=self.FRAME_BG,
            font=(self.FONT_FAMILY, 10)
        )
        self.file_info_label.pack(pady=(0, 5))
        
        tk.Label(
            file_frame,
            textvariable=self.file_path,
            wraplength=500,
            fg="#7F8C8D",
            bg=self.FRAME_BG,
            font=(self.FONT_FAMILY, 8)
        ).pack()
        
        # Start Button
        start_btn = tk.Button(
            main_frame,
            text="🚀 Start Scraping",
            command=self.start,
            bg=self.ACCENT_COLOR,
            fg=self.BUTTON_FG,
            font=(self.FONT_FAMILY, 12, "bold"),
            bd=1,
            relief=tk.RAISED,
            padx=20,
            pady=8,
            activebackground="#2ECC71",
            activeforeground=self.BUTTON_FG
        )
        start_btn.pack(pady=15)
        
        # Progress Bar
        self.progress_bar = ttk.Progressbar(
            main_frame,
            orient='horizontal',
            length=500,
            mode='determinate'
        )
        self.progress_bar.pack(pady=(10, 5))
        
        # Status Label
        self.status_label = tk.Label(
            main_frame,
            text="Ready to start. Please upload an Excel file.",
            wraplength=500,
            fg=self.STATUS_FG,
            bg=self.FRAME_BG,
            font=(self.FONT_FAMILY, 10)
        )
        self.status_label.pack(pady=10)
        
        # Footer
        footer_frame = tk.Frame(self.root, bg=self.FOOTER_BG, height=60)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Copyright text
        # tk.Label(
        #     footer_frame,
        #     text="Flipkart FSIN Scraper © 2023",
        #     bg=self.FOOTER_BG,
        #     fg=self.STATUS_FG,
        #     font=(self.FONT_FAMILY, 9)
        # ).pack(pady=(5, 0))
        
        # Attribution text
        tk.Label(
            footer_frame,
            text="Developed by Mukund Singh   |   For internal use at 1DS   |   Created: July 2025",
            bg=self.FOOTER_BG,
            fg=self.STATUS_FG,
            font=(self.FONT_FAMILY, 8)
        ).pack()
        
        # tk.Label(
        #     footer_frame,
        #     text="For internal use at 1DS",
        #     bg=self.FOOTER_BG,
        #     fg=self.STATUS_FG,
        #     font=(self.FONT_FAMILY, 8)
        # ).pack()
        
        # tk.Label(
        #     footer_frame,
        #     text="Created: July 2025",
        #     bg=self.FOOTER_BG,
        #     fg=self.STATUS_FG,
        #     font=(self.FONT_FAMILY, 8)
        # ).pack(pady=(0, 5))
        
        # Add hover effects
        upload_btn.bind("<Enter>", lambda e: upload_btn.config(bg=self.BUTTON_HOVER))
        upload_btn.bind("<Leave>", lambda e: upload_btn.config(bg=self.BUTTON_BG))
        
        start_btn.bind("<Enter>", lambda e: start_btn.config(bg="#2ECC71"))
        start_btn.bind("<Leave>", lambda e: start_btn.config(bg="#27AE60"))
    
    def on_drag_enter(self, event, widget):
        widget.config(bg=self.DROP_HIGHLIGHT)
        self.file_info_label.config(text="Drop Excel file here...", fg=self.BUTTON_BG)
    
    def on_drag_leave(self, event, widget):
        widget.config(bg=self.FRAME_BG)
        if not self.file_path.get():
            self.file_info_label.config(text="", fg="green")
    
    def on_drop(self, event):
        # Get the dropped file path
        path = event.data.strip()
        
        # Remove curly braces if present (Windows adds them)
        if path.startswith('{') and path.endswith('}'):
            path = path[1:-1]
        
        # Check if file has correct extension
        if not path.lower().endswith('.xlsx'):
            messagebox.showwarning("Invalid File", "Please drop an Excel file (.xlsx)")
            return
        
        self.process_file(path)
    
    def upload_file(self):
        path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if path:
            self.process_file(path)
    
    def process_file(self, path):
        self.file_path.set(path)
        self.file_name.set(f"Selected: {os.path.basename(path)}")
        self.status_label.config(text="File selected. Click 'Start Scraping' to begin.", fg="green")
    
    def start(self):
        path = self.file_path.get()
        if not path:
            messagebox.showwarning("No file", "Please select an Excel file.")
            return
        
        self.status_label.config(text="Scraping in progress... Please wait.", fg=self.BUTTON_BG)
        self.progress_bar['value'] = 0
        
        def progress_callback(completed, total):
            percent = int((completed / total) * 100)
            self.progress_bar['value'] = percent
            self.progress_bar.update()
        
        def run_scraping():
            try:
                success_count, failure_count, output_path = start_scraping(path, progress_callback)
                self.status_label.config(
                    text=f"✅ Scraping completed!\nSuccess: {success_count} | Failed: {failure_count}\nOutput saved to:\n{output_path}",
                    fg=self.SUCCESS_COLOR
                )
                self.progress_bar['value'] = 100
            except Exception as e:
                self.status_label.config(
                    text=f"❌ Error occurred: {str(e)}",
                    fg="red"
                )
                self.progress_bar['value'] = 0
        
        threading.Thread(target=run_scraping, daemon=True).start()

if __name__ == "__main__":
    root = TkinterDnD.Tk()  # Use TkinterDnD's Tk instead of tkinter's
    app = FlipkartScraperApp(root)
    root.mainloop()
