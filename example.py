from glob import glob
import math

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

import digscannerlib as dsl

img_input_list = glob('C:/Users/Matteo/Desktop/scans/*.JPG')
img = cv.imread(img_input_list[1], cv.IMREAD_UNCHANGED)
img = cv.resize(img, (900, 600))
# plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB), interpolation='nearest')
# plt.show()

start_px = dsl.get_start_px(img=img, crop_perc=0.05)
start_px

plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB), interpolation='nearest')

for side, start in start_px.items():
    if side in ['top', 'bottom']:
        plt.plot([0, img.shape[1]], [start, start], color='red', linestyle='-', linewidth=1)
    else:
        plt.plot([start, start], [0, img.shape[0]], color='red', linestyle='-', linewidth=1)

plt.show()

r = 0