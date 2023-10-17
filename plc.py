import cv2
import datetime
cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter.fourcc('m', 'p', '4', 'v')
name = 'D:/BaiduNetdiskDownload/2/' + str(datetime.date.today()) + '.avi'
out = cv2.VideoWriter(name, fourcc, 20, (640, 480))
while (cap.isOpened()):
    ret, frame = cap.read()
    if ret:
        out.write(frame)
        cv2.imshow('video', frame)
        c = cv2.waitKey(1)
        if c == 27:
            break
    else:
        break
cap.release()
out.release()
cv2.destroyAllWindows()