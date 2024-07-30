import csv
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class Countries:
    """CONTAINS COUNTRIES INFOS"""
    # List of countries and URLs
    COUNTRY_URLS = [
        {"NAME": "AUSTRALIA", "URL": "https://www.insiderscreener.com/en/explore/au"},
        {"NAME": "CANADA", "URL": "https://www.insiderscreener.com/en/explore/ca"}
        # Add more countries and URLs here if needed
    ]


def create_webdriver():
    """Sets up and returns a Selenium WebDriver instance."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    return webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()), options=chrome_options
    )


def extract_links(driver, url: str):
    """Extracts all unique links from the given URL.

    Args:
        driver: Selenium WebDriver instance
        url (str): URL of the page to extract links from

    Returns:
        list: List of extracted links
    """
    try:
        driver.get(url)
        driver.implicitly_wait(10)  # Allow time for the page to load

        links = driver.find_elements(By.CSS_SELECTOR, "a")
        return [link.get_attribute("href") for link in links if link.get_attribute("href")]

    except Exception as e:
        print(f"Error extracting links from {url}: {e}")
        return []


def save_links_to_csv(filename, links):
    """Saves the list of links to a CSV file.

    Args:
        filename (str): The path to the CSV file
        links (list): List of links to save
    """
    try:
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Link"])
            writer.writerows([[link] for link in links])
        print(f"Links saved to {filename}")

    except IOError as e:
        print(f"Error saving links to CSV file: {e}")


def main():
    output_dir = "all_links"
    os.makedirs(output_dir, exist_ok=True)

    all_links = []

    with create_webdriver() as driver:
        for country_info in Countries.COUNTRY_URLS:
            print(f"Extracting links for {country_info['NAME']}...")
            links = extract_links(driver, country_info["URL"])
            
            if links:
                all_links.extend(links)
                print(f"Links extracted for {country_info['NAME']}")
            else:
                print(f"No links found for {country_info['NAME']}")

            # To avoid server restrictions
            time.sleep(2)

    # Save all links to a single CSV file
    filename = os.path.join(output_dir, "all_insider_links.csv")
    save_links_to_csv(filename, all_links)


if __name__ == "__main__":
    main()
