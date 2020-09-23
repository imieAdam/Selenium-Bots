__all__ = ["chromeObjects", "configObjects", "pageObjects"]

if __name__ == "__main__":

    from chromeObjects import existingChrome
    from pageObjects.searchPage import searchPage
    from selenium.webdriver.common.by import By

    driver = existingChrome.startChrome()
    


    searchPage = searchPage(driver, 3)
    searchPage.searchAndSelect("city", "Kraków")
    searchPage.searchAndSelect("serviceVariant", "Stomatolog")
    searchPage.searchAndSelectDropdown(By.TAG_NAME, "facilities", "dropdown-list-group-item", "dropdown-chevron-click-area", "ul. Opolska 114")
    searchPage.visibilityOfXPath("//*[@id='facilities']//*[@class='dropdown-multiselect-clear']")
    searchPage.clickSearch()
    searchPage.checkResults()