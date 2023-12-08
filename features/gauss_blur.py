import numpy as np
import scipy as sp
from scipy import signal

def blur(im, halfw):
    var = np.square(halfw/3)  # square std to get variance
    cov = np.array([[var, 0],[0, var]])
    filter = create_gau_kernel(cov, halfw) # mean is 0 so I did not include it
    filter = filter / np.sum(filter) # normalize

    blurred_im = np.copy(im)
    blurred_im[:,:,0] = sp.signal.convolve2d(im[:, :, 0], filter, mode='same', boundary='fill') # r
    blurred_im[:,:,1] = sp.signal.convolve2d(im[:, :, 1], filter, mode='same', boundary='fill') # g
    blurred_im[:,:,2] = sp.signal.convolve2d(im[:, :, 2], filter, mode='same', boundary='fill') # b

    return blurred_im.astype(np.uint8)


def create_gau_kernel(cov, halfw):
    width = int(halfw*2 + 1)
    x = np.linspace(-halfw, halfw, width)
    y = np.linspace(-halfw, halfw, width)

    xc, yc = np.meshgrid(x, y) # coordinates
    xy = np.zeros([width, width, 2])
    xy[:, :, 0] = xc
    xy[:, :, 1] = yc

    invcov = np.linalg.inv(cov)
    kernel = np.ones([xy.shape[0], xy.shape[1]])
    for x in range(xy.shape[0]):
        for y in range(xy.shape[1]):
            v = xy[x, y, :].reshape(2,1)
            kernel[x, y] = np.dot(np.dot(np.transpose(v), invcov), v)
    kernel = np.exp(-kernel/2)

    return kernel