from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Chrome options
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

# ChromeDriver service (same folder)
service = Service("chromedriver.exe")

# Start browser
driver = webdriver.Chrome(service=service, options=options)

# Open IMDb Top 250 page
driver.get("https://www.imdb.com/chart/top/")
time.sleep(8)  # page fully load aaganum

# Get all movie list items
movies = driver.find_elements(By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item")

data = []

for i, movie in enumerate(movies, start=1):
    try:
        title = movie.find_element(By.CSS_SELECTOR, "h3").text
        rating = movie.find_element(By.CSS_SELECTOR, "span.ipc-rating-star").text.split()[0]

        data.append({
            "Rank": i,
            "Title": title,
            "Rating": rating
        })
    except:
        continue

# Save to CSV
df = pd.DataFrame(data)
df.to_csv("imdb_top_250.csv", index=False)

# Close browser
driver.quit()

print("SCRAPING DONE – CSV CREATED")
