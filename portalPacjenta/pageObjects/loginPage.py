import keyring
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class loginPage:

    def __init__(self, driver, delay = 3):
        driver : webdriver
        self.driver = driver

    def login(self, driver, user, pasService, pasUser):
        login = self.driver.find_element_by_name("Login")
        password = self.driver.find_element_by_name("Password") 
        login.send_keys(Keys.CONTROL + "a")
        login.send_keys(Keys.DELETE)
        login.send_keys(user)
        password.send_keys(Keys.CONTROL + "a")
        password.send_keys(Keys.DELETE)
        password.send_keys(keyring.get_credential(pasService, pasUser).password)
        password.send_keys(Keys.RETURN)