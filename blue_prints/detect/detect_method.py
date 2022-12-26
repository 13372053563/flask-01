# -*- coding: utf-8 -*-
"""
@author: zhangshihao
@file: detect_method.py
@time: 2022/12/15 20:03
"""
import os

import torch

from blue_prints.detect.models.experimental import attempt_load
from blue_prints.detect.utils.datasets import LoadImages
from blue_prints.detect.utils.general import non_max_suppression, \
    scale_coords, xyxy2xywh
from blue_prints.detect.utils.num2label import num2label
from blue_prints.detect.utils.torch_utils import select_device

# model = attempt_load(os.path.split(os.path.realpath(__file__))[0] + "/best.pt",
#                      map_location=select_device())  # load FP32 model
# path = os.path.split(os.path.realpath(__file__))[0]
# model = torch.hub.load(path, 'best.pt', source='local')


# @profile(precision=4, stream=open("memory_profiler.log", "w+"))
def detect_method(source=r"D:\project\python\Python-Web\flask-01\blue_prints\detect\inference\images\bus.jpg",
                  weights="yolov7.pt",
                  # model='',
                  source_shape=[],
                  img_size=640,
                  conf_thres=0.25,
                  iou_thres=0.1,
                  save_conf=False,
                  augment=False,
                  ):
    h, w, _ = source_shape[0], source_shape[1], source_shape[2]

    device = select_device()
    half = device.type != 'cpu'  # half precision only supported on CUDA

    model = attempt_load(weights, map_location=device)  # load FP32 model
    stride = int(model.stride.max())  # model stride

    if half:
        model.half()  # to FP16

    dataset = LoadImages(source, old_shape=source_shape, img_size=img_size, stride=stride)
    names = model.module.names if hasattr(model, 'module') else model.names

    # Run inference
    if device.type != 'cpu':
        model(torch.zeros(1, 3, img_size, img_size).to(device).type_as(next(model.parameters())))  # run once

    for img, im0s in dataset:
        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        with torch.no_grad():
            pred = model(img, augment=augment)[0]
        pred = non_max_suppression(pred, conf_thres, iou_thres, classes=None, agnostic=False)

        # Process detections
        result_one_image = []
        for i, det in enumerate(pred):  # detections per image
            s, im0, frame = '', im0s, getattr(dataset, 'frame', 0)

            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()
                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string
                for *xyxy, conf, cls in reversed(det):
                    cls = cls.tolist()
                    xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                    x_, y_, w_, h_ = xywh[0], xywh[1], xywh[2], xywh[3]
                    x1 = w * x_ - 0.5 * w * w_
                    x2 = w * x_ + 0.5 * w * w_
                    y1 = h * y_ - 0.5 * h * h_
                    y2 = h * y_ + 0.5 * h * h_
                    xywh = []
                    xywh.append(x1)
                    xywh.append(y1)
                    xywh.append(x2)
                    xywh.append(y2)
                    line = (num2label(int(cls)), *xywh, conf) if save_conf else (
                        num2label(int(cls)), *xywh)  # label format
                    result_one_image.append(line)
    del model, dataset
    return result_one_image

# if __name__ == '__main__':
#     with torch.no_grad():
#         result_one_image = detect_method()
