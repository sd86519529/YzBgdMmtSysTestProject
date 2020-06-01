from selenium import webdriver
import pyttsx3

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')

chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=chrome_options)

nexturl ='https://www.xsbiquge.com/68_68007/3510793.html'


i = 1

while i <10 :

    driver.get(nexturl)

    print(driver.title)

    content = driver.find_element_by_id("content").text

    sound = pyttsx3.init()

    rate = sound.getProperty("rate")

    # voice =sound.getProperty("voices")

    # sound.setProperty('voice',voice[2].id)

    sound.setProperty("rate", rate + 10)

    sound.say(content)

    sound.runAndWait()

    url = driver.find_element_by_xpath("/html/body/div[1]/div[4]/div/div[2]/div[1]/a[3]")

    nexturl = url.get_attribute("href")

    i = i+1

print("'%s'"%(url.get_attribute("href")))

driver.quit()