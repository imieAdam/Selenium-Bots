# PYTHON Example

'''
https://medium.com/@harith.sankalpa/connect-selenium-driver-to-an-existing-chrome-browser-instance-41435b67affd
'''

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import shlex, subprocess
import psutil

def checkForChromeInstance(proc, args) -> bool:   
    for process in psutil.process_iter():
        if proc in str(process.cmdline) and args in " ".join(process.cmdline()):
            return True
    raise InstanceException("Instance not found")

def runChrome(args : str) -> None:
    subprocess.Popen(shlex.split(args), shell=True)

def getExistingChrome(chromeDriverPath) -> webdriver:
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    chrome_driver = chromeDriverPath
    driver = webdriver.Chrome(chrome_driver, options=chrome_options)
    return driver

def test() -> webdriver:
    dr = getExistingChrome(r"C:\Users\Adam_Belica\Chrome Drive\chromedriver.exe")
    return dr
    #print(dr.title)

class InstanceException(Exception):
    def __init__(self, message):
        self.message = message

if __name__ == '__main__':
    from portalPacjenta_searchPage import portalPacjenta_searchPage

    try:
        checkForChromeInstance("chrome.exe", "--remote-debugging-port=9222")  
    except InstanceException:
        runChrome(r"'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe' --remote-debugging-port=9222")

    driver = test()
    print(portalPacjenta_searchPage(driver, 3).checkResults())