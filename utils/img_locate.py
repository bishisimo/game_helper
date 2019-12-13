"""
@author '彼时思默'
@time 2019/12/7 17:51
@describe:
  定位图片
"""
import os

import pyautogui
from loguru import logger

from root import root
from utils.adb import adb
from utils.image_converter import byte2img


class ImgLocate:
    PATH_FREE_REFUEL_810_1440 = os.path.join(root, 'res/810_1440/img/free_refuel.png')
    PATH_OK_810_1440 = os.path.join(root, 'res/810_1440/img/ok.png')
    PATH_START_COOK_810_1440 = os.path.join(root, 'res/810_1440/img/start_cook.png')
    PATH_USE_810_1440 = os.path.join(root, 'res/810_1440/img/use.png')
    PATH_VIDEO_810_1440 = os.path.join(root, 'res/2340_1080/video.png')
    PATH_START_ADVENTURE_810_1440 = os.path.join(root, 'res/810_1440/img/start_adventure.png')

    def locate(self, img_path):
        img_bk = byte2img(adb.shot_screen())
        position=pyautogui.locate(img_path, img_bk,grayscale=True)
        logger.debug(position)
        target_position = pyautogui.center(position)
        logger.debug(target_position)
        return target_position.x, target_position.y


img_locate = ImgLocate()
