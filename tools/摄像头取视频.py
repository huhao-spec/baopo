import cv2
from predict import yuce
import threading
import time
class mian():
    # url = "rtsp://admin:a12345678@169.254.26.101/Streaming/Channels/101"
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    c = 0
    while ret:
        t1 = time.time()
        ret, frame = cap.read()
        cv2.imshow('1', frame)
        # cropImg = frame[240:600, 720:1400]
        cv2.imwrite('D:/BaiduNetdiskDownload/2/'+str(c)+'.jpg', frame)
        yuce('D:/BaiduNetdiskDownload/2/'+str(c)+'.jpg')
        print('D:/BaiduNetdiskDownload/2/'+str(c)+'.jpg')
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        c=c+1
        t2 = time.time()
        print(t2-t1)
    cv2.destroyAllWindows()
    cap.release()