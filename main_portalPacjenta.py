from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import config_reader
import existingChrome
import portalPacjenta_results
from portalPacjenta_loginPage import portalPacjenta_loginPage
from portalPacjenta_mainPage import portalPacjenta_mainPage
from portalPacjenta_searchPage import portalPacjenta_searchPage

try:
    existingChrome.checkForChromeInstance("chrome.exe", "--remote-debugging-port=9222")
    driver = existingChrome.getExistingChrome(r"C:\Users\Adam_Belica\Chrome Drive\chromedriver.exe")
except existingChrome.InstanceException:
    existingChrome.runChrome(r"'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe' --remote-debugging-port=9222")
    driver = existingChrome.getExistingChrome(r"C:\Users\Adam_Belica\Chrome Drive\chromedriver.exe")
except:
    raise

driver.get("https://rezerwacja.luxmed.pl/start/portalpacjenta")
assert "LUX MED" in driver.title

dataFull = config_reader.getConfigJsonData()
if datetime.strptime(dataFull['services'][0]['service']['bookedDateTime'], '%Y-%m-%dT%H:%M:%S.%f') < datetime.now():
    dataFull['services'][0]['service']['bookedDateTime'] = ""
    config_reader.writeToConfig(dataFull)

portalPacjenta_loginPage(driver).login(driver, "belica.adam@gmail.com", "luxmed", "belica.a")
mainPage = portalPacjenta_mainPage(driver, "belica.adam@gmail.com")
mainPage.clickBookAVisit()
mainPage = None

searchPage = portalPacjenta_searchPage(driver, 3)
searchPage.searchAndSelect(By.ID, "city", "text-higlight", "Kraków")
searchPage.searchAndSelect(By.ID, "serviceVariant", "multi-select-item.leaf-item", "Stomatolog")
searchPage.searchAndSelectDropdown(By.TAG_NAME, "app-select-multi-facilities", "pt-1", "ul. Opolska 114")
searchPage.clickSearch()

try:
    if searchPage.checkResults():
        divs = portalPacjenta_results.getAvailableDatesDivs(driver)
        dateDetails = portalPacjenta_results.getAvailableDateAndDiv(driver, dataFull['services'][0]['service'], divs)
        portalPacjenta_results.selectAvailableDate(driver, dateDetails[1])
        dataFull['services'][0]['service']['bookedDateTime'] =  dateDetails[0].isoformat(timespec='milliseconds')
        config_reader.writeToConfig(dataFull)
finally:
    #print("Close driver")
    driver.close()
    pass
