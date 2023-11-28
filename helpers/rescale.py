import numpy as np

def scale_sampling(sampling_points):
    scaled_samples = np.copy(sampling_points)
    for r in range(sampling_points.shape[0]):
        if not sampling_points[r].is_integer():  # scale values to (0, 1) range 
            scaled_samples[r] = sampling_points[r] - np.floor(sampling_points[r])
        elif sampling_points[r] != 0:            # whole number would scale down to 1
            scaled_samples[r] -= scaled_samples[r] - 1
    
    # print(f'scaled_samples to 0-1: {scaled_samples}')
    return scaled_samples