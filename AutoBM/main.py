# Main Thread
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
except ImportError: raise ImportError("Selenium not found")
import time
from configparser import ConfigParser

def configread(): # reads the config.ini files for use
    config = ConfigParser()
    config.read("config.ini")
    return config
def _printhtml(x): print(x.get_attribute("innerHTML")) # DEBUG FUNCTION

def main():
    # for termux, make sure vncserver is working properly,
    # TODO: add code for headless mode (after everything is done)
    with webdriver.Firefox() as driver:
        driver.install_addon("plugins/ublock_origin.xpi", temporary=True) # DEBUG
        driver.get("https://www.messenger.com/login")
        config = configread()
        form = driver.find_element(By.ID, "login_form") # returns a <form> element
        driver.execute_script(
            "arguments[0].value = arguments[1]; arguments[2].value = arguments[3];",
            form.find_element(By.NAME, "email"), config["Login"]["Email"],
            form.find_element(By.NAME, "pass"), config["Login"]["Password"])
        form.submit()
        time.sleep(30) # Termux-Specific Delay, should be closer to 15seconds
        print("Test Complete")
        breakpoint()
        # Problem: monitor the chats
        while True: pass # DEBUG
if __name__ == "__main__": main()
