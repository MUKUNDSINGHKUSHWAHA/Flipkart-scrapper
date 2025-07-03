import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from threading import Thread
from queue import Queue
from utils import get_headers, clean_text, extract_data
import os

prod_data = []
failed_fsins = Queue()

def fetch_worker(queue, progress_callback=None, completed=None, total=None):
    while not queue.empty():
        fsin = queue.get()
        for attempt in range(2):  # 1 retry
            try:
                url = f"https://www.flipkart.com/-/p/-?pid={fsin}"
                response = requests.get(url, headers=get_headers(), timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    data = extract_data(soup, fsin)
                    if data:
                        prod_data.append(data)
                        break
                else:
                    print(f"HTTP {response.status_code} for {fsin}")
            except Exception as e:
                print(f"Error for {fsin}: {e}")
        else:
            failed_fsins.put(fsin)
        if completed is not None:
            completed[0] += 1
            if progress_callback:
                progress_callback(completed[0], total)
        queue.task_done()

def start_scraping(file_path, progress_callback=None):
    df = pd.read_excel(file_path, header=None)
    fsins = df.iloc[:, 0].dropna().astype(str).tolist()
    total = len(fsins)
    completed = [0]
    q = Queue()
    for fsin in fsins:
        q.put(fsin)

    threads = []
    for _ in range(15):
        t = Thread(target=fetch_worker, args=(q, progress_callback, completed, total))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_dir = "D:/flipkart-scrapper"
    os.makedirs(output_dir, exist_ok=True)
    output_path = f"{output_dir}/flipkart_output_{now}.xlsx"
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        pd.DataFrame(prod_data).to_excel(writer, sheet_name="Success", index=False)
        pd.DataFrame(list(failed_fsins.queue), columns=["fsin"]).to_excel(writer, sheet_name="Failed", index=False)

    return len(prod_data), failed_fsins.qsize(), output_path
