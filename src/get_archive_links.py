import os
import sys
from datetime import datetime
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By

ARCHIVE_MONTHS = {  "JAN" : 1, "FEB" : 2, "MAR" : 3, "APR" : 4, "MAY" : 5,
                "JUN" : 6, "JUL" : 7, "AUG" : 8, "SEP" : 9, "OCT" : 10, 
                "NOV": 11, "DEC" : 12 }


def parse_args():
    # --
    # run: python get_links_from_archive.py start=%m/%Y end=%m/%Y --headless
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

def get_archive_links(start_date: datetime, end_date: datetime, options):
    driver = webdriver.Chrome(options=options)

    current_year = start_date.year
    months_links = []
    month_checker = lambda date : date >= start_date and date <= end_date

    while current_year <= end_date.year:
        url = f"https://web.archive.org/web/{current_year}0101000000*/www.istoe.com.br"
        driver.get(url)
        
        sleep(3)
        
        while True:
            try:
                all_months = driver.find_elements(By.CLASS_NAME, "month")
                break
            except:
                pass
        
        print("Finding all month in the page...\n")
        for i in range(len(all_months)):
            all_months = driver.find_elements(By.CLASS_NAME, "month")
            month = all_months[i]
            
            x = month.location["x"]
            y = month.location["y"]
            driver.execute_script("window.scrollTo(%s,%s);" % (x, y))
            sleep(1)
            
            while True:
                try:
                    month_title_pt = month.find_element(By.CLASS_NAME, "month-title").text
                    
                    if month_checker(datetime(current_year, ARCHIVE_MONTHS[month_title_pt], 1)) == True:
                        calendar_day_list = month.find_elements(By.CLASS_NAME, "calendar-day")
                        
                        href_list = []
                        for day_number, calendar_day in enumerate(calendar_day_list, start= 1):
                            print(f"month: {month_title_pt}, day : {day_number}")
                            
                            href_list.append(calendar_day.find_element(By.TAG_NAME, "a").get_attribute("href"))
                    
                        months_links.append((month_title_pt, href_list))
                    break
                except:
                    pass
        
        current_year += 1

    driver.quit()
    
    return months_links

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
    # Getting all links from internet archive
    # --
    months_links = get_archive_links(start_date, end_date, options)
    
    # --
    # Saving each set of links into path "data/archive-links/"
    # --
    for month, links in months_links:
        os.makedirs("data", exist_ok=True)
        os.makedirs("data/archive-links", exist_ok=True)
        
        with open(f"data/archive-links/links-{month}.txt", "w") as file:
            file.write("\n".join(links))


if __name__ == "__main__":
    main()