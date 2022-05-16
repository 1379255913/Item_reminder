import datetime
import random
import codecs
import time

from flask import jsonify, redirect, render_template,send_file,request
import os
from . import main
from .errors import bad_request, servererror,missed
from openpyxl import Workbook
import threading
def setTimeout(cbname,delay,*argments):
    threading.Timer(delay,cbname,argments).start()
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))+"\src"
def create_uuid():  # 生成唯一的的名称字符串，防止重名问题
    nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # 生成当前时间
    randomNum = random.randint(0, 100)  # 生成的随机整数n，其中0<=n<=100
    if randomNum <= 10:
        randomNum = str(0) + str(randomNum)
    uniqueNum = str(nowTime) + str(randomNum)
    return uniqueNum
def test (x):
    os.remove(os.path.join(basedir,x[0]+x[1]))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1]

@main.route("/download/<Ino>")
def download(Ino):
    file_path = os.path.join(basedir,str(Ino))
    if os.path.isfile(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return missed("not found")


@main.route("/upload", methods=["POST"])
def upload():
    type1 = request.get_json()['type']
    data = request.get_json()['data']
    t=create_uuid()
    if type1==0 :
        p = ["information", "manufacture_time", "fresh_time_number", "fresh_time_unit", "expiration_time","reminder_time", "state", "id", "type", "type_id"]
        ans = ",".join(p)+"\n"
        for i in range(len(data)):
            p = []
            for item in data[i]:
                p.append(str(data[i][item]))
            ans+=",".join(p)+"\n"
        with codecs.open(os.path.join(basedir,t+".csv"), "w","UTF-8") as fo:
            fo.write("\uFEFF"+ans)
        setTimeout(test,10,[t,".csv"])
    elif type1==1:
        # 创建一个 workbook
        wb = Workbook()
        # 获取被激活的 worksheet
        ws = wb.active
        # 设置单元格内容
        # 设置一行内容
        ws.append(['物品名', '生产日期', '保质期', '保质期单位', '过期日期', '提醒日期', '状态'])
        # python 数据类型可以被自动转换
        for i in range(len(data)):
            p=[]
            for item in data[i] :
                if item not in ["id", "type", "type_id"]:
                    p.append(str(data[i][item]))
            ws.append(p)
        # 保存 Excel 文件
        wb.save(os.path.join(basedir,t+".xlsx"))
        setTimeout(test, 10, [t, ".xlsx"])
    return jsonify({'data': t, 'message': 'OK', 'code': 200}
                       )




