import urllib
from selenium import webdriver
import time
import zipfile
import glob
import os
import sqlite3
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def to_mp3(rijeci_raw):
    koliko = len(rijeci_raw)
    print(koliko)
    url = "http://online-audio-converter.com/"
    fp = webdriver.FirefoxProfile()
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
    driver = webdriver.Firefox(fp)
    driver.get(url)
    driver.implicitly_wait(2)


    conn = sqlite3.connect('.\\word_database\\words.db')
    cursor = conn.execute("SELECT sound_file from words order by ROWID DESC limit {}".format(koliko))
    dajvise = []
    for rijec in cursor:
        print(rijec[0])
        dajvise.append(rijec)

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type=\"file\"]')))



        el = driver.find_element_by_css_selector("input[type=\"file\"]")
        el.send_keys("C:\\Users\\jjjjj\\Desktop\\pythonia\\oxford_dict\\rijeci_sound\\" + rijec[0])
        time.sleep(1)
    conn.close()
    time.sleep(2)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.button_1_inner_1:nth-child(1) > div:nth-child(1)')))

    driver.find_element_by_css_selector("div.button_1_inner_1:nth-child(1) > div:nth-child(1)").click()

    # time.sleep(5)
    wait.until(EC.frame_to_be_available_and_switch_to_it('download_iframe'))

    # driver.switch_to.frame("download_iframe")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#download_file_link')))

    driver.find_element_by_css_selector("#download_file_link").click()

    time.sleep(5)

    a = glob.glob('C:\\Users\\jjjjj\\Downloads\\*mp3*.zip')

    for sve in a:
        print('ovo je a'+ sve)
        with zipfile.ZipFile(sve, "r") as z:
            z.extractall("C:\\Users\\jjjjj\\Desktop\\pythonia\\oxford_dict\\rijeci_sound\\zip\\")
        time.sleep(2)
        os.remove(sve)
   # driver.close()




    #populating mp3 to memrise--------------------------

    url = "https://www.memrise.com/course/1417154/intermediate-english-with-audio/edit/#l_5393587"
    url1 = 'http://www.memrise.com/course/1401947/pandas/edit/#l_5337085'
    fp1 = webdriver.FirefoxProfile('C:/Users/jjjjj/AppData/Roaming/Mozilla/Firefox/Profiles/47nscnxi.default')

    driver = webdriver.Firefox(fp1)
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    # time.sleep(5)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type=\"file\"]')))


    elementi = driver.find_elements_by_css_selector("input[type=\"file\"]")

    print(len(elementi))


    elem = elementi[-koliko:]

    # for all in el:
    #     print('zadnji-----------'+ str(all))
    for sve1 in dajvise:
        print('rijec' + str(sve1))

    zipano = zip(elem, dajvise)
    #
    print(str(zipano))

    for eleme,rijeci in zipano:
        print(eleme,rijeci)
        eleme.send_keys("C:\\Users\\jjjjj\\Desktop\\pythonia\\oxford_dict\\rijeci_sound\\zip\\" + (rijeci[0][:-3] + 'mp3'))
        time.sleep(2)

    driver.close()


#
#
