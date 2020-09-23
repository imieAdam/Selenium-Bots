from portalPacjenta.chromeObjects import existingChrome as EC
from portalPacjenta.pageObjects.loginPage import loginPage
from portalPacjenta.pageObjects.mainPage import mainPage
from portalPacjenta.pageObjects.searchPage import searchPage
from portalPacjenta.configObjects import config_reader
from selenium.webdriver.common.by import By

driver = EC.startChrome()
dataFull = config_reader.getConfigJsonData()
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
searchPage.searchAndSelectDropdown(By.TAG_NAME, "facilities", "dropdown-list-group-item", "dropdown-chevron-click-area", "ul. Opolska 114")
searchPage.visibilityOfXPath("//*[@id='facilities']//*[@class='dropdown-multiselect-clear']")
searchPage.clickSearch()