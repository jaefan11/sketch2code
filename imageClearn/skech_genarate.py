import cv2
import numpy as np
import random
import os
def img_detect(path,name):
    domList = []
    img = cv2.imread(path)
    # img = cv2.medianBlur(img,3)
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, img_bin = cv2.threshold(imgray, 127, 255, cv2.THRESH_BINARY)
    color_bound={"red":[[10,255,255],[0,43,46]],"yellow":[[34,255,255],[26,43,46]],"green":[[77,255,255],[35,43,46]],"blue":[[124,255,255],[100,43,46]],"violet":[[155,255,255],[125,43,46]]}
    color_type = {"red":"paragraph","yellow":"button","green":"title","blue":"input","violet":"img"}
    colors = list(color_bound.keys())
    for cl in colors:
        orange_lower = np.array(color_bound[cl][1], dtype="uint8")
        orange_upper = np.array(color_bound[cl][0], dtype="uint8")
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, orange_lower, orange_upper)
        coutours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        if len(coutours)>0:
            for i in range(len(coutours)):
                dom = {}
                x,y,w,h = cv2.boundingRect(coutours[i])
                dom["type"] = color_type[cl]
                dom["x"] = x
                dom["y"] = y
                dom["width"] = w
                dom["height"] = h
                if w<3 or h<3:
                    continue
                domList.append(dom)
                el_path = color_type[cl] + "/"+color_type[cl]+str(random.randint(0,4))+".png"
                sk = cv2.imread(el_path, cv2.IMREAD_GRAYSCALE)
                ret, sk_bin = cv2.threshold(sk, 127, 255, cv2.THRESH_BINARY)
                if color_type[cl]=="title":
                    x1 = float(sk_bin.shape[1])
                    y1 = float(sk_bin.shape[0])
                    y1 = y1*w/x1
                    x1 = w
                    if y1>h:
                        x1 = x1*h/y1
                        y1 = h
                    x1 = int(x1)
                    y1 = int(y1)
                    if x1==0 or y1==0:
                        break
                    ip = cv2.INTER_AREA
                    if x1 > sk_bin.shape[1] or y1>sk_bin.shape[0]:
                        ip = cv2.INTER_CUBIC
                    sk_bin = cv2.resize(sk_bin, (x1, y1), interpolation=ip)
                    x = int(x+(w-x1)/2)
                    y = int(y+(h-y1)/2)
                    img_bin[y:y + y1, x:x + x1] = sk_bin
                else:
                    ip = cv2.INTER_AREA
                    if w > sk_bin.shape[1] or h > sk_bin.shape[0]:
                        ip = cv2.INTER_CUBIC
                    sk_bin = cv2.resize(sk_bin, (w, h), interpolation=ip)
                    img_bin[y:y + h, x:x + w] = sk_bin
    cv2.imwrite(os.path.join("web_sk/",name),img_bin)

fpath=os.listdir("web_norm/")
# print(fpath)
# for path in fpath:
#     print(path)np.zeros_like
#     img_detect(os.path.join("web_norm/",path),path)
img_detect(os.path.join("web_norm/","1.png"),"1.png")
cv2.morphologyEx(img_bin,cv2.MORPH_CLOSE,kernel,iterations=5)