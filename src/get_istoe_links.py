import os
import sys
from datetime import datetime
from time import sleep
from tqdm import tqdm

from selenium import webdriver
from selenium.webdriver.common.by import By

ARCHIVE_MONTHS = {  "JAN" : 1, "FEB" : 2, "MAR" : 3, "APR" : 4, "MAY" : 5,
                "JUN" : 6, "JUL" : 7, "AUG" : 8, "SEP" : 9, "OCT" : 10, 
                "NOV": 11, "DEC" : 12 }

def parse_args():
    # --
    # run: python get_istoe_links.py start=%m/%Y end=%m/%Y --headless
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

def get_month_year_from_file_name(file):
    splited_file = file.split('-')
    
    desc = splited_file[0]
    month = splited_file[1]
    year = int(splited_file[2].split('.')[0])
    
    return desc, month, year

def get_files_in_time_range(directory, start_date: datetime, end_date: datetime):
    files = os.listdir(directory)
    _files_in_time_range = []
    
    for file in files:
        _, month, year = get_month_year_from_file_name(file)
        _file_date = datetime(day=1, month=ARCHIVE_MONTHS[month], year=year)
        
        if start_date <= _file_date <= end_date:
            _files_in_time_range.append(file)
    
    return _files_in_time_range

def get_and_save_istoe_links(start_date: datetime, end_date: datetime, options):
    path_to_archive_links = os.path.join("data", "archive-links")
    istoe_links_dir = os.path.join("data", "istoe-links")
    log_dir = os.path.join("data", "logs")
    
    _files_list = get_files_in_time_range(path_to_archive_links, start_date, end_date)
    os.makedirs(istoe_links_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)
    
    for file in _files_list:
        month_title = file.split(".")[0].split("-")[1]
        year = file.split(".")[0].split("-")[2]
        with open(os.path.join(path_to_archive_links, file)) as f:
            lines = f.readlines()
        
        __all_months_links = []
        _logs = []
        with tqdm(total=len(lines), desc=f"Links {month_title}: ", unit="l") as pb_links:
            for i, link in enumerate(lines):
                driver = webdriver.Chrome(options=options)
                
                try:
                    driver.get(link)
                except Exception:
                    _logs.append(f"Problema ao ler link {link.strip('\n')}")
                
                sleep(3)
                
                while True:
                    try:
                        noticias = driver.find_elements(By.TAG_NAME, 'article')
                        break
                    except:
                        pass
                
                
                for noticia in noticias:
                    try:
                        __all_months_links.append(noticia.find_element(By.TAG_NAME, "a").get_attribute("href"))
                    except Exception:
                        pass
                
                pb_links.update()
                
                driver.quit()

        with open(os.path.join(istoe_links_dir, file), "w") as f, open(os.path.join(log_dir, f"istoe-links-log-{month_title}-{year}.txt"), "w") as log:
            f.write("\n".join(__all_months_links))
            log.write("\n".join(_logs))

def main():
    start_date, end_date, headless = parse_args()
    
    # --
    # Defining all options for Chrome
    # --
    options = webdriver.ChromeOptions()

    options.add_argument("--no-sandbox")
    options.add_argument("--log-level=3")
    options.add_argument("--start-maximized")
    if headless:
        options.add_argument("--headless")

    options.page_load_strategy = "normal"
    
    # --
    # Getting all links to istoe pages and saving them
    # --
    get_and_save_istoe_links(start_date, end_date, options)


if __name__ == "__main__":
    main()