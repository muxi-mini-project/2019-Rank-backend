import re
import json
import requests


def login(username, password):
    s = requests.Session()
    s.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0' \
                              '.3538.77 Safari/537.36'
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


def get_books_num(username, password):
    s = requests.Session()
    s.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0' \
                              '.3538.77 Safari/537.36'
    res = s.get("https://account.ccnu.edu.cn/cas/login?service=http%3A%2F%2F202.114.34.15%2Freader%2Flogin.php")
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
    res = s.post(
        "https://account.ccnu.edu.cn/cas/login;jsessionid=8BF05E58F48DEF0E7FF9A4FC705F0EE4hgu50C?service=http://"
        "202.114.34.15/reader/login.php", data=data)
    if "您输入的用户名或密码有误" in res.text:
        raise ValueError()
    if res.history[0].status_code == 302:
        res = s.get('http://202.114.34.15/reader/book_lst.php')
        books_num = re.search(r'当前借阅\( <b class="blue">(\d)</b>', res.text).group(1)
        return int(books_num)
    else:
        raise ConnectionError()
