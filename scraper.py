import requests
import time
import json
import pandas as pd
from bs4 import BeautifulSoup

url = "http://quotes.toscrape.com/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

data = []

try:
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    quotes_divs = soup.find_all("div", class_="quote")

    for q in quotes_divs:
        text = q.find("span", class_="text").get_text(strip=True)
        author = q.find("small", class_="author").get_text(strip=True)

        data.append({
            "Quote": text,
            "Author": author
        })

        time.sleep(1)

    df = pd.DataFrame(data)
    df.to_csv("output.csv", index=False, encoding="utf-8")

    summary = {
        "total_quotes": len(data),
        "unique_authors": len(set(item["Author"] for item in data)),
        "source": url,
        "status": "Success"
    }

    with open("summary_report.json", "w") as f:
        json.dump(summary, f, indent=4)

    print("Scraping completed successfully!")
    print(summary)

except requests.exceptions.RequestException as e:
    print("Error:", e)
