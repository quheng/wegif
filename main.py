#coding=utf8
import itchat, time
import requests
import io
import random
import urllib.request

from scrapy.http import HtmlResponse
from scrapy.selector import Selector

image_name = 'tmp.gif' # to-do
TRIGGER_WORD = '/gif'

def get_image(key_word):
    url = f'http://www.gifmiao.com/search/{key_word}/3'
    xpath = "//img[@class='gifImg']/@xgif"
    r = requests.get(url)
    image_list = Selector(text=r.content).xpath(xpath).extract()
    image_url = image_list[random.randint(0, len(image_list)-1)]
    urllib.request.urlretrieve(image_url, image_name)
    print(f'send image url: {image_url}')


@itchat.msg_register([itchat.content.TEXT])
def text_reply(msg):
    me = itchat.search_friends()['UserName']
    if me ==  msg['FromUserName']:
        spllited = msg['Text'].split(' ')
        if spllited[0] == TRIGGER_WORD:
            key_word = ''
            if len(spllited) > 0:
                key_word = spllited[1]
            print(f'get key word {key_word}')
            get_image(key_word)
            itchat.send_image(image_name, toUserName=msg['ToUserName'])


itchat.auto_login(True, enableCmdQR=2)
itchat.run()
