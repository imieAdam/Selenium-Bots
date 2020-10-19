from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import logging

def searchAndSelect(by, field, dropdownClass, searchString, clear = False):
    WebDriverWait(driver, delay).until(EC.invisibility_of_element((By.CLASS_NAME, "spinner-wrapper")))
    mainElement = WebDriverWait(driver, delay).until(EC.presence_of_element_located((by, field)))
    mainElement.find_element_by_class_name("form-control.text-input.text-input-transparent.ng-untouched.ng-pristine.ng-valid").click()
    mainElement.find_element_by_class_name("form-control.text-input.text-input-transparent.ng-untouched.ng-pristine.ng-valid").send_keys(searchString)
    #service.find_element_by_class_name("click-area").click()

    for el in mainElement.find_elements_by_class_name(dropdownClass):
        if searchString == el.text:
            el.click()
            break
        #logging.error(str(searchString) + " Not selected")
    
    if clear:
        mainElement.find_element_by_class_name("form-control.text-input.ng-valid.ng-dirty.ng-touched.text-input-full.dropdown-opened").clear()
        driver.execute_script("return document.getElementsByClassName('form-control text-input ng-valid ng-dirty ng-touched text-input-transparent dropdown-opened')[0].blur();")

def searchAndSelectDropdown(by, field, dropdownClass, *searchStrings):
    WebDriverWait(driver, delay).until(EC.invisibility_of_element((By.CLASS_NAME, "spinner-wrapper")))
    mainElement = WebDriverWait(driver, delay).until(EC.presence_of_element_located((by, field)))
    mainElement.find_element_by_class_name("form-control.text-input.text-input-transparent.ng-untouched.ng-pristine.ng-valid").click()
    #mainElement.find_element_by_class_name("form-control.text-input.text-input-transparent.ng-untouched.ng-pristine.ng-valid").send_keys(searchString)
    #service.find_element_by_class_name("click-area").click()

    for searchString in searchStrings:
        for el in mainElement.find_elements_by_class_name(dropdownClass):
            if searchString == el.text:
                el.click()
                break
            logging.error(str(searchString) + " Not selected")

user = "belica.adam@gmail.com"
psw = "Dajzdrowie12"
delay = 3
contactButtonClass = r"button.right.main_popup_submit_btn"


driver = webdriver.Firefox()
driver.get("https://rezerwacja.luxmed.pl/start/portalpacjenta")
assert "LUX MED" in driver.title

login = driver.find_element_by_name("Login")
password = driver.find_element_by_name("Password")

login.send_keys(user)
password.send_keys(psw)


password.send_keys(Keys.RETURN)

#WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable ((By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/div/div[1]/div/div[2]/form/div[2]/div[2]/button/span[1]")))


try:
    #acceptContactInfoButton = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[5]/div/div/div/div/form/div[7]/a[1]")))
    acceptContactInfoButton = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, contactButtonClass)))
    #acceptContactInfoButton = driver.find_element_by_class_name(contactButtonClass)
    #acceptContactInfoButton = driver.find_element_by_xpath("/html/body/div[1]/div[5]/div/div/div/div/form/div[7]/a[1]")
    acceptContactInfoButton.click()
except:
    logging.warning("No question for contact details present")

mailInfo = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "email")))
assert user in mailInfo.text
#logging.warning(mailInfo.text)

bookAVisit = driver.find_element_by_class_name("button.accept.calendar.bg-green")
bookAVisit.click()

searchAndSelect(By.ID, "city", "text-higlight", "Kraków")
searchAndSelect(By.ID, "serviceVariant", "multi-select-item.leaf-item", "Stomatolog")
searchAndSelectDropdown(By.TAG_NAME, "app-select-multi-facilities", "pt-1", "ul. Opolska 114", "ul. Jasnogórska 11")
btn = driver.find_element_by_class_name("btn.btn-success.btn-lg.mb-10.btn-search")
driver.execute_script("arguments[0].click();", btn)
#driver.close()