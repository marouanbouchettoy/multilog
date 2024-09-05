from selenium import webdriver as wd
import config as cf
from concurrent.futures import ProcessPoolExecutor, TimeoutError
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
    driver = wd.Chrome(options=options)
    driver.get("https://www.google.com/")
    return driver.title + str(index)


if __name__ == "__main__":
    index = [1, 2, 3, 4]
    timeout_seconds = 20  # Set the desired timeout for each task

    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(main, idx) for idx in index]
        results = []

        for future in futures:
            try:
                result = future.result(timeout=timeout_seconds)
                results.append(result)
            except TimeoutError:
                print(f"Processing item {future} timed out")
                results.append(None)

        for result in results:
            print(result)
