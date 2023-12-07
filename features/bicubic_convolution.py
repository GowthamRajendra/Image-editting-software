import numpy as np
import cv2
from PySimpleGUI import one_line_progress_meter

# PROJECT: Bicubic Convolution Interpolation

def u(s):
    # this kernel uses -0.5 value for 'a'
    a = -0.5

    if (s >= 0) & (s <= 1):
        return (a + 2) * (s**3) - (a + 3) * (s**2) + 1
    elif (s > 1) & (s <= 2):
        return a * (s**3) - (5*a) * (s**2) + (8 * a) * s - 4 * a

    return 0  # return 0 for any other values


def resize(im, new_h, new_w):
    # image dimensions
    height, width, channels = im.shape

    # padding image by repeating boundary
    im = cv2.copyMakeBorder(im, 2, 2, 2, 2, cv2.BORDER_REPLICATE)

    # new empty image
    new_im = np.zeros((new_h, new_w, channels))

    # creating sampling points
    sampling_heights = np.linspace(0, height, new_h+1) + 2
    sampling_widths = np.linspace(0, width, new_w+1) + 2

    for h in range(new_h):

        # progress bar
        one_line_progress_meter("Bicubic Convolution Resizing", h, new_h-1, "Progress", orientation="h", no_button=True, keep_on_top=True)

        for w in range(new_w):
            # current sampling points
            y = sampling_heights[h]
            x = sampling_widths[w]

            # scaled x and y values used for kernel
            x1 = abs((x % 1) - -1)  # for clarity
            x2 = abs((x % 1) - 0)
            x3 = abs((x % 1) - 1)
            x4 = abs((x % 1) - 2)

            y1 = abs((y % 1) - -1)  # for clarity
            y2 = abs((y % 1) - 0)
            y3 = abs((y % 1) - 1)
            y4 = abs((y % 1) - 2)

            # creating x and y kernels
            kernel_x = np.array([u(x1), u(x2), u(x3), u(x4)])
            kernel_y = np.array([[u(y1)], [u(y2)], [u(y3)], [u(y4)]])

            for c in range(channels):
                # x1,..,x4 , y1,..,y4 are distances from current pixel
                # 2 pixels on left of current pixel
                # 2 pixels on right of current pixel
                values = np.array([[im[int(y-y1), int(x-x1), c],
                                   im[int(y-y2), int(x-x1), c],
                                   im[int(y+y3), int(x-x1), c],
                                   im[int(y+y4), int(x-x1), c]],
                                  [im[int(y-y1), int(x-x2), c],
                                   im[int(y-y2), int(x-x2), c],
                                   im[int(y+y3), int(x-x2), c],
                                   im[int(y+y4), int(x-x2), c]],
                                  [im[int(y-y1), int(x+x3), c],
                                   im[int(y-y2), int(x+x3), c],
                                   im[int(y+y3), int(x+x3), c],
                                   im[int(y+y4), int(x+x3), c]],
                                  [im[int(y-y1), int(x+x4), c],
                                   im[int(y-y2), int(x+x4), c],
                                   im[int(y+y3), int(x+x4), c],
                                   im[int(y+y4), int(x+x4), c]]])

                new_im[h, w, c] = np.dot(np.dot(kernel_x, values), kernel_y)

    # clip values to avoid overflow
    return np.clip(new_im, 0, 255)
