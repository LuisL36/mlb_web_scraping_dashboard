from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

# Set up headless Chrome
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

url = "https://www.baseball-almanac.com/yearmenu.shtml"
driver.get(url)
time.sleep(3)

# Scrape all available years and links
years = []
links = []
rows = driver.find_elements(By.XPATH, "//a[contains(@href, 'yearly')]")

for row in rows:
    try:
        year = row.text.strip()
        link = row.get_attribute('href')
        if year.isdigit():
            years.append(year)
            links.append(link)
    except:
        continue

driver.quit()

# Save to CSV
df = pd.DataFrame({'year': years, 'link': links})
df.to_csv("data/mlb_yearly_events.csv", index=False)
print("Saved data/mlb_yearly_events.csv")
