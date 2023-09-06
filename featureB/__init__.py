from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import expected_conditions
import time
import multiprocessing
import requests
import io
from PIL import Image
from matplotlib.backends.backend_pdf import PdfPages
#Chromeを操作
def get_path(URL_path,adress):
    ##第一関数　ほしいデータのURL
    ##第二関数　とりたいデータの住所
    driver_path = webdriver.Chrome()
    driver_path.get(URL_path)
    driver_path.implicitly_wait(1)
    if(driver_path.current_url!=URL_path): 
        #確認画面のクリック
        serch_element=driver_path.find_element(By.XPATH, '//*[@id="contents"]/div/div[2]/a[1]')
        serch_element.click()     
    #地図サイズの縮尺の変更
    driver_path.find_element(By.XPATH,'//*[@id="zoom_18"]').click()
    driver_path.implicitly_wait(20)

    #町名入力
    mail_element=driver_path.find_element(By.XPATH, '//*[@id="fac_name"]')
    driver_path.implicitly_wait(20)
    mail_element.send_keys(adress)
    driver_path.implicitly_wait(20)
    serch_element=driver_path.find_element(By.XPATH, '//*[@id="submit_search"]')
    driver_path.implicitly_wait(20)
    serch_element.click()
    driver_path.implicitly_wait(20)
    
    #検索した市町村の選択
    driver_path.find_element(By.XPATH,'//*[@id="search_menu_feature"]/div/div[2]/div[1]/div/p').click()
    driver_path.implicitly_wait(20)

    #画像を表示
    driver_path.find_element(By.XPATH,'//*[@id="main_menu"]/button/span').click()
    wait = WebDriverWait(driver_path, 20)
    time.sleep(2)
    elem_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main_menu"]/ul/li[3]/button/span')))
    elem_button.click()

    #画像を取得
    elem_imgUrl = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="copy"]/div[2]/div/div/div[2]/img')))
    driver_path.implicitly_wait(20)
    img_url = elem_imgUrl.get_attribute('src')
    img = requests.get(img_url).content
    img_file = io.BytesIO(img)
    img_rec = Image.open(img_file)
    return img_rec
    

"""
def get_dutywater(URL_path,adress):
    ##
    driver_duty = webdriver.Chrome()
    driver_duty.get(URL_path)
    time.sleep(0.5)
    if(driver_duty.current_url!=URL_path):
        serch_element=driver_duty.find_element(By.XPATH, '//*[@id="contents"]/div/div[2]/a[1]')
        serch_element.click()     
    
    mail_element=driver_duty.find_element(By.XPATH, '//*[@id="fac_name"]')
    mail_element.send_keys(adress)
    serch_element=driver_duty.find_element(By.XPATH, '//*[@id="submit_search"]')
    serch_element.click()
"""
def main():
    #道路のURL
    URL_path="https://www.sonicweb-asp.jp/saitama/map?theme=th_31#pos=139.64570430607762%2C35.86413196358075&scale=30000"
    #下水のURL
    URL_duty="https://www.sonicweb-asp.jp/saitama/map?theme=th_90#pos=139.62844162611339%2C35.898370027849545&scale=30000"
    result_queue = multiprocessing.Queue()
    """
    executor.submit(get_path)
    executor.submit(get_dutywater)
    """
    process1 = multiprocessing.Process(target=get_path, args=(URL_path, "仲町"))
    process2 = multiprocessing.Process(target=get_path, args=(URL_duty, "仲町"))
    # プロセスを開始
    print("道路スタート")
    process1.start()
    print("下水スタート")
    process2.start()

    # プロセスが終了するまで待機
    process1.join()
    process2.join()
    #道路のテスト
    #image_path = get_path(URL_path,"仲町")
    #下水のテスト
    #image_duty = get_path(URL_duty,"仲町")
    image_path = result_queue.get()
    image_duty = result_queue.get()
    image_path.save('image_path(1).pdf')
    image_duty.save('image_duty(1).pdf')


if __name__ == "__main__":
    main()