# 📦 Flipkart FSIN Scraper

This tool extracts product details from Flipkart using a list of FSINs stored in an Excel file. It features a simple GUI to upload your file, click Start, and get results in a new Excel file.

---

## ✨ Features

- ✅ Input via Excel file (no header required)
- ✅ Multithreaded scraping (15 threads)
- ✅ Automatically retries once if FSIN fails
- ✅ Extracts:
  - Title
  - Brand
  - Category
  - Price
  - Delivery Info
  - Seller Name
  - Rating
  - Review Count
- ✅ Simple GUI interface
- ✅ Excel output with `Success` and `Failed` FSINs

---

## 🧰 Requirements

- Windows, Mac, or Linux
- Python 3.8 or newer
- VS Code (optional)

---

## 🛠️ Setup Instructions

### Step 1: Install Python

📥 Download Python:  
https://www.python.org/downloads/

✅ During install, **check**: “Add Python to PATH”

Verify installation:

```
python --version
```
You should see something like:

```
Python 3.11.7
```

Download Visual Studio Code from:- https://code.visualstudio.com/

Open VS Code -> Go to File → Open Folder... and select the extracted folder (flipkart_scraper)

Open a terminal in VS Code:(shortcut below)
```
Ctrl + `
```
In the terminal, run(Only one time)
```
pip install -r requirements.txt
```
Run the GUI app:
```
python main.py
```
---

# 📤 Output File
File Stored in D Drive / Flipkart-Scapper Folder
It will contain:
  - Success sheet: products that worked
  - Failed sheet: FSINs that failed after retry


