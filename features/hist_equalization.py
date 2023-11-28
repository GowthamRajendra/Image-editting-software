import numpy as np
import cv2

def equalize(im):
    hsv_im = cv2.cvtColor(im, cv2.COLOR_RGB2HSV) # rgb to hsv
    L = 256
    bins = np.arange(L+1)
    hist, _ = np.histogram(hsv_im[:, :, 2], bins) # histogram from v-channel
    pdf = hist / np.sum(hist) 
    cdf = np.cumsum(pdf)      
    adjustment_curve = cdf*255

    adjusted_image = np.copy(hsv_im)
    adjusted_image[:, :, 2] = adjustment_curve[hsv_im[:, :, 2]].astype(np.uint8) # apply equalization to v-channel
    adjusted_image = cv2.cvtColor(adjusted_image, cv2.COLOR_HSV2RGB) # hsv to rgb

    return adjusted_image