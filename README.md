# pipeline

# Feed Ingestion Pipeline

This project is a Python-based threat intelligence pipeline that collects and stores data from:

- CISA RSS feed
- CVE JSON API
- ThreatPost web scraping

## 🔧 Features
- Fetches top 5 entries from each source
- Stores data in SQLite database: `threat_feeds.db`
- Saves source, title, link, published date, and timestamp

## 💻 How to Run

1. Make sure Python is installed.
2. Install required libraries:
3. Run the script:
4. Open `threat_feeds.db` using DB Browser for SQLite to view the data.

## 📂 Output
The collected data is saved in an SQLite database with a table `threat_data`.

## ✅ Done By
Unnati Panchal & Team, Group 7 - Autonomous Threat Intelligence Aggregator (Capstone Project)
