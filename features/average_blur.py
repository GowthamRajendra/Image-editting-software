import scipy as sp
import numpy as np
from scipy import signal

def blur(im, half_w):
    f_height = int(half_w*2 + 1) # square shape
    filter = np.ones(shape=(f_height, f_height), dtype=float) / (f_height * f_height)

    blurred_im = np.copy(im)
    blurred_im[:,:,0] = sp.signal.convolve2d(im[:, :, 0], filter, mode='same', boundary='fill') # r
    blurred_im[:,:,1] = sp.signal.convolve2d(im[:, :, 1], filter, mode='same', boundary='fill') # g
    blurred_im[:,:,2] = sp.signal.convolve2d(im[:, :, 2], filter, mode='same', boundary='fill') # b

    return blurred_im.astype(np.uint8)