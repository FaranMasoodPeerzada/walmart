import time
import undetected_chromedriver as uc
from selenium.common.exceptions import NoSuchElementException

from selenium.common.exceptions import NoSuchElementException, WebDriverException

chrome_options = uc.ChromeOptions()
# chrome_options.add_argument("--headless")  # Run in headless mode
# chrome_options.add_argument("--disable-gpu")  # Necessary for headless mode
chrome_options.add_argument("--window-size=1920,1080")  # Set window size




# Initialize the driver
driver = uc.Chrome(options=chrome_options)

# Maximize the window
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
        if product_url:  # Ensure the URL is not None
            product_urls.append(product_url)

# Loop through all the pages
while True:
    # Scroll down the page to load all items
    driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(5)  # Adjust sleep time if necessary

    # Scrape the product URLs on the current page
    scrape_product_urls()

    # Check if there is a pagination button with the given class
    try:
        # Find the pagination button by its CSS class
        next_button = driver.find_element(by="css selector", value='i.ld.ld-ChevronRight.pv1.primary')
        next_button.click()
        time.sleep(10)  # Wait for the next page to load
    except NoSuchElementException:
        print("No more pages to scrape or button not found.")
        break
print(f"Number of unique product URLs: {len(product_urls)}")

# Function to extract product details
def extract_product_details(url):
    driver.get(url)
    time.sleep(5)  # Allow the page to load completely

    try:
        title = driver.find_element(by="css selector", value='h1#main-title').text
    except NoSuchElementException:
        title = "N/A"

    try:
        upc = driver.find_element(by="css selector", value='span.price').text
    except NoSuchElementException:
        upc = "N/A"

    try:
        price = driver.find_element(by="xpath", value='//*[@id="maincontent"]/section/main/div[2]/div[2]/div/div[1]/div/div[2]/div/div/span[1]/span[2]/span').text
    except NoSuchElementException:
        price = "N/A"

 
    try:
        description = driver.find_element(by="xpath", value='//*[@id="product-description-section"]/section/div[2]/div/div/div[1]/span').text
    except NoSuchElementException:
        description = "N/A"

    return {
        "Title": title,
        "Price": price,
        "UPC": upc,
        "Description": description
    }

# Process each product URL
for url in product_urls:
    details = extract_product_details(url)
    print(details)




# Close the browser
driver.quit()

