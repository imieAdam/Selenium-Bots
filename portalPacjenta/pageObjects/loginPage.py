import keyring
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class LoginPage:

    def __init__(self, driver, delay = 3):
        self.driver = driver
        self.delay = delay

    def login(self, user, pasService, pasUser):
        login = self.driver.find_element_by_name("Login")
        password = self.driver.find_element_by_name("Password") 
        login.send_keys(Keys.CONTROL + "a")
        login.send_keys(Keys.DELETE)
        login.send_keys(user)
        password.send_keys(Keys.CONTROL + "a") #TODO try: with id TempPassword except:
        password.send_keys(Keys.DELETE)
        password.send_keys(keyring.get_credential(pasService, pasUser).password)
        password.send_keys(Keys.RETURN)
        WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.CLASS_NAME, "email")))

    def relog(self):
        relog = WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, "//*[@class='log-in-again-link']")))
        relog.click()
