"""
list GMail Inbox.

Usage:
  listmail.py <query> <tag> <count>
  listmail.py -h | --help
  listmail.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
"""
#Aでのインポート
from featureA.listmail import output_, main_A
import logging
from docopt import docopt

#Bでのインポート
from featureB.get_map import main_B

#Cでのインポート
# from featureC.   import main_C

#住所を綺麗に取り出す，リスとで返す
def adress_output(mail_dict):
    adress = mail_dict["body"]

    target = "住所："
    lines = adress.split()
    get_target = [s.replace(target,"") for s in lines if target in s]
    return get_target
#メアドを綺麗に取り出す，文字列で返す
def mail_output(mail_dict):
    lines =  mail_dict["from"]
    # print(type(lines))
    start = lines.index("<")
    end = lines.index(">")
    return mail_dict["from"][start+1:end]
    



if __name__=="__main__":
    arguments = docopt(__doc__, version="0.1")
    query = arguments["<query>"]
    tag = arguments["<tag>"]
    count = arguments["<count>"]
    logging.basicConfig(level=logging.DEBUG)
    
    messages_ = main_A(query=query, tag=tag, count=count)
    
    #全体のループ
    while True:
        
        mail_dict = output_(messages_,query,tag,count)
        print(mail_dict)
        
        adress = adress_output(mail_dict)
        print(adress)

        mail = mail_output(mail_dict)
        print(mail)

        imagelist = main_B(adress)
        print(imagelist)

        # main_c(imagelist,mail)
        


        messages_ = None
