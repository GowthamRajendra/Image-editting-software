import numpy as np
from PySimpleGUI import one_line_progress_meter
from helpers import rescale

# resizes image using bilinear interpolation
def resize(im, new_h, new_w):
    new_im = np.zeros(shape=(new_h, new_w, 3))

    sampling_heights = np.linspace(0, im.shape[0]-1, new_h)
    sampling_widths = np.linspace(0, im.shape[1]-1, new_w)

    # add 0.001 so edge sampling points (whole numbers) are not repeated during
    # interpolation. 
    ints = np.mod(sampling_heights, 1)
    sampling_heights[ints == 0] += 0.001
    sampling_heights[-1] -= 0.001 # last point should be unaltered

    ints = np.mod(sampling_widths, 1)
    sampling_widths[ints == 0] += 0.001
    sampling_widths[-1] -= 0.001

    new_h = new_w = 0 # tracks where to place newly resized patch into resized image
    rp_h = rp_w = 0   # step for iterating new_h and new_w

    for h in range(im.shape[0]-1):
        # sampling locations within current height
        s_h = sampling_heights[np.logical_and(sampling_heights>=h, sampling_heights<=h+1)]

        # we put a progress bar because our bilinear is slow
        one_line_progress_meter("Bilinear Resizing", h, im.shape[0]-2, "Progress", orientation="h", no_button=True, keep_on_top=True)

        for w in range(im.shape[1]-1):   
            patch = im[h:h+2, w:w+2] # 2x2 patch to interpolate
            # sampling locations within current width 
            s_w = sampling_widths[np.logical_and(sampling_widths>=w, sampling_widths<=w+1)]

            # if there are sampling points within current 2x2 patch
            if len(s_h) > 0 and len(s_w) > 0:
                resized_patch = bilin_interpolate(patch, s_h, s_w)
                rp_h, rp_w, _ = resized_patch.shape # used for indexing in the resized image
                new_im[new_h:new_h+rp_h, new_w:new_w+rp_w] = resized_patch
                
                new_w += rp_w
            else:
                rp_w = rp_h = 0
        
        new_h += rp_h
        new_w = 0 # reset width index for the resized image every loop
    
    return new_im.astype(np.uint8)

# takes 2x2 patch and calculates unknowns to create equation that fits the plane
# then interpolates values at the sampling points
def bilin_interpolate(patch, sampling_heights, sampling_widths):
    new_patch = np.zeros(shape=(sampling_heights.shape[0], sampling_widths.shape[0], 3))

    sampling_heights = rescale.scale_sampling(sampling_heights) # scale values to [0, 1]
    sampling_widths = rescale.scale_sampling(sampling_widths)

    xc, yc = np.meshgrid(sampling_widths, sampling_heights)

    # sampling locations are scaled to 0-1 so this matrix is always the same
    locations_mat = np.array([[1, 0, 0, 0],
                              [1, 1, 0, 0],
                              [1, 0, 1, 0],
                              [1, 1, 1, 1]])

    for i in range(3): # channels
        channel = patch[:,:,i]

        Ix1y1 = channel[0, 0]
        Ix2y1 = channel[0, 1]
        Ix1y2 = channel[1, 0]
        Ix2y2 = channel[1, 1]
        
        intensities_mat = np.array([[Ix1y1],
                                    [Ix2y1],
                                    [Ix1y2],
                                    [Ix2y2]])

        # derivatives
        a0, a1, a2, a3 = np.matmul(np.linalg.inv(locations_mat), intensities_mat)
        
        new_patch[:, :, i] = a0 + a1*xc + a2*yc + a3*xc*yc
    
    return new_patch