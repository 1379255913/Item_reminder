# -*- coding:utf-8 -*-
import datetime
from flask_sqlalchemy import SQLAlchemy
import pymysql

# url的格式为：数据库的协议：//用户名：密码@ip地址：端口号（默认可以不写）/数据库名
# 创建数据库的操作对象
db = SQLAlchemy()
# class Connect(db.Model):
#     __tablename__ = "connect"
#     object_id=db.Column( db.String(128), db.ForeignKey('object.id'), primary_key=True)
#     type_id=db.Column(db.String(128), db.ForeignKey('objecttype.id'), primary_key=True)



class UserInformation(db.Model):
    __tablename__ = "userinformation"

    username = db.Column(db.String(40), primary_key=True)
    password = db.Column(db.String(255), nullable=False)
    nickname = db.Column(db.String(40), nullable=False)
    children1 = db.relationship("Object", backref="userinformation")
    children2 = db.relationship("ObjectType", backref="userinformation")
    def __repr__(self):
        return "Role: %s %s %s" % (
        self.username, self.password, self.nickname,)

    def to_json(self):
        json_user = {
            'username': self.username,
            'nickname': self.nickname,
        }
        return json_user


class Object(db.Model):
    __tablename__ = "object"

    username = db.Column(db.String(40),db.ForeignKey('userinformation.username') ,nullable=False)
    information = db.Column(db.Text, nullable=False)
    expiration_time = db.Column(db.DateTime, nullable=False)
    reminder_time = db.Column(db.DateTime, nullable=False)
    state = db.Column(db.String(20), nullable=False)
    id = db.Column(db.String(128), primary_key=True)
    obt = db.relationship("ObjectType",backref="objects",secondary="connect")
    def __repr__(self):
        return "Role: %s %s %s %s %s %s" % (
        self.username, self.information, self.expiration_time, self.reminder_time,self.state,self.id,)
#self.userinformation.nickname
    def change(self,x):
        return str(x)[0:10]
    def to_json(self):
        json_user = {
            'username': self.username,
            'information': self.information,
            'expiration_time': self.change(self.expiration_time),
            'reminder_time': self.change(self.reminder_time),
            'state': self.state,
            'id': self.id,
            'nickname': self.userinformation.nickname,
            'type':[j.type for j in self.obt][0],
            'type_id':[j.id for j in self.obt][0]
        }
        return json_user

class ObjectType(db.Model):
    __tablename__ = "objecttype"

    username = db.Column(db.String(40),db.ForeignKey('userinformation.username') ,nullable=False)
    type = db.Column(db.String(20), nullable=False)
    orderlist = db.Column(db.Integer, nullable=False)
    id = db.Column(db.String(128), primary_key=True)
    def __repr__(self):
        return "Role: %s %s %s %s" % (
        self.username, self.type, self.orderlist, self.id,)
# self.userinformation.nickname
    def to_json(self):
        # def func(x):
        #     ans=[]
        #     for j in x:
        #         ans.append({
        #             'username': j.username,
        #             'information': j.information,
        #             'expiration_time': j.expiration_time,
        #             'reminder_time': j.reminder_time,
        #         })
        #     return ans
        json_user = {
            'username': self.username,
            'type': self.type,
            'orderlist': self.orderlist,
            'id': self.id,
            'nickname': self.userinformation.nickname,
            'count': len(self.objects),
        }
        return json_user


# connect = db.Table('connect',
#                        db.Column('object_id', db.String(128), db.ForeignKey('object.id'), primary_key=True),
#                        db.Column('type_id', db.String(128), db.ForeignKey('objecttype.id'), primary_key=True)
#                        )

class Connect(db.Model):
    __tablename__ = "connect"

    object_id =db.Column(db.String(128),db.ForeignKey('object.id'), primary_key=True)
    type_id = db.Column(db.String(128),db.ForeignKey('objecttype.id'), primary_key=True)

# class User(db.Model):
#     # 给表重新定义一个名称，默认名称是类名的小写，比如该类默认的表名是user。
#     __tablename__ = "users"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(16), unique=True)
#     email = db.Column(db.String(32), unique=True)
#     password = db.Column(db.String(16))
#     # 创建一个外键，和django不一样。flask需要指定具体的字段创建外键，不能根据类名创建外键
#     role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
#
#     def __repr__(self):
#         return "User: %s %s %s %s" % (self.id, self.name, self.password, self.role_id)
