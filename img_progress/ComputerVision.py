import cv2
import numpy as np
import random
import os
class ComputerVision(object):
    @classmethod
    def img_detect(self,path):
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        ret, img_bin = cv2.threshold(img, 230, 255, cv2.THRESH_BINARY)
        coutours, hierarchy = cv2.findContours(img_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        rectangle = []
        img_aim = []
        domJson = []
        for cnt in range(len(coutours)):
            epsilon = 0.05 * cv2.arcLength(coutours[cnt], True)
            approx = cv2.approxPolyDP(coutours[cnt], epsilon, True)
            # 分析几何形状
            area = cv2.contourArea(coutours[cnt])
            corners = len(approx)
            if corners == 4 and area > 3:
                rectangle.append(cnt)

        for m in rectangle:
            triangle = []
            if hierarchy[0][m][2] != -1:
                child = hierarchy[0][m][2]
                while child != -1:
                    epsilon = 0.05 * cv2.arcLength(coutours[child], True)
                    approx = cv2.approxPolyDP(coutours[child], epsilon, True)
                    corners = len(approx)
                    area = cv2.contourArea(coutours[cnt])
                    if corners == 3 and area > 3:
                        triangle.append(child)
                    child = hierarchy[0][child][0]
                if len(triangle) == 3 or len(triangle) == 4:
                    rec_area = cv2.contourArea(coutours[m])
                    tri_area = 0
                    for j in triangle:
                        tri_area += cv2.contourArea(coutours[j])
                    if tri_area / rec_area > 0.75:
                        img_aim.append(m)


        for i in img_aim:
            dom = {}
            x, y, w, h = cv2.boundingRect(coutours[i])
            dom["type"] = "img"
            dom["x"] = x
            dom["y"] = y
            dom["width"] = w
            dom["height"] = h
            dom["contains"] = []
            domJson.append(dom)

        return domJson
    @classmethod
    def paragraph_detect(self,path):
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        ret, img_bin = cv2.threshold(img, 230, 255, cv2.THRESH_BINARY_INV)
        contours, hierarchy = cv2.findContours(img_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        not_closed_contours = []
        paragraphs = []
        domJson = []
        img_bin_filter = np.zeros_like(img_bin, dtype="uint8")
        for cnt in range(len(contours)):
            epsilon = 0.5 * cv2.arcLength(contours[cnt], True)
            approx = cv2.approxPolyDP(contours[cnt], epsilon, True)
            if cv2.isContourConvex(approx) == False:
                x, y, w, h = cv2.boundingRect(contours[cnt])
                if h < 25 and float(h) / w < 0.25:
                    not_closed_contours.append(cnt)
                    img_bin_filter[y:y + h, x:x + w] = img_bin[y:y + h, x:x + w]

        kernel = np.ones((5, 5), np.uint8)
        img_bin_filter_dilation = cv2.morphologyEx(img_bin_filter, cv2.MORPH_CLOSE, kernel, iterations=8)
        contours1, hierarchy1 = cv2.findContours(img_bin_filter_dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in range(len(contours1)):
            x, y, w, h = cv2.boundingRect(contours1[cnt])
            ROI = img_bin_filter[y:y + h, x:x + w]
            contours2, hierarchy2 = cv2.findContours(ROI, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            lines = []
            for i in range(len(contours2)):
                epsilon = 0.5 * cv2.arcLength(contours2[i], True)
                approx = cv2.approxPolyDP(contours2[i], epsilon, True)
                if cv2.isContourConvex(approx) == False:
                    x1, y1, w1, h1 = cv2.boundingRect(contours2[i])
                    if h1 < 25 and float(h1) / w1 < 0.25:
                        lines.append(i)
            if len(lines) >= 3:
                paragraphs.append(cnt)

        for i in paragraphs:
            dom = {}
            x, y, w, h = cv2.boundingRect(contours1[i])
            dom["type"] = "paragraph"
            dom["x"] = x
            dom["y"] = y
            dom["width"] = w
            dom["height"] = h
            dom["contains"] = []
            domJson.append(dom)

        return domJson