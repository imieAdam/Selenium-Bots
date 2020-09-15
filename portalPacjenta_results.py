from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
import locale
from config_reader import getConfigJsonData
from config_reader import writeToConfig

def getAvailableDate(rawDate) -> datetime:
    locale.setlocale(locale.LC_TIME, "pl")
    for i in range(1,12):
        if datetime.strptime(str(i).zfill(2), '%m').strftime('%b') in rawDate.split(',')[0].split(' ')[1]:
            return(datetime.strptime( rawDate.split(',')[0].split(' ')[0] + '-' + str(i).zfill(2) + '-' + str(datetime.today().year), "%d-%m-%Y"))
    return ""

def getAvailableTime(rawTime) -> str:
    return ""

def checkXpath():
    driver.find_element_by_xpath("/html/body/modal-container/div/div/form/div[2]/div/button[1]")

def getAvailableDatesDivs(driver):
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "card.card-no-border.card-box-shadow.p-0")))
    dateDivs = driver.find_elements_by_class_name("card.card-no-border.card-box-shadow.p-0")
    return dateDivs


def getAvailableDateAndDiv(driver, service, dateDivs) -> tuple:
    for dateDiv in dateDivs:
        availableDate = getAvailableDate(dateDiv.find_element_by_class_name("title.h4.m-0").text)
        if not service['notBefore'] or availableDate >= datetime.strptime(service['notBefore'], "%Y-%m-%d"):
            for line in dateDiv.find_elements_by_class_name("time"):
                availableDate = availableDate.replace(hour=int(line.text.split(":")[0]), minute=int(line.text.split(":")[1]))
                for timeFrame in service['timeFrames']:
                    if ((availableDate.time() >= datetime.strptime(timeFrame['start'], "%H:%M").time() and 
                        availableDate.time() <= datetime.strptime(timeFrame['end'], "%H:%M").time()) and
                        (not service['bookedDateTime'] or 
                        availableDate <  datetime.strptime(service['bookedDateTime'], '%Y-%m-%dT%H:%M:%S.%f'))):
                        return (availableDate, dateDiv)
    raise Exception("No visit available")

def selectAvailableDate(driver, dateDiv) -> None:
    ActionChains(driver).move_to_element(dateDiv.find_elements_by_class_name("term-item")[0].find_element_by_class_name("chevron")).perform()
    dateDiv.find_elements_by_class_name("term-item")[0].find_element_by_class_name("btn.btn-primary").click()
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//div[@class='modal-dialog modal-dialog-centered']//button[@class='btn btn-primary']")))
    driver.find_element_by_xpath(r"//div[@class='modal-dialog modal-dialog-centered']//button[@class='btn btn-primary']").click()
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//div[@class='modal-content']//button[@class='btn btn-primary']")))
        driver.find_element_by_xpath(r"//div[@class='modal-content']//button[@class='btn btn-primary']").click()
    except:
        pass

def updateJsonWithDate(availableDate):
    pass

if __name__ == "__main__":
    #temp
    import existingChrome
    try:
        existingChrome.checkForChromeInstance("chrome.exe", "--remote-debugging-port=9222")
        driver = existingChrome.getExistingChrome(r"C:\Users\Adam_Belica\Chrome Drive\chromedriver.exe")
    except existingChrome.InstanceException:
        existingChrome.runChrome(r"'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe' --remote-debugging-port=9222")
        driver = existingChrome.getExistingChrome(r"C:\Users\Adam_Belica\Chrome Drive\chromedriver.exe")
    except:
        raise
    #temp

    #tempHardcodedJSON
    #bookAVisit(driver)



'''
if(date.today().strftime("%#d") in dateDiv.find_element_by_class_name("card-header-content").text):
    ActionChains(driver).move_to_element(dateDiv.find_elements_by_class_name("term-item")[0].find_element_by_class_name("chevron")).perform()
    dateDiv.find_elements_by_class_name("term-item")[0].find_element_by_class_name("btn.btn-primary").click()
    break
'''