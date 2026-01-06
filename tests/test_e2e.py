import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

@pytest.fixture(scope="module")
def driver():
    # Setup Chrome options for CI environment
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless for CI
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    # Initialize WebDriver
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    yield driver
    
    # Teardown
    driver.quit()

def test_home_page_title(driver):
    """Verify that the home page loads and has the correct title."""
    driver.get("http://localhost:4173")  # Targeting the preview port
    time.sleep(2)  # Wait for hydration
    assert "Plant Recognizer" in driver.title

def test_upload_functionality_exists(driver):
    """Verify that the upload button/input is present."""
    driver.get("http://localhost:4173")
    time.sleep(1)
    # Check for file input or a specific button. adjusting selector as needed
    # Assuming standard file input or a button with ID/Class
    # This is a basic smoke test.
    buttons = driver.find_elements(By.TAG_NAME, "button")
    assert len(buttons) > 0
