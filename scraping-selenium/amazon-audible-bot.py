from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

options = Options()
options.headless = False
# options.add_argument('window-size=1920x1080')

web = 'https://www.audible.com/search'
path = '../../../Downloads/chromedriver_mac_arm64'
service = Service(path)

driver = webdriver.Chrome(service=service, options=options)
driver.get(web)
driver.maximize_window()

# Get the number of search result pages to scrape
pagination = driver.find_elements(By.XPATH, './/ul[contains(@class, "pagingElements")]')
pages = pagination.find_elements(By.TAG_NAME, 'li')
last_page = int(pages[-2].text)


# Loop through each search result page
current_page = 1

while current_page <= last_page:
    time.sleep(2) # Wait for the page to load
    container = driver.find_element(By.CLASS_NAME, 'adbl-impression-container')
    products = container.find_elements(By.XPATH, './li')

    book_title = []
    book_author = []
    book_length = []

    for product in products:
        book_title.append(product.find_element(By.XPATH, './/h3[contains(@class, "bc-heading")]').text)
        book_author.append(product.find_element(By.XPATH, './/li[contains(@class, "authorLabel")]').text)
        book_length.append(product.find_element(By.XPATH, './/li[contains(@class, "runtimeLabel")]').text)

    current_page += 1

    # Click the "Next" button to go to the next search result page
    try:
        next_page = driver.find_elements(By.XPATH, './/span[contains(@class, "nextButton")]')
        next_page.click()
    except:
        pass

# Close the browser window
driver.quit()

# Store the book data in a pandas DataFrame and save it to a CSV file
df_books = pd.DataFrame({'title': book_title, 'author': book_author, 'length': book_length})
df_books.to_csv('books.csv', index=False)