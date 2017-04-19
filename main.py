#coding=utf8
import itchat
import requests
import random
import urllib.request
from itchat.content import *
from scrapy.selector import Selector

GIF_TRIGGER = '/g'


def gif_path(name):
    return f'./gif/{name}.gif'


# The temporary use of the recipient the name of the store image
def get_image(key_word, receiver):
    if not key_word:
        key_word = '啦啦啦'
    url = f'http://www.gifmiao.com/search/{key_word}/3'
    xpath = "//img[@class='gifImg']/@xgif"
    r = requests.get(url)
    image_list = Selector(text=r.content).xpath(xpath).extract()
    image_url = image_list[random.randint(0, len(image_list)-1)]
    urllib.request.urlretrieve(image_url, gif_path(receiver))
    print(f'send image url: {image_url}')


def gif_process(spllited, receiver):
    key_word = ''
    if len(spllited) > 1:
        key_word = spllited[1]
    print(f'get key word {key_word}')
    get_image(key_word, receiver)
    print(receiver)
    itchat.send_image(gif_path(receiver), toUserName=receiver)


def incoming_msg(msg):
    fromUserName = msg['FromUserName']
    spllited = msg['Text'].split(' ')

    if spllited[0] == GIF_TRIGGER:
        gif_process(spllited, fromUserName)


@itchat.msg_register(TEXT)
def text_reply(msg):
    incoming_msg(msg)


@itchat.msg_register(TEXT, isGroupChat=True)
def group_text_reply(msg):
    incoming_msg(msg)


itchat.auto_login(True, enableCmdQR=True)
itchat.run()
