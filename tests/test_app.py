import pytest
import os
import glob
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Configuration ---
BASE_URL = os.getenv('BASE_URL', 'http://localhost:3000')

def get_real_test_image():
    """
    Finds the first available image in the 'data' folder at Project Root.
    """
    # CORRECTED PATH: Points to 'data' in the current working directory (Root)
    data_folder = os.path.join(os.getcwd(), 'data')
    
    # Debug print to help you verify the path if it fails
    print(f"\n📂 Looking for images in: {data_folder}")
    
    # Look for common image formats
    extensions = ['*.jpg', '*.jpeg', '*.png', '*.webp']
    images = []
    
    for ext in extensions:
        images.extend(glob.glob(os.path.join(data_folder, ext)))
        
    if not images:
        pytest.fail(f"❌ No images found in {data_folder}. Please add a test image there.")
        
    # Return the absolute path of the first image found
    print(f"📷 Using test image: {os.path.basename(images[0])}")
    return os.path.abspath(images[0])

@pytest.fixture(scope="module")
def driver():
    chrome_options = Options()
    
    # ⬇️ UNCOMMENT THIS FOR JENKINS (Headless Mode) ⬇️
    chrome_options.add_argument("--headless=new") 
    
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()

def test_plant_recognition_flow(driver):
    print(f"\n🚀 Starting Test on {BASE_URL}...")

    # 1. Load App
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "nav"))
        )
        print("✅ App Loaded")
    except Exception as e:
        pytest.fail(f"❌ App failed to load. Is 'npm run dev' running? Error: {e}")

    # 2. Upload Real Photo from Data Folder
    try:
        image_path = get_real_test_image()
        
        file_input = driver.find_element(By.ID, "fileInput")
        driver.execute_script("arguments[0].style.display = 'block';", file_input)
        file_input.send_keys(image_path)
        
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//img[@alt='Preview']"))
        )
        print("✅ Image Uploaded")
        
    except Exception as e:
        driver.save_screenshot("upload_fail.png")
        pytest.fail(f"❌ Failed to upload image: {e}")

    # 3. Click Recognize
    try:
        recognize_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Recognize Plant')]"))
        )
        recognize_btn.click()
        print("✅ Clicked 'Recognize Plant'")
        
        WebDriverWait(driver, 5).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "nav"), "Scanning...")
        )
        print("✅ Analysis started")
        
    except Exception as e:
        driver.save_screenshot("button_fail.png")
        pytest.fail(f"❌ Failed to initiate recognition: {e}")

    # 4. Detect Success OR Error
    try:
        print("⏳ Waiting for results...")
        
        WebDriverWait(driver, 20).until(
            lambda d: d.find_elements(By.XPATH, "//*[contains(text(), 'Identification Successful')]") or \
                      d.find_elements(By.XPATH, "//*[contains(text(), 'Failed to connect')]")
        )
        
        body_text = driver.find_element(By.TAG_NAME, "body").text
        
        if "Failed to connect" in body_text:
            driver.save_screenshot("backend_error.png")
            pytest.fail("❌ Frontend reported: 'Failed to connect'. Check your VITE_API_URL or Render status.")
            
        elif "Identification Successful" in body_text:
            print("✅ Result received: 'Identification Successful'")
            driver.save_screenshot("success_result.png")
            
        else:
            pytest.fail("❌ Unknown state: Result did not appear.")
            
    except Exception as e:
        driver.save_screenshot("inference_fail.png")
        pytest.fail(f"❌ Result section did not appear (Timeout): {e}")

    print("🎉 Test Cycle Complete")