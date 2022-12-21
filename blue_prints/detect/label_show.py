# -*- coding: utf-8 -*-
"""
@author: zhangshihao
@file: label_show.py
@time: 2022/11/17 21:45
"""
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def cv2ImgAddText(img, text, left, top, textColor=(0, 255, 0), textSize=20):
    if (isinstance(img, np.ndarray)):  # 判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img)
    # 字体的格式
    fontStyle = ImageFont.truetype(
        "simsun.ttc", textSize, encoding="utf-8")
    # 绘制文本
    draw.text((left, top - textSize), text, textColor, font=fontStyle)
    # 转换回OpenCV格式
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


def view_image(image_path, result):
    img = cv2.imread(image_path)
    h, w, _ = img.shape

    for loc in result:
        cls = str(loc[0])
        temp = loc[1:]
        x1, y1, x2, y2 = temp[0], temp[1], temp[2], temp[3]
        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0))
        img = cv2ImgAddText(img, cls, int(x1), int(y1), (0, 255, 0), 15)

    cv2.imshow('windows', img)
    cv2.waitKey(0)
