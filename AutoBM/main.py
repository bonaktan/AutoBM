# Main Thread
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
except ImportError: raise ImportError("Selenium not found")
import time
from configparser import ConfigParser

def configread():
    config = ConfigParser()
    config.read("config.ini")
    return config
def _printhtml(x): print(x.get_attribute("innerHTML"))

def main():
    # for termux, make sure vncserver is working properly
    # TODO: add code for headless mode (after everything is done)
    with webdriver.Firefox() as driver:
        driver.install_addon("plugins/ublock_origin.xpi", temporary=True)
        driver.get("https://www.messenger.com/login")
        config = configread()
        form = driver.find_element(By.ID, "login_form")
        driver.execute_script(
            "arguments[0].value = arguments[1]; arguments[2].value = arguments[3];",
            form.find_element(By.NAME, "email"), config["Login"]["Email"],
            form.find_element(By.NAME, "pass"), config["Login"]["Password"])
        form.submit()
        time.sleep(30)
        print("Test Complete")
        breakpoint()
        # Problem: monitor the chats
        while True: pass
if __name__ == "__main__": main()
