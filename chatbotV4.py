# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 23:50:42 2017

@author: Sikura
"""


# news source https://bits.media/news/
# btc exchange rate source https://yobit.net/
# scrape  http://docs.python-guide.org/en/latest/scenarios/scrape/
# name for a bot GET_NEWS
# t.me/GET_NEWS_CRYPTO_BOT
# token = 439823716:AAGm2J8pmDIw-olYyyDmf4BEIl6H8G6Bws0

# how to send message from browser-line https://api.telegram.org/bot439823716:AAGm2J8pmDIw-olYyyDmf4BEIl6H8G6Bws0/sendmessage?chat_id=407938124&text=where%27s_detonator

import requests
from lxml import html
from time import sleep

# https://api.telegram.org/bot439823716:AAGm2J8pmDIw-olYyyDmf4BEIl6H8G6Bws0/sendmessage?chat_id=407938124&text=where%27s_detonator


URL = 'https://api.telegram.org/bot'+'439823716:AAGm2J8pmDIw-olYyyDmf4BEIl6H8G6Bws0'+'/'

global last_update_id
last_update_id = 0

def get_updates():
    url = URL + 'getupdates'
    r = requests.get(url)
    return r.json()

 
def get_message():
    
    #we have to answer only for a new messages
    # that's why we get update_id of each new message and copmpare 
    # it with a last update id
    
    data = get_updates()
    last_object = data['result'][-1]
    current_update_id = last_object['update_id']
    
    global last_update_id
    if last_update_id != current_update_id:
        last_update_id = current_update_id
        chat_id = last_object['message']['chat']['id']
        message_text = last_object['message']['text']
        message = {'chat_id':chat_id, 'text': message_text}
        return message
    return None

def send_message(chat_id, text='Wait a second please...'):
    url = URL+'sendmessage?chat_id={}&text={}'.format(chat_id, text)
    requests.get(url)
    
# 2 functions to get cryptocurrency exchange rate
def get_btc():
    url = 'https://yobit.net/api/2/btc_usd/ticker'
    response = requests.get(url).json()
    price = (response['ticker']['last'])
    return 'Курс bitcoin '+str(price)+' usd'

def get_ltc():
    url = 'https://yobit.net/api/2/ltc_usd/ticker'
    response = requests.get(url).json()
    price = (response['ticker']['last'])
    return 'Курс litecoin '+str(price)+' usd'

# function to get news from website
def get_news():
    page = requests.get("https://bits.media/news/").text
    doc = html.fromstring(page)

    i =-8
    z=1
    t=""
    nl = '\n'
    while i <-1:
        a = ("https://bits.media/news/"+doc.cssselect("li a")[i].get('href') )
        t=t+nl+str(z)+') '+(doc.cssselect("li a")[i].text_content())+nl+'Читать подробнее:'+nl+a+nl+nl
        i=i+1
        z=z+1
        
    return t

def main():
        
    answer = get_message()  
    chat_id = answer['chat_id']
    send_message(chat_id,'Доброго времени суток! Я могу помочь вам узнать последние новости из мира криптовалют, а также курсы криптовалют bitcoin и litecoin' )
    while True: 
        answer = get_message()
        
        if answer != None:
            chat_id = answer['chat_id']
            text = answer['text']
            if text == '/news': 
                send_message(chat_id, get_news())
            elif text == '/btc':
                send_message(chat_id, get_btc())
            elif text == '/ltc':
                send_message(chat_id, get_ltc())
            elif 'привет' or 'hello' or 'hi' or 'Здравствуйте' or 'Привет' in text:
                send_message(chat_id, 'Воспользуйтесь командами бота для получения курса криптовалют или новостей из мира риптовалют')
        else:
            continue
        
        sleep(2)
           
if __name__ == '__main__':
    main()