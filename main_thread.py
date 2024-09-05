from selenium import webdriver as wd
import config as cf
from concurrent.futures import ThreadPoolExecutor
import os
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import resultFunction as rf

'''from fake_useragent import UserAgent'''

def Clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def closing_process(message_of_close):
    print(message_of_close)
    time.sleep(5)
    
    closing = "Closing Process "
    
    for i in range(4):
        Clear()
        print(closing)
        time.sleep(0.5)
        closing += "."
    time.sleep(0.5)
    os.system("exit")

def KillChrome():
    os.system('taskkill /F /IM chrome.exe')

def enter_email(driver, email):
    email_input_element = driver.find_element(By.ID, "identifierId")
    email_input_element.clear()
    for i in email:
        email_input_element.send_keys(i)
    email_input_element.send_keys(Keys.RETURN)
    time.sleep(5)

def check_email(driver):
    div_error_email = driver.find_element(By.CLASS_NAME, 'Ekjuhf.Jj6Lae')
    error_email = div_error_email.text
    return error_email

def enter_password(driver, password):
    password_input_element = driver.find_element(By.NAME, "Passwd")
    password_input_element.clear()
    for i in password:
        password_input_element.send_keys(i)
    password_input_element.send_keys(Keys.RETURN)

def check_password(driver):
    div_error_password = driver.find_element(By.CSS_SELECTOR, 'div.Ly8vae.uSvLId div span')
    error_password = div_error_password.text
    return error_password

def enter_recover_email(driver, recover_email):
    li_div_div_svg_path_elements = driver.find_elements(By.CSS_SELECTOR,
                                                        'li.aZvCDf.cd29Sd.zpCp3.SmR8 svg path[d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 14H4V8l8 5 8-5v10zm-8-7L4 6h16l-8 5z"]')
    li_div_div_svg_path_element = li_div_div_svg_path_elements[1]
    li_div_div_svg_element = li_div_div_svg_path_element.find_element(By.XPATH, '..')
    li_div_div_element = li_div_div_svg_element.find_element(By.XPATH, '..')
    li_div_element = li_div_div_element.find_element(By.XPATH, '..')
    li_element = li_div_element.find_element(By.XPATH, '..')

    li_element.click()
    time.sleep(2)

    email_recover_input_element = driver.find_element(By.ID, "knowledge-preregistered-email-response")
    email_recover_input_element.clear()
    for i in recover_email:
        email_recover_input_element.send_keys(i)
    email_recover_input_element.send_keys(Keys.RETURN)
    time.sleep(5)

def check_recover_email(driver):
    div_error_recover_email = driver.find_element(By.CSS_SELECTOR, 'div.Ekjuhf.Jj6Lae')
    error_recover_email = div_error_recover_email.text
    return error_recover_email

def getLastIndexToMyProfiles():
    folder_names = [name for name in os.listdir(cf.local['directory']) if os.path.isdir(os.path.join(cf.local['directory'], name))]
    folder_numbers = [int(name.replace('profile', '')) for name in folder_names]
    folder_numbers.sort()
    if len(folder_numbers) == 0:
        return 0
    return folder_numbers[-1]

def main(boite):
    #lastIndex = getLastIndexToMyProfiles()
    
    '''ua = UserAgent()
    user_agent = ua.random'''

    
    options = wd.ChromeOptions()
    '''options.add_argument(f'user-agent={user_agent}')
    options.add_argument(f"user-data-dir={cf.local['userDataDir']}{lastIndex + 1}")'''
    
    # Désactive le mode sandbox de Chrome, souvent utilisé dans des environnements de conteneurs ou de VM.
    options.add_argument("--no-sandbox")

    # Désactive l'utilisation du répertoire /dev/shm par Chrome, utile dans certains systèmes Linux avec mémoire partagée limitée.
    options.add_argument("--disable-dev-shm-usage")

    # Désactive certaines fonctionnalités de Blink qui détectent si le navigateur est automatisé.
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Supprime l'argument de ligne de commande --enable-automation pour masquer le fait que le navigateur est automatisé.
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    # Désactive l'extension d'automatisation de Chrome, rendant plus difficile pour les sites web de détecter l'automatisation.
    options.add_experimental_option('useAutomationExtension', False)

    # Désactive certaines fonctionnalités de Blink (option redondante dans ce contexte).
    options.add_argument("--disable-blink-features")

    # Répète la désactivation des fonctionnalités de détection d'automatisation (déjà fait plus haut, redondant ici).
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Préférences pour désactiver le gestionnaire de mots de passe de Chrome.
    prefs = {
        "credentials_enable_service": False,  # Désactive les services d'enregistrement des mots de passe.
        "profile.password_manager_enabled": False  # Désactive le gestionnaire de mots de passe de profil.
    }

    # Applique les préférences définies ci-dessus.
    options.add_experimental_option("prefs", prefs)

    driver = wd.Chrome(options=options)
    
    time.sleep(2)

    driver.get("https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&ifkv=AS5LTAQD9a4oPjkvuTPriRcxp7d3vsx5qwDEoo9KM8o4nSzzSQRK24p_e4FG3TDhgAB0-88UY3Eaow&rip=1&sacu=1&service=mail&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S940119914%3A1719931494548591&ddm=0")

    result = ""

    enter_email(driver, boite["email"])
    try:
        check_email(driver)
        result = "Email Not Found"
    except:
        time.sleep(5)
        enter_password(driver, boite["password"])
        try:
            check_password(driver)
            result = "Password Is Incorrect"
        except:
            time.sleep(5)
            try:
                enter_recover_email(driver, boite["recover_email"])
                try:
                    check_recover_email(driver)
                    result = "Recover Email Is Incorrect"
                except:
                    result = "login succ"
            except:
                result = "login succ"

    driver.quit()
    return "Email: " + boite["email"] + " | Result: " + result + "\n"
 

if __name__ == "__main__":
    global futures

    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(main, boite): boite for boite in cf.boites}
    KillChrome()
    Clear()
    rst = ''
    for result in futures:
        rst += result.result()
        
    rf.saveResult(rst)
    
    closing_process("finish process check file of result in this path results/results.txt")
