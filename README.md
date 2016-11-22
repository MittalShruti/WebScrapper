# WebScrapper

Scrape products from ebay using Selenium


## Run this once before running the main script
import pandas as pd
start = pd.DataFrame()
start.to_csv('auction.csv')
value = pd.DataFrame()
value = value.append({'c':0}, ignore_index=True).astype(int)
value.to_csv('a.csv', index=False)

