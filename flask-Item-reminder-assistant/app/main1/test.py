import random
from flask import jsonify, redirect, render_template, request, flash, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql

pymysql.install_as_MySQLdb()
from . import main
from .errors import bad_request, servererror
from app.models import *
from app.run import db
import datetime
from sqlalchemy import or_, and_


def gengenerateID():
    re = ""
    for i in range(128):
        re += chr(random.randint(65, 90))
    return re


# 增加物品
@main.route("/createobject", methods=['POST'])
def createobject():
    if request.method == 'POST':
        username = request.get_json()['username']
        information = request.get_json()['information']
        expiration_time = request.get_json()['expiration_time']
        t = request.get_json()['reminder_time']
        type = request.get_json()['type']
        type = type.split("/")
        if not all([username, information, expiration_time, t, type]):
            return bad_request('missing param')
        expiration_time = datetime.datetime.strptime(expiration_time, '%Y-%m-%d %H:%M:%S')
        reminder_time = expiration_time - datetime.timedelta(seconds=int(t))
        time = expiration_time - datetime.datetime.now()
        k = time.days * 86400 + time.seconds
        print(k)
        if expiration_time < datetime.datetime.now():
            state = '已过期'
        elif k > int(t):
            state = '未过期'
        else:
            state = '快过期'
        try:
            while 1:
                ID = gengenerateID()
                str2 = Object.query.filter_by(id=ID).first()
                if not str2: break
            inf = Object(username=username, information=information, expiration_time=expiration_time,
                         reminder_time=reminder_time, state=state, id=ID)
            for j in type:
                o = db.session.query(ObjectType).filter_by(id=j).first()
                inf.obt.append(o)
            db.session.add(inf)
            db.session.commit()
            response = jsonify({'data': {
                'username': username,
                'information': information,
                'expiration_time': expiration_time,
                'reminder_time': reminder_time,
                'type': type,
                'state': state,
                'id': ID,
            }, 'message': 'OK', 'code': 200}
            )
            response.status_code = 200
            return response
        except Exception as e:
            raise e


# 修改物品
@main.route("/modifyobject", methods=['POST'])
def modifyobject():
    if request.method == 'POST':
        id = request.get_json()['id']
        username = request.get_json()['username']
        information = request.get_json()['information']
        expiration_time = request.get_json()['expiration_time']
        t = request.get_json()['reminder_time']
        state = ""
        reminder_time = ""
        type = request.get_json()['type']
        if not all([id]):
            return bad_request('missing param')
        try:
            if expiration_time and t:
                expiration_time = datetime.datetime.strptime(expiration_time, '%Y-%m-%d %H:%M:%S')
                reminder_time = expiration_time - datetime.timedelta(seconds=int(t))
                time = expiration_time - datetime.datetime.now()
                k = time.days * 86400 + time.seconds
                if expiration_time < datetime.datetime.now():
                    state = '已过期'
                elif k > int(t):
                    state = '未过期'
                else:
                    state = '快过期'
                db.session.query(Object).filter(Object.id == id).update(
                    {Object.expiration_time: expiration_time, Object.reminder_time: reminder_time, Object.state: state})
            if information:
                db.session.query(Object).filter(Object.id == id).update({Object.information: information})
            if type:
                type = type.split("/")
                db.session.query(Connect).filter(Connect.object_id == id).delete()
                for j in type:
                    inf = Connect(object_id=id, type_id=j)
                    db.session.add(inf)
            db.session.commit()
            response = jsonify({'data': {
                'username': username,
                'information': information,
                'expiration_time': expiration_time,
                'reminder_time': reminder_time,
                'type': type,
                'state': state,
            }, 'message': 'OK', 'code': 200}
            )
            response.status_code = 200
            return response
        except Exception as e:
            raise e


# 删除所有object记录
@main.route("/deleteallobject", methods=['POST'])
def deleteallobject():
    secret=request.get_json()['secret']
    if secret=="藏羚羊":
        db.session.query(Object).filter(1 == 1).delete()
        db.session.commit()
        return jsonify({'data': {}, 'message': 'OK', 'code': 200}
                       )
    else:return bad_request('password error')

# 增加物品类型
@main.route("/createobjecttype", methods=['POST'])
def createobjecttype():
    if request.method == 'POST':
        username = request.get_json()['username']
        type = request.get_json()['type']
        if not all([username, type]):
            return bad_request('missing param')
        try:
            while 1:
                ID = gengenerateID()
                str2 = Object.query.filter_by(id=ID).first()
                if not str2: break
            inf = ObjectType(username=username, type=type, id=ID)
            db.session.add(inf)
            db.session.commit()
            response = jsonify({'data': {
                'username': username,
                'type': type,
                'id': ID,
            }, 'message': 'OK', 'code': 200}
            )
            response.status_code = 200
            return response
        except Exception as e:
            raise e


