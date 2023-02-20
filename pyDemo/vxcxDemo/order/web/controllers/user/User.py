# -*- coding: utf-8 -*-
from flask import Blueprint,request,jsonify,make_response,redirect,g
from common.libs.UrlManager import UrlManager
import json
from common.models.User import User
from common.libs.user.UserService import UserService
from application import app,db
from common.libs.Helper import ops_render

route_user = Blueprint( 'user_page',__name__ )


@route_user.route( "/edit" , methods=["GET", "POST"] )
def edit():
    if request.method == "GET":
        return ops_render( "user/edit.html" ,{'current':'edit'})

    resp = {'code':200,'msg':'操作成功', 'data':{}}

    req = request.values
    nickname = req['nickname'] if 'nickname' in req else ''
    email = req['email'] if 'email' in req else ''

    if nickname is None or len(nickname)<1:
        resp['code']=-1
        resp['msg']='请输入符合规范的姓名'
        return jsonify(resp)

    if email is None or len(email)<1:
        resp['code']=-1
        resp['msg']='请输入符合规范的邮箱'
        return jsonify(resp)

    user_info = g.current_user
    user_info.nickname = nickname
    user_info.email = email

    db.session.add(user_info)
    db.session.commit()
    return jsonify(resp)


@route_user.route( "/login", methods = ["GET", "POST"] )
def login():
    if request.method == "GET":
        return ops_render( "user/login.html" )

    req = request.values
    login_name = req['login_name'] if 'login_name' in req else ''
    login_pwd = req['login_pwd'] if 'login_pwd' in req else ''

    resp = {'code':200, 'msg':'登录成功', 'data':{}}
    if login_name is None or len(login_name)<1:
        resp['code']=-1
        resp['msg']="请输入正确的登录用户名~"
        return jsonify(resp)

    if login_pwd is None or len(login_pwd)<1:
        resp['code']=-1
        resp['msg']="请输入正确的登录密码~"
        return jsonify(resp)

    user_info = User.query.filter_by(login_name=login_name).first()
    print('============',type(user_info))
    if not user_info:
        resp['code'] = -1
        resp['msg'] = "请输入正确的登录用户名和密码1"
        return jsonify(resp)

    if user_info.login_pwd != UserService.genePwd(login_pwd,user_info.login_salt):
        resp['code'] = -1
        resp['msg'] = "请输入正确的登录用户名和密码2"
        return jsonify(resp)

    # if user_info != 1:
    #     resp['code'] = -1
    #     resp['msg'] = '账号已经被删除，请联系管理员处理'
    #     return jsonify(resp)

    responce = make_response(json.dumps(resp))
    responce.set_cookie(app.config["AUTH_COOKIE_NAME"], "%s#%s"%(UserService.geneAuthCode(user_info), user_info.uid))


    return responce



@route_user.route( "/logout")
def logout():
    responce = make_response( redirect( UrlManager.buildUrl("/user/login") ) )
    responce.delete_cookie(app.config["AUTH_COOKIE_NAME"])
    return responce

@route_user.route( "/reset-pwd" , methods=["GET", "POST"])
def resetPwd():
    if request.method == "GET":
        return ops_render( "user/reset_pwd.html",{'current':'reset_pwd'} )

    resp = {'code': 200, 'msg': '操作成功', 'data': {}}

    req = request.values
    old_password = req['old_password'] if 'old_password' in req else ''
    new_password = req['new_password'] if 'new_password' in req else ''

    if old_password is None or len(old_password) < 6:
        resp['code'] = -1
        resp['msg'] = '请输入符合规范的原密码'
        return jsonify(resp)

    if new_password is None or len(new_password) < 6:
        resp['code'] = -1
        resp['msg'] = '请输入符合规范的修改后的密码'
        return jsonify(resp)

    if old_password == new_password:
        resp['code'] = -1
        resp['msg'] = '密码相同，请再次输入'
        return jsonify(resp)

    user_info = g.current_user
    user_info.login_pwd = UserService.genePwd(new_password, user_info.login_salt)

    db.session.add(user_info)
    db.session.commit()

    responce = make_response(json.dumps(resp))
    responce.set_cookie(app.config["AUTH_COOKIE_NAME"], "%s#%s" % (UserService.geneAuthCode(user_info), user_info.uid))


    return jsonify(resp)


