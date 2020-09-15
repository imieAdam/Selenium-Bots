from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class portalPacjenta_searchPage:

    def __init__(self, driver, delay):
        self.driver = driver
        self.delay = delay

    def searchAndSelect(self, by, field, dropdownClass, searchString, clear = False):
        WebDriverWait(self.driver, self.delay).until(EC.invisibility_of_element((By.CLASS_NAME, "spinner-wrapper")))
        mainElement = WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((by, field)))
        mainElement.find_element_by_class_name("form-control.text-input.text-input-transparent.ng-untouched.ng-pristine.ng-valid").click()
        #mainElement.find_element_by_xpath("//input[1]").click()
        #form-control text-input ng-untouched ng-pristine ng-valid text-input-transparent
        mainElement.find_element_by_class_name("form-control.text-input.text-input-transparent.ng-untouched.ng-pristine.ng-valid").send_keys(searchString)

        for el in mainElement.find_elements_by_class_name(dropdownClass):
            if searchString == el.text:
                el.click()
                break
        
        if clear:
            mainElement.find_element_by_class_name("form-control.text-input.ng-valid.ng-dirty.ng-touched.text-input-full.dropdown-opened").clear()
            self.driver.execute_script("return document.getElementsByClassName('form-control text-input ng-valid ng-dirty ng-touched text-input-transparent dropdown-opened')[0].blur();")

    def searchAndSelectDropdown(self, by, field, dropdownClass, *searchStrings):
        WebDriverWait(self.driver, self.delay).until(EC.invisibility_of_element((By.CLASS_NAME, "spinner-wrapper")))
        mainElement = WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((by, field)))
        mainElement.find_element_by_class_name("form-control.text-input.text-input-transparent.ng-untouched.ng-pristine.ng-valid").click()

        for searchString in searchStrings:
            for el in mainElement.find_elements_by_class_name(dropdownClass):
                if searchString == el.text:
                    el.click()
                    break

    def clickSearch(self):
        btn = self.driver.find_element_by_class_name("btn.btn-success.btn-lg.mb-10.btn-search")
        self.driver.execute_script("arguments[0].click();", btn)

    def checkResults(self):
        try:
            WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.CLASS_NAME, "no-terms-message.text-center.mx-4")))
            print("No visits available")
            return False
        except:
            return True