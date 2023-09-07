from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from multiprocessing import Process, Pipe
import requests
import io
from PIL import Image
from matplotlib.backends.backend_pdf import PdfPages
#wepageに対応させるため市区を消すプログラム
def arrange_adress(adress):
    if "区" in adress:
        return adress.split('区')[1]
    elif "市" in adress:
        return adress.split('市')[1]
    else:
        return adress


def get_path(URL_path,adress,que,send_rev):
    ##第一関数　ほしいデータのURL
    ##第二関数　とりたいデータの住所
    ##第三関数　地図の種類
    ##第四関数　データを送る魔法
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
    driver_path.implicitly_wait(50)
    #送られてきた市町村があるかどうかのチェック
    if "該当する情報はありません。" == driver_path.find_element(By.XPATH, '//*[@id="search_menu_feature"]/div/div[2]/div').get_attribute("textContent"):
        print(adress)
        send_rev.send(["該当する情報はありません。",False])
    else:
        try:
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
            #あえて早く動作を確認するといいと
            img_url = elem_imgUrl.get_attribute('src')
            img = requests.get(img_url).content
            img_file = io.BytesIO(img)
            img_rec = Image.open(img_file)
            img_rec.save(adress+ '.pdf')
            send_rev.send([que+''+adress+ '.pdf',True])
        except Exception as e:
            print("住所はあったのに悲しいな")
            send_rev.send(["住所はあったのに悲しいな",False])
        send_rev.close()
def main(adress_list):
    #Aから送られてきたlistをひとつづつ処理
    image_list=[]
    for i in adress_list:
        get_rev_path,send_rev_path  = Pipe()
        get_rev_duty,send_rev_duty  = Pipe()
        adress = arrange_adress(i)
        #道路のURL
        URL_path="https://www.sonicweb-asp.jp/saitama/map?theme=th_31#pos=139.64570430607762%2C35.86413196358075&scale=30000"
        #下水のURL
        URL_duty="https://www.sonicweb-asp.jp/saitama/map?theme=th_90#pos=139.62844162611339%2C35.898370027849545&scale=30000"
        process1 = Process(target=get_path, args=(URL_path, adress, "image_path",send_rev_path))
        process2 = Process(target=get_path, args=(URL_duty, adress, "image_duty",send_rev_duty))
        # プロセスを開始
        process1.start()
        process2.start()
        get_p = get_rev_path.recv()
        get_d = get_rev_duty.recv()
        # プロセスが終了するまで待機
        process1.join()
        process2.join()
        get_p.extend(get_d)
        image_list.append(get_p)
        print(image_list)

   
if __name__ == "__main__":
    list_adress=["埼玉県さいたま市大宮区大門町2丁目1-1",
        "埼玉県さいたま市大宮区大門町２ー1-１",
        "埼玉県さいたま市大宮区大門町2-1-1",
        "さいたま市大宮区大門町２－１－１",
        "埼玉県川口市栄町3-14-3",
        "埼玉県さいたま市南区沼影1-20-1",
        "埼玉県さいたま市南区沼影一丁目20-1",
        "さいたま市南区沼影１丁目20-1",
        "埼玉県さいたま市南区沼影１丁目２０番地１号",
        "埼玉県さいたま市大宮区大門町６丁目５"]
    main(list_adress)