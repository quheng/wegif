#coding=utf8
import itchat
import os
import requests
import random
import urllib.request
from itchat.content import *
from scrapy.selector import Selector

GIF_TRIGGER = '/g'
TURING_TRIGGER = '/t'


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


def gif_process(spllited, receiver):
    key_word = ''
    if len(spllited) > 1:
        key_word = spllited[1]
    get_image(key_word, receiver)
    itchat.send_image(gif_path(receiver), toUserName=receiver)


def turing_process(spllited, receiver):
    url = 'http://www.tuling123.com/openapi/api'
    if len(spllited) < 2:
        return

    payload = {
        'key': os.environ['turingKey'],
        'info': ' '.join(spllited[1:]),
        'userid': receiver[1:]
    }

    res = requests.post(url, data=payload)
    resJson = res.json()
    code = resJson['code']
    if code == 100000:
        itchat.send(resJson['text'], receiver)
    elif code == 200000:
        itchat.send(f"{resJson['text']}: {resJson['url']}", receiver)
    elif code == 302000:
        info = resJson['list'][random.randrange(len(resJson))]
        itchat.send(f"{info['article']}: {info['detailurl']}", receiver)
    elif code == 308000:
        info = resJson['list'][random.randrange(len(resJson))]
        itchat.send(f"名称: {info['name']}, 简介：{info['info']}, 地址：{info['detailurl']}", receiver)


def incoming_msg(msg):
    fromUserName = msg['FromUserName']
    spllited = msg['Text'].split(' ')
    if spllited[0] == GIF_TRIGGER:
        gif_process(spllited, fromUserName)
    elif spllited[0] == TURING_TRIGGER:
        turing_process(spllited, fromUserName)


@itchat.msg_register(TEXT)
def text_reply(msg):
    incoming_msg(msg)


@itchat.msg_register(TEXT, isGroupChat=True)
def group_text_reply(msg):
    incoming_msg(msg)

# itchat.auto_login(True)
itchat.auto_login(True, enableCmdQR=True)
itchat.run()
