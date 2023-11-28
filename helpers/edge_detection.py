import numpy as np

# clips line at edge
def detectEdge(grad_mags, p1, p2):
    x_coor = np.arange(p1[0], p2[0]+1).round().astype(int) # x-values along line
    y_coor = np.interp(x_coor, [p1[0], p2[0]], [p1[1], p2[1]]).round().astype(int) # y-values along line
    coordinates = np.column_stack((x_coor, y_coor)) # coordinates along stroked line

    for x,y in coordinates:
        if grad_mags[y, x] > 0: # check each pixel in the line, if on a edge, clip it.
            return p1, (x, y) # p1, clipped p2
    
    # if no edges, return original line
    return p1, p2