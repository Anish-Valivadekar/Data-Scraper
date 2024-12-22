# Data-Scraper

Overview

This is a Python web scraper designed to extract data from multiple websites with paginated content. It uses requests and BeautifulSoup to fetch and parse data and saves the results as a CSV file.


Features

- Scrapes data from multiple websites.
- Handles paginated content.
- Saves cleaned data in CSV format.
- Includes error handling for failed requests.


Requirements

- Python 3.7 or above


Python libraries:

- requests
- beautifulsoup4
- pandas


Example Output

Sample data from books.toscrape.com:

| Source |         Title        |   Price  | Availability |
|--------|----------------------|----------|--------------|
| Books  | A Light in the Attic | £51.77   | In stock      |
| Books  | Tipping the Velvet   | £53.74   | In stock      |


Notes

- Always check the website’s terms of service before scraping.
- Modify the parse_data function to fit the structure of different websites.
- Start with a small test to ensure the scraper works as expected.





