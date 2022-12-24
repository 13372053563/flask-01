# -*- coding: utf-8 -*-
"""
@author: zhangshihao
@file: detect_api.py
@time: 2022/12/15 19:41
"""
import os
import requests
from flask import Blueprint, make_response, jsonify, request
from flask_restplus import Api, Resource

from blue_prints.detect.label_show import view_image
from blue_prints.detect.detect_method import detect

detect_api = Blueprint("detect_api", __name__)
api = Api(detect_api, version='1.0', title='crystal detection API',
          description='结晶检测接口文档')
ns = api.namespace('detect_api', description='结晶检测相关接口')


@ns.route('/start_detect/')
# 需要先处理图片为 640, 图片路径请传入绝对路径
class DETECT(Resource):
    def get(img_path='not specified'):
        """
            输入一张结晶图片, 返回
            :param img_path:
            :return:
        """
        # 传入参数，path绝对路径
        source = request.args.get("path")
        # 如果图片来源于网络，那么就把图片下载下来
        if "http" in source:
            req = requests.get(source)
            fileName = str(source).split("/")[-1]
            source = os.path.split(os.path.realpath(__file__))[0] + '/detect/inference/images/' + fileName
            with open(source, 'wb') as f:
                f.write(req.content)
        else:
            source = source

        result = detect(
            source=source,
            weights=os.path.split(os.path.realpath(__file__))[0] + "/detect/best.pt",
            img_size=640,
            conf_thres=0.25,
            iou_thres=0.1,
            save_conf=False,
            augment=False,
        )
        # view_image(image_path=source, result=result)
        # 结果可能还需要处理为整数
        response = make_response(jsonify(
            {"description": "result中的元素的第一个位置是类别，剩下四个是x1y1x2y2", "code": 200, "result": result}
        ))

        # 检测完成之后，将图片删除
        if os.path.exists(source):
            os.remove(source)
            print('成功删除文件:', source)
        else:
            print('未找到此文件:', source)
        return response

# @ns.route('/start_detect/<path:img_path>')
# class DETECT(Resource):
#     def get(self, img_path='not specified'):
#         if "http" in img_path:
#             req = requests.get(img_path)
#             fileName = str(img_path).split("/")[-1]
#             source = os.path.split(os.path.realpath(__file__))[0] + '/detect/inference/images/' + fileName
#             with open(source, 'wb') as f:
#                 f.write(req.content)
#         else:
#             source = img_path
#
#         result = detect(
#             source=source,
#             weights=os.path.split(os.path.realpath(__file__))[0] + "/detect/best.pt",
#             img_size=640,
#             conf_thres=0.25,
#             iou_thres=0.1,
#             save_conf=False,
#             augment=False,
#         )
#         # view_image(image_path=source, result=result)
#         response = make_response(jsonify(
#             {"description": "result中的元素的第一个位置是类别，剩下四个是x1y1x2y2", "code": 2000, "result": result}
#         ))
#         if os.path.exists(source):
#             os.remove(source)
#             print('成功删除文件:', source)
#         else:
#             print('未找到此文件:', source)
#         return response
