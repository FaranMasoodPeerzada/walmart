import requests
from bs4 import BeautifulSoup
import re
import csv

# Function to get page content
def get_page_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Check if request was successful
    return response.text

# Function to find UPC from page content
def find_upc_from_page(page_content):
    upc_pattern = r'"upc":"(\d{12})"'
    upc_codes = re.findall(upc_pattern, page_content)
    return upc_codes[0] if upc_codes else "N/A"

# Function to extract product details
def extract_product_details(url):
    page_content = get_page_content(url)
    soup = BeautifulSoup(page_content, 'html.parser')

    title = soup.find('h1', id='main-title')
    title = title.get_text(strip=True) if title else "N/A"
    print(title)

    upc = find_upc_from_page(page_content)

    price_element = soup.find('span', {'data-testid': 'price-wrap'})
    if price_element:
        price_text = price_element.get_text(strip=True)
        price_digits = re.search(r"\$([\d,.]+)", price_text)
        price_digits = price_digits.group(1) if price_digits else "N/A"
    else:
        price_digits = "N/A"

    description = soup.find('span', {'data-testid': 'product-description'})
    description = description.get_text(strip=True) if description else "N/A"

    return {
        "Title": title,
        "Price": price_digits,
        "UPC": upc,
        "Description": description
    }

# Function to extract product URLs from the main page
def get_product_urls(main_url):
    page_content = get_page_content(main_url)
    soup = BeautifulSoup(page_content, 'html.parser')

    # Example of finding product URLs - update the selector based on actual HTML structure
    product_urls = [a['href'] for a in soup.find_all('a', href=True) if '/product/' in a['href']]
    return product_urls

# Main execution
def main():
    # URL of the page to scrape
    target_url = 'https://www.walmart.com/shop/deals/all-home/floor-care'
    
    # Get product URLs
    product_urls = get_product_urls(target_url)

    # Write header to the CSV file
    csv_file_path = 'product_details.csv'
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Title', 'Price', 'UPC', 'Description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    # Collect all product details and write to CSV
    for url in product_urls:
        full_url = f"https://www.walmart.com{url}"
        details = extract_product_details(full_url)
        
        # Display details in console
        print(details)
        
        # Check if any value is not 'N/A' before writing to CSV
        if not all(value == "N/A" for value in details.values()):
            with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow(details)

    print("Product details have been saved to 'product_details.csv'.")

if __name__ == "__main__":
    main()
