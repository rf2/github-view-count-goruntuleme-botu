
import time
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.common.by import By

URL = "https://github.com/rf2"   # your github addres
REFRESH_INTERVAL = 1                    
USE_EXISTING_PROFILE = False            
CHROME_USER_DATA_DIR = r""              
CHROME_PROFILE_DIRECTORY = "Default"    

def make_driver():
    options = webdriver.ChromeOptions()
    if USE_EXISTING_PROFILE and CHROME_USER_DATA_DIR:
        options.add_argument(f"--user-data-dir={CHROME_USER_DATA_DIR}")
        options.add_argument(f"--profile-directory={CHROME_PROFILE_DIRECTORY}")

    options.add_argument("--window-size=1200,900")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(30)
    return driver

def run_refresher(url, interval):
    driver = None
    try:
        driver = make_driver()
    except WebDriverException as e:
        print(f"[!] cant start webdriver {e}")
        sys.exit(1)

    try:
        print(f"[i] going to {url} ")
        driver.get(url)
        print("[i] press ctrl+c to stop")

        while True:
            try:
                time.sleep(interval)
                driver.refresh()
                print(f"[{time.strftime('%H:%M:%S')}] Refreshed.")
            except TimeoutException:
                print("[!] try again")
                try:
                    driver.get(url)
                except Exception as e:
                    print(f"[!] cannot refresh {e}")
            except WebDriverException as e:
                print(f"[!] WebDriver issue: {e} — restarting")
                try:
                    driver.quit()
                except:
                    pass
                driver = make_driver()
                driver.get(url)
    except KeyboardInterrupt:
        print("\n[i] stopped")
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass
        print("[i] ")

if __name__ == "__main__":
    run_refresher(URL, REFRESH_INTERVAL)
