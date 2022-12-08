# Main Thread
try: from selenium import webdriver
except ImportError: raise ImportError("Selenium not found, run 'pip install selenium'")
import time
def main():
    # for termux, make sure vncserver is working properly
    with webdriver.Firefox() as driver:
        driver.install_addon("plugins/ublock_origin.xpi", temporary=True)
        
if __name__ == "__main__": main()
