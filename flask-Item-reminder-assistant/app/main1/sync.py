from flask import jsonify, redirect, render_template, request, flash, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql

pymysql.install_as_MySQLdb()
from . import main
from .errors import bad_request, servererror
from app.models import *
from app.run import db
from .decorators import login_limit, generate_token, validate_token
from json import loads
import datetime

#同步数据到服务器
@main.route("/upsync", methods=['POST'])
@login_limit
def upsync():
    if request.method == 'POST':
        tags = request.get_json()['tags']
        objects = request.get_json()['objects']
        if not all([tags, objects]):
            return bad_request("缺少数据")
        tags = loads(tags)
        objects = loads(objects)
        token = request.headers["Authorization"]
        user = validate_token(token.encode("utf-8"))["user"]
        str1 = db.session.query(ObjectType).filter(ObjectType.username == user).all()
        for item in str1:
            db.session.query(Object).filter(Object.obt.any(ObjectType.id == item.id)).delete(synchronize_session=False)
            db.session.query(Connect).filter(Connect.type_id == item.id).delete(synchronize_session=False)
            db.session.query(ObjectType).filter(ObjectType.id == item.id).delete(synchronize_session=False)
        db.session.commit()
        for item in tags:
            inf = ObjectType(username=user, type=item['type'], id=item['id'])
            db.session.add(inf)
        db.session.commit()
        for item in objects:

            expiration_time = datetime.datetime.strptime(item['expiration_time'], '%Y-%m-%d')
            reminder_time = datetime.datetime.strptime(item['reminder_time'], '%Y-%m-%d')
            if item['manufacture_time']:
                manufacture_time = datetime.datetime.strptime(item['manufacture_time'], '%Y-%m-%d')
                inf = Object(username=user, information=item['information'], manufacture_time=manufacture_time,
                             fresh_time_number=item['fresh_time_number'],fresh_time_unit=item['fresh_time_unit'],expiration_time=expiration_time,
                             reminder_time=reminder_time, state=item['state'], id=item['id'])
            else:
                inf = Object(username=user, information=item['information'],
                             fresh_time_number=item['fresh_time_number'], fresh_time_unit=item['fresh_time_unit'],
                             expiration_time=expiration_time,
                             reminder_time=reminder_time, state=item['state'], id=item['id'])
            o = db.session.query(ObjectType).filter_by(id=item['type_id']).first()
            inf.obt.append(o)
            db.session.add(inf)
        db.session.commit()
        response = jsonify({'data': {
            'username': user,
        }, 'message': 'OK', 'code': 200}
        )
        response.status_code = 200
        return response


#同步数据到本地
@main.route("/downsync", methods=['POST'])
@login_limit
def downsync():
    if request.method == 'POST':
        token = request.headers["Authorization"]
        user = validate_token(token.encode("utf-8"))["user"]
        str1 = db.session.query(ObjectType).filter(ObjectType.username == user).all()
        str2 = db.session.query(Object).filter(Object.username == user).all()
        response = jsonify({'data':{
            "tags" : [post.to_json() for post in str1],
            "objects" : [post.to_json() for post in str2]
        }
           , 'message': 'OK', 'code': 200}
        )
        response.status_code = 200
        return response