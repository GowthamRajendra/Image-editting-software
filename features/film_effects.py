import numpy as np
import cv2

# adjusts the image's color palette, contrast, and saturation based on user chosen slider values
def adjust_image(im, pal_val, con_val, sat_val):
    adjusted_im = np.copy(im)

    adjusted_im = changePalette(adjusted_im, pal_val)
    adjusted_im = changeContrast(adjusted_im, con_val)
    adjusted_im = changeSaturation(adjusted_im, sat_val)

    return adjusted_im

# helper functions, only used here so I didn't put them in their own files
# changes saturation of image based on slider value
def changeSaturation(image, slider_val):
    if slider_val == 0:
        return image

    hsv_im = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    hsv_im[:, :, 1] = np.clip(hsv_im[:, :, 1] + slider_val, 0, 255) # add slider value to S-channel
    editted_im = cv2.cvtColor(hsv_im, cv2.COLOR_HSV2RGB)
    return editted_im

# changes contrast of image based on slider value
def changeContrast(image, slider_val):
    if slider_val == 0:
        return image
    
    x0, y0 = (0, 0) # interpolation points
    x1, y1 = (85+(slider_val*41.5), 85-(slider_val*85)) # slider value changes the s-shape curve
    x2, y2 = (170-(slider_val*41.5), 170+(slider_val*85))
    x3, y3 = (255,255)

    # print(f'points: (x0,y0)=({x0},{y0})\n(x1,y1)=({x1},{y1})\n(x2,y2)=({x2},{y2})\n(x3,y3)=({x3},{y3})\n')    

    x_mat = np.array([
        [0,     0,     0,  1],
        [x1**3, x1**2, x1, 1],
        [x2**3, x2**2, x2, 1],
        [x3**3, x3**2, x3, 1]
    ])

    y_mat = np.array([
        [y0],
        [y1],
        [y2],
        [y3]
    ])

    a,b,c,d = np.matmul(np.linalg.inv(x_mat), y_mat)
    
    hsv_im = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    curve = np.arange(256)
    curve = a*curve**3 + b*curve**2 + c*curve + d # cubic curve that goes through the 4 points
    curve = np.clip(curve, 0, 255)
    hsv_im[:, :, 2] = curve[hsv_im[:, :, 2]] # apply curve

    # print(f'v-min: {np.min(hsv_im[:, :, 2])}, v-max: {np.max(hsv_im[:, :, 2])}')
    # editted_im = cv2.cvtColor(hsv_im, cv2.COLOR_HSV2RGB)
    
    editted_im = cv2.cvtColor(hsv_im, cv2.COLOR_HSV2RGB)

    return editted_im

# changes color palette of image based on slider value
def changePalette(image, slider_val):
    if slider_val == 0:
        return image
    editted_im = np.copy(image)
    editted_im[:, :, 0] = np.clip(image[:, :, 0] + slider_val, 0, 255) # change red with slider_val
    editted_im[:, :, 2] = np.clip(image[:, :, 2] + (-slider_val), 0, 255) # change blue
    return editted_im   