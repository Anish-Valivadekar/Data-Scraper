import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import os


# Function to get the page content
def get_page_content(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for 4xx and 5xx status codes
        return response.content
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error: {e}")
    except requests.exceptions.Timeout as e:
        print(f"Timeout Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"General Error: {e}")
    return None


# Function to parse data from a page
def parse_data(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    business_data = []

    # Parsing book details (or business details for a custom scraper)
    books = soup.find_all('article', class_='product_pod')
    for book in books:
        title = book.h3.a['title']
        price = book.find('p', class_='price_color').text.strip()
        availability = book.find('p', class_='instock availability').text.strip()

        business_data.append({
            'Title': title,
            'Price': price,
            'Availability': availability
        })
    return business_data


# Function to clean and process scraped data
def clean_data(data):
    df = pd.DataFrame(data)

    # Clean data: strip whitespace, remove duplicates, handle missing values
    df['Title'] = df['Title'].apply(lambda x: x.strip())
    df.fillna('Unknown', inplace=True)
    df.drop_duplicates(inplace=True)

    return df


# Function to save the cleaned data to a CSV file
def save_data(dataframe, filename="scraped_data.csv"):
    # Use a safe directory for saving
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_path = os.path.join(output_dir, filename)

    try:
        dataframe.to_csv(file_path, index=False)
        print(f"Data saved to {file_path}")
    except PermissionError:
        print(f"Permission denied: Unable to save to {file_path}. Check file permissions.")
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")


# Main function to run the scraper
def main():
    base_url = "http://books.toscrape.com/catalogue/page-{}.html"
    all_data = []

    for page in range(1, 6):  # Adjust the range for more pages
        print(f"Scraping page {page}...")
        url = base_url.format(page)
        page_content = get_page_content(url)

        if page_content:
            data = parse_data(page_content)
            all_data.extend(data)
            time.sleep(random.uniform(1, 3))  # Add random delay to avoid server blocking
        else:
            print(f"Failed to scrape page {page}.")

    if all_data:
        print("Cleaning and processing data...")
        cleaned_data = clean_data(all_data)
        save_data(cleaned_data)
    else:
        print("No data collected. Please check the scraper.")


if __name__ == "__main__":
    main()
