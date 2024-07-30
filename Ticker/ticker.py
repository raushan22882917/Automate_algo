import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_insider_trades(ticker):
    # Format the URL with the given ticker
    url = f"https://www.marketbeat.com/stocks/LON/{ticker}/insider-trades/"

    # Send a GET request to the URL
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table
    table = soup.find('table', class_='scroll-table sort-table')

    # Check if table exists
    if table is None:
        print("No table found for ticker:", ticker)
        return

    # Extract table headers
    headers = [header.text.strip() for header in table.find_all('th')]

    # Extract table rows
    rows = []
    for row in table.find_all('tr')[1:]:  # Skip the header row
        cols = [col.text.strip() for col in row.find_all('td')]
        rows.append(cols)

    # Create a DataFrame
    df = pd.DataFrame(rows, columns=headers)

    # Save the DataFrame to a CSV file
    filename = f'insider_trades_{ticker}.csv'
    df.to_csv(filename, index=False)

    print(f"Data has been scraped and saved to '{filename}'")

# Example usage
ticker = input("Enter the ticker symbol: ")
scrape_insider_trades(ticker)
