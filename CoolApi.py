import json
import os
import random
import re
import string

from bs4 import BeautifulSoup
import requests

from Captcha import captcha
from Log import *

args = {}
cookie_str = ""
cookies = {}
headers = {
    'Cookie': '',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://account.coolapk.com',
    'Referer': 'https://account.coolapk.com/auth/loginByCoolapk'
}
api_headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "DNT": "1",
    "Host": "account.coolapk.com",
    "Origin": "https://account.coolapk.com",
    "Pragma": "no-cache",
    "Referer": "https://account.coolapk.com/auth/loginByCoolapk",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "sec-ch-ua": "\"Google Chrome\";v=\"111\", \"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"111\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "x-requested-with": "XMLHttpRequest",
}
page_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': '',
    'DNT': '1',
    'Host': 'developer.coolapk.com',
    'Pragma': 'no-cache',
    'Referer': 'https://developer.coolapk.com/do?c=apk&m=myList&listType=publish',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"'
}
uploads_headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "DNT": "1",
    "Host": "developer.coolapk.com",
    "Origin": "https://developer.coolapk.com",
    "Pragma": "no-cache",
    "Referer": "https://developer.coolapk.com/do?c=apk&m=edit&id=286892&listType=all&activeTab=2",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "content-type": "application/octet-stream",
    "sec-ch-ua": "\"Google Chrome\";v=\"111\", \"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"111\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\""
}

session = requests.session()
session.headers.update(headers)

count = 0


def checkUser(request_hash):
    global args, cookie_str, api_headers
    url = 'https://account.coolapk.com/auth/loginByCoolapk'
    data = {
        'submit': '1',
        'requestHash': request_hash,
        'login': args.get('username'),
        'type': "checkAdmin",
        'randomNumber': '0undefined' + ''.join(random.choices('0123456789', k=16))
    }
    api_headers['Cookie'] = cookie_str
    response = session.post(url, data=data, headers=api_headers, cookies=cookies)
    rep = json.loads(response.text)
    # updateCookie()
    # print(rep)


# 获取初始Cookie
def getRequestHash(url):
    response = session.get(url)
    updateCookie()
    return getRequestHashFromText(response.text)


def getRequestHashFromText(text):
    pattern = r'data-request-hash="(\w+)"'
    match = re.search(pattern, text)
    if match:
        request_hash = match.group(1)
        log("request_hash", request_hash, SUCCESS)
    else:
        log("request_hash", "Failed to extract the request hash from the response.", ERROR)
        log("Response From Coolapk Site ", text, INFO)
        exit(255)
    return request_hash


def updateCookie():
    global cookie_str, cookies
    cookies = session.cookies.get_dict()
    if cookies:
        log("request_cookie", cookies, SUCCESS)
        session.cookies.update(cookies)
        cookie_str = "; ".join([str(x) + "=" + str(y) for x, y in cookies.items()])


# 读取验证码，并调用百度验证
def readCaptcha():
    global count, cookie_str
    img = session.get("https://account.coolapk.com/auth/showCaptchaImage", headers={'Cookie': cookie_str})
    fileDir = os.getcwd() + "/img.png"
    with open(fileDir, 'wb') as f:
        f.write(img.content)
    # print(img.cookies)
    # updateCookie()
    cap = captcha(args.get("baidu_app"), args.get("baidu_id"), args.get("baidu_secret"))
    verifyCode = cap.read(fileDir, count)
    log("Login", "VerifyCode is " + verifyCode, INFO)
    return verifyCode


def login(arg):
    global args, cookie_str
    args = arg
    request_hash = getRequestHash("https://account.coolapk.com/auth/loginByCoolapk")
    checkUser(request_hash)
    url = 'https://account.coolapk.com/auth/loginByCoolapk'
    captcha_data = readCaptcha()
    while not is_valid_string(captcha_data):
        captcha_data = readCaptcha()
    data = {
        'submit': '1',
        'requestHash': request_hash,
        'login': args.get('username'),
        'password': args.get('password'),
        'captcha': captcha_data,
        'code': '',
        'randomNumber': '0undefined' + ''.join(random.choices('0123456789', k=16))
    }
    global api_headers
    api_headers['Cookie'] = cookie_str
    response = session.post(url, data=data, headers=api_headers, cookies=cookies)
    rep = json.loads(response.text)
    while rep["messageStatus"] != 1:
        log("Login", "Failed!", ERROR)
        log("Login Full", response.text, ERROR)
        log("Login Msg", rep["message"], ERROR)
        login(arg)
        if count > 10:
            log("Login Msg", "The number of login failures has exceeded the maximum number of attempts", ERROR)
            exit(255)
    callback_url = "https://account.coolapk.com" + rep["message"]
    updateCookie()
    api_headers['Cookie'] = cookie_str
    repo = session.get(callback_url, headers=api_headers)
    # print(repo.text)
    repos = json.loads(repo.text)
    log("Login", "Success!", SUCCESS)
    log("===========================Login Successful===============================", None, SUCCESS)
    log("Coolapk", "Welcome, " + repos["SESSION"]["username"] + " " + repos["SESSION"]["groupName"] + "!", SUCCESS)
    log("===========================Login Successful===============================", None, SUCCESS)
    listApps()
    # uploaderApp()
    deleteUnReleaseApp()


