import re
from selenium import webdriver
from selenium.webdriver.common.by import By

# Set up the Chrome driver with headless option
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

# URL of the web page you want to scrape
url = "https://whoicf2.whoi.edu/science/B/whalesounds/index.cfm"  # Replace with your desired URL

driver.get(url)

# Find all div elements with the class name "large-3 columns"
large_divs = driver.find_elements(By.CLASS_NAME, "large-3.columns")

# Initialize a list to store the number of files in each table
num_files_list = []

# Loop through the found divs
for div in large_divs:
    a_tag = div.find_element(By.TAG_NAME, "a")
    href = a_tag.get_attribute("href")
    if not href.startswith("mailto:"):
        driver.get(href)
        
        try:
            # Find the table corresponding to the current download URL
            table = driver.find_element(By.TAG_NAME, "table")

            # Find all "Download" links within the table
            download_links = table.find_elements(By.PARTIAL_LINK_TEXT, "Download")
            
            # Count the number of files in this table
            num_files = len(download_links)
            num_files_list.append(num_files)

        except Exception as e:
            print(f"Error counting files from URL: {href}, Error: {e}")

# Close the browser
driver.quit()

# Print the list of the number of files in each table
for i, num_files in enumerate(num_files_list):
    print(f"Table {i}: {num_files} files")
