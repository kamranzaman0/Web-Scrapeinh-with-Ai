from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup

def scrape_website(website):
    print("Launching Chrome Browser...")
    
    # Path to the ChromeDriver
    chrome_driver_path = "./chromedriver.exe"
    
    # Set Chrome options
    options = Options()
    options.add_argument("--headless")  # Runs Chrome in headless mode (without GUI)
    
    # Initialize the Chrome driver
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Open the website
        driver.get(website)
        print('Page loaded...')
        
        # Get the page source (HTML content)
        html = driver.page_source
        time.sleep(5)  # Wait for 5 seconds to let the page load properly
        
        return html
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        driver.quit()

def extract_body_content(html_content):
    soup=BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clear_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()
    
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()                        
    )
    return cleaned_content

def split_dom_content(dom_content, max_length=600):
    return [
        dom_content[i: i +max_length] for i in range(0, len(dom_content), max_length)
    ]