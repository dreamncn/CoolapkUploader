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
        self.handle()
        client = AipOcr(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        options = {
            "language_type": "ENG",
            "detect_direction": "true",
            "detect_language": "true",
            "probability": "false"
        }
        """ 带参数调用通用文字识别 """
        with open(path, 'rb') as f:
            log("Captcha","Try to process captcha image by Baidu OCR")
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

    def handle(self):
        import cv2
        # 读入验证码图像
        img = cv2.imread('img.png')
        # 灰度化
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 二值化
        ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        # 去噪
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        blur = cv2.medianBlur(thresh, 3)
        cv2.imwrite('img.png', blur)



