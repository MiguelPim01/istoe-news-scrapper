import os
import sys
import threading
from datetime import datetime
from time import sleep
from tqdm import tqdm

from selenium import webdriver
from selenium.webdriver.common.by import By

def is_istoe_link(url):
    return "istoe" in url.lower()

def get_texts_from_month(file, istoe_links_dir, news_dir, log_dir, options):
    month_title = file.split(".")[0].split("-")[1]
    with open(os.path.join(istoe_links_dir, file)) as f:
        lines = f.readlines()
    
    _logs = []
    _all_texts = []
    with tqdm(total=len(lines), desc=f"Links {month_title}: ", unit="l") as pb_links:
        for i, link in enumerate(lines):
            if not is_istoe_link(link):
                pb_links.update()
                continue
            driver = webdriver.Chrome(options=options)
            
            try:
                driver.get(link)
            except Exception:
                _logs.append(f"Problema ao ler link {link.strip('\n')}")
            
            sleep(3)
            
            while True:
                try:
                    textos = driver.find_elements(By.TAG_NAME, 'p')
                    break
                except Exception:
                    pass
            
            for t in textos:
                try:
                    _all_texts.append(t.text)
                except Exception:
                    pass

            pb_links.update()
            driver.quit()
        
        with open(os.path.join(news_dir, f"news-{month_title}.txt"), "w") as f, open(os.path.join(log_dir, f"news-log-{month_title}.txt"), "w") as log:
            f.write("\n".join(_all_texts))
            log.write("\n".join(_logs))

def parse_args():
    # --
    # run: python get_news.py start=%m/%Y end=%m/%Y --headless
    # --
    
    args = sys.argv
    
    if len(args) < 3:
        print("ERROR: Invalid number of arguments. Must be: start=%m/%Y end=%m/%Y")
        exit(1)
    
    start = datetime.strptime("01/" + args[1].split("=")[-1], "%d/%m/%Y")
    end = datetime.strptime("01/" + args[2].split("=")[-1], "%d/%m/%Y")
    
    if len(args) == 4 and args[3] == "--headless":
        headless = True
    else:
        headless = False
    
    return start, end, headless

def main():
    start_date, end_date, headless = parse_args()
    
    # --
    # Defining all options for Chrome
    # --
    options = webdriver.ChromeOptions()

    options.add_argument("--no-sandbox")
    options.add_argument("--log-level=3")
    if headless:
        options.add_argument("--headless")

    options.page_load_strategy = "eager"
    
    # --
    # Getting all files
    # --
    istoe_links_dir = os.path.join("data", "istoe-links")
    news_dir = os.path.join("data", "news")
    log_dir = os.path.join("data", "logs")

    os.makedirs(news_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)

    _files_list = os.listdir(istoe_links_dir)
    
    # --
    # Creating threads for each month
    # At this part, we define the maximum number of threads as four
    # --
    threads = []
    _max_threads = 4
    _cur_number_threads = 0
    
    for file in _files_list:
        try:
            if _cur_number_threads == _max_threads:
                raise Exception
            
            t = threading.Thread(target=get_texts_from_month, args=(file, istoe_links_dir, news_dir, log_dir, options))
            t.start()
            threads.append(t)
            sleep(1)
            
            _cur_number_threads += 1
        except Exception:
            for t in threads:
                t.join()
                _cur_number_threads -= 1
            
            threads.clear()
        
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()