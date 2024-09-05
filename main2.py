from selenium import webdriver as wd
import config as cf
from concurrent.futures import ProcessPoolExecutor
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time

global driver


def enter_email(email):
    # Trouver l'input de l'email avec Id = identifierId
    email_input_element = driver.find_element(By.ID, "identifierId")

    # Pour vider input
    email_input_element.clear()

    # Entrer la valeur de l'email entré dans l'input de l'email lettre par lettre
    for i in email:
        email_input_element.send_keys(i)

    # Appuyer sur la touche Entrée pour valider le champ sélectionné et passer au suivant
    email_input_element.send_keys(Keys.RETURN)

    time.sleep(5)


def check_email():
    div_error_email = driver.find_element(By.CLASS_NAME, 'Ekjuhf.Jj6Lae')
    error_email = div_error_email.text
    return error_email


def enter_password(password):
    # Trouver l'input du mot de passe avec Name = Passwd
    password_input_element = driver.find_element(By.NAME, "Passwd")

    # Pour vider input
    password_input_element.clear()

    # Entrer la valeur du mot de passe dans l'input de mot de passe lettre par lettre
    for i in password:
        password_input_element.send_keys(i)

    # Appuyer sur la touche Entrée pour valider le champ sélectionné et passer au suivant
    password_input_element.send_keys(Keys.RETURN)


def check_password():
    div_error_password = driver.find_element(By.CSS_SELECTOR, 'div.Ly8vae.uSvLId div span')
    error_password = div_error_password.text
    return error_password


def enter_recover_email(recover_email):
    li_div_div_svg_path_elements = driver.find_elements(By.CSS_SELECTOR,
                                                        'li.aZvCDf.cd29Sd.zpCp3.SmR8 svg path[d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 14H4V8l8 5 8-5v10zm-8-7L4 6h16l-8 5z"]')
    li_div_div_svg_path_element = li_div_div_svg_path_elements[1]
    li_div_div_svg_element = li_div_div_svg_path_element.find_element(By.XPATH, '..')
    li_div_div_element = li_div_div_svg_element.find_element(By.XPATH, '..')
    li_div_element = li_div_div_element.find_element(By.XPATH, '..')
    li_element = li_div_element.find_element(By.XPATH, '..')

    li_element.click()

    time.sleep(2)

    # Trouver l'input de l'email recover avec Id = knowledge-preregistered-email-response
    email_recover_input_element = driver.find_element(By.ID, "knowledge-preregistered-email-response")

    # Pour vider input
    email_recover_input_element.clear()

    # Entrer la valeur de l'email recover entré dans l'input de l'email recover lettre par lettre
    for i in recover_email:
        email_recover_input_element.send_keys(i)

    # Appuyer sur la touche Entrée pour valider le champ sélectionné et passer au suivant
    email_recover_input_element.send_keys(Keys.RETURN)

    time.sleep(5)


def check_recover_email():
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
    lastIndex = getLastIndexToMyProfiles()
    options = wd.ChromeOptions()
    #options.add_argument(f"user-data-dir={cf.local['userDataDir']}{lastIndex + 1}")

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")

    prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
    options.add_experimental_option("prefs", prefs)

    driver = wd.Chrome(options=options)

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            });
        """
    })

    driver.get("https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&ifkv=AS5LTAQD9a4oPjkvuTPriRcxp7d3vsx5qwDEoo9KM8o4nSzzSQRK24p_e4FG3TDhgAB0-88UY3Eaow&rip=1&sacu=1&service=mail&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S940119914%3A1719931494548591&ddm=0")

    enter_email(boite["email"])
    try:
        check_email()
    except:
        time.sleep(5)
        enter_password(boite["password"])
        try:
            check_password()
        except:
            time.sleep(5)
            try:
                enter_recover_email(boite["recover_email"])
                try:
                    check_recover_email()
                except:
                    pass
            except:
                pass

    return boite["email"] + " " + boite["password"] + " " + boite["recover_email"]


if __name__ == "__main__":
    boites = [
        {
            "email": "diegochitay20@gmail.com",
            "password": "ybRAphspQd3q2R",
            "recover_email": "tienvan.07051971@gmail.com"
        },
        {
            "email": "mdjamirul9360@gmail.com",
            "password": "c99855386770ey8",
            "recover_email": "01191790006s@gmail.com"
        },
        {
            "email": "zzcat79@gmail.com",
            "password": "dK2H594M5y9675mP",
            "recover_email": "01263392916q@gmail.com"
        },
        {
            "email": "dacnam1410@gmail.com",
            "password": "zkHdgnQZ1dzpNU1",
            "recover_email": "01712760181f@gmail.com"
        }
    ]

    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(main, boite): boite for boite in boites}
        for result in futures:
            print(result)
