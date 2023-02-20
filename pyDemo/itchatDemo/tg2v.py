# -*- encoding=utf8 -*-
__author__ = "颜立全"

import time

import requests

import telebot
from discord_webhook import DiscordWebhook, DiscordEmbed

bot = telebot.TeleBot("6291256191:AAExAaaagpZgEAdBvhOMRN2JxlXr8om4qJA")
def floor(slug):
    nft=requests.get('https://app.nfttrack.ai/api/search?q='+slug).json()['data']['collections'][0]['opensea_slug']
    res=requests.get('https://app.nfttrack.ai/api/collection_info/'+nft)
    return nft+'地板：'+str(res.json()['data']['floor_price'])

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        name=message.from_user.first_name +message.from_user.last_name

    except:
        name=message.from_user.first_name
    try:
        reply = '\nreply2:\n'+message.reply_to_message.text
    except:
        reply=''
    json = {
        "msgtype": "text",
        "text": {
            "content": name+ ':\n' + message.text+reply,
        }
    }
    requests.post('https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=dc326a08-1641-4d78-b5ac-24f143ae7449',
                  json=json)
    print(name+ ':\t' + message.text)
bot.infinity_polling()
