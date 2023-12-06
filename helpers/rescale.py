import numpy as np

def scale_sampling(sampling_points):
    scaled_samples = np.copy(sampling_points)
    for r in range(sampling_points.shape[0]):
        if not sampling_points[r].is_integer():  # scale values to (0, 1) range 
            scaled_samples[r] = sampling_points[r] - np.floor(sampling_points[r])
        elif r == sampling_points.shape[0]-1:
            scaled_samples[r] = 1
        elif r == 0:
            scaled_samples[r] = 0
    
    # print(f'{sampling_points} scaled -> {scaled_samples}')
    return scaled_samples