# -*- coding: utf-8 -*-
SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1/mysql?charset=utf8mb4'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SERVER_PORT = 8999
DEBUG = False
SQLALCHEMY_ECHO  = False
AUTH_COOKIE_NAME = "mooc_food"
#过滤url
IGNORE_URLS = [
    r"^/user/login"
]

IGNORE_CHECK_LOGIN_URLS = [
    r"^/static",
    r"^/favicon.ico"
]
API_IGNORE_URLS = [
    "^/api"
]
PAGE_SIZE=1
PAGE_DISPLAY=10
STATUS_MAPPING = {
    "1":"正常",
    "0":"已删除"
}
BADDEST_APP = {
    'appid' : 'wx024268fffe7368d2',
    'appkey' : '1ed17c6f10d03781e50a8c543dde4103'
}
UPLOAD = {
    'ext':[ 'jpg','gif','bmp','jpeg','png' ],
    'prefix_path':'/web/static/upload/',
    'prefix_url':'/static/upload/'
}
APP = {
    'domain':'http://92bpak.natappfree.cc/'
}


PAY_STATUS_DISPLAY_MAPPING = {
    "0":"订单关闭",
    "1":"支付成功",
    "-8":"待支付",
    "-7":"待发货",
    "-6":"待确认",
    "-5":"待评价"
}

