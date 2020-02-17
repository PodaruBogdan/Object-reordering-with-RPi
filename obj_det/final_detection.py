import keras
from keras_retinanet.utils.image import read_image_bgr, preprocess_image, resize_image
from keras_retinanet.utils.visualization import draw_box, draw_caption
from keras_retinanet.utils.colors import label_color
from keras_retinanet.utils.gpu import setup_gpu
from keras_retinanet.models import load_model
# import miscellaneous modules
import matplotlib.pyplot as plt
import cv2
import os
import numpy as np
import time
gpu = 0
setup_gpu(gpu)
model_path = "/home/pi/py_projects/obj_det/keras-retinanet/snapshots/resnet50_coco_best_v2.1.0.h5"
model = load_model(model_path, backbone_name='resnet50')
labels_to_names = {0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus', 6: 'train', 7: 'truck', 8: 'boat', 9: 'traffic light', 10: 'fire hydrant', 11: 'stop sign', 12: 'parking meter', 13: 'bench', 14: 'bird', 15: 'cat', 16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow', 20: 'elephant', 21: 'bear', 22: 'zebra', 23: 'giraffe', 24: 'backpack', 25: 'umbrella', 26: 'handbag', 27: 'tie', 28: 'suitcase', 29: 'frisbee', 30: 'skis', 31: 'snowboard', 32: 'sports ball', 33: 'kite', 34: 'baseball bat', 35: 'baseball glove', 36: 'skateboard', 37: 'surfboard', 38: 'tennis racket', 39: 'bottle', 40: 'wine glass', 41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl', 46: 'banana', 47: 'apple', 48: 'sandwich', 49: 'orange', 50: 'broccoli', 51: 'carrot', 52: 'hot dog', 53: 'pizza', 54: 'donut', 55: 'cake', 56: 'chair', 57: 'couch', 58: 'potted plant', 59: 'bed', 60: 'dining table', 61: 'toilet', 62: 'tv', 63: 'laptop', 64: 'mouse', 65: 'remote', 66: 'keyboard', 67: 'cell phone', 68: 'microwave', 69: 'oven', 70: 'toaster', 71: 'sink', 72: 'refrigerator', 73: 'book', 74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear', 78: 'hair drier', 79: 'toothbrush'}
img1 = read_image_bgr("/home/pi/py_projects/PI_Incoming/imgr.jpg")
img2 = read_image_bgr("/home/pi/py_projects/PI_Incoming/imgt.jpg")
draw = img1.copy()
draw2 = img2.copy()
draw = cv2.cvtColor(draw, cv2.COLOR_BGR2RGB)
draw2 = cv2.cvtColor(draw2, cv2.COLOR_BGR2RGB)

# preprocess image for network
img1 = preprocess_image(img1)
img1, scale1 = resize_image(img1)

img2 = preprocess_image(img2)
img2, scale2 = resize_image(img2)

# process image
start = time.time()
boxes1, scores1, labels1 = model.predict_on_batch(np.expand_dims(img1, axis=0))
#boxes2, scores2, labels2 = model.predict_on_batch(np.expand_dims(img2, axis=0))
print("processing time: ", time.time() - start)

# correct for image scale
boxes1 /= scale1
#boxes2 /= scale2

img1t = cv2.imread("/home/pi/py_projects/PI_Incoming/imgr.jpg")
img2t = cv2.imread("/home/pi/py_projects/PI_Incoming/imgt.jpg")
# visualize detections
count = 0
templates = []
found1 = []
for box, score, label in zip(boxes1[0], scores1[0], labels1[0]):
    count = count + 1
    if score < 0.7:
        break
    color = label_color(label)
    b = box.astype(int)
    x1 = b[0]
    y1 = b[1]
    x2 = b[2]
    y2 = b[3]
    crop_img=img1t[y1:y2,x1:x2]
    cv2.imwrite("cropped_"+labels_to_names[label]+str(count)+".jpg",crop_img)
    gray_img = cv2.cvtColor(img1t, cv2.COLOR_BGR2GRAY)
    template = cv2.imread("cropped_"+labels_to_names[label]+str(count)+".jpg", cv2.IMREAD_GRAYSCALE)
    templates.append(template)
    w, h = template.shape[::-1]
    result = cv2.matchTemplate(gray_img, template, cv2.TM_CCORR_NORMED  )
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    img_copy = img1t.copy()
    cv2.rectangle(img_copy,top_left,bottom_right, (0, 255, 0), 3)
    found1.append((top_left[0], top_left[1]))

found2 = []
for template in templates:
    gray_img = cv2.cvtColor(img2t, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(gray_img, template, cv2.TM_CCORR_NORMED  )
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    img_copy = img2t.copy()
    cv2.rectangle(img_copy, top_left, bottom_right, (0, 255, 0), 3)
    found2.append((top_left[0], top_left[1]))


def relative_order(list):
    l = []
    for i in range(0,len(list)-1):
        l.append(np.sign(list[i]-list[i+1]))
    return l


def check_signs(signs1, signs2):
    for i in range(0, len(signs1)):
        if signs1[i] != signs2[i]:
            return 0
    return 1

xcoords1 = [x for (x, y) in found1]
xcoords2 = [x for (x, y) in found2]
signs1 = relative_order(xcoords1)
signs2 = relative_order(xcoords2)
result = check_signs(signs1, signs2)
with open("/home/pi/py_projects/result.txt","w+") as file:
    file.write("IN ORDER" if result==1 else "NOT IN ORDER")
print("IN ORDER" if result==1 else "NOT IN ORDER")
