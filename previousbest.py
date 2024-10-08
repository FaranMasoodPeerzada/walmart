import time
import undetected_chromedriver as uc
from selenium.common.exceptions import NoSuchElementException
import re

# Initialize Chrome with options
chrome_options = uc.ChromeOptions()
chrome_options.add_argument("--window-size=1920,1080")  # Set window size

# Initialize the driver
driver = uc.Chrome(options=chrome_options)
driver.maximize_window()

# Target URL to scrape products
driver.get('https://www.walmart.com/shop/deals/all-home/floor-care')

# List to store product URLs
product_urls = []

# Function to scrape product URLs on the current page
def scrape_product_urls():
    items = driver.find_elements(by="xpath", value='//*[@id="0"]/section/div/div/div/div/a')
    for item in items:
        product_url = item.get_attribute('href')
        if product_url:
            product_urls.append(product_url)

# Loop through all the pages
while True:
    # Scroll down the page to load all items
    driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(5)  # Adjust sleep time if necessary

    # Scrape the product URLs on the current page
    scrape_product_urls()

    try:
        # Find and click the pagination button to move to the next page
        next_button = driver.find_element(by="css selector", value='i.ld.ld-ChevronRight.pv1.primary')
        next_button.click()
        time.sleep(10)  # Wait for the next page to load
    except NoSuchElementException:
        print("No more pages to scrape or button not found.")
        break

print(f"Number of unique product URLs: {len(product_urls)}")

# Function to find UPC from the page's HTML content
def find_upc_from_page():
    page_source = driver.page_source  # Get the HTML source of the current page
    upc_pattern = r'"upc":"(\d{12})"'
    upc_codes = re.findall(upc_pattern, page_source)
    return upc_codes

# Function to extract product details
def extract_product_details(url):
    driver.get(url)
    time.sleep(5)  # Allow the page to load completely

    try:
        title = driver.find_element(by="css selector", value='h1#main-title').text
    except NoSuchElementException:
        title = "N/A"
        

    upc = find_upc_from_page()

    try:
        price_element = driver.find_element(by="xpath", value='//span[@data-testid="price-wrap"]//span[@itemprop="price"]')
        price_text = price_element.text
        # Use regular expression to extract the digits part
        price_digits = re.search(r"\$([\d,.]+)", price_text)
        if price_digits:
            price_digits =  price_digits.group(1)  # Extracted price digits
        else:
            price_digits = "N/A"  # If the price format is different or not found
    except NoSuchElementException:
        price_digits = "N/A" 
    
    try:
        description = driver.find_element(by="xpath", value='//*[@id="product-description-section"]/section/div[2]/div/div/div[1]/span').text
    except NoSuchElementException:
        description = "N/A"

    return {
        "Title": title,
        "Price": price_digits,
        "UPC": upc,
        "Description": description
    }

# Process each product URL
for url in product_urls:
    details = extract_product_details(url)
    print(details)

# Close the browser
driver.quit()
