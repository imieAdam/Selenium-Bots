
from chromeObjects import existingChrome as EC
from pageObjects.loginPage import LoginPage
from pageObjects.mainPage import MainPage
from pageObjects.searchPage import SearchPage
from pageObjects.resultPage import ResultPage
from configObjects import config_reader
from selenium.webdriver.common.by import By
import os

jsonFile = os.path.join(os.path.dirname(__file__), r"configObjects/config.json")
driver = EC.startChrome()
dataFull = config_reader.getConfigJsonData(jsonFile)
"""
if datetime.strptime(dataFull['services'][0]['service']['bookedDateTime'], '%Y-%m-%dT%H:%M:%S.%f') < datetime.now():
    dataFull['services'][0]['service']['bookedDateTime'] = ""
    config_reader.writeToConfig(dataFull)
"""

driver.get("https://rezerwacja.luxmed.pl/start/portalpacjenta")
assert "LUX MED" in driver.title

loginPage = LoginPage(driver)

try:
    loginPage.login("belica.adam@gmail.com", "luxmed", "belica.a")
except:
    loginPage.relog()
    loginPage.login("belica.adam@gmail.com", "luxmed", "belica.a")

loginPage = None
mainPage = MainPage(driver, "belica.adam@gmail.com")
mainPage.clickBookAVisit()
mainPage = None

searchPage = SearchPage(driver, 3)
searchPage.searchAndSelect("city", "Kraków")
searchPage.searchAndSelect("serviceVariant", "Stomatolog")
searchPage.searchAndSelectDropdown("facilities", "dropdown-chevron-click-area", "ul. Opolska 114")
searchPage.visibilityOfXPath("//*[@id='facilities']//*[@class='dropdown-multiselect-clear']")
searchPage.clickSearch()

if searchPage.checkResults():
    resultPage = ResultPage(driver, 3)
    try:
        dataFull = resultPage.selectVisit(dataFull)
        config_reader.writeToConfig(jsonFile, dataFull)
    except Exception as e:
        print(str(e))

driver.close()