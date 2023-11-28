import numpy as np
import cv2
import scipy as sp

# calculate the image gradient magnitude and angles
def calcGradient(image, threshold):
    Ix = np.array([[-1, 1]]) # already flipped for convolution
    Iy = np.array([[-1],[1]])

    g_im = cv2.GaussianBlur(image, (5,5), 0) # smooth before calcing gradient
    g_im = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) # grayscale for easier calculation

    xgradient = sp.signal.convolve2d(g_im, Ix, 'same')
    ygradient = sp.signal.convolve2d(g_im, Iy, 'same')

    # print(xgradient, "\n\n", ygradient)
    
    grad_mags = np.sqrt(np.square(xgradient) + np.square(ygradient)) # calc magnitudes
    grad_angles = np.arctan2(xgradient, ygradient) # calc angles
        
    ming = np.min(grad_mags)
    maxg = np.max(grad_mags) 

    grad_mags = ((grad_mags - ming) * 255) / (maxg - ming) # rescale magnitudes to 0-255
    if threshold > 0: # remove edges that are less than the threshold
        grad_mags = np.where(grad_mags > threshold, grad_mags, 0)

    return grad_mags.astype(np.uint8), grad_angles