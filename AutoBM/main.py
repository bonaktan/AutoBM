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

def configread(): # reads the config.ini files for use
    config = ConfigParser()
    config.read("config.ini")
    return config

def listofconvo(driver):
    convo = bs4(driver.find_elements(By.XPATH,
            '//div[@role="grid"]')[1].get_attribute("outerHTML"),
            "html.parser").findChild().children
    """
    TODO: convert all of this to javascript equivalents
    """
    convo = [[i.text.strip() for i in chat.findChild().findChild().children
              if i.text != ""]
             for chat in convo] # NO MEDIA, IMPROVE
    convo = [[i[0], i[-2]] for i in convo if len(i) >= 3]
    return convo
def _printhtml(x): print(x.get_attribute("innerHTML")) # DEBUG FUNCTION


def main():
    # for termux, make sure vncserver is working properly,
    config = configread(); debug = config["Developer"].getboolean("Debug")
    options = Options()
    logging.basicConfig(level=logging.INFO if debug else logging.WARNING)
    options.headless = not config["Developer"].getboolean("Debug")
    logging.info(f"Launching Firefox {'in debug' if debug else ''}")
    with webdriver.Firefox(options=options) as driver:
        driver.install_addon("plugins/ublock_origin.xpi", temporary=True) # DEBUG
        logging.info("Logging In")
        driver.get("https://www.messenger.com/login")
        form = driver.find_element(By.ID, "login_form") # returns a <form> element
        driver.execute_script(
            "arguments[0].value = arguments[1]; arguments[2].value = arguments[3];",
            form.find_element(By.NAME, "email"), config["Login"]["Email"],
            form.find_element(By.NAME, "pass"), config["Login"]["Password"])
        form.submit()
        # TODO: assert that the credentials entered are correct
        time.sleep(5)

        driver.get(config["Chats"]["MonitorChat"])
        logging.info("Loading Convo")
        while True:
            try: driver.find_elements(By.XPATH,'//div[@role="grid"]')[1]
            except: continue
            break
        time.sleep(2)
        logging.info("Loaded Convo")
        try:
            convo = listofconvo(driver)
            old = convo[-1]
            while True:
                convo = [i for i in listofconvo(driver)]
                if convo[-1] != old:
                    print(f"{convo[-1][0]}: {convo[-1][1]}"); old=convo[-1]
        except:
            import traceback
            traceback.format_exc()
            post_mortem()
        """
        TODO: The whole loop is computationally expensive, use queue to process shit
        properly
        """
if __name__ == "__main__": main()
