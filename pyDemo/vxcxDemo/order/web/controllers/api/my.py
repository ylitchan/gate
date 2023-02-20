# -*- coding: utf-8 -*-
from web.controllers.api import route_api
from flask import request, jsonify,g
from common.models.food.Food import Food
from application import app,db
from common.models.pay.PayOrder import PayOrder
from common.models.pay.PayOrderItem import PayOrderItem
from common.libs.UrlManager import UrlManager
from common.libs.Helper import selectFilterObj,getDictFilterField,getCurrentDate
from common.models.member.MemberComments import MemberComments
import json,datetime
from common.models.member.MemberAddress import MemberAddress
@route_api.route("/my/order")
def myOrderList():
	resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
	member_info = g.member_info
	req = request.values
	status = int( req['status'] ) if 'status' in req else 0
	query = PayOrder.query.filter_by( member_id = member_info.id )
	if status == -8 :#等待付款
		query = query.filter( PayOrder.status == -8 )
	elif status == -7:#待发货
		query = query.filter( PayOrder.status == 1,PayOrder.express_status == -7,PayOrder.comment_status == 0 )
	elif status == -6:#待确认
		query = query.filter(PayOrder.status == 1, PayOrder.express_status == -6,PayOrder.comment_status == 0)
	elif status == -5:#待评价
		query = query.filter(PayOrder.status == 1, PayOrder.express_status == 1,PayOrder.comment_status == 0)
	elif status == 1:#已完成
		query = query.filter(PayOrder.status == 1, PayOrder.express_status == 1,PayOrder.comment_status == 1 )
	else:
		query = query.filter( PayOrder.status == 0 )

	pay_order_list = query.order_by( PayOrder.id.desc() ).all()
	data_pay_order_list = []
	if pay_order_list:
		pay_order_ids = selectFilterObj( pay_order_list,"id" )
		pay_order_item_list = PayOrderItem.query.filter( PayOrderItem.pay_order_id.in_( pay_order_ids ) ).all()
		food_ids = selectFilterObj( pay_order_item_list,"food_id" )
		food_map = getDictFilterField( Food,Food.id,"id",food_ids )
		pay_order_item_map = {}
		if pay_order_item_list:
			for item in pay_order_item_list:
				if item.pay_order_id not in pay_order_item_map:
					pay_order_item_map[ item.pay_order_id ] = []

				tmp_food_info = food_map[ item.food_id ]
				pay_order_item_map[item.pay_order_id].append({
					'id':item.id,
					'food_id':item.food_id,
					'quantity':item.quantity,
					'price':str( item.price ),
					'pic_url':UrlManager.buildImageUrl( tmp_food_info.main_image ),
					'name':tmp_food_info.name
				})


		for item in pay_order_list:
			tmp_data = {
				'status':item.pay_status,
				'status_desc':item.status_desc,
				'date':item.created_time.strftime("%Y-%m-%d %H:%M:%S"),
				'order_number':item.order_number,
				'order_sn':item.order_sn,
				'note':item.note,
				'total_price':str( item.total_price ),
				'goods_list':pay_order_item_map[ item.id ]
			}

			data_pay_order_list.append( tmp_data )
	resp['data']['pay_order_list'] = data_pay_order_list
	return jsonify(resp)


@route_api.route("/my/comment/list" )
def myCommentList():
	resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
	member_info = g.member_info
	comment_list = MemberComments.query.filter_by( member_id=member_info.id )\
		.order_by(MemberComments.id.desc()).all()
	data_comment_list = []
	if comment_list:
		pay_order_ids = selectFilterObj( comment_list,"pay_order_id" )
		pay_order_map = getDictFilterField( PayOrder,PayOrder.id,"id",pay_order_ids )
		for item in comment_list:
			tmp_pay_order_info = pay_order_map[ item.pay_order_id ]
			tmp_data = {
				"date":item.created_time.strftime("%Y-%m-%d %H:%M:%S"),
				"content":item.content,
				"order_number":tmp_pay_order_info.order_number
			}
			data_comment_list.append( tmp_data )
	resp['data']['list'] = data_comment_list
	return jsonify(resp)


@route_api.route("/my/address/index")
def myAddressList():
	resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
	member_info = g.member_info
	list = MemberAddress.query.filter_by( status = 1, member_id = member_info.id )\
		.order_by( MemberAddress.id.desc() ).all()
	data_list = []
	if list:
		for item in list:
			tmp_data = {
				"id":item.id,
				"nickname":item.nickname,
				"mobile":item.mobile,
				"is_default":item.is_default,
				"address":"%s%s%s%s"%( item.province_str,item.city_str,item.area_str,item.address ),
			}
			data_list.append( tmp_data )
	resp['data']['list'] = data_list
	return jsonify(resp)

