from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import urllib.request
import time

# Set the URL of the website you want to scrape
url = "https://whoicf2.whoi.edu/science/B/whalesounds/fullCuts.cfm"


driver = webdriver.Chrome()

try:
    # Open the URL in the browser
    driver.get(url)

    # Locate the select elements within the specified structure
    search_inside_div = driver.find_element(By.CLASS_NAME, "search-inside")
    row_div = search_inside_div.find_element(By.CLASS_NAME, "row")
    large_columns_div = row_div.find_element(By.CLASS_NAME, "large-4.medium-4.columns.left")
    form = large_columns_div.find_element(By.NAME, "searchSpecies")

    # Find the select element with id "searchSpecies" inside the form
    species_select = Select(form.find_element(By.ID, "getSpecies"))

    # Loop through each option in the select element
    
    counter_species = 1 
    species_select_options_cached_length = len(species_select.options[44:])-1
    while counter_species < species_select_options_cached_length:
        # Select the option
        search_inside_div = driver.find_element(By.CLASS_NAME, "search-inside")
        row_div = search_inside_div.find_element(By.CLASS_NAME, "row")
        large_columns_div = row_div.find_element(By.CLASS_NAME, "large-4.medium-4.columns.left")
        form = large_columns_div.find_element(By.NAME, "searchSpecies")
        species_select = Select(form.find_element(By.ID, "getSpecies"))
        option = species_select.options[44:][counter_species]
        option_value = option.get_attribute("value")
        option_text = option.text

        # Select the option
        species_select.select_by_value(option_value)

        # # Wait for the page to refresh
        # time.sleep(10)  # Adjust the sleep time as needed

        # Locate the select element with id "pickYear" after the page refresh
        year_select = Select(driver.find_element(By.NAME, "pickYear"))
        year_select_options_cached = year_select.options

        # # Loop through each option in the "pickYear" select element
        first_fetch = True
        while True:
            if first_fetch:
                year_option = year_select.options[1]
                year_option_value = year_option.get_attribute("value")
                year_select.select_by_value(year_option_value)

                # Wait for the page to refresh
                # time.sleep(10)  # Adjust the sleep time as needed

                table = driver.find_element(By.TAG_NAME, "table")
                download_links = table.find_elements(By.PARTIAL_LINK_TEXT, "Download")
                for link_index,download_link in enumerate(download_links):
                    download_url = download_link.get_attribute("href")
                    filename = f"downloaded_file_{option_text}_{0}_{link_index}.wav"
                    urllib.request.urlretrieve(download_url, filename)
                    print(f"Downloaded {filename}")
                first_fetch = False
            else:
                counter = 1
                while counter < len(year_select_options_cached[1:]):
                    year_select = Select(driver.find_element(By.NAME, "pickYear"))
                    print(list(map(lambda x: x.text,year_select.options)))
                    year_select = Select(driver.find_element(By.NAME, "pickYear"))
                    year_option = year_select.options[counter]
                    year_option_value = year_option.get_attribute("value")
                    year_select.select_by_value(year_option_value)

                    # Wait for the page to refresh
                    # time.sleep(10)  # Adjust the sleep time as needed

                    table = driver.find_element(By.TAG_NAME, "table")
                    download_links = table.find_elements(By.PARTIAL_LINK_TEXT, "Download")
                    for link_index,download_link in enumerate(download_links):
                        download_url = download_link.get_attribute("href")
                        filename = f"downloaded_file_{option_text}_{counter}_{link_index}.wav"
                        urllib.request.urlretrieve(download_url, filename)
                        print(f"Downloaded {filename}")
                    counter+=1
                break
        counter_species+=1
            
            


finally:
    # Close the browser
    driver.quit()