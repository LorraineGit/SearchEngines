# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import time
import Queue

q = Queue.Queue()
link_list = []
sy = {'link':'http://www.view.sdu.edu.cn/','title':'shandashouye'}
link_list.append(sy)

def add(l, t):

    dic = {'link': l, 'title': t}
    is_in = 0
    for i in range(len(link_list)):
        if (l == link_list[i]['link']):
            is_in = 1
            break
    if (is_in == 0):
        q.put(l)
        link_list.append(dic)

def search_link(url):
    print url
    headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
    all_url = 'http://www.view.sdu.edu.cn/'
    news_url = 'http://www.view.sdu.edu.cn/new/'
    start_html = requests.get(url,  headers=headers)

    Soup = BeautifulSoup(start_html.text, 'lxml')
    all_a = Soup.find_all('a')
    dic = {}

    for a in all_a:

            link = a['href']
            str_link = str(link)
            title = a.get_text()

            if title is None:

                start_html = requests.get(str_link, headers=headers)
                Soup = BeautifulSoup(start_html.text, 'lxml')
                title = Soup.find('head').find('title')
                title = title.split('_')[0]
                print title

            if (str_link.__contains__('http') and not str_link.__contains__(all_url)):
                print 'outside website'
            if(str_link.__contains__(all_url)):
                add(str_link, title)
            if (not str_link.__contains__('http')):
                if (str_link.__contains__('jpg')):
                    print 'jpg'
                else:
                    if (str_link.__contains__('comment')):
                         print 'comment'
                    else:
                        if (str_link.__contains__('doc')):
                            print 'doc'
                        else:
                            if (str_link.__contains__('new')):
                                str_link = all_url + str_link
                            else:
                                str_link = news_url + str_link

                            add(str_link, title)


    while not q.empty():
        url = q.get()
        print url

        try:
            search_link(url)
        except:
            print 'wrong url'


if __name__ == '__main__':
    search_link('http://www.view.sdu.edu.cn/')
    print len(link_list)
    for i in range(len(link_list)):
        if (link_list[i]['link'] == "http://www.view.sdu.edu.cn/new/2017/0421/89944.html" ):
            print link_list[i]['title'].decode('gbk')
