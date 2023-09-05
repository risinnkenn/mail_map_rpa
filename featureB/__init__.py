from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import threading
#Chromeを操作
def get_path(adress):
    ##
    driver_path = webdriver.Chrome()
    driver_path.get("https://www.sonicweb-asp.jp/saitama/map?theme=th_31#pos=139.64570430607762%2C35.86413196358075&scale=30000")
    mail_element=driver_path.find_element(By.XPATH, '//*[@id="fac_name"]')
    mail_element.send_keys(adress)
    serch_element=driver_path.find_element(By.XPATH, '//*[@id="submit_search"]')
    serch_element.click()
def get_dutywater(adress):
    ##
    driver_duty = webdriver.Chrome()
    driver_duty.get("https://www.sonicweb-asp.jp/saitama/map?theme=th_90#pos=139.62844162611339%2C35.898370027849545&scale=30000")
    mail_element=driver_duty.find_element(By.XPATH, '//*[@id="fac_name"]')
    mail_element.send_keys(adress)
    serch_element=driver_duty.find_element(By.XPATH, '//*[@id="submit_search"]')
    serch_element.click()
def main():
    """
    executor.submit(get_path)
    executor.submit(get_dutywater)
    """
    thread1 = threading.Thread(target=get_path("仲町"))
    thread2 = threading.Thread(target=get_dutywater("仲町"))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

if __name__ == "__main__":
    main()
    time.sleep(40)