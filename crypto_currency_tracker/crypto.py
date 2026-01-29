# core_scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from email_alert import send_email
import time

def scrape_crypto():
    # ---------------- Step 1: Scrape top 10 cryptos ----------------
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://coinmarketcap.com/")

    wait = WebDriverWait(driver, 20)
    table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))
    rows = table.find_elements(By.TAG_NAME, "tr")[:10]

    coins, prices, changes, market_caps = [], [], [], []

    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        coins.append(cols[2].text)
        prices.append(cols[3].text)
        changes.append(cols[4].text)
        market_caps.append(cols[6].text)

    driver.quit()

    # ---------------- Step 2: Clean data ----------------
    def clean_price(p):
        try:
            return float(p.replace("$","").replace(",",""))
        except:
            return 0.0

    def clean_change(c):
        try:
            return float(c.replace("%","").replace(",",""))
        except:
            return 0.0

    def clean_market(m):
        try:
            return float(m.replace("$","").replace(",",""))
        except:
            return 0.0

    df = pd.DataFrame({
        "Coin": coins,
        "Price": [clean_price(p) for p in prices],
        "24h Change": [clean_change(c) for c in changes],
        "Market Cap": [clean_market(m) for m in market_caps],
        "Time": datetime.now()
    })

    # ---------------- Step 3: Save CSV ----------------
    file_name = datetime.now().strftime("crypto_%Y-%m-%d.csv")
    df.to_csv(file_name, index=False)
    print(f"✅ Crypto Prices Saved Successfully! ({file_name})")

    # ---------------- Step 4: Send email alerts for all coins >5% ----------------
    big_gainers = df[df["24h Change"] > 5]
    if not big_gainers.empty:
        for _, row in big_gainers.iterrows():
            send_email(
                subject=f"Crypto Alert 🚀 {row['Coin']} is up!",
                body=f"{row['Coin']} gained {row['24h Change']}% in the last 24 hours!"
            )
        print(f"📧 Sent email alerts for {len(big_gainers)} coin(s).")
    else:
        print("No coin gained more than 5% in last 24h.")

    # ---------------- Step 5: Plot chart ----------------
    plt.figure(figsize=(10,6))

    # Find the top gainer
    top_gainer_idx = df["24h Change"].idxmax()

    # Set colors: top gainer in green, others in blue
    colors = ["green" if i == top_gainer_idx else "blue" for i in range(len(df))]

    # Plot the bar chart
    sns.barplot(x="Coin", y="24h Change", data=df, palette=colors)

    # Customize plot
    plt.title("Top 10 Crypto 24h Change (Highest Gainer in Green)")
    plt.ylabel("24h % Change")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save and close plot
    plt.savefig("crypto_chart.png")
    plt.close()

    # Return the DataFrame from the function
    return df
 

# ---------------- Step 6: Auto-run every hour ----------------
if __name__ == "__main__":
    while True:
        print("⏱ Running crypto scraper...")
        scrape_crypto()
        print("✅ Waiting 1 hour for next run...\n")
        time.sleep(3600)  # 3600 seconds = 1 hour