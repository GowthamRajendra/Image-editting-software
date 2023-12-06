import cv2
import numpy as np
import scipy as sp
from PySimpleGUI import one_line_progress_meter
from helpers import rescale

# PROJECT: Bicubic Spline Interpolation
def resize(im, new_h, new_w):
    new_im = np.zeros(shape=(new_h, new_w, 3))

    # sampling points, np.meshgrid to make coordinates
    sampling_h = np.linspace(0, im.shape[0]-1, new_h)
    sampling_w = np.linspace(0, im.shape[1]-1, new_w)

    # add 0.001 so edge sampling points (whole numbers) are not repeated during
    # interpolation. 
    ints = np.mod(sampling_h, 1)
    sampling_h[ints == 0] += 0.001
    sampling_h[-1] -= 0.001 # last point should be unaltered

    ints = np.mod(sampling_w, 1)
    sampling_w[ints == 0] += 0.001
    sampling_w[-1] -= 0.001

    im = cv2.copyMakeBorder(im,1,1,1,1,0) # pad image with 0s

    new_h = new_w = 0 # for indexing in new image
    rp_h = rp_w = 0

    for h in range(im.shape[0]-3): # exclude right and bottom padding
        # sampling points in the center (2x2 section) of the 4x4 patch
        s_h = sampling_h[np.logical_and(sampling_h>=h, sampling_h<=h+1)]

        # progress bar
        one_line_progress_meter("Bicubic Spline Resizing", h, im.shape[0]-4, "Progress", orientation="h", no_button=True, keep_on_top=True)

        for w in range(im.shape[1]-3):
            s_w = sampling_w[np.logical_and(sampling_w>=w, sampling_w<=w+1)]
            
            # if there are sampling points within current patch, then interpolate them
            if len(s_h) > 0 and len(s_w) > 0:
                for c in range(3):
                    # calculate bicubic coefficients for this 4x4 patch
                    coefs = calc_coefs(im[h:h+4, w:w+4, c])

                    # interpolate the values of the sampling points
                    resized_patch = interp(coefs, s_h, s_w)

                    # for placing resized patch into correct spot in new image
                    rp_h, rp_w = resized_patch.shape
                    new_im[new_h:new_h+rp_h, new_w:new_w+rp_w, c] = resized_patch

                new_w += rp_w # move pointer to where to insert next patch
            else:
                rp_h = rp_w = 0

        new_h += rp_h
        new_w = 0

    return new_im.astype(np.uint8)

def interp(coefs, s_h, s_w):
    # changed structure to fit formula for calculating points
    coefs = np.array([
        [coefs[0], coefs[4], coefs[8], coefs[12]],
        [coefs[1], coefs[5], coefs[9], coefs[13]],
        [coefs[2], coefs[6], coefs[10], coefs[14]],
        [coefs[3], coefs[7], coefs[11], coefs[15]]
    ])

    # rescale sampling points to [0, 1]
    s_h = rescale.scale_sampling(s_h)
    s_w = rescale.scale_sampling(s_w)

    xc, yc = np.meshgrid(s_w, s_h)

    # iterate through points and interpolate their values
    resized_patch = np.zeros_like(xc)
    for x in range(resized_patch.shape[1]):
        for y in range(resized_patch.shape[0]):
            x_mat = np.array([1, xc[y,x], xc[y,x]**2, xc[y,x]**3])
            y_mat = np.array([[1], [yc[y,x]], [yc[y,x]**2], [yc[y,x]**3]])

            resized_patch[y,x] = np.dot(np.dot(x_mat, coefs), y_mat)

    # clip values to prevent overflow because cubic curves overshoot and undershoot.
    return np.clip(resized_patch, 0, 255).astype(np.uint8)

# calculate bicubic coefficients
def calc_coefs(patch=0):
    # inverse coefficients matrix, always the same
    A_inv = np.array([
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [-3, 3, 0, 0, -2, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [2, -2, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, -3, 3, 0, 0, -2, -1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 2, -2, 0, 0, 1, 1, 0, 0],

        [-3, 0, 3, 0, 0, 0, 0, 0, -2, 0, -1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, -3, 0, 3, 0, 0, 0, 0, 0, -2, 0, -1, 0],
        [9, -9, -9, 9, 6, 3, -6, -3, 6, -6, 3, -3, 4, 2, 2, 1],
        [-6, 6, 6, -6, -3, -3, 3, 3, -4, 4, -2, 2, -2, -2, -1, -1],

        [2, 0, -2, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 2, 0, -2, 0, 0, 0, 0, 0, 1, 0, 1, 0],
        [-6, 6, 6, -6, -4, -2, 4, 2, -3, 3, -3, 3, -2, -1, -2, -1],
        [4, -4, -4, 4, 2, 2, -2, -2, 2, -2, 2, -2, 1, 1, 1, 1],
    ]) 

    fxs = x_derv(patch.astype(np.float32))
    fys = y_derv(patch.astype(np.float32))
    fxys = x_derv(y_derv(patch.astype(np.float32))) # mixed partial derv


    # A^-1 * b = x, x is unknown coefficients matrix
    b = np.array([patch[1,1], patch[1,2], patch[2,1], patch[2,2], 
                  fxs[1,1], fxs[1,2], fxs[2,1], fxs[2,2],
                  fys[1,1], fys[1,2], fys[2,1], fys[2,2], 
                  fxys[1,1], fxys[1,2], fxys[2,1], fxys[2,2]])
    
    x = np.dot(A_inv, b.T)
    return x

# derivative in x-direction
def x_derv(patch):
    # this 3x3 kernel produces a more pronounced cubic curve
    # than its 1x3 variant
    kernel = np.array([
        [1, 0, -1],
        [1, 0, -1],
        [1, 0, -1]]
    )
    # kernel = [[-1, 0, 1]]

    return sp.ndimage.convolve(patch, kernel)

# derivative in y-direction
def y_derv(patch):
    kernel = np.array([[1,1,1], 
                       [0,0,0], 
                       [-1,-1,-1]])

    # kernel = [[-1],[0],[1]]

    return sp.ndimage.convolve(patch, kernel)

    


