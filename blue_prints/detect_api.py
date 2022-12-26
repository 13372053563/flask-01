# -*- coding: utf-8 -*-
"""
@author: zhangshihao
@file: detect_api.py
@time: 2022/12/15 19:41
"""
import os
from io import BytesIO

import cv2
import numpy as np
import requests
from PIL import Image
from flask import Blueprint, make_response, jsonify
from flask_restplus import Api, Resource

from blue_prints.detect.detect_method import detect_method

detect_api = Blueprint("detect_api", __name__)
api = Api(detect_api, version='1.0', title='crystal detection API',
          description='结晶检测接口文档')
ns = api.namespace('detect_api', description='结晶检测相关接口')


@ns.route('/start_detect/<path:img_path>')
class DETECT(Resource):
    def get(self, img_path='not specified'):
        # 从网络获取图片，并转为cv2格式
        response = requests.get(img_path)
        image = Image.open(BytesIO(response.content))
        source = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
        source_shape = source.shape

        result = detect_method(
            source=source,
            source_shape=source_shape,
            weights=os.path.split(os.path.realpath(__file__))[0] + "/detect/best.pt",
            img_size=640,
            conf_thres=0.25,
            iou_thres=0.1,
            save_conf=False,
            augment=False,
        )
        # view_image(source=source, result=result, shape=source_shape)
        response = make_response(jsonify(
            {"description": "result中的元素的第一个位置是类别，剩下四个是x1y1x2y2", "code": 200, "result": result}
        ))
        # print(u'当前进程的内存使用：%.4f GB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024 / 1024))
        return response
