#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import urlretrieve
import requests
from bs4 import BeautifulSoup
from os import remove
import random
from datetime import *
from dateutil.parser import *
import json
import numpy as np
import operator
try:
    import cookielib
except:
    import http.cookiejar as cookielib
try:
    from PIL import Image
except:
    pass

datas = {'active': 'verification'}
headers = {'Host':'bjllfx.com',
           'Referer': 'http://bjllfx.com/mbe/login.html',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
           'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
           'Accept': '*/*',
           'Accept-Language': 'zh-CN',
           'Accept-Encoding':'gzip, deflate',
           'Connection': 'Keep-Alive'}

def login():
    login_url = 'http://bjllfx.com/mbe/api/login.ashx'
    datas['mobile'] = '139########'
    datas['pwd'] = '********'
    datas['r'] = random.random()
    resp = session.post(login_url, data=datas, headers=headers)
    if resp.status_code == 200:
        session.cookies.save()
    else:
        return False
    return True

def book_car():
    #Input booking date
    number = -1
    while number < 0 or number > 2:
        str_number = input('Input a date - 0: Today; 1: T+1; 2: T+2 (Default) : ')
        if str_number.strip() == '':
            number = 2
        else:
            number = int(str_number)
         
#    book_date = parse(input('Please input booking date:')).date()
    today =  date.today()
    book_date = today + timedelta(days=number)
    print("Date Inputed: %s "% book_date.strftime('%Y-%m-%d'))
    #Query available time 
    headers = {'Host':'bjllfx.com',
           'Referer': 'http://bjllfx.com/mbe/online.html',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
           'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
           'Accept': '*/*',
           'Accept-Language': 'zh-CN',
           'Accept-Encoding':'gzip, deflate'}
    post_url = "http://bjllfx.com/mbe/api/online.ashx?r=0.943978761644576"
    post_data = {'active':'availabletime',
                 'trainerID':'123',
                 'carID':'51',
                 'hour':'2',
                 'service':'计时卡'}
    post_data['date'] = book_date.strftime('%Y-%m-%d')
    post_data['r'] = random.random()
    resp = session.post(post_url, data=post_data, headers=headers)
    resp.encoding = resp.apparent_encoding
    json_data = resp.json()
    msg = json_data.get('msg')
    #User logout, relogin
    if msg.strip() != 'success':
        print(msg)
        login()
        resp = session.post(post_url, data=post_data, headers=headers)
        resp.encoding = resp.apparent_encoding
        json_data = resp.json()

    data = json_data.get('data')[1:-1]

    #Car is not available on this day
    if data.strip() == '':
        print("Car is not available!")
        return False
    dict_data = eval(data)

    #Select a training time
    print("  ID      StartTime   EndTime")
    print("————————————")
    idx = 1
    if isinstance(dict_data, dict):
        option = dict_data
        start_time = int(option['startTime']) / 60
        end_time = int(option['endTime']) / 60
        print( "%3d)       %2d:00         %2d:00" % (idx,start_time, end_time), end='\n')
    else:
        for option in dict_data:
            start_time = int(option['startTime']) / 60
            end_time = int(option['endTime']) / 60
            print( "%3d)       %2d:00         %2d:00" % (idx,start_time, end_time), end='\n')
            idx = idx + 1
    print("————————————")
    return True
    number = 0
    while number < 1 or number > idx:
        number = int(input('Please input a number:  '))
    verify = 'N'
    while verify != 'Y':
        verify = input('Yes/No: ')[0].upper()
    return True
    post_data = {'active':'addOrder',
                 'cardNum':'192109',
                 'cardType':'12小时卡',
                 'cardService':'计时卡',
                 'cardPriceType':'110.00元/小时(新款帕萨特自动)',
                 'address':'丰台区东大街西里南二门',
                'date':'2019-5-28',
                 'trainerID':'123',
                 'trainerName':'李胜喜',
                 'trainerGrade':'1',
                 'trainerPhone':'15600718319',
                 'carID':'51',
                 'carName':'新款帕萨特自动',
                 'carNum':'京P0EM06',
                 'priceType':'110.00',
                 'service':'计时卡',
                 'note':''}
    post_data['itemTime'] = '{\"startTime\":'+str(dict_data[number-1]['startTime'])+',\"duration\":'+str(dict_data[number-1]['duration'])+'}'
    post_data['r'] = random.random()
    resp = session.post(post_url, data=post_data, headers=headers)
    resp.encoding = resp.apparent_encoding
#    print(resp)
    return True


if __name__ == '__main__':
    # try login with cookie at first
    session = requests.session()
    session.cookies = cookielib.LWPCookieJar(filename='YueChe_cookies')
    try:
        session.cookies.load(ignore_discard=True)
    except:
        print("Cookies load failed! \n")
        login()
        
    book_car()
