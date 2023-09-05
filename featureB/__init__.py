from selenium import webdriver
from selenium.webdriver.common.by import By
import time
#Chromeを操作
def get_path():
    ##
    driver_path = webdriver.Chrome()
    driver_path.get("https://www.sonicweb-asp.jp/saitama/map?theme=th_31#pos=139.64570430607762%2C35.86413196358075&scale=30000")


def get_dutywater():
    ##
    driver_duty = webdriver.Chrome()
    driver_duty.get("https://www.sonicweb-asp.jp/saitama/map?theme=th_90#pos=139.62844162611339%2C35.898370027849545&scale=30000")
def main():
    print("a")

if __name__ == "__main__":
    main()