import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

# -----------------------------------
# CONFIG
# -----------------------------------

URL = "https://www.bundeswirtschaftsministerium.de/Redaktion/DE/Veranstaltungen/2026/20260126-nordsee-gipfel-2026-in-hamburg.html"

HEADERS = {
    "User-Agent": "Academic Policy Research Bot (Non-commercial, EU-compliant)"
}

os.makedirs("data", exist_ok=True)

# -----------------------------------
# FETCH PAGE
# -----------------------------------

response = requests.get(URL, headers=HEADERS)
response.raise_for_status()

soup = BeautifulSoup(response.text, "lxml")

# -----------------------------------
# EXTRACT METADATA
# -----------------------------------

# Title
title = soup.find("h1").get_text(strip=True)

# Date
date_tag = soup.select_one(".headline .date")
date = date_tag.get_text(strip=True) if date_tag else ""

# -----------------------------------
# EXTRACT REAL CONTENT (KEY FIX)
# -----------------------------------

content_div = soup.select_one("div.rich-text")

paragraphs = []
if content_div:
    for elem in content_div.find_all(["p", "li"]):
        text = elem.get_text(strip=True)
        if text:
            paragraphs.append(text)

content = "\n\n".join(paragraphs)

# -----------------------------------
# SAVE OUTPUT
# -----------------------------------

df = pd.DataFrame([{
    "date": date,
    "title": title,
    "content": content,
    "url": URL
}])

timestamp = datetime.now().strftime("%Y%m%d")
output_file = f"data/bmwk_event_{timestamp}.csv"

df.to_csv(output_file, index=False, encoding="utf-8-sig")

print(f"Extracted article successfully → {output_file}")
