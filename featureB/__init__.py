from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time
import threading
#Chromeを操作
def get_path(adress):
    ##
    driver_path = webdriver.Chrome()
    URL_path="https://www.sonicweb-asp.jp/saitama/map?theme=th_31#pos=139.64570430607762%2C35.86413196358075&scale=30000"
    driver_path.get(URL_path)
    time.sleep(0.5)
    if(driver_path.current_url!=URL_path): 
        #確認画面のクリック
        serch_element=driver_path.find_element(By.XPATH, '//*[@id="contents"]/div/div[2]/a[1]')
        serch_element.click()     
    #地図サイズの縮尺の変更
    driver_path.find_element(By.XPATH,'//*[@id="zoom_18"]').click()
    time.sleep(2)

    #町名入力
    mail_element=driver_path.find_element(By.XPATH, '//*[@id="fac_name"]')
    time.sleep(2)
    mail_element.send_keys(adress)
    time.sleep(5)
    serch_element=driver_path.find_element(By.XPATH, '//*[@id="submit_search"]')
    time.sleep(5)
    serch_element.click()
    time.sleep(5)
    
    #検索した市町村の選択
    driver_path.find_element(By.XPATH,'//*[@id="search_menu_feature"]/div/div[2]/div[1]/div/p').click()
    time.sleep(5)

    #画像を表示
    driver_path.find_element(By.XPATH,'//*[@id="main_menu"]/button/span').click()
    time.sleep(5)
    driver_path.find_element(By.XPATH,'//*[@id="main_menu"]/ul/li[3]/button/span').click()
    time.sleep(5)
def get_dutywater(adress):
    ##
    driver_duty = webdriver.Chrome()
    URL_path="https://www.sonicweb-asp.jp/saitama/map?theme=th_90#pos=139.62844162611339%2C35.898370027849545&scale=30000"
    driver_duty.get(URL_path)
    time.sleep(0.5)
    if(driver_duty.current_url!=URL_path):
        serch_element=driver_duty.find_element(By.XPATH, '//*[@id="contents"]/div/div[2]/a[1]')
        serch_element.click()     
    
    mail_element=driver_duty.find_element(By.XPATH, '//*[@id="fac_name"]')
    mail_element.send_keys(adress)
    serch_element=driver_duty.find_element(By.XPATH, '//*[@id="submit_search"]')
    serch_element.click()
def main():
    """
    executor.submit(get_path)
    executor.submit(get_dutywater)
    """
    """
    thread1 = threading.Thread(target=get_path("仲町"))
    thread2 = threading.Thread(target=get_dutywater("仲町"))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    """
    image = get_path("仲町")


if __name__ == "__main__":
    main()