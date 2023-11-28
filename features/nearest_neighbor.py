import numpy as np

def resize(image, new_height,new_width):
    new_image = np.zeros(shape=(new_height, new_width, 3))

    sampling_heights = np.round(np.linspace(0, image.shape[0]-1, new_height)).astype(int)
    sampling_widths = np.round(np.linspace(0, image.shape[1]-1, new_width)).astype(int)


    for h in range(len(sampling_heights)):
        for w in range(len(sampling_widths)):
            new_image[h,w] = image[sampling_heights[h], sampling_widths[w]]
    
    return new_image.astype(np.uint8)