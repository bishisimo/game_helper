"""
@author '彼时思默'
@time 2019/12/7 14:41
@describe:
  ocr封装
"""
import base64

# import pytesseract

from loguru import logger

from config.pypytesseract_path import pytesseract_path
from utils.adb import adb
from utils.baidu import baidu
from utils.image_converter import byte2img


class Ocr:
    # pytesseract.pytesseract.tesseract_cmd = pytesseract_path

    # def pytesseract(self):
    #     img = byte2img(adb.shot_screen())
    #     text = pytesseract.image_to_string(img, lang='chi_sim')
    #     logger.debug(text)
    #     return text

    def baidu(self):
        img_byte = adb.shot_screen()
        img_base64 = base64.b64encode(img_byte)
        text = baidu.baidu_ocr(img_base64)
        logger.debug(text)
        return text

ocr=Ocr()
if __name__ == '__main__':
    ocr.baidu()