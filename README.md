# HQ OddsPortal Scraper

A custom Python-based headless scraping solution for extracting betting odds from OddsPortal.com. 

## Features
- Supports NBA, WNBA, MLB, NHL, NFL, College Football, and Tier 1/2 Soccer
- Extracts: Moneyline, Draw No Bet, Double Chance, Spreads
- Filters matches starting in next 24 hours
- Handles dynamic JavaScript content
- Stealth mode: proxy rotation, fake headers, randomized delays
- Exports to both CSV and JSON

## Tech Stack
- Python 3.10+
- Playwright
- pandas
- httpx
- cron (optional for Mac automation)

## Run Instructions
```bash
bash run.sh
