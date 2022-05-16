import pymysql

DEBUG = False

SECRET_KEY = "ILOVEFZU"

db2 = pymysql.connect(host='localhost', user='root', password='1379255913zyy', db='reminderassistant', port=3306)
SQLALCHEMY_DATABASE_URI="mysql://root:1379255913zyy@localhost:3306/reminderassistant"
SQLALCHEMY_TRACK_MODIFICATIONS=False
TEMPLATES_AUTO_RELOAD =True