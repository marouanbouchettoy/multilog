from selenium import webdriver as wd
import config as cf
from concurrent.futures import ProcessPoolExecutor, TimeoutError, as_completed
import os


def getLastIndexToMyProfiles():
    folder_names = [name for name in os.listdir(cf.local['directory']) if os.path.isdir(os.path.join(cf.local['directory'], name))]
    folder_numbers = [int(name.replace('profile', '')) for name in folder_names]
    folder_numbers.sort()
    if len(folder_numbers) == 0:
        return 0
    return folder_numbers[-1]


def main(index):
    lastIndex = getLastIndexToMyProfiles()
    options = wd.ChromeOptions()
    options.add_argument(f"user-data-dir={cf.local['userDataDir']}{lastIndex + 1}")
    
    # Add arguments to make Chrome undetectable
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    #options.add_argument('--headless')  # Optional: run in headless mode

    # Prevent detection of headless mode
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Disable the "Chrome is being controlled by automated test software" notification
    prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
    options.add_experimental_option("prefs", prefs)

    driver = wd.Chrome(options=options)
    
    # Additional steps to further avoid detection
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            });
        """
    })
    
    driver.get("https://www.google.com/")
    time.sleep(10)
    return driver.title + str(index)


if __name__ == "__main__":
    index = [1, 2, 3, 4, 5]
    timeout_seconds = 300  # Set the desired timeout for each task

    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(main, idx): idx for idx in index}
        results = []

        for future in as_completed(futures):
            idx = futures[future]
            try:
                result = future.result(timeout=timeout_seconds)
                results.append(result)
            except TimeoutError:
                print(f"Processing item {idx} timed out")
                results.append(None)

        for result in results:
            print(result)
