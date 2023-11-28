import numpy as np
from helpers import rescale

# resizes image using bilinear interpolation
def resize(im, new_h, new_w):
    new_im = np.zeros(shape=(new_h, new_w, 3))

    sampling_heights = np.linspace(0, im.shape[0]-1, new_h)
    sampling_widths = np.linspace(0, im.shape[1]-1, new_w)

    new_h = new_w = 0 # tracks where to place newly resized patch into resized image
    rp_h = rp_w = 0   # step for iterating new_h and new_w

    for h in range(im.shape[0]-1):
        # sampling locations within current height
        s_h = sampling_heights[np.logical_and(sampling_heights>=h, sampling_heights<=h+1)]

        for w in range(im.shape[1]-1):   
            patch = im[h:h+2, w:w+2] # 2x2 patch to interpolate
            # sampling locations within current width 
            s_w = sampling_widths[np.logical_and(sampling_widths>=w, sampling_widths<=w+1)]

            # if there are sampling points within current 2x2 patch
            if len(s_h) > 0 and len(s_w) > 0:
                resized_patch = bilin_interpolate(patch, s_h, s_w)
                rp_h, rp_w, _ = resized_patch.shape # used for indexing in the resized image
                new_im[new_h:new_h+rp_h, new_w:new_w+rp_w] = resized_patch
                
                next_s_w = sampling_widths[np.logical_and(sampling_widths>=w+1, sampling_widths<=w+2)]
                # for 1x1 edge values do not shift the index (prevents dupe values).
                if len(s_w) == 1 and np.array_equal(s_w, next_s_w):
                    continue
                # overlap the edge values
                elif len(next_s_w) > 1:
                    if s_w[-1] == next_s_w[0]:
                        new_w += rp_w - 1
                    else: # else shift new_h so the next interpolated patch is in the correct spot in the new image
                        new_w += rp_w
                else: # else shift new_h so the next interpolated patch is in the correct spot in the new image
                    new_w += rp_w
                

        # if a row was skipped due to having no sampling points in it, do not shift the new_h value.
        if len(s_h) == 0:
            continue
        
        elif len(s_h) > 0:
            next_s_h = sampling_heights[np.logical_and(sampling_heights>=h+1, sampling_heights<=h+2)]
            if len(s_h) == 1:
                # for 1x1 edge values do not shift the index if the next sampling point is the exact same (prevents dupe values). 
                # Not a problem for sizes above 1
                if np.array_equal(s_h, next_s_h):
                    continue
                else:
                    new_h += rp_h
            elif len(next_s_h) > 1:
                    # overlap the edge values
                if s_h[-1] == next_s_h[0]:
                        new_h += rp_h - 1
                else: # else shift new_h so the next interpolated patch is in the correct spot in the new image
                        new_h += rp_h
            else: # else shift new_h so the next interpolated patch is in the correct spot in the new image
                new_h += rp_h
        new_w = 0 # reset width index for the resized image every loop
    
    return new_im.astype(np.uint8)

# takes 2x2 patch and calculates unknowns to create equation that fits the plane
# then interpolates values at the sampling points
def bilin_interpolate(patch, sampling_heights, sampling_widths):
    new_patch = np.zeros(shape=(sampling_heights.shape[0], sampling_widths.shape[0], 3))
    # print(new_patch.shape)

    sampling_heights = rescale.scale_sampling(sampling_heights) # scale values to [0, 1]
    sampling_widths = rescale.scale_sampling(sampling_widths)

    xc, yc = np.meshgrid(sampling_widths, sampling_heights)
    # print(xc.shape)
    # print(yc.shape)

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

        # for h in range(new_patch.shape[0]):
        #     for w in range(new_patch.shape[1]):
        #         new_patch[h,w,i] = apply_polynomial(xc[h,w], yc[h,w], a0, a1, a2, a3)
        
        new_patch[:, :, i] = a0 + a1*xc + a2*yc + a3*xc*yc

    # print(f'new: {new_patch}')
    # print(f'new2: {new_patch2}')
    # exit()
    
    return new_patch