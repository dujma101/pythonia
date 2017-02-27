import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


driver = webdriver.Firefox()
driver.get("http://www.python.org")
assert "Python" in driver.title

driver.execute_script("window.scrollTo(600, 600);")
time.sleep(2)
driver.execute_script("window.scrollTo(0, 0);")

assert "No results found." not in driver.page_source

driver.close()