import requests
import re
from flask import jsonify,request
from . import main
from .errors import servererror,bad_request

@main.route("/barcode", methods=['POST'])
def barcode():
    code = request.get_json().get("code")
    if not code: return bad_request("编号错误")
    # ch_options = Options()
    # ch_options.add_argument('--headless')
    # driver = webdriver.Chrome(options= ch_options)
    # driver.set_page_load_timeout(4)
    # try:
    #     url = "http://www.1034.cn/"
    #     driver.get(url)
    #     driver.find_element("id","inputSearchExample3").send_keys(code)
    #     driver.find_element("xpath", '//*[@id="topsearch"]/div/div[1]/span/button').click()
    #     ans = driver.find_element("xpath", '/html/body/div[1]/div/div[1]/div/div[2]').text
    #     driver.close()
    # except Exception as e:
    #     return servererror("访问超时，请稍后再试")
    try:
        res = requests.get(url="http://www.1034.cn/search/?tm=" + str(code)).text
    except Exception as e:
        return servererror("访问超时，请稍后再试")
    obj = re.compile('商品名称</button>&nbsp;(?P<name>.*?)<hr>', re.S)
    result = obj.finditer(res)
    ans = ""
    for item in result:
        ans = str(item.group("name")).strip()
    if ans:
        response = jsonify({'data': ans
                , 'message': 'OK', 'code': 200})
    else:
        response = jsonify({'data': "未找到相关记录"
                               , 'message': 'OK', 'code': 200})
    response.status_code = 200
    return response


@main.route("/lotno", methods=['POST'])
def lotno():
    brand = request.get_json().get("brand")
    number = request.get_json().get("number")
    if not all([brand,number]): return bad_request("参数错误")
    ans = []
    try:
        url = "http://www.cosmedna.com/query/"
        params = {"ppid":brand,"scph":number}
        res = requests.get(url=url,params=params).text
    except Exception as e:
        return servererror("访问超时，请稍后再试")
    obj = re.compile(
        '生产日期：(?P<date1>.*?)</td>.*?过期日期：(?P<date2>.*?)</td>',
        re.S)
    result = obj.finditer(res)
    for item in result:
        ans = [item.group("date1"),item.group("date2")]
    if ans:
        response = jsonify({'data': {  "expiration_time" : ans[1] , "manufacture_time" : ans[0]  }
                    , 'message': 'OK', 'code': 200})
    else:
        response = jsonify({'data': "未找到相关记录", 'message': 'OK', 'code': 200})
    response.status_code = 200
    return response





