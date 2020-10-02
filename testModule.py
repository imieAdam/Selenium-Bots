from portalPacjenta.chromeObjects import existingChrome as EC
from portalPacjenta.pageObjects.loginPage import loginPage
from portalPacjenta.pageObjects.mainPage import mainPage
from portalPacjenta.pageObjects.searchPage import searchPage
from portalPacjenta.pageObjects.resultPage import ResultPage
from portalPacjenta.configObjects import config_reader
from selenium.webdriver.common.by import By

jsonFile = r".\config.json"
driver = EC.startChrome()
dataFull = config_reader.getConfigJsonData(jsonFile)
"""
if datetime.strptime(dataFull['services'][0]['service']['bookedDateTime'], '%Y-%m-%dT%H:%M:%S.%f') < datetime.now():
    dataFull['services'][0]['service']['bookedDateTime'] = ""
    config_reader.writeToConfig(dataFull)
"""

driver.get("https://rezerwacja.luxmed.pl/start/portalpacjenta")
assert "LUX MED" in driver.title

logingPage = loginPage(driver)
logingPage.login(driver, "belica.adam@gmail.com", "luxmed", "belica.a")
loginPage = None
mainPage = mainPage(driver, "belica.adam@gmail.com")
mainPage.clickBookAVisit()
mainPage = None

searchPage = searchPage(driver, 3)
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