import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_insider_trades(ticker):
    url = f"https://www.marketbeat.com/stocks/LON/{ticker}/insider-trades/"

    response = requests.get(url)
    response.raise_for_status() 

    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table', class_='scroll-table sort-table')

    if table is None:
        print("No table found for ticker:", ticker)
        return

    headers = [header.text.strip() for header in table.find_all('th')]

    rows = []
    for row in table.find_all('tr')[1:]: 
        cols = [col.text.strip() for col in row.find_all('td')]
        rows.append(cols)

    df = pd.DataFrame(rows, columns=headers)

    filename = f'insider_trades_{ticker}.csv'
    df.to_csv(filename, index=False)

    print(f"Data has been scraped and saved to '{filename}'")

ticker = input("Enter the ticker symbol: ")
scrape_insider_trades(ticker)
