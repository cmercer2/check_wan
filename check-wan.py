#!/usr/bin/env python
"""
Check current wan and log changes to txt file
"""

import subprocess
from datetime import datetime, date, time
import logging

current_wan = None
new_wan = None
cmd = "dig TXT +short o-o.myaddr.l.google.com @ns1.google.com | sed 's/\"//g'"
current_time = datetime.now().__format__("%a %m-%d-%y %I:%M:%S %p")
file_handle = open("wan-ip-log.txt", "a+")
logging.basicConfig(filename="check-wan.log",level=logging.DEBUG)

def main():
    new = getNewWan()
    current = getCurrentWan()
    compareWans(new, current)

#get new wan ip from google dns
def getNewWan():    
    new_wan = subprocess.check_output(cmd, shell=True, universal_newlines=True).strip()
    print("new_wan: {new}".format(new=new_wan))
    return new_wan

#get current wan from file
def getCurrentWan():
    file_handle.seek(0)
    file_line_list = file_handle.readlines()
    try:
        current_wan = file_line_list[-1]
        ip, date = current_wan.split(",")
        print("current_wan: {ip}".format(ip=ip))
        return ip
    except IndexError as error:
        logging.exception(error)
        logging.error("No WAN found in file, ending script")

#compare new wan to current wan, skip write if the same
def compareWans(new_wan, current_wan): 
    print("new_wan: {new}, current_wan: {current}".format(new=new_wan, current=current_wan))   
    if(new_wan == current_wan):
        print("no change")
        logging.info("IP did not change, ending script on {date}, new_wan: {new}, current_wan: {current}".format(date=current_time, new=new_wan, current=current_wan))
    else:
        print("changed")
        file_handle.write("{new}, {date}\n".format(new=new_wan, date=current_time))
        logging.info("New Wan IP detected, logging to file on {date}".format(date=current_time))    
    file_handle.close()

main()
exit()