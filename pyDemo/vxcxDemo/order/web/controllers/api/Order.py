# -*- coding: utf-8 -*-
from web.controllers.api import route_api
from flask import request, jsonify,g
from application import app, db
import json, decimal
from common.models.food.Food import Food
from common.libs.UrlManager import UrlManager
from common.libs.Helper import getCurrentDate
from common.libs.member.CartService import CartService
from common.models.member.OauthMemberBind import OauthMemberBind
from common.libs.pay.PayService import PayService

@route_api.route("/order/info", methods=[ "POST" ])
def orderInfo():
	resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
	req = request.values
	params_goods = req['goods'] if 'goods' in req else None
	member_info = g.member_info
	params_goods_list = []
	if params_goods:
		params_goods_list = json.loads(params_goods)

	food_dic = {}
	for item in params_goods_list:
		food_dic[item['id']] = item['number']

	food_ids = food_dic.keys()
	food_list = Food.query.filter(Food.id.in_(food_ids)).all()
	data_food_list = []
	yun_price = pay_price = decimal.Decimal(0.00)
	if food_list:
		for item in food_list:
			tmp_data = {
				"id": item.id,
				"name": item.name,
				"price": str(item.price),
				'pic_url': UrlManager.buildImageUrl(item.main_image),
				'number': food_dic[item.id]
			}
			pay_price = pay_price + item.price * int( food_dic[item.id] )
			data_food_list.append(tmp_data)

	# 获取地址
		default_address = {
			"name": "虚幻私塾",
			"mobile": "12345678901",
			"address": "上海市浦东新区XX",
		}

	resp['data']['food_list'] = data_food_list
	resp['data']['pay_price'] = str(pay_price)
	resp['data']['yun_price'] = str(yun_price)
	resp['data']['total_price'] = str(pay_price + yun_price)
	resp['data']['default_address'] = default_address
	return jsonify(resp)




@route_api.route("/order/create", methods=[ "POST"])
def orderCreate():
	resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
	req = request.values
	type = req['type'] if 'type' in req else ''
	note = req['note'] if 'note' in req else ''
	params_goods = req['goods'] if 'goods' in req else None

	items = []
	if params_goods:
		items = json.loads(params_goods)

	if len( items ) < 1:
		resp['code'] = -1
		resp['msg'] = "下单失败：没有选择商品~~"
		return jsonify(resp)

	member_info = g.member_info
	target = PayService()
	params = {
	}
	resp = target.createOrder( member_info.id ,items ,params)
	#如果是来源购物车的，下单成功将下单的商品去掉
	if resp['code'] == 200 and type == "cart":
		CartService.deleteItem( member_info.id,items )

	return jsonify( resp )
