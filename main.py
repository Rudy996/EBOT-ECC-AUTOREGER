from selenium import webdriver
import requests
import time
import re
from random import choice, randint
from string import digits, ascii_uppercase
from multiprocessing import Pool

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--incognito")
options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-plugins-discovery");
options.add_argument('--profile-directory=Default')
options.add_argument("--mute-audio")
# options.add_extension("MetaMask.crx")
# options.add_extension("Phantom.crx")
# options.add_argument("--window-size=1920,1080")
options.add_argument('headless')

def rabota(url):
    while True:
        try:
            r = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1")
            mail = r.text
            # mail = "u67tlpf6@1secmail.com"
            mal = mail.replace('[', '').replace(']', '').replace('"', '')
            mails = mal.split("@")
            driver = webdriver.Chrome(executable_path=r"chromedriver\chromedriver.exe", options=options)
            driver.get("https://ebot.finance/get-airdrop/84yWTPggWg") # реф ссылка
            time.sleep(3)
            name = ''.join(choice(ascii_uppercase) for i in range(12))
            driver.find_element_by_xpath("//input[@name='name']").send_keys(name)
            number = ''.join(choice(digits) for i in range(12))
            driver.find_element_by_xpath("//input[@name='mobile']").send_keys(number)
            driver.find_element_by_xpath("//input[@name='email']").send_keys(mal)
            password = ''.join(choice(ascii_uppercase) for i in range(12))
            driver.find_element_by_xpath("//input[@name='password']").send_keys(password)
            driver.find_element_by_xpath("//input[@name='password_confirmation']").send_keys(password)
            driver.find_element_by_xpath("//select[@name='country']").send_keys("A")
            driver.find_element_by_class_name("btn-block").click()
            time.sleep(30)
            h = requests.get(f"https://www.1secmail.com/api/v1/?action=getMessages&login={mails[0]}&domain={mails[1]}")  # проверка письма
            y = h.json()[0]["id"]
            o = requests.get(f'https://www.1secmail.com/api/v1/?action=readMessage&login={mails[0]}&domain={mails[1]}&id={y}')
            t = o.json()["body"]
            myString_list = [r.group("url") for r in (re.search("(?P<url>https?://[^\s]+)", i) for i in t.split(" ")) if
                             r is not None]
            confirm1 = myString_list[2]
            confirm = confirm1.replace('"','')
            driver.get(confirm)
            time.sleep(3)
            driver.find_element_by_id("telegramLink").click()
            time.sleep(0.2)
            driver.switch_to.window(driver.window_handles[0])
            driver.find_element_by_id("twitterLink").click()
            time.sleep(0.2)
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(0.5)
            driver.find_element_by_xpath("//button[@type='submit']").click()
            time.sleep(2)
            print("Зареган", mal)
            driver.quit()


        except Exception as ex:
            print(ex)
        finally:
            driver.close()
            driver.quit()


if __name__ == '__main__':
    while True:
        try:
            p = Pool(processes=10) # кол-во процессов
            url = "p"
            urls = url * 10000000
            p.map(rabota, urls)
        except:
            print("Ашибка йобаный рот")