import numpy as np
from random import randrange
import cv2
from helpers import gradient, edge_detection

# paintfyies the image
def drawStrokes(image, threshold, s_len, s_wid):
    new_image = np.copy(image)
    grad_mags, grad_angles = gradient.calcGradient(image, threshold)

    # subset of pixels to paint, I chose every third pixel
    for h in range(0, new_image.shape[0]-1, 3):
        for w in range(0, new_image.shape[1]-1, 3):

            pixel = image[h, w]
            length = randrange(1, s_len+1) # random length, based on slider
            p1 = (w, h)
            angle = grad_angles[h, w] 
            # right triangle, solve for new x, new y with soh cah toa. 
            p2 = (np.round(w + length*np.cos(angle)).astype(int), np.round(h + length*np.sin(angle)).astype(int))

            # keep line within image so no errors from edge detection function
            if p2[0] >= new_image.shape[1]:
                p2 = (new_image.shape[1]-1, p2[1])
            if p2[1] >= new_image.shape[0]:
                p2 = (p2[0], new_image.shape[0]-1)
            
            if p2[0] < 0:
                p2 = (0, p2[1])
            if p2[1] < 0:
                p2 = (p2[0], 0)
        
            # check for edge and clip the line
            p1, p2 = edge_detection.detectEdge(grad_mags, p1, p2) 
            color = tuple([int(x) for x in pixel])

            width = randrange(1, s_wid+1) #random width, based on slider
            cv2.line(new_image, p1, p2, color, width)
    
    return new_image