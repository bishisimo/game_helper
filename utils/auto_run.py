"""
@author '彼时思默'
@time 2019/12/7 12:39
@describe:
  运行封装
"""
import os
import time

import pyautogui
from PIL import Image
from loguru import logger

from res import fields, tap
from root import root
from utils.adb import adb
from utils.image_converter import byte2img
from utils.img_locate import img_locate
from utils.ocr import ocr


class Auto:
    any_where = (500, 1000)

    def __call__(self, *args, **kwargs):
        self.run_app()
        self.double_income()

    def tab_img(self, img_path):
        target_position = img_locate.locate(img_path)
        logger.debug(target_position)
        adb.tap(*target_position)

    def run_app(self):
        adb.run_app()
        time.sleep(20)
        logger.info('app is running!')

    def watch_video(self, n=1):
        for i in range(n):
            adb.tap(*tap.XY_video)
            adb.tap(*tap.XY_video_ok)
            logger.info('开始广告')
            time.sleep(35)
            adb.tap(*tap.XY_close_video)
            logger.info('关闭广告')
            adb.tap(*self.any_where)
            time.sleep(1)

    def double_income(self):
        text = ocr.baidu()
        logger.debug(text)
        if fields.double_income in text:
            logger.debug(text)
            adb.tap(*adb.XY_DOUBLE_INCOME)
            time.sleep(1)
            self.tab_img(img_locate.PATH_USE_810_1440)
            time.sleep(1)
            adb.tap(*adb.XY_DOUBLE_INCOME)

    def start_adventure(self):
        # 开始第一次冒险
        adb.tap(*tap.XY_START_ADVENTURE)
        # 后续冒险
        num=1
        while True:
            time.sleep(10)
            text=ocr.baidu()
            if fields.free_charge in text:
                adb.tap(*tap.XY_free_charge)
                adb.tap(*tap.XY_use)
            elif fields.re_adventure in text:
                adb.tap(*tap.XY_re_adventure)
                adb.tap(*tap.XY_re_adventure_ok)
                num+=1
                logger.info(f'第{num}次冒险开始...')

    def analysis_ocr(self, data):
        data_list = data.split('@')[1:-1]
        for data in data_list:
            if '/' in data:
                num_list = data.split('/')
                current_num = int(num_list[0])
                origin_target_num = num_list[1]
                target_num = 0
                for char in origin_target_num:
                    target_num = target_num * 10 + int(char)
                    if target_num >= current_num:
                        pass

    def check_adventure_stop(self,text):
        pass


    def collect(self):
        adb.swipe(400, 150, 400, 1300)
        time.sleep(1)
        adb.swipe(400, 150, 400, 1300)
        time.sleep(1)
        adb.swipe(400, 150, 400, 1300)
        time.sleep(1)
        adb.swipe(400, 150, 400, 1300)
        time.sleep(2)

        adb.swipe(400, 1300, 400, 0)
        time.sleep(3)
        adb.tap(*adb.XY_COLLECT_LIST[0])
        adb.swipe(400, 1000, 400, 550)
        time.sleep(3)
        adb.tap(*adb.XY_COLLECT_LIST[1])
        adb.tap(*adb.XY_COLLECT_LIST[2])
        adb.tap(*adb.XY_COLLECT_LIST[3])
        adb.swipe(400, 1000, 400, 400)
        time.sleep(3)
        adb.tap(*adb.XY_COLLECT_LIST[4])
        adb.tap(*adb.XY_COLLECT_LIST[5])
        adb.tap(*adb.XY_COLLECT_LIST[6])
        adb.swipe(400, 1000, 400, 400)
        time.sleep(3)
        adb.tap(*adb.XY_COLLECT_LIST[7])
        adb.tap(*adb.XY_COLLECT_LIST[8])
        adb.tap(*adb.XY_COLLECT_LIST[9])
        time.sleep(2)
        adb.swipe(400, 1300, 400, 0)
        time.sleep(3)
        adb.tap(*adb.XY_COLLECT_LIST[10])
        time.sleep(1)


auto = Auto()
if __name__ == '__main__':
    # auto.run_app()
    # auto.double_income()
    # auto.watch_video(100)
    auto.start_adventure()
    # auto.collect()
