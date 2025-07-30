import os
import sys
from liguard.gui.gui_utils import resolve_for_application_root, resolve_for_default_workspace, import_module
import glob
import time
import threading

lbl_dir = os.path.dirname(os.path.realpath(__file__))

supported_label_types = [lbl_handler.split('_')[1].replace('.py','') for lbl_handler in os.listdir(lbl_dir) if 'handler' in lbl_handler]

class FileIO:
    """
    Class for handling file input/output operations related to label files.
    """
    def __init__(self, cfg: dict, calib_reader: callable):
        """
        Initializes a FileIO object.

        Args:
            cfg (dict): Configuration dictionary containing parameters for file IO.
            calib_reader (callable): Function to read calibration data.

        Raises:
            NotImplementedError: If the calibration type is not supported.
        """
        # get params from config
        self.cfg = cfg
        main_dir = cfg['data']['main_dir']
        if not os.path.isabs(main_dir): main_dir = os.path.join(self.cfg['data']['pipeline_dir'], main_dir)
        self.lbl_dir = os.path.join(main_dir, cfg['data']['label_subdir'])
        if not os.path.exists(self.lbl_dir): raise FileNotFoundError(f'Directory {self.lbl_dir} does not exist.')
        self.lbl_type = cfg['data']['label']['lbl_type']
        self.lbl_start_idx = cfg['data']['start']['label']
        self.global_zero = cfg['data']['start']['global_zero']
        self.lbl_end_idx = self.lbl_start_idx + cfg['data']['count']
        
        # Add custom supported calibration types to the list
        custom_data_handlers_dir = os.path.join(cfg['data']['pipeline_dir'], 'data_handler')
        custom_label_data_handlers_dir = os.path.join(custom_data_handlers_dir, 'label')
        if os.path.exists(custom_label_data_handlers_dir):
            if custom_data_handlers_dir not in sys.path: sys.path.append(custom_data_handlers_dir)
            custom_supported_label_types = [lbl_handler.split('_')[1].replace('.py','') for lbl_handler in os.listdir(custom_label_data_handlers_dir) if 'handler' in lbl_handler]
            supported_label_types.extend(custom_supported_label_types)
        else:
            custom_supported_label_types = []
        # Check if the label type is supported
        if self.lbl_type not in supported_label_types: raise NotImplementedError("Label type not supported. Supported file types: " + ', '.join(supported_label_types) + ".")
        # Import the handler for the label type
        if self.lbl_type in custom_supported_label_types:
            h = import_module(f'label.handler_{self.lbl_type}', fromlist=['label_file_extension', 'Handler'])
        else:
            h = import_module('liguard.lbl.handler_'+self.lbl_type, fromlist=['label_file_extension', 'Handler'])
        self.lbl_ext, self.reader = h.label_file_extension, h.Handler
        self.clb_reader = calib_reader
        
        files = glob.glob(os.path.join(self.lbl_dir, '*' + self.lbl_ext))
        if len(files) == 0: raise FileNotFoundError(f'No label files found in {self.lbl_dir}.')
        file_basenames = [os.path.splitext(os.path.basename(file))[0] for file in files]
        # Sort the file basenames based on the numbers in the filenames
        file_basenames.sort(key=lambda file_name: int(''.join(filter(str.isdigit, file_name))))
        self.files_basenames = file_basenames[self.lbl_start_idx:self.lbl_end_idx][self.global_zero:]

        # read the calibration files in async mode
        
        self.data_lock = threading.Lock()
        self.data = []
        self.stop = threading.Event()
        threading.Thread(target=self.__async_read_fn__).start()
        
    def get_abs_path(self, idx: int) -> str:
        """
        Returns the absolute path of the label file at the given index.

        Args:
            idx (int): Index of the label file.

        Returns:
            str: Absolute path of the label file.

        """
        lbl_path = os.path.join(self.lbl_dir, self.files_basenames[idx] + self.lbl_ext)
        return lbl_path
        
    def __async_read_fn__(self):
        """
        Asynchronously reads label files and annotations.

        """
        for idx in range(len(self.files_basenames)):
            if self.stop.is_set(): break
            lbl_abs_path = self.get_abs_path(idx)
            annotation = self.reader(lbl_abs_path, self.clb_reader(idx)[1] if self.clb_reader else None)
            with self.data_lock: self.data.append((lbl_abs_path, annotation))
            time.sleep(self.cfg['threads']['io_sleep'])
        
    def __len__(self) -> int:
        """
        Returns the number of label files.

        Returns:
            int: Number of label files.
        """
        return len(self.files_basenames)
    
    def __getitem__(self, idx) -> tuple:
        """
        Returns the label file path and annotation at the given index.

        Args:
            idx: Index of the label file.

        Returns:
            tuple: Label file path and annotation.
        """
        try:
            with self.data_lock: return self.data[idx]
        except:
            lbl_abs_path = self.get_abs_path(idx)
            annotation = self.reader(lbl_abs_path, self.clb_reader(idx)[1] if self.clb_reader else None)
            return (lbl_abs_path, annotation)
        
    def close(self):
        """
        Closes the label files reading thread.

        """
        self.stop.set()