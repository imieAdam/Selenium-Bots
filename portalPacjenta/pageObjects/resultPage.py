from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
import locale
from configObjects.config_reader import getConfigJsonData, writeToConfig

class ResultPage:
    def __init__(self, driver, delay = 3):
        self.driver = driver
        self.delay = delay
        self.PLMONTHS = ['sty', 'lut', 'mar', 'kwi', 'maj', 'cze', 'lip', 'sie',
                        'wrz', 'paź', 'lis', 'gru']    

    def __getAvailableDate(self, rawDate) -> datetime:
        locale.setlocale(locale.LC_TIME, "pl")
        for i in range(1, 12):
            #if datetime.strptime(str(i).zfill(2), '%m').strftime('%b') in rawDate.split(',')[0].split(' ')[1]:
            if self.PLMONTHS[i-1] in rawDate.split(',')[0].split(' ')[1]:
                return(datetime.strptime(rawDate.split(',')[0].split(' ')[0] + '-' + str(i).zfill(2) + '-' + str(datetime.today().year), "%d-%m-%Y"))
        raise Exception("Invalid date format: " + str(rawDate))

    def getAvailableTime(self, rawTime) -> str:
        return ""

    def checkXpath(self):
        self.driver.find_element_by_xpath("/html/body/modal-container/div/div/form/div[2]/div/button[1]")

    def __getAvailableDatesDivs(self) -> object:
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "card.card-no-border.card-box-shadow.p-0")))
        dateDivs = self.driver.find_elements_by_class_name("card.card-no-border.card-box-shadow.p-0")
        return dateDivs


    def __getAvailableDateAndDiv(self, service, dateDivs) -> tuple:
        for dateDiv in dateDivs:
            availableDate = self.__getAvailableDate(dateDiv.find_element_by_class_name("title.h4.m-0").text)
            if not service['afterDate'] or availableDate >= datetime.strptime(service['afterDate'], "%Y-%m-%d"):
                for line in dateDiv.find_elements_by_class_name("time"):
                    availableDate = availableDate.replace(hour=int(line.text.split(":")[0]), minute=int(line.text.split(":")[1]))
                    for timeFrame in service['timeFrames']:
                        if ((availableDate.time() >= datetime.strptime(timeFrame['start'], "%H:%M").time() and 
                            availableDate.time() <= datetime.strptime(timeFrame['end'], "%H:%M").time()) and
                            (not service['bookedDateTime'] or availableDate < datetime.strptime(service['bookedDateTime'], '%Y-%m-%dT%H:%M:%S.%f'))):
                            return (availableDate, dateDiv)
        raise Exception("Visits do not meet the criteria for booking")

    def __selectAvailableDate(self, dateDiv) -> None:
        ActionChains(self.driver).move_to_element(dateDiv.find_elements_by_class_name("term-item")[0].find_element_by_class_name("chevron")).perform()
        dateDiv.find_elements_by_class_name("term-item")[0].find_element_by_class_name("btn.btn-primary").click()
        WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, "//div[@class='modal-dialog modal-dialog-centered']//button[@class='btn btn-primary']")))
        self.driver.find_element_by_xpath(r"//div[@class='modal-dialog modal-dialog-centered']//button[@class='btn btn-primary']").click()
        try:
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, "//div[@class='modal-content']//button[@class='btn btn-primary']")))
            driver.find_element_by_xpath(r"//div[@class='modal-content']//button[@class='btn btn-primary']").click()
        except:
            pass

    def updateJsonWithDate(self, availableDate):
        pass

    def selectVisit(self, service) -> str:
        divs = self.__getAvailableDatesDivs()
        dateDetails = self.__getAvailableDateAndDiv(service['services'][0]['service'], divs)
        self.__selectAvailableDate(dateDetails[1])
        service['services'][0]['service']['bookedDateTime'] =  dateDetails[0].isoformat(timespec='milliseconds')
        return service