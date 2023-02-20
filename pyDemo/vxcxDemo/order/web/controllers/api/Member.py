import json
from web.controllers.api import route_api
from flask import request,jsonify,g
from common.models.food.WxShareHistory import WxShareHistory
from application import app,db
import requests
from common.models.member.Member import Member
from common.models.member.OauthMemberBind import OauthMemberBind
from common.libs.Helper import getCurrentDate
from common.libs.member.MemberService import MemberService


@route_api.route( "/member/login", methods = ['GET', 'POST'] )
def login():
    resp = {'code':200,'msg':'操作成功', 'data':{}}
    req = request.values
    #app.logger.info(req)


    code = req['code'] if 'code' in req else ''
    if not code or len(code)<1:
        resp['code'] = -1
        resp['msg'] = '需要code'
        return jsonify(resp)

    openid =  MemberService.getWeChatOpenId(code)
    if openid is None:
        resp['code'] = -1
        resp['msg'] = '调用微信出错'
        return jsonify(resp)
    '''
    判断是否已经注册过，已注册直接返回信息
    '''
    bind_info = OauthMemberBind.query.filter_by(openid=openid,type=1).first()
    if not bind_info:
        nickname = req['nickname'] if 'nickname' in req else ''
        sex = req['gender'] if 'gender' in req else ''
        avatar = req['avatarUrl'] if 'avatarUrl' in req else ''

        model_name = Member()
        model_name.nickname = nickname
        model_name.sex = sex
        model_name.avatar = avatar
        model_name.salt = MemberService.geneSalt()
        model_name.updated_time = model_name.created_time = getCurrentDate()
        db.session.add(model_name)
        db.session.commit()

        model_bind = OauthMemberBind()
        model_bind.member_id = model_name.id
        model_bind.type = 1
        model_bind.openid = openid
        model_bind.extra = ''
        model_bind.updated_time = model_bind.created_time = getCurrentDate()
        db.session.add(model_bind)
        db.session.commit()

        bind_info = model_bind

    member_info = Member.query.filter_by(id = bind_info.member_id).first()
    token = "%s#%s" % (MemberService.geneAuthCode(member_info), member_info.id)
    resp['data'] = {'token': token}
    return jsonify(resp)

@route_api.route( "/member/check-reg", methods = ['GET', 'POST'] )
def checkReg():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    # app.logger.info(req)

    code = req['code'] if 'code' in req else ''
    if not code or len(code) < 1:
        resp['code'] = -1
        resp['msg'] = '需要code'
        return jsonify(resp)

    openid = MemberService.getWeChatOpenId(code)
    if openid is None:
        resp['code'] = -1
        resp['msg'] = '調用微信出錯'
        return jsonify(resp)

    # 判断是否注册过，没有注册就注册
    bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()

    if not bind_info:
        resp['code'] = -1
        resp['msg'] = '未绑定'
        return jsonify(resp)

    member_info = Member.query.filter_by(id=bind_info.member_id).first()
    if not member_info:
        resp['code'] = -1
        resp['msg'] = '没有查询到绑定信息'
        return jsonify(resp)

    token = "%s#%s"%(MemberService.geneAuthCode(member_info),member_info.id)
    resp['data'] = {'token':token}
    return jsonify(resp)



@route_api.route("/member/share",methods = [ "POST" ])
def memberShare():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    url = req['url'] if 'url' in req else ''
    member_info = g.member_info
    model_share = WxShareHistory()
    if member_info:
        model_share.member_id = member_info.id
    model_share.share_url = url
    model_share.created_time = getCurrentDate()
    db.session.add(model_share)
    db.session.commit()
    return jsonify(resp)

@route_api.route("/member/info")
def memberInfo():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    member_info = g.member_info
    resp['data']['info'] = {
        "nickname":member_info.nickname,
        "avatar_url":member_info.avatar
    }
    return jsonify(resp)
