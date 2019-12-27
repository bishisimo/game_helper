"""
@author '彼时思默'
@time 2019/12/7 12:39
@describe:
  运行封装
"""
import json
import os
import time
from loguru import logger

from config import fields, tap
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

    def watch_ad(self):
        adb.tap(*tap.XY_ONE)
        adb.tap(*tap.XY_ONE_MAIN)
        i=0
        while True:
            i+=1
            adb.tap(*tap.XY_video)
            adb.tap(*tap.XY_video_ok)
            logger.info(f'第{i}次开始广告')
            time.sleep(1)
            # 通过ocr读取广告时间
            key=ocr.baidu()
            text = key[:2]
            if text.isdigit():
                stop_time = int(text)
                if stop_time<10:
                    stop_time=30
            else:
                stop_time = 30
            logger.debug(stop_time)
            time.sleep(stop_time)
            # 根据广告内容点击关闭按钮
            text = ocr.baidu()
            if '58' in text:
                adb.tap(*tap.XY_close_video_58)
                time.sleep(1)
            elif '预估收益烹饪' in text:
                logger.error('第i次ad,误入cook!')
                adb.tap(*tap.XY_LB_CLOSE)
                adb.tap(*tap.XY_ONE_MAIN)
                continue
            elif '魔法药水每档首次购买获得双倍魔法药水' in text:
                logger.error('第i次ad,误入shop!')
                adb.tap(*tap.XY_LB_CLOSE)
                adb.tap(*tap.XY_ONE_MAIN)
                continue
            else:
                adb.tap(*tap.XY_close_video)
            logger.info(f'第{i}次广告完成')
            adb.tap(*self.any_where)
            time.sleep(1)
            text = ocr.baidu()
            text=text.split('秒')[0][-2:]
            if text.isdigit():
                sec = int(text)
                logger.debug(f'广告还需{sec}s')
                time.sleep(sec)

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

    def start_adventure(self,index:int=1):
        # 开始第一次冒险
        adb.tap(*tap.XY_TOW)
        adb.tap(*tap.XY_START_ADVENTURE[index - 1])
        num = 1
        time.sleep(30)
        # 后续冒险
        while True:
            time.sleep(30)
            text = ocr.baidu()
            if fields.free_charge in text or fields.free_refuel in text:
                adb.tap(*tap.XY_free_charge)
                adb.tap(*tap.XY_use)
            elif fields.re_adventure in text:
                if self.is_adventure_stop:
                    logger.warning(f'第{num}次冒险后暂停,需要升级!')
                    return
                adb.tap(*tap.XY_re_adventure)
                adb.tap(*tap.XY_re_adventure_ok)
                num += 1
                logger.info(f'第{num}次冒险开始...')

    @property
    def is_adventure_stop(self):
        result = False
        target_num = 0
        x_start = 150
        x_end = 950
        y_start = 1000
        y_end = 1100
        img_bk = byte2img(adb.shot_screen())
        pix = img_bk.load()
        for x in range(x_start, x_end):
            for y in range(y_start, y_end):
                color = pix[x, y][:-1]
                if color == (141, 255, 0):
                    target_num += 1
        logger.info(f'目标像素个数为:{target_num}')
        if target_num > 0:
            result = True
        return result

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
    auto.watch_ad()
    # auto.start_adventure(1)
    # auto.collect()
