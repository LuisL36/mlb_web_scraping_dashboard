from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time

# Headless Chrome setup
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(options=options)
driver.set_page_load_timeout(10)

# Step 1: Get all year links
base_url = "https://www.baseball-almanac.com/yearmenu.shtml"
driver.get(base_url)
time.sleep(3)

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
    except Exception:
        continue

print(f"✅ Found {len(years)} yearly links to scrape.")

# Step 2: Scrape each year's stat tables
data = []

for i, (year, link) in enumerate(zip(years, links), 1):
    print(f"[{i}/{len(years)}] Scraping year {year} ...", end=" ")
    try:
        driver.get(link)
        driver.implicitly_wait(5)

        # Find all rows in stat tables
        rows = driver.find_elements(By.CSS_SELECTOR, "div.ba-table table.boxed tbody tr")
        if not rows:
            print("No data found.")
            continue

        for r in rows:
            cells = r.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 4:
                stat = cells[0].text.strip()
                player = cells[1].text.strip()
                team = cells[2].text.strip()
                value = cells[3].text.strip()

                # Optional: grab stat link
                try:
                    stat_link = cells[0].find_element(By.TAG_NAME, "a").get_attribute("href")
                except Exception:
                    stat_link = ""

                data.append({
                    "year": year,
                    "stat": stat,
                    "player": player,
                    "team": team,
                    "value": value,
                    "link": stat_link
                })

        print(f"✅ {len(rows)} rows scraped.")
    except TimeoutException:
        print("⏳ Timeout — skipping")
        continue
    except Exception as e:
        print(f"❌ Error: {e}")
        continue

driver.quit()

# Step 3: Save data to CSV
df = pd.DataFrame(data)
df.to_csv("mlb_stat_leaders.csv", index=False)
print(f"📄 Saved {len(df)} stat rows to mlb_stat_leaders.csv")
