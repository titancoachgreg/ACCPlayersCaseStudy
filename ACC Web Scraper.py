import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd

# initiate the chromedriver path
driver_path = r'C:\Users\nateb\OneDrive\Documents\chromedriver-win64\chromedriver.exe'
url = 'https://hokiesports.com/sports/baseball/roster/season/2024?view=table'

chrome_options = Options()

service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# search url for table elements
try:
    driver.get(url)
    table = driver.find_element(By.CSS_SELECTOR, "table")
    rows = table.find_elements(By.CSS_SELECTOR, 'tr')
    table_data = []
    for row in rows:
        columns = row.find_elements(By.TAG_NAME, "td")
        row_data = [column.text for column in columns]
        if row_data:
            table_data.append(row_data)

    # convert the table to a pandas data frame and save to csv
    data_frame = pd.DataFrame(table_data)
    csv_file_name = 'VTech_baseball_roster_2024.csv'
    data_frame.to_csv(csv_file_name, index = False)

    print(data_frame)
    os.startfile(csv_file_name)

finally:
    driver.quit()
