import requests
import feedparser
import sqlite3
from bs4 import BeautifulSoup
from datetime import datetime

RSS_FEED_URL = "https://www.cisa.gov/news.xml"
JSON_API_URL = "https://cve.circl.lu/api/last"
SCRAPE_URL = "https://threatpost.com/category/vulnerabilities/"
DB_NAME = "threat_feeds.db"

conn = sqlite3.connect(DB_NAME)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS threat_data (
                source TEXT,
                title TEXT,
                url TEXT,
                published TEXT,
                timestamp TEXT
            )''')
conn.commit()

def insert_data(source, title, url, published):
    timestamp = datetime.utcnow().isoformat()
    c.execute("INSERT INTO threat_data (source, title, url, published, timestamp) VALUES (?, ?, ?, ?, ?)",
              (source, title, url, published, timestamp))
    conn.commit()

def fetch_rss():
    print("Fetching RSS feed...")
    feed = feedparser.parse(RSS_FEED_URL)
    for entry in feed.entries[:5]:
        published = getattr(entry, 'published', "N/A")
        insert_data("RSS", entry.title, entry.link, published)

def fetch_json():
    print("Fetching JSON API...")
    try:
        response = requests.get(JSON_API_URL)
        response.raise_for_status()
        data = response.json()
        for item in data[:5]:
            title = item.get("id", "CVE")
            url = f"https://cve.mitre.org/cgi-bin/cvename.cgi?name={title}"
            published = item.get("Published", "N/A")
            insert_data("JSON API", title, url, published)
    except Exception as e:
        print("Error fetching JSON API:", e)

def scrape_site():
    print("Scraping website...")
    try:
        response = requests.get(SCRAPE_URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.select("article h2 a")[:5]
        for article in articles:
            insert_data("Scraper", article.text.strip(), article.get('href', 'N/A'), "N/A")
    except Exception as e:
        print("Error scraping site:", e)

fetch_rss()
fetch_json()
scrape_site()

print("Ingestion complete. Data stored in:", DB_NAME)
conn.close()
