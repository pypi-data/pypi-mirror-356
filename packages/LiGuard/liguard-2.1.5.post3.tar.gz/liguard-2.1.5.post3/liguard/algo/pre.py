import inspect
from liguard.gui.gui_utils import resolve_for_application_root, resolve_for_default_workspace
from liguard.gui.logger_gui import Logger
from liguard.algo.utils import AlgoType, algo_func, get_algo_params, make_key
algo_type = AlgoType.pre

@algo_func(required_data=['current_point_cloud_numpy'])
def remove_nan_inf_allzero_from_pcd(data_dict: dict, cfg_dict: dict, logger: Logger):
    """
    Removes NaN values from the point cloud.

    Args:
        data_dict (dict): A dictionary containing the required data.
        cfg_dict (dict): A dictionary containing configuration parameters.
        logger (Logger): A logger object for logging messages.
    """
    #########################################################################################################################
    # standard code snippet that gets the parameters from the config file and checks if required data is present in data_dict
    # usually, this snippet is common for all the algorithms, so it is recommended to not remove it
    algo_name = inspect.stack()[0].function
    params = get_algo_params(cfg_dict, algo_type, algo_name, logger)
    
    # check if required data is present in data_dict
    for key in remove_nan_inf_allzero_from_pcd.required_data:
        if key not in data_dict:
            logger.log(f'{key} not found in data_dict', Logger.ERROR)
            return
    # standard code snippet ends here
    #########################################################################################################################
    
    # imports
    import numpy as np

    # Get required data from data_dict
    current_point_cloud_numpy = data_dict['current_point_cloud_numpy']

    # Remove NaN, inf, and zero values from the point cloud
    current_point_cloud_numpy = current_point_cloud_numpy[~np.isnan(current_point_cloud_numpy).any(axis=1), ...]
    current_point_cloud_numpy = current_point_cloud_numpy[~np.isinf(current_point_cloud_numpy).any(axis=1), ...]
    current_point_cloud_numpy = current_point_cloud_numpy[~np.all(current_point_cloud_numpy[:, :3] == 0, axis=1), ...]

    # update data_dict
    data_dict['current_point_cloud_numpy'] = current_point_cloud_numpy

@algo_func(required_data=[])
def manual_calibration(data_dict: dict, cfg_dict: dict, logger: Logger):
    """
    Manually calibrates the point cloud data.

    Args:
        data_dict (dict): A dictionary containing the required data.
        cfg_dict (dict): A dictionary containing configuration parameters.
        logger (Logger): A logger object for logging messages
    """
    #########################################################################################################################
    # standard code snippet that gets the parameters from the config file and checks if required data is present in data_dict
    # usually, this snippet is common for all the algorithms, so it is recommended to not remove it
    algo_name = inspect.stack()[0].function
    params = get_algo_params(cfg_dict, algo_type, algo_name, logger)
    
    # check if required data is present in data_dict
    for key in manual_calibration.required_data:
        if key not in data_dict:
            logger.log(f'{key} not found in data_dict', Logger.ERROR)
            return
    # standard code snippet ends here
    #########################################################################################################################

    # imports
    import numpy as np
    
    # parse params and add to data_dict
    try:
        Tr_velo_to_cam = np.array([float(x) for x in params['T_lidar_to_cam_4x4'].split(' ')], dtype=np.float32).reshape(4, 4)
        R0_rect = np.array([float(x) for x in params['rotation_matrix_4x4'].split(' ')], dtype=np.float32).reshape(4, 4)
        P2 = np.array([float(x) for x in params['cam_intrinsic_3x4'].split(' ')], dtype=np.float32).reshape(3, 4)
        calib = {'Tr_velo_to_cam': Tr_velo_to_cam, 'R0_rect': R0_rect, 'P2': P2}
        data_dict['current_calib_path'] = None
        data_dict['current_calib_data'] = calib
    except Exception as e:
        logger.log(f'Error: {e}', Logger.ERROR)