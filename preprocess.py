import numpy as np
import cv2
import os
from matplotlib import pyplot as plt

def ImgPreprocess(path):
    upper_path=path.split("/")[0]+"/"
    print(upper_path)
    if not os.path.exists(upper_path):
        os.makedirs(path)
        os.makedirs(os.path.join(upper_path,"original"))
        os.makedirs(os.path.join(upper_path,"generated"))
        os.makedirs(os.path.join(upper_path,"canny_img"))
        os.makedirs(os.path.join(upper_path,"result_pics"))
        # print("Please put the pictures in {0}/original".format(upper_path))
    else:
        for filename in os.listdir(path):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                in_filename = os.path.join(path, filename)
                img = cv2.imread(in_filename)
                ##須針對不同的資料來源進行調整，未來可用yolo補齊
                # img = img[300:850,620:1170] #照片
                img = img[200:1000,400:1200] #照片
                img = img[500:1000,500:1000]#banana
                # img=img[500:1400,1080:1500]#影片截圖
                # res = cv2.resize(img,(512, 512), interpolation = cv2.INTER_CUBIC)
                cv2.imwrite(os.path.join(upper_path,"generated/") + os.path.splitext(os.path.basename(in_filename))[0] + ".png",img)
                # cv2.imwrite(os.path.join(upper_path,"generated/") + os.path.splitext(os.path.basename(in_filename))[0] + ".tif",img)

if __name__ == '__main__':
    main()
