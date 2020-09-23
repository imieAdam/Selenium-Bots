from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class searchPage:

    def __init__(self, driver, delay = 3):
        self.driver = driver
        self.delay = delay

    def searchAndSelect(self, fieldID, searchString):
        WebDriverWait(self.driver, self.delay).until(EC.invisibility_of_element((By.CLASS_NAME, "spinner-wrapper")))
        mainElement = self.driver.find_elements_by_xpath("//*[@id='{}']//input".format(fieldID))[0] #WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((by, field)))
        self.driver.execute_script("arguments[0].click();", mainElement)
        mainElement = self.driver.find_elements_by_xpath("//*[@id='{}']//*[text() = '{}']".format(fieldID, searchString))[0]
        self.driver.execute_script("arguments[0].click();", mainElement)


    def searchAndSelectDropdown(self, by, fieldID, dropdownClass, chevron, *searchStrings):
        WebDriverWait(self.driver, self.delay).until(EC.invisibility_of_element((By.CLASS_NAME, "spinner-wrapper")))
        mainElement = self.driver.find_elements_by_xpath("//*[@id='{}']//input".format(fieldID))[0]
        mainElement.click()
        mainElements = self.driver.find_elements_by_class_name(dropdownClass)

        for searchString in searchStrings:
            for el in mainElements:
                if searchString == el.text:
                    el.click()
                    break

        self.driver.find_elements_by_xpath("//*[@id='{}']//*[@class='{}']".format(fieldID, chevron))[0].click()

    def clickSearch(self):
        btn = self.driver.find_element_by_class_name("btn.btn-success.btn-lg.mb-10.btn-search")
        self.driver.execute_script("arguments[0].click();", btn)
        WebDriverWait(self.driver, self.delay).until(EC.invisibility_of_element_located((By.CLASS_NAME, "btn.btn-success.btn-lg.mb-10.btn-search")))

    def checkResults(self):
        WebDriverWait(self.driver, self.delay).until(EC.invisibility_of_element_located((By.XPATH, "//*[@class='item']")))
        try:
            WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.CLASS_NAME, "no-terms-message.text-center.mx-4")))
            print("No visits available")
            return False
        except:
            return True

    def visibilityOfXPath(self, xpath):
        WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, xpath)))