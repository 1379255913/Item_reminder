from functools import wraps
from flask import session,jsonify,url_for,redirect
from .errors import forbidden

# 登录限制的装饰器 用于某些只让登录用户查看的网页
def login_limit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 我们这里用来区分是否登录的方法很简答，就是查看session中是否赋值了email，如果赋值了，说明已经登录了
        if session.get('username'):
            # 如果登录了，我们就正常的访问函数的功能
            return func(*args, **kwargs)
        else:
            # 如果没登录，我们就将它重定向到登录页面，这里大家也可以写一个权限错误的提示页面进行跳转
            return forbidden('not login')
    return wrapper