def is_valid_string(input_str):
    pattern = r'^[0-9a-zA-Z]{4}$'
    return bool(re.match(pattern, input_str))


def listApps():
    url = 'https://developer.coolapk.com/do?c=apk&m=myList'
    page_headers['Cookie'] = cookie_str

    repo = session.get(url, headers=page_headers)
    soup = BeautifulSoup(repo.text, 'html.parser')

    # 查找所有符合条件的HTML段
    table_rows = soup.find_all('tr')
    find = False
    # 在每个HTML段中提取需要的字段
    log("===========================App List===============================", None, INFO)
    for row in table_rows[1:]:
        # print(row)
        alls = row.find_all("a")
        if len(alls) == 0:
            continue
        a = row.find_all("a")[1].text.strip()
        # 使用正则表达式进行匹配
        pattern = r'<br/>([\S\s]*?)<span'
        result = re.search(pattern, str(row))
        # 提取匹配结果
        if result:
            version = result.group(1).strip()
        else:
            continue
        # 使用正则表达式进行匹配
        pattern = r'data-cell--(\d+)'
        result = re.search(pattern, str(row))
        # 提取匹配结果
        if result:
            app_id = result.group(1)
        else:
            continue

        log("Coolapk", "[ " + a + " ] " + version + "  ID: " + app_id, INFO)

        if app_id == args.get("id"):
            find = True
    log("======================================================================", None, INFO)
    if not find:
        log("Coolapk", "Can\'t find the id of " + args.get("id") + "，Please ensure that you had released the app in "
                                                                   "coolapk market!", ERROR)
        exit(220)


def generate_random_string(length):
    """生成指定长度的随机字符串"""
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(length))


def deleteUnReleaseApp():
    global page_headers
    # request_hash = getRequestHash("https://account.coolapk.com/auth/loginByCoolapk")
    params = {
        "c": "apk",
        "m": "edit",
        "id": "268462",
        "listType": "all",
        "activeTab": "2"
    }
    page_headers['Cookie'] = cookie_str
    url = "https://developer.coolapk.com/do"
    response = session.get(url, headers=page_headers, params=params)
    request_hash = getRequestHashFromText(response.text)
    print(response.text)
    matches = re.findall(r'data-(\w+)="(.*?)"', response.text)

    for match in matches:
        print(match)


def uploaderApp():
    # 分块上传
    upload_url = "https://developer.coolapk.com/apk/uploadApkFile"
    aid = args.get("id")
    chunk_size = 5242880  # 5 MB
    path = args.get("path")
    if not os.path.isfile(path):
        log("Coolapk", "No such file or directory:  " + path, ERROR)
        exit(255)
    log("Coolapk Uploader", "Start to upload file : " + path, INFO)
    # 生成随机字符串
    id = "o_" + generate_random_string(30)
    upload_path = ""

    with open(args.get("path"), 'rb') as f:
        chunk_num = 0
        file_size = os.path.getsize(args.get("path"))
        total_chunks = -(-file_size // chunk_size)  # 计算总块数

        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            uploads_headers["Cookie"] = cookie_str

            params = {
                'name': 'test.apk',
                'chunk': chunk_num,
                'chunks': total_chunks,
                'aid': aid,
                'id': id,
                'type': 'application/vnd.android.package-archive',
                'size': file_size
            }
            log("Coolapk Uploader", "Process : " + str(chunk_num / total_chunks * 100) + "%", INFO)
            r = requests.post(upload_url, headers=uploads_headers, params=params, data=chunk)
            if chunk_num + 1 == total_chunks:
                log("Coolapk Uploader", "Upload completed !", INFO)
                rep = json.loads(r.text)
                if 'result' in rep:
                    log("Coolapk Uploader", "Upload successful !", SUCCESS)
                    log("Coolapk Uploader", "File url: " + rep['result'], SUCCESS)
                else:
                    log("Coolapk Uploader", "Upload error !" + rep["error"]["message"], ERROR)
                    log("Coolapk Uploader", "Upload error Raw Data:" + r.text, ERROR)
                    exit(230)
            chunk_num += 1


def saveAppLogs():
    # 保存app更新日志
    pass


def saveAndPushApp():
    # 保存并推送app更新
    pass
