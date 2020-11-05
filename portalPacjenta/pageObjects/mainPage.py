from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

class MainPage:

    def __init__(self, driver, userMail):

        self.contactButtonClass = r"//*[@class='button right main_popup_submit_btn']"
        self.delay = 3
        self.driver = driver
        try:
            WebDriverWait(self.driver, self.delay).until(EC.invisibility_of_element((By.CLASS_NAME, "spinner-wrapper")))
            acceptContactInfoButton = WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, self.contactButtonClass)))
            acceptContactInfoButton.click()
        except:
            pass
        mailInfo = WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.CLASS_NAME, "email")))
        assert userMail in mailInfo.text, ("MailInfo does not match userMail expected %s, but got %s", userMail, mailInfo.text)

    def clickBookAVisit(self):
        WebDriverWait(self.driver, self.delay).until(EC.invisibility_of_element((By.CLASS_NAME, "spinner-wrapper")))
        WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.CLASS_NAME, "button.accept.calendar.bg-green"))).click()

    def goToSetting(self, setting):
        drpDwn = self.driver.find_element_by_class_name("currentUser.dropdown")
        ActionChains(self.driver).move_to_element(drpDwn).perform()
        ul = drpDwn.find_element_by_class_name("dropMenu")
        for el in ul.find_elements_by_tag_name("a"):
            print(el.text)
            if setting in el.text:
                el.click()
                return