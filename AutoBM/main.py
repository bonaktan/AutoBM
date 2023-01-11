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
from pdb import post_mortem
import logging

def media_subroutine(message): # Temporary Code
    # Assuming this already returned elem[1]
    return list(message.children)[1].img
def configread(): # reads the config.ini files for use
    config = ConfigParser()
    config.read("config.ini")
    return config
def listofconvo(driver):
    convo = bs4(driver.find_elements(By.XPATH,
            '//div[@role="grid"]')[1].get_attribute("outerHTML"),
            "lxml").findChild().children
    # first 2 lines of code selects the container containing the convo
    # last line bs4-ises it, then selects the indiv. chat containers
    # breakpoint()
    convo = [[i.text.strip() for i in chat.findChild().findChild().children
              if i.text != ""]
             for chat in convo] # DEPRECATE
    # VITALXPATH = message/div/div/div[1]/div[2]/div[1]/div[1]/div[1]/span
    convo = [[i[0], i[-2]] for i in convo if len(i) >= 3] # DEPRECATE
    return convo
def _printhtml(x): print(x.get_attribute("innerHTML")) # DEBUG FUNCTION


def main():
    # for termux, make sure vncserver is working properly,
    config = configread(); debug = config["Developer"].getboolean("Debug")
    options = Options(); options.headless = not debug
    logging.basicConfig(level=logging.INFO if debug else logging.WARNING)

    logging.info(f"Launching Firefox {'in debug' if debug else ''}")
    with webdriver.Firefox(options=options) as driver:
        driver.install_addon("plugins/ublock_origin.xpi", temporary=True) # DEBUG

        driver.get("https://www.messenger.com/login")
        logging.info("Fetched Messenger")
        form = driver.find_element(By.ID, "login_form") # returns a <form> element
        driver.execute_script(
            "arguments[0].value = arguments[1]; arguments[2].value = arguments[3];",
            form.find_element(By.NAME, "email"), config["Login"]["Email"],
            form.find_element(By.NAME, "pass"), config["Login"]["Password"])
        logging.info("Signing In")
        form.submit()
        time.sleep(5)

        logging.info("Loading Converdation")
        driver.get(config["Chats"]["MonitorChat"])
        while True:
            try: driver.find_elements(By.XPATH, "//div[@role='grid']")[1]
            except: continue
            break
        logging.info("Monitoring")
        try:
            convo = listofconvo(driver)
            old = convo[-1]
            while True:
                convo = [i for i in listofconvo(driver)]
                if convo[-1] != old:
                    print(f"{convo[-1][0]}: {convo[-1][1]}"); old=convo[-1]
        except: post_mortem()
if __name__ == "__main__": main()
