import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import urllib.request


# Set up the Chrome driver with headless option
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

# URL of the web page you want to scrape
url = "https://whoicf2.whoi.edu/science/B/whalesounds/index.cfm"  # Replace with your desired URL

driver.get(url)

# Find all div elements with the class name "large-3 columns"
large_divs = driver.find_elements(By.CLASS_NAME, "large-3.columns")

# Initialize a list to store the URLs
download_urls = []

# Loop through the found divs, extract the href attribute, and add to the list
for div in large_divs:
    a_tag = div.find_element(By.TAG_NAME, "a")
    href = a_tag.get_attribute("href")
    if not href.startswith("mailto:"):
        download_urls.append(href)

table_index = 0

# Iterate through the download URLs
for download_url in download_urls:
    driver.get(download_url)
    # all_cuts_link = driver.find_element(By.PARTIAL_LINK_TEXT,"ALL CUTS")
    # wait = WebDriverWait(driver, 20)
    
    # driver.get(all_cuts_link.get_attribute("href"))
    try:
        # Find the table corresponding to the current download URL
        table = driver.find_element(By.TAG_NAME, "table")

        # Find all "Download" links within the table
        download_links = table.find_elements(By.PARTIAL_LINK_TEXT, "Download")

        # Create a base file name using the table index
        page_text = driver.page_source
        base_file_name = ''
        match = re.search(r'Best of.*?\(', page_text)
        if match:
            extracted_string = match.group(0)[:-1]  # Remove the last character, which is an open parenthesis
            base_file_name = extracted_string
        file_name = base_file_name

        # Iterate through the "Download" links and save the files
        for link_index, download_link in enumerate(download_links):
            download_url = download_link.get_attribute("href")

            # Create a filename with an index for each link in the table
            file_name_indexed = f"All_cuts_{table_index}_{link_index}.wav"

            # Perform the download and save the file
            urllib.request.urlretrieve(download_url, file_name_indexed)
            print(f"Downloaded: {file_name_indexed}")

        # Increment the table index
        table_index += 1
    except Exception as e:
        print(f"Error downloading files from URL: {download_url}, Error: {e}")

# Close the browser
driver.quit()






