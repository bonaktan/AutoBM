try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.firefox.options import Options
except ImportError: raise ImportError("Selenium not found")

try: from bs4 import BeautifulSoup as bs4
except: raise ImportError("bs4 not found")
import time
from configparser import ConfigParser
from pdb import set_trace as breakpoint

def configread(): # reads the config.ini files for use
    config = ConfigParser()
    config.read("config.ini")
    return config
def listofconvo(driver):
    convo = driver.find_elements(By.XPATH,
            '//div[@role="grid"]')[1].get_attribute("outerHTML")
    convoconvotes= [list(i.findChild().findChild().children) for i in convotes]
    breakpoint()
def _printhtml(x): print(x.get_attribute("innerHTML")) # DEBUG FUNCTION


def main(debug=False):
    # for termux, make sure vncserver is working properly,
    options = Options(); options.headless = not debug
    with webdriver.Firefox(options=options) as driver:
        driver.install_addon("plugins/ublock_origin.xpi", temporary=True) # DEBUG

        driver.get("https://www.messenger.com/login")
        config = configread()
        form = driver.find_element(By.ID, "login_form") # returns a <form> element
        driver.execute_script(
            "arguments[0].value = arguments[1]; arguments[2].value = arguments[3];",
            form.find_element(By.NAME, "email"), config["Login"]["Email"],
            form.find_element(By.NAME, "pass"), config["Login"]["Password"])
        form.submit()
        time.sleep(5)
        driver.get("https://www.messenger.com/t/4576805812442937")
        time.sleep(30) # Termux-Specific Delay, should be closer to 15seconds

        print("Monitoring")
        oldconvo = listofconvo(driver)
        while True:
            newmessages = bs4(driver.find_element(By.XPATH,
                '//div[@role="grid"]')[1].get_attribute("outerHTML"),
                "html.parser").findChild().children
            if oldmessages != newmessages: print("UPDATE"); newmessages=oldmessages
if __name__ == "__main__": main(debug=False)
