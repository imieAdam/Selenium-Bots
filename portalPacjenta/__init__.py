__all__ = ["chromeObjects", "configObjects", "pageObjects"]

if __name__ == "__main__":

    from chromeObjects import existingChrome
    from pageObjects.searchPage import searchPage
    from selenium.webdriver.common.by import By

    try:
        existingChrome.checkForChromeInstance("chrome.exe", "--remote-debugging-port=9222")
        driver = existingChrome.getExistingChrome(r"C:\Users\Adam_Belica\Chrome Drive\chromedriver.exe")
    except existingChrome.InstanceException:
        existingChrome.runChrome(r"'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe' --remote-debugging-port=9222")
        driver = existingChrome.getExistingChrome(r"C:\Users\Adam_Belica\Chrome Drive\chromedriver.exe")
    except:
        raise

    searchPage = searchPage(driver, 3)
    searchPage.searchAndSelect(By.ID, "city", "text-higlight", "Kraków")
    searchPage.searchAndSelect(By.ID, "serviceVariant", "multi-select-item.leaf-item", "Stomatolog")
    searchPage.searchAndSelectDropdown(By.TAG_NAME, "app-select-multi-facilities", "pt-1", "ul. Opolska 114")