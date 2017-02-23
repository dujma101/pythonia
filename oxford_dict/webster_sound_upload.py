from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
url = "http://www.memrise.com/course/1404214/advanced-english/edit/#l_5348207"
url1 = 'http://www.memrise.com/course/1401947/pandas/edit/#l_5337085'
fp = webdriver.FirefoxProfile('C:/Users/jjjjj/AppData/Roaming/Mozilla/Firefox/Profiles/47nscnxi.default')

driver = webdriver.Firefox(fp)
driver.get(url1)

driver.implicitly_wait(2)
#el = driver.find_elements_by_class_name("thing")

elementi = driver.find_elements_by_css_selector("input[type=\"file\"]")


sound = ['tax00001.mp3', 'discer02.mp3', 'filibu01.mp3', 'clamp001.mp3', 'grovel02.mp3', 'snub0001.mp3']
zipano = zip(elementi,sound)


for el,rijec in zipano:
    print(el,rijec)
    el.send_keys("C:\\Users\\jjjjj\\Downloads\\rijeci\\" + rijec)
    time.sleep(2)
\\Users\\jjjjj\\Downloads\\abide001.mp3")
#
driver.close()
