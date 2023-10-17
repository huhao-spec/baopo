# import cv2
#
# capture = cv2.imread("D:\BaiduNetdiskDownload/爆破析晶/1.mp4")
# while(True):
#     rval, frame = capture.read()
#     c = 0
#     rval = capture.isOpened()
#     while rval:
#         c = c + 1
#         folder_name = 'D:/__easyHelper__/2/1'
#         pic_path = folder_name + '/'
#         cropImg = frame[240:600, 720:1400]  # 裁剪【y1,y2：x1,x2】
#         pic_path_1 = pic_path + str(c) + '.png'
#         cv2.imwrite(pic_path_1, cropImg)
#         print(pic_path_1)
#     capture.release()

import cv2
import os

def save_img():

    video_path = 'D:\BaiduNetdiskDownload'
    videos = os.listdir(video_path)
    for video_name in videos:
        # file_name = video_name.split('.')[0]
        # file_name = '3.mp4'
        # folder_name = video_path + file_name
        # os.makedirs(folder_name, exist_ok=True)
        # video_name
        # vc = cv2.VideoCapture(video_path+'/'+video_name)
        vc = cv2.VideoCapture('D:\HAIKANG\iVMS-4200 Site/UserData\Video\RecordFile/20231016/192.168.2.3_8000_1_3419F0BEC5F44FE7BAE535586DC6D6F8_/9.mp4')
        c=0
        rval=vc.isOpened()
        folder_name = 'D:\HAIKANG\iVMS-4200 Site/UserData\Video\RecordFile/20231016/192.168.2.3_8000_1_3419F0BEC5F44FE7BAE535586DC6D6F8_/9'
        while rval:
            c = c + 1
            rval, frame = vc.read()
            pic_path = folder_name+'/'
            if rval:
                # cropImg = frame[240:600, 720:1400]
                cv2.imwrite(pic_path + str(c) + '.png', frame)
                print(pic_path + str(c) + '.png')
                cv2.waitKey(0)
            else:
                break
        vc.release()
        print('save_success')
        print(folder_name)

save_img()

