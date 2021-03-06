#!/usr/bin/env python
# -*- coding:utf-8 -*-
import random
from bs4 import BeautifulSoup
import requests
from  threading import Thread
import Queue



def random_choice(choice_lst):
    randomNum = random.randint(0,len(choice_lst)-1)
    return choice_lst[randomNum]




#多线程版本
def doubanrespinfo(url,queue):
    r = requests.get(url)
    htmlinfo = r.text
    soup = BeautifulSoup(htmlinfo,"html5lib")
    book_section = soup.find_all("tr",class_="item")
    for i in book_section:
        #book image
        book_image = i.find("td",valign="top",width="100").a.img["src"]
        #book name 
        book_name = i.find("td",valign="top",width=False).a.get_text().replace("\n","").replace(' ', '').strip()
        #book score
        book_score = i.find("span",class_="rating_nums").get_text()
        try:
            book_score_float = float(book_score)
        except:
            book_score_float = 0.0
        queue.put({"book_name":book_name,"book_score":book_score_float,"book_img":book_image})
            
def getDouBanBooks(baseurl,pagelist):
    queue = Queue.Queue()
    threads = []
    for i in pagelist:
        url = baseurl %(i)
        t = Thread(target=doubanrespinfo,args=(url,queue,))
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    result = []
    while  not queue.empty():
        result.append(queue.get())
    result_book_list = sorted(result,key=lambda x:x.get('book_score',None),reverse=True)
    return result_book_list



