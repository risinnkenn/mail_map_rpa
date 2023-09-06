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
from featureA.listmail import output_, main
import logging
from docopt import docopt
import time

def adress_output(mail_dict):
    adress = mail_dict["body"]

    target = "住所："
    # idx = adress.find(target)
    # print(adress[idx+3: ]if idx!= -1 else "not found")
    lines = adress.split()
    get_target = [s.replace(target,"") for s in lines if target in s]
    return get_target

def mail_output(mail_dict):
    lines =  mail_dict["from"]
    print(type(lines))
    start = lines.index("<")
    end = lines.index(">")
    return mail_dict["from"][start+1:end]
    



if __name__=="__main__":
    arguments = docopt(__doc__, version="0.1")
    query = arguments["<query>"]
    tag = arguments["<tag>"]
    count = arguments["<count>"]
    logging.basicConfig(level=logging.DEBUG)
    
    messages_ = main(query=query, tag=tag, count=count)
    # output_(messages_,query,tag,count)
    
    while True:
        
        mail_dict = output_(messages_,query,tag,count)
        print(mail_dict)
        
        adress = adress_output(mail_dict)
        print(adress)

        mail = mail_output(mail_dict)
        print(mail)

        


        messages_ = None