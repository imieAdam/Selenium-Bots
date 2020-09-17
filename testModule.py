from portalPacjenta.chromeObjects import existingChrome as EC
from portalPacjenta.pageObjects.loginPage import loginPage as loginPage
from portalPacjenta.pageObjects.mainPage import mainPage as mainPage
from portalPacjenta.configObjects import config_reader

try:
    EC.checkForChromeInstance("chrome.exe", "--remote-debugging-port=9222")
    driver = EC.getExistingChrome(r"C:\Users\Adam_Belica\Chrome Drive\chromedriver.exe")
except EC.InstanceException:
    EC.runChrome(r"'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe' --remote-debugging-port=9222")
    driver = EC.getExistingChrome(r"C:\Users\Adam_Belica\Chrome Drive\chromedriver.exe")
except:
    raise

dataFull = config_reader.getConfigJsonData()

driver.get("https://rezerwacja.luxmed.pl/start/portalpacjenta")
assert "LUX MED" in driver.title

logingPage = loginPage(driver)
logingPage.login(driver, "belica.adam@gmail.com", "luxmed", "belica.a")
loginPage = None
mainPage = mainPage(driver, "belica.adam@gmail.com")
mainPage.clickBookAVisit()
mainPage = None