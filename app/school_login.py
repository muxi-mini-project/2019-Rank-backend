import re
import json
import requests


def login(username, password):
    s = requests.Session()
    s.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    s.get("https://account.ccnu.edu.cn/cas/login")
    res = s.get("https://account.ccnu.edu.cn/cas/login")
    execution = re.search('execution" value="(.+?)"', res.text).group(1)
    lt = re.search('lt" value="(.+?)"', res.text).group(1)
    data = {
        "username": username,
        "password": password,
        "execution": execution,
        "lt": lt,
        "_eventId": "submit",
        "submit": "登录"
    }
    res = s.post("https://account.ccnu.edu.cn/cas/login;jsessionid=" + s.cookies['JSESSIONID'], data=data)
    if '登录成功' in res.text:
        s.get('http://one.ccnu.edu.cn/')
        s.get('http://one.ccnu.edu.cn/index')
        s.headers['Authorization'] = 'Bearer ' + s.cookies['PORTAL_TOKEN']
        res = s.post('http://one.ccnu.edu.cn/user_portal/index')
        return json.loads(res.text)

    else:
        return False
