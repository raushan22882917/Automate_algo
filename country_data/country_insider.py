import csv
import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class Countries:
    """CONTAINS COUNTRIES INFOS"""

    AU = {"NAME": "AUSTRALIA", "URL": "https://www.insiderscreener.com/en/explore/au"}
    CA = {"NAME": "CANADA", "URL": "https://www.insiderscreener.com/en/explore/ca"}
    GE = {"NAME": "GERMAN", "URL": "https://www.insiderscreener.com/en/explore/de"}


def scrape_table(driver, url: str):
    """Function to extract necessary table's headers and rows

    Args:
        driver: Selenium WebDriver instance
        url (str): link of the page

    Returns:
        tuple(list): containing headers at 0th index and rows at 1st
    """
    driver.get(url)
    time.sleep(3)  # Allow time for the page to load

    table = driver.find_element(By.CSS_SELECTOR, "div.table-responsive-md table")

    if table:
        headers = [
            th.text.strip() for th in table.find_elements(By.CSS_SELECTOR, "thead th")
        ]
        rows = []
        for row in table.find_elements(By.CSS_SELECTOR, "tbody tr"):
            cells = [td.text.strip() for td in row.find_elements(By.TAG_NAME, "td")]
            rows.append(cells)
        return headers, rows
    else:
        print(f"Table not found for URL: {url}")
        return None, None


def save_to_csv(filename, headers, rows):
    """Function to save data to a CSV file

    Args:
        filename (str): the name of the CSV file
        headers (list): the table headers
        rows (list): the table rows
    """
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(rows)


def print_as_json(headers, rows):
    """Function to print data in JSON format

    Args:
        headers (list): the table headers
        rows (list): the table rows
    """
    data = [dict(zip(headers, row)) for row in rows]
    print(json.dumps(data, indent=4))


def main():
    # Set up Selenium WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()), options=chrome_options
    )

    output_dir = "country_data"
    os.makedirs(output_dir, exist_ok=True)

    for country_code, country_info in vars(Countries).items():
        if (
            isinstance(country_info, dict)
            and "NAME" in country_info
            and "URL" in country_info
        ):
            print(f"Scraping data for {country_info['NAME']}...")
            headers, rows = scrape_table(driver, country_info["URL"])

            if headers and rows:
                filename = os.path.join(
                    output_dir, f"{country_info['NAME'].lower()}_insider_data.csv"
                )
                save_to_csv(filename, headers, rows)
                print(f"Data saved to {filename}")

                # Print data in JSON format
                print_as_json(headers, rows)
            else:
                print(f"No data found for {country_info['NAME']}")

            # to avoid server restrictions
            time.sleep(2)

    driver.quit()
    print("Data extraction complete.")


if __name__ == "__main__":
    main()
