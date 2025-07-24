import time
import os
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up paths and constants
DOWNLOAD_FOLDER = "/Users/joshmontgomery/Downloads"
TARGET_FOLDER = "/Users/joshmontgomery/Library/Mobile Documents/com~apple~CloudDocs/Desktop/Swimming/Hart PowerBI Report/Python Scripts/Clean Data"
FINAL_FILENAME = "swim_manager_members.xlsx"
target_path = os.path.join(TARGET_FOLDER, FINAL_FILENAME)

# Set up the WebDriver (without headless for debugging)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

# Open the login page
driver.get("https://hart.swimmanager.co.uk/login")

# Set up wait
wait = WebDriverWait(driver, 20)  # Increased wait time to 20 seconds

try:
    # Log in
    email_input = wait.until(EC.presence_of_element_located((By.NAME, "email")))
    password_input = driver.find_element(By.NAME, "password")
    email_input.send_keys("monty53@sky.com")
    password_input.send_keys("Spiderman53")

    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()

    # Print the current URL to confirm we're on the correct page
    print(driver.current_url)

    # Wait until login is successful and "Account" link is present
    wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Account")))

    # Navigate to the times page
    driver.get("https://hart.swimmanager.co.uk/club/members")

    # Wait for the export button to be clickable
    export_button = wait.until(EC.element_to_be_clickable((By.NAME, "export")))
    export_button.click()

    # Give time for the download to start
    time.sleep(5)

    # Wait for a .csv file to appear in the download folder
    downloaded_file = None
    timeout = 30  # seconds
    start_time = time.time()

    while time.time() - start_time < timeout:
        xlsx_files = [f for f in os.listdir(DOWNLOAD_FOLDER) if f.endswith(".xlsx")]
        if xlsx_files:
            downloaded_file = sorted(xlsx_files, key=lambda x: os.path.getctime(os.path.join(DOWNLOAD_FOLDER, x)))[-1]
            break
        time.sleep(1)

    if downloaded_file:
        latest_file = os.path.join(DOWNLOAD_FOLDER, downloaded_file)
        os.makedirs(TARGET_FOLDER, exist_ok=True)
        shutil.move(latest_file, target_path)
        print(f"File saved to: {target_path}")

        # --- XLSX to CSV conversion ---
        import openpyxl
        import csv

        # Define CSV output path
        csv_path = os.path.join(TARGET_FOLDER, "swim_manager_members.csv")

        # Load the workbook and active sheet
        wb = openpyxl.load_workbook(target_path)
        sheet = wb.active

        # Write to CSV
        with open(csv_path, "w", newline="") as f:
            writer = csv.writer(f)
            for row in sheet.iter_rows(values_only=True):
                writer.writerow(row)

        print(f"Converted to CSV: {csv_path}")
    else:
        print("XLSX file not found in time!")



except Exception as e:
    print(f"Error: {e}")
finally:
    driver.quit()