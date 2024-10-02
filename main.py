import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import traceback
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time



# Creates an instance of the option class. Setting preferences for the browser before it starts.
chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--start-maximized")

# initalize the driver and go to the website
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.worldaquatics.com/results?year=2024&month=latest&disciplines=")


def get_sport_category():
    # Dictionary mapping user-friendly names to filter values and their corresponding element IDs
    categories = {
        "all": "all--radio",
        "swimming": "SW--radio",
        "water polo": "WP--radio",
        "diving": "DV--radio",
        "artistic swimming": "SY--radio",
        "open water": "OW--radio",
        "high diving": "HD--radio"
    }

    # Displaying category options
    print("Please choose a category from the following options:")
    for category in categories.keys():
        print(f"- {category.capitalize()}")

    # Getting user input
    user_choice = input("\nEnter the name of the category you would like information from: ").strip().lower()

    # Checking if the user choice is valid
    if user_choice in categories:
        return categories[user_choice]
    else:
        print("Invalid category. Please try again.")
        return get_sport_category()


def select_category(driver, category_id):
    try:
        # Find the radio button by its ID
        radio_button = driver.find_element(By.ID, category_id)

        # Use JavaScript in Python to click the element directly
        driver.execute_script("arguments[0].click();", radio_button)
        print(f"Selected the {category_id} category.")
    except Exception as e:
        print(f"An error occurred while selecting the category: {e}")

def select_year(driver):
    """Prompt the user for a year and select it from the dropdown menu."""
    while True:
        # Ask the user for a year between 2024 and 1908
        year = input("Please enter a year between 2024 and 1908 from which you want data from: ").strip()

        try:
            # Wait for the dropdown button to be clickable and click it
            print("Waiting for the dropdown button...")
            wait = WebDriverWait(driver, 15)
            dropdown_button = wait.until(EC.element_to_be_clickable((By.ID, 'listbox-button-filter-comp-year')))
            button = driver.find_element(By.ID, "listbox-button-filter-comp-year")


            # Scroll to the dropdown button first
            driver.execute_script("arguments[0].scrollIntoView(true);", dropdown_button)

            # Use JavaScript to click the dropdown button
            print("Clicking the dropdown button using JavaScript...")
            driver.execute_script("arguments[0].click();", dropdown_button)
            time.sleep(2)  # Small delay to ensure dropdown opens

            # Verify the dropdown list is open and visible
            dropdown_list = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'js-listbox-list')))
            print("Dropdown list is visible.")

            # Start scrolling to find the desired year
            max_scroll_attempts = 15  # Set a limit on how many times we scroll to avoid infinite loops
            scroll_attempts = 0
            found = False

            while not found and scroll_attempts < max_scroll_attempts:
                try:
                    # Construct the XPath for the desired year
                    year_xpath = f"//li[@data-value='{year}']"
                    print(f"Looking for the year {year} using XPath: {year_xpath}")

                    # Check if the year element is visible
                    year_element = driver.find_element(By.XPATH, year_xpath)

                    # Scroll the year element into view if found
                    driver.execute_script("arguments[0].scrollIntoView(true);", year_element)

                    # Click the year element using JavaScript to ensure click event is fired
                    print(f"Clicking the year {year} using JavaScript...")
                    driver.execute_script("arguments[0].click();", year_element)
                    driver.execute_script("arguments[0].click();", button)

                    # If successful, exit the loop
                    found = True
                    print(f"Successfully clicked the year {year}.")
                    break

                except NoSuchElementException:
                    # If the year element isn't visible, scroll down the dropdown
                    print("Year not found, scrolling down...")
                    driver.execute_script("arguments[0].scrollTop += 100;", dropdown_list)
                    scroll_attempts += 1
                    time.sleep(1)  # Add a small delay after each scroll to allow page to render

            if not found:
                print(f"Could not find or select the year {year} after scrolling.")

            # Pause to keep the browser open
            input("Press Enter to close the browser...")

            return

        except TimeoutException:
            print(f"TimeoutException: The year {year} could not be found or selected within the timeout.")
            continue
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            traceback.print_exc()
            continue

select_year = select_year(driver)

# Get the user input for category selection
category_id = get_sport_category()

# Use Selenium to select the radio button on the webpage
select_category(driver, category_id)

time.sleep(30)
