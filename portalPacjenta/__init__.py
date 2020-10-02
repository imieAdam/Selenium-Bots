
__all__ = ["chromeObjects", "configObjects", "pageObjects"]

if __name__ == "__main__":

    from chromeObjects import existingChrome
    from pageObjects.searchPage import searchPage as SearchPage
    from selenium.webdriver.common.by import By

    driver = existingChrome.startChrome()
    searchPage = SearchPage(driver, 3)
    searchPage.searchAndSelectDropdown("facilities", "dropdown-chevron-click-area", "ul. Opolska 114", "ul. Jasnogórska 11")
