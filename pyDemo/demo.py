import asyncio
import datetime
import re
import time

import requests
# while 1:
#     resp=requests.post('https://bitkeep.com/marketApi/quotev2/getTokenMarket',json={"chain":"arbitrum","contract":"0x463913d3a3d3d291667d53b8325c598eb88d3b0e"})
#     print(resp.json()['data']['price'])
#     time.sleep(2)
headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41","cookie":"cf_clearance=AZeCWKZ4AcZ4k4G7m0_jwqZ0vwTqg7s8bW1IHHLt9m8-1676532903-0-160; chakra-ui-color-mode=dark; _ga=GA1.1.1029131385.1676532909; alertsMigration=1.0.0; watchlistInitialStateMigration=1.0.0; globalChartSettingsMigration=1.0.0; pairChartSettingsMigration=1.0.0; studyTemplatesMigration=1.0.0; watchlistsMigration=1.0.0; __cf_bm=thag8DXkDe0gdqct9ytTFcK37V4RYbRCaPCk1CzE5Zs-1676535399-0-AYpa9LVelLeWmcH0B4O+s+egpdiKcQiGcbak8rKDQLm13ckt7zdFPzpv/5/XdBSWA1IwY5VDceETihfOXOEPju0O/KupHlp+FTesrqUWWtN9; _ga_532KFVB4WT=GS1.1.1676532909.1.1.1676536662.60.0.0"}
# a=requests.post("https://dexscreener.com/arbitrum/0x751f3b8ca139bc1f3482b193297485f14208826a",headers=headers)
# print(a.text)
from pyquery import PyQuery as pq
def push(title, content):
    json = {
        "token": "e73179f25ade41729eae654a2decec15",
        "title": title,
        "content": content,
        "topic": "1",
        "template": "html"
    }
    requests.post(url='http://www.pushplus.plus/send/', json=json)
while 1:
    doc = pq(url='https://dexscreener.com/arbitrum/0x751f3b8ca139bc1f3482b193297485f14208826a',headers=headers)
    price=float(re.search(r'\$.*? ',doc('title').text()).group().replace('$',''))
    print(datetime.datetime.now(),price,price-0.1830,(price-0.1830)/0.001830)
    if price>=0.2730:
        push('sliz',price)
        break
    time.sleep(60)

# print(price=int(re.search(r'\$.*? ',doc('title').text()).group()))

