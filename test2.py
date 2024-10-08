import undetected_chromedriver as uc
chrome_options = uc.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--use_subprocess")

driver = uc.Chrome(options=chrome_options)

driver.maximize_window()

# URL to scrape
url = "https://www.walmart.com/shop/deals/all-home/floor-care"


product_urls=[]
# Open the webpage
driver.get(url)
items = driver.find_elements(by="xpath", value='//*[@id="0"]/section/div/div/div/div/a')
for item in items:
    product_url = item.get_attribute('href')
    if product_url:
            product_urls.append(product_url)

print(product_urls)

# Close the WebDriver
driver.quit()