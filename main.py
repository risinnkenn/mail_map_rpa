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




if __name__=="__main__":
    arguments = docopt(__doc__, version="0.1")
    query = arguments["<query>"]
    tag = arguments["<tag>"]
    count = arguments["<count>"]
    logging.basicConfig(level=logging.DEBUG)
    
    messages_ = main(query=query, tag=tag, count=count)
    output_(messages_,query,tag,count)
    
    while True:
        
        adress = output_(messages_,query,tag,count)
        
        messages_ = None