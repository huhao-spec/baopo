import cv2
import os
import numpy as np

class TestLoader:
    # imdb image_path(list)
    def __init__(self, imdb, batch_size=1, shuffle=False):
        self.imdb = imdb
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.size = len(imdb)  # num of data
        # self.index = np.arange(self.size)

        self.cur = 0
        self.data = None
        self.label = None

        self.reset()
        self.get_batch()

    def reset(self):
        self.cur = 0
        if self.shuffle:
            # shuffle test image
            np.random.shuffle(self.imdb)

    def iter_next(self):
        return self.cur + self.batch_size <= self.size

    # realize __iter__() and next()--->iterator
    # return iter object
    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        if self.iter_next():
            self.get_batch()
            self.cur += self.batch_size
            return self.data
        else:
            raise StopIteration

    def getindex(self):
        return self.cur / self.batch_size

    def getpad(self):
        if self.cur + self.batch_size > self.size:
            return self.cur + self.batch_size - self.size
        else:
            return 0

    def get_batch(self):
        imdb = self.imdb[self.cur]
        '''
        cur_from = self.cur
        cur_to = min(cur_from + self.batch_size, self.size)
        #picked image
        imdb = [self.imdb[self.index[i]] for i in range(cur_from, cur_to)]
        # print(imdb)
        '''
        # print type(imdb)
        # print len(imdb)
        # assert len(imdb) == 1, "Single batch only"
        im = cv2.imread(imdb)
        self.data = im

path = "D:/BaiduNetdiskDownload/2" # 保存测试图片的地方
gt_imdb=[]
for item in os.listdir(path):
    gt_imdb.append(os.path.join(path,item))
test_data = TestLoader(gt_imdb)

count = 0
for imagepath in gt_imdb:
    print(imagepath)
    image = cv2.imread(imagepath)
    save_path = 'D:/pycharm/test/'   # 图片保存的路径
    count += 1
    cv2.imwrite(save_path+'%d.jpg'%(count),image)
    # os.path.dirname(path)
    # 语法：os.path.dirname(path)
    # 功能：去掉文件名，返回目录
    os.makedirs(os.path.dirname(save_path),exist_ok=True)