@route_api.route("/my/address/set",methods = [ "POST" ])
def myAddressSet():
	resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
	req = request.values
	id = int( req['id'] ) if 'id' in req and req['id'] else 0
	nickname = req['nickname'] if 'nickname' in req else ''
	address = req['address'] if 'address' in req else ''
	mobile = req['mobile'] if 'mobile' in req else ''

	province_id = int( req['province_id'] ) if ( 'province_id' in req and req['province_id'] ) else 0
	province_str = req['province_str'] if 'province_str' in req else ''
	city_id = int( req['city_id'] ) if (  'city_id' in req  and  req['city_id'])else 0
	city_str = req['city_str'] if 'city_str' in req else ''
	district_id = int( req['district_id'] ) if ( 'district_id' in req and req['district_id'] ) else 0
	district_str = req['district_str'] if 'district_str' in req else ''

	member_info = g.member_info

	if not nickname:
		resp['code'] = -1
		resp['msg'] = "请填写联系人姓名~~"
		return jsonify(resp)

	if not mobile:
		resp['code'] = -1
		resp['msg'] = "请填写手机号码~~"
		return jsonify(resp)

	if province_id < 1:
		resp['code'] = -1
		resp['msg'] = "请选择地区~~"
		return jsonify(resp)

	if city_id < 1:
		resp['code'] = -1
		resp['msg'] = "请选择地区~~"
		return jsonify(resp)

	if district_id < 1:
		district_str = ''

	if not address:
		resp['code'] = -1
		resp['msg'] = "请填写详细地址~~"
		return jsonify(resp)

	if not member_info:
		resp['code'] = -1
		resp['msg'] = "系统繁忙，请稍后再试~~"
		return jsonify(resp)

	address_info = MemberAddress.query.filter_by( id = id,member_id = member_info.id ).first()
	if address_info:
		model_address = address_info
	else:
		default_address_count = MemberAddress.query.filter_by( is_default = 1,member_id = member_info.id ,status = 1).count()
		model_address = MemberAddress()
		model_address.member_id = member_info.id
		model_address.is_default = 1 if default_address_count == 0 else 0
		model_address.created_time = getCurrentDate()

	model_address.nickname = nickname
	model_address.mobile = mobile
	model_address.address = address
	model_address.province_id = province_id
	model_address.province_str = province_str
	model_address.city_id = city_id
	model_address.city_str = city_str
	model_address.area_id = district_id
	model_address.area_str = district_str
	model_address.updated_time = getCurrentDate()
	db.session.add(model_address )
	db.session.commit()
	return jsonify(resp)

@route_api.route("/my/address/info")
def myAddressInfo():
	resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
	req = request.values
	id = int( req['id'] ) if 'id' in req else 0
	member_info = g.member_info

	if id < 1 or  not member_info:
		resp['code'] = -1
		resp['msg'] = "系统繁忙，请稍后再试~~"
		return jsonify(resp)

	address_info = MemberAddress.query.filter_by( id = id ).first()
	if not address_info:
		resp['code'] = -1
		resp['msg'] = "系统繁忙，请稍后再试~~"
		return jsonify(resp)

	resp['data']['info'] = {
		"nickname":address_info.nickname,
		"mobile":address_info.mobile,
		"address":address_info.address,
		"province_id":address_info.province_id,
		"province_str":address_info.province_str,
		"city_id":address_info.city_id,
		"city_str":address_info.city_str,
		"area_id":address_info.area_id,
		"area_str":address_info.area_str
	}
	return jsonify(resp)


@route_api.route("/my/address/ops",methods = [ "POST" ])
def myAddressOps():
	resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
	req = request.values
	id = int(req['id']) if 'id' in req else 0
	act = req['act'] if 'act' in req else ''
	member_info = g.member_info

	if id < 1 or not member_info:
		resp['code'] = -1
		resp['msg'] = "系统繁忙，请稍后再试~~"
		return jsonify(resp)

	address_info = MemberAddress.query.filter_by(id=id,member_id = member_info.id).first()
	if not address_info:
		resp['code'] = -1
		resp['msg'] = "系统繁忙，请稍后再试~~"
		return jsonify(resp)

	if act == "del":
		address_info.status = 0
		address_info.updated_time = getCurrentDate()
		db.session.add(address_info)
		db.session.commit()
	elif act == "default":
		MemberAddress.query.filter_by( member_id=member_info.id)\
			.update({ 'is_default' :0 })
		address_info.is_default = 1
		address_info.updated_time = getCurrentDate()
		db.session.add(address_info)
		db.session.commit()
	return jsonify(resp)
