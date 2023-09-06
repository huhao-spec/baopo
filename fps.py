import json
import os
import time

import cv2
import numpy as np
import torch
from PIL import Image
from torchvision.transforms import transforms

from model import efficientnet_b0 as create_model
device = torch.device('cuda:0')
model = create_model(num_classes = 3).to(device)
fps = 0.0
video = cv2.VideoCapture("D:/__easyHelper__/1/1.mp4")
while(True):
    # data_transform = transforms.Compose(
    #     [transforms.Resize(224),
    #      transforms.CenterCrop(224),
    #      transforms.ToTensor(),
    #      transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])
    # t1 = time.time()
    # open, frame = video.read()
    # frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    # img = data_transform(frame)
    # # expand batch dimension
    # img = torch.unsqueeze(img, dim=0)
    # json_path = './class_indices.json'
    # assert os.path.exists(json_path), "file: '{}' dose not exist.".format(json_path)
    # with open(json_path, "r") as f:
    #     class_indict = json.load(f)
    # # create model
    # model = create_model(num_classes=3).to(device)
    # # load model weights
    # model_weight_path = "./weights/1.pth"
    # model.load_state_dict(torch.load(model_weight_path, map_location=device))
    # model.eval()
    # fps = (fps+(1./(time.time()-t1)))/2
    # print(fps)

    # capture = cv2.VideoCapture(0)  # 0代表调用电脑的默认摄像头
    # # # 检测视频
    # capture = cv2.VideoCapture("1.mp4")  #对视频进行检测，则将0改为视频文件

    # 定义起始fps
    fps = 0.0
    while (True):
        # 检测图片的起始时间
        t1 = time.time()
        # 读取某一帧
        ref, frame = video.read()
        # 格式转变，BGRtoRGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 利用OpenCV读取出来的图片的格式是BGR的，而目标检测中用到的图片格式是RGB
        # 转变成Image
        frame = Image.fromarray(np.uint8(frame))  # 平时进行目标检测的库PIL中的Image，因此图片转换成Image进行存储。将读取出来的以数组形式存储的图片转换成图片Image

        # 网络进行检测fps计算
        # 对传入的图片使用自己的目标检测算法进行检测
        frame = np.array(yolo.detect_image(frame))
        # RGBtoBGR满足opencv显示格式
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        # 将我们检测好了的图片的格式从RGB转换成OpenCV可处理的BGR的格式进行图片的展示

        # fps的计算
        fps = (fps + (1. / (time.time() - t1))) / 2  # 此处的time.time()就是检测完这张图片的结束时间,除以2是为了和之前的fps求一个平均
        print("fps= %.2f" % fps)
        frame = cv2.putText(frame, "fps= %.2f" % (fps), (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # 检测完的图片的展示
        cv2.imshow("video", frame)
        c = cv2.waitKey(30) & 0xff
        if c == 27:
            capture.release()
            break



