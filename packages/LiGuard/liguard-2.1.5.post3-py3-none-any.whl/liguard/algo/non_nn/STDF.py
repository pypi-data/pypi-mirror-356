import pickle
import numpy as np

"""
Author: Muhammad Shahbaz (m.shahbaz.kharal@outlook.com)
Github: github.com/m-shahbaz-kharal

Spatio-Temporal Density Filter (STDF)
======================================

A simple implementation of a spatio-temporal density-based background filter that can operate on "unstructured" point cloud data (as well as structured). This term "unstructured", here, means that the point cloud cannot be represented by a fixed size HXV (horizontal resolution x vertical resolution) matrix. For example, if a LiDAR generate arbitrary number of points in each frame, and each point doesn't necessarily belong to a fixed azimuth and elevation ray, then the point cloud is unstructured. The algorithm can be used for such unstructured point clouds.

The algorithm is summarized in the following steps:
Since the number of points in each frame is not fixed, all the point clouds (gathered temporally) are stacked together to form a single point cloud.

1. A 3D (for spatial dimensions x, y, z) histogram of the point cloud is calculated across all frames.
2. The histogram is then normalized by the number of frames.
3. The normalized histogram is then used to filter out the background points as follows:
    a. For each point in the query point cloud, the point coordinates are used to find the bin index in the histogram.
    b. The density of the bin is then compared with a threshold:
        - If the density is less than the threshold, the point is considered as foreground,
        - otherwise background.
"""

def calc_STDF_params(point_cloud_set: list, # a list of point clouds, points in each frame must be equal
         lidar_range_in_unit_length: float, # maximum range of lidar in lidar unit length
         bins_per_unit_length: int, # number of bins per unit length
):
    number_of_frames = len(point_cloud_set)
    point_cloud_set = np.vstack(point_cloud_set).reshape(-1, point_cloud_set[0].shape[1])
    bins_per_side = int(lidar_range_in_unit_length * bins_per_unit_length)
    bins = np.linspace(-lidar_range_in_unit_length, lidar_range_in_unit_length, bins_per_side+1)
    histogram_range = [-lidar_range_in_unit_length, lidar_range_in_unit_length]
    histogram_3d, edges = np.histogramdd(point_cloud_set[:,:3], bins=(bins, bins, bins), range=[histogram_range, histogram_range, histogram_range])
    normalized_histogram_3d = histogram_3d / number_of_frames

    filter_params = dict(
        bins=bins,
        bins_per_side=bins_per_side,
        normalized_histogram_3d=normalized_histogram_3d
    )

    return filter_params
    
def make_STDF_filter(point_cloud: np.ndarray, # Nx3 or Nx4,
            background_density_threshold: float, # if the point falls in a bin with density less than this threshold, it is considered as foreground
            bins: np.ndarray, # bins for histogram
            bins_per_side: int, # number of bins per side
            normalized_histogram_3d: np.ndarray, # normalized histogram 3d
    ):
    voxel_indices = np.digitize(point_cloud[:,:3], bins) - 1
    voxel_indices = np.clip(voxel_indices, 0, bins_per_side-1)
    mask = normalized_histogram_3d[voxel_indices[:,0], voxel_indices[:,1], voxel_indices[:,2]] < background_density_threshold
    return mask

def save_STDF_params(filter_params, filename):
    filename = filename.split('.')[0] + '.pkl'
    with open(filename, 'wb') as f: pickle.dump(filter_params, f)
    return filename

def load_STDF_params(filename):
    try:
        filename = filename.split('.')[0] + '.pkl'
        with open(filename, 'rb') as f: return pickle.load(f)
    except:
        return None