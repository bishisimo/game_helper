"""
@author '彼时思默'
@time 2019/12/7 17:12
@describe:
  转换图片格式
"""
import io

from PIL import Image


def byte2img(img_byte):
    return Image.open(io.BytesIO(img_byte))