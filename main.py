#coding=utf8
import itchat, time
import requests
import io
import random
import urllib.request
from itchat.content import *

from scrapy.http import HtmlResponse
from scrapy.selector import Selector

image_name = 'tmp.gif' # to-do
GIF_TRIGGER = '/g'

def get_image(key_word):
    if not key_word:
        key_word = '啦啦啦'
    url = f'http://www.gifmiao.com/search/{key_word}/3'
    xpath = "//img[@class='gifImg']/@xgif"
    r = requests.get(url)
    image_list = Selector(text=r.content).xpath(xpath).extract()
    image_url = image_list[random.randint(0, len(image_list)-1)]
    urllib.request.urlretrieve(image_url, image_name)
    print(f'send image url: {image_url}')


def gif_process(spllited, receiver):
    key_word = ''
    if len(spllited) > 1:
        key_word = spllited[1]
    print(f'get key word {key_word}')
    get_image(key_word)
    itchat.send_image(image_name, toUserName=receiver)


@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    spllited = msg['Text'].split(' ')
    if spllited[0] == GIF_TRIGGER:
        gif_process(spllited, msg['ToUserName'])

itchat.auto_login(True)
itchat.run()
