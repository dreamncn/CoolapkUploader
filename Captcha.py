# coding=utf-8
import json
import re

from aip import AipOcr

from Log import log, INFO, DANGER


class captcha:
    APP_ID = '你的appid'
    API_KEY = '你的apikey'
    SECRET_KEY = '你的secretkey'

    def __init__(self, appid, key, secret):
        self.APP_ID = appid
        self.API_KEY = key
        self.SECRET_KEY = secret

    def ocr(self, path):
        client = AipOcr(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        options = {
            "language_type": "ENG",
            "detect_direction": "true",
            "detect_language": "true",
            "probability": "false"
        }
        """ 带参数调用通用文字识别 """
        with open(path, 'rb') as f:
            img = f.read()
        result = client.basicGeneral(img, options)
        text = ''
        log("Captcha", "OCR Result: " + json.dumps(result), INFO)
        if 'words_result' in result:
            for w in result['words_result']:
                text = text + w['words'].replace(" ", "")
        return text.replace("-", "").replace("_", "").replace(".", "")

    def read(self, path, count):
        if self.APP_ID == "" or self.API_KEY == "" or self.SECRET_KEY == "" or count > 10:
            log("Captcha", "Can't find any data about baidu ocr ", DANGER)
            exit(255)
        log("Captcha", "Try to process captcha image.", INFO)
        return self.ocr(path)


