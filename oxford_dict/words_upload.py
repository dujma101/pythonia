from selenium import webdriver
import sqlite3
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
def upload_words(rijeci_raw):

    koliko1 = len(rijeci_raw)
    url = "https://www.memrise.com/course/1417154/intermediate-english-with-audio/edit/#l_5393587"
    url1 = 'http://www.memrise.com/course/1401947/pandas/edit/#l_5337085'
    fp = webdriver.FirefoxProfile('C:/Users/jjjjj/AppData/Roaming/Mozilla/Firefox/Profiles/47nscnxi.default')

    driver = webdriver.Firefox(fp)
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    add = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.dropdown-toggle:nth-child(1)')))
    add.click()

    confirm = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'ul.dropdown-menu > li:nth-child(1) > a:nth-child(1)')))

    confirm.click()

    # driver.find_element_by_css_selector("button.dropdown-toggle:nth-child(1)").click()
    # driver.find_element_by_css_selector("ul.dropdown-menu > li:nth-child(1) > a:nth-child(1)").click()

    time.sleep(1)

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.control-group:nth-child(5) > textarea:nth-child(1)')))
    elem = driver.find_element_by_css_selector("div.control-group:nth-child(5) > textarea:nth-child(1)")



    conn = sqlite3.connect('.\\word_database\\words.db')

    cursor = conn.execute("select word, definition, etymology FROM words ORDER BY ROWID DESC LIMIT {}".format(koliko1))
    for sve in cursor:
        print(sve)
        # elem.send_keys(str(row))



        elem.send_keys(sve[0] + '\t')
        elem.send_keys(sve[1] +'\t')
        elem.send_keys(sve[2] + '\n')

    conn.close()

    driver.find_element_by_css_selector(".btn-primary").click()


    driver.close()

# upload_words()