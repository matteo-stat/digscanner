import math
import numpy as np
import cv2 as cv


def get_start_px(img, crop_perc=0.05):
    
    # pixels to consider as border
    crop_px = int(math.sqrt(img.shape[0]**2 + img.shape[1]**2) * crop_perc)
    
    # kernel size for gaussian blur must be an odd integer
    blur_kernel_size = int(crop_px / 4)
    if blur_kernel_size % 2 == 0:
        blur_kernel_size += 1
    blur_kernel_size = (blur_kernel_size, blur_kernel_size)
        
    # image borders
    borders_list = {
        'top': img[:crop_px],
        'bottom': img[-crop_px:],
        'left': img[:,:crop_px],
        'right': img[:,-crop_px:]
    }
    
    # image start px
    start_px = {}
    
    # for each side find image start px
    for side, border in borders_list.items():
        
        # convert to gray, blur the image and get a binary mask with otsu threshold
        gray = cv.cvtColor(border, cv.COLOR_BGR2GRAY)
        blur = cv.GaussianBlur(gray, ksize=blur_kernel_size, sigmaX=0)
        ret, th = cv.threshold(blur, thresh=0, maxval=255, type=cv.THRESH_BINARY + cv.THRESH_OTSU)

        # calculate distances between side and the beginning of the image
        if side in ['top', 'bottom']:
            dist = np.sum(th == 255, axis=0)
        else:
            dist = np.sum(th == 255, axis=1)

        # exclude useless sides
        dist = dist[np.where(dist < crop_px)]

        # remove extreme distances, useful since binary mask is not 100% accurate
        dist = dist[np.where((dist > np.percentile(dist, q=5)) & (dist < np.percentile(dist, q=95)))]

        # fingers crossed and hope that image start at median distance
        start = int(np.percentile(dist, q=50))
        if side == 'bottom':
            start = img.shape[0] - start
        elif side == 'right':
            start = img.shape[1] - start

        # set start px
        start_px[side] = start            
            
        # plt.imshow(th, cmap='gray', vmin=0, vmax=255)
        # plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB), interpolation='nearest')
        # if side in ['top', 'bottom']:
        #    plt.plot([0, img.shape[1]], [start, start], color='red', linestyle='-', linewidth=1)
        # else:
        #    plt.plot([start, start], [0, img.shape[0]], color='red', linestyle='-', linewidth=1)
                    
    return start_px