# 修改物品类型的名称
@main.route("/modifyobjecttype", methods=['POST'])
def modifyobjecttype():
    if request.method == 'POST':
        id = request.get_json()['id']
        type = request.get_json()['type']
        if not all([id, type]):
            return bad_request('missing param')
        try:
            inf = db.session.query(ObjectType).filter(ObjectType.id == id).first()
            inf.type=type
            db.session.commit()
            response = jsonify({'data': {
                'type': type,
                'id': id,
                'username':inf.username
            }, 'message': 'OK', 'code': 200}
            )
            response.status_code = 200
            return response
        except Exception as e:
            raise e

# 删除对应id的Object
@main.route("/deleteobject", methods=['POST'])
def deleteobject():
    id = request.get_json()['id']
    db.session.query(Object).filter(Object.id == id).delete()
    db.session.query(Connect).filter(Connect.object_id == id).delete()
    db.session.commit()
    return jsonify({'data': {
        "id": id,
    }, 'message': 'OK', 'code': 200}
    )


# 删除对应id的Objecttype
@main.route("/deleteobjecttype", methods=['POST'])
def deleteobjecttype():
    id = request.get_json()['id']
    if not all([id]):
        return bad_request('missing param')
    db.session.query(Object).filter(Object.obt.any(ObjectType.id == id)).delete(synchronize_session=False)
    db.session.query(Connect).filter(Connect.type_id == id).delete(synchronize_session=False)
    db.session.query(ObjectType).filter(ObjectType.id == id).delete(synchronize_session=False)
    db.session.commit()
    return jsonify({'data': {
        "id": id,
    }, 'message': 'OK', 'code': 200}
    )


# 查询对应id的Object
@main.route("/queryobject", methods=['POST'])
def queryobject():
    id = request.get_json()['id']
    if not all([id]):
        return bad_request('missing param')
    str1 = db.session.query(Object).filter(Object.id == id).all()
    j = str1[0]
    if j.expiration_time < datetime.datetime.now():
        j.state = '已过期'
    elif j.reminder_time < datetime.datetime.now():
        j.state = '快过期'
    else:
        j.state = '未过期'
    db.session.commit()
    return jsonify({'data':
                        [post.to_json() for post in str1][0]
                       , 'message': 'OK', 'code': 200}
                   )


# 查询用户所有的的Objecttype
@main.route("/queryallobjecttype", methods=['POST'])
def queryallobjecttype():
    username = request.get_json()['username']
    if not all([username]):
        return bad_request('missing param')
    str1 = db.session.query(ObjectType).filter(ObjectType.username == username).all()
    return jsonify({'data':
                        [post.to_json() for post in str1]
                       , 'message': 'OK', 'code': 200}
                   )


# 查询用户所有的Object
@main.route("/queryuserobject", methods=['POST'])
def queryuserobject():
    username = request.get_json()['username']
    state = request.get_json()['state']
    page = request.get_json()['page']
    if not page:page=1
    else:page=int(page)
    if not all([username]):
        return bad_request('missing param')
    if state and state not in ['已过期', '快过期', '未过期']:
        return bad_request('param error')
    if not state:
        pagination = db.session.query(Object).filter(Object.username == username).order_by(
            Object.expiration_time).paginate(page, per_page=10,
                                             error_out=False)
    else:
        pagination = db.session.query(Object).filter(and_(Object.username == username, Object.state == state)).order_by(
            Object.expiration_time).paginate(page, per_page=10,
                                             error_out=False)
    posts = pagination.items
    for j in posts:
        if j.expiration_time < datetime.datetime.now():
            j.state = '已过期'
        elif j.reminder_time < datetime.datetime.now():
            j.state = '快过期'
        else:
            j.state = '未过期'
    db.session.commit()
    prev = None
    if pagination.has_prev:
        prev = page - 1
    next = None
    if pagination.has_next:
        next = page + 1
    return jsonify({'data': {
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total,
    }
        , 'message': 'OK', 'code': 200}
    )


# 查询对应id的Objecttype
@main.route("/queryobjecttype", methods=['POST'])
def queryobjecttype():
    id = request.get_json()['id']
    page = request.get_json()['page']
    if not page:page=1
    else:page=int(page)
    pagination = db.session.query(Object).filter(Object.obt.any(ObjectType.id == id)).order_by(
        Object.expiration_time).paginate(page, per_page=10,
                                         error_out=False)
    # str1 = db.session.query(Object).join(ObjectType, Object.obt).filter(ObjectType.id==id).all()
    posts = pagination.items
    for j in posts:
        if j.expiration_time < datetime.datetime.now():
            j.state = '已过期'
        elif j.reminder_time < datetime.datetime.now():
            j.state = '快过期'
        else:
            j.state = '未过期'
    db.session.commit()
    prev = None
    if pagination.has_prev:
        prev = page - 1
    next = None
    if pagination.has_next:
        next = page + 1
    str2 = db.session.query(ObjectType).filter(ObjectType.id == id).all()
    return jsonify({'data': {
        'type': [post.to_json() for post in str2][0],
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total,
    }, 'message': 'OK', 'code': 200}
    )
