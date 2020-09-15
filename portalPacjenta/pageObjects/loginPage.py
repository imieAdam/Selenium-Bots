import keyring
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class loginPage:

    def __init__(self, driver):
        driver : webdriver
        self.driver = driver

    def login(self, driver, user, pasService, pasUser):
        login = self.driver.find_element_by_name("Login")
        password = self.driver.find_element_by_name("Password") 
        login.send_keys(user)
        password.send_keys(keyring.get_credential(pasService, pasUser).password)
        password.send_keys(Keys.RETURN)