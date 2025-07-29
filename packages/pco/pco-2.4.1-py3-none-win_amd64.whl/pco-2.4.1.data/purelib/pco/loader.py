import sys
import os.path
import ctypes as C
from ctypes.wintypes import HMODULE
import platform

import logging

logger = logging.getLogger(__name__)
if not logger.hasHandlers():
    logger.addHandler(logging.NullHandler())

class SharedLibrayLoader:
    def __init__(self):
        self.open_count = 0
        self.libraries = dict()
    
    def increment(self):
        if (self.open_count == 0):
            self._load_all()
        self.open_count = self.open_count + 1
    
    def decrement(self):
        self.open_count = self.open_count - 1
        if (self.open_count == 0):
            self._free_all()
    
    def _load_all(self):

        if platform.architecture()[0] != "64bit":
            logger.error("Python Interpreter not x64")
            raise OSError

        lib_path = os.path.dirname(__file__)

        if sys.platform.startswith('win32'):
            if platform.machine().lower().startswith('amd64'):
                archictecture = "win_x64"
            else:
                raise SystemError("pco.python is not supported for 32bit windows platforms architecture")
            self._sdk_name = "sc2_cam.dll"
            self._recorder_name = "pco_recorder.dll"
            self._convert_name = "pco_conv.dll"
            self._xcite_name = "etc_xcite.dll"

        elif sys.platform.startswith('linux'):
            if platform.machine().lower().startswith("x86_64"):
                archictecture = "lnx_amd64"
            elif platform.machine().lower().startswith("aarch64"):
                archictecture = "lnx_arm64"
            else:
                raise SystemError("pco.python is not supported for linux platform " + platform.machine())
            self._sdk_name = "libpco_sc2cam.so.1"
            self._recorder_name = "libpco_recorder.so.3"
            self._convert_name = "libpco_convert.so.1"
            self._xcite_name = "libetc_xcite.so.1"

        else:
            logger.error("Package not supported on platform " + sys.platform)
            raise SystemError
        
        # set working directory
        # workaround, due to implicit load of PCO_File.dll
        current_working_directory = os.getcwd()
        os.chdir(lib_path)

        try:
            if sys.platform.startswith('win32'):
                # find kaya system path for python user installations
                kaya_bin_path = os.getenv('KAYA_VISION_POINT_BIN_PATH')
                if isinstance(kaya_bin_path, str) and os.path.isdir(kaya_bin_path) and os.add_dll_directory(kaya_bin_path):
                    os.add_dll_directory(kaya_bin_path)
                
                self.libraries["sdk"] = C.windll.LoadLibrary(os.path.join(lib_path, archictecture, self._sdk_name))
                self.libraries["sdk"].PCO_InitializeLib()
                self.libraries["recorder"] = C.windll.LoadLibrary(os.path.join(lib_path, archictecture, self._recorder_name))
                self.libraries["convert"] = C.windll.LoadLibrary(os.path.join(lib_path, archictecture, self._convert_name))
                self.libraries["xcite"] = C.windll.LoadLibrary(os.path.join(lib_path, archictecture, self._xcite_name))
            elif sys.platform.startswith('linux'):
                self.libraries["sdk"] = C.cdll.LoadLibrary(os.path.join(lib_path, archictecture, self._sdk_name))
                self.libraries["sdk"].PCO_InitializeLib()
                self.libraries["recorder"] = C.cdll.LoadLibrary(os.path.join(lib_path, archictecture, self._recorder_name))
                self.libraries["convert"] = C.cdll.LoadLibrary(os.path.join(lib_path, archictecture, self._convert_name))
                self.libraries["xcite"] = C.cdll.LoadLibrary(os.path.join(lib_path, archictecture, self._xcite_name))
            else:
                logger.error("Package not supported on platform " + sys.platform)
                raise SystemError
        except OSError:
            logger.error(
                'Error: "'
                + self._sdk_name
                + '" not found in directory "'
                + lib_path
                + '".'
            )
            os.chdir(current_working_directory)
            raise
        
        os.chdir(current_working_directory)       

    def _free_all(self):
        try:
            if sys.platform.startswith('win32'):
                C.windll.kernel32.FreeLibrary.argtypes = [HMODULE]
                C.windll.kernel32.FreeLibrary(self.libraries["xcite"]._handle)
                C.windll.kernel32.FreeLibrary(self.libraries["convert"]._handle)
                C.windll.kernel32.FreeLibrary(self.libraries["recorder"]._handle)
                self.libraries["sdk"].PCO_ResetLib()
                self.libraries["sdk"].PCO_CleanupLib()
                C.windll.kernel32.FreeLibrary(self.libraries["sdk"]._handle)
            else:  # if sys.platform.startswith('linux'):
                try:
                    stdlib = C.CDLL("")
                except OSError:
                    # Alpine Linux.
                    stdlib = C.CDLL("libc.so")
                dll_close = stdlib.dlclose
                dll_close.argtypes = [C.c_void_p]
                dll_close(self.libraries["xcite"]._handle)
                dll_close(self.libraries["convert"]._handle)
                dll_close(self.libraries["recorder"]._handle)
                self.libraries["sdk"].PCO_ResetLib()
                self.libraries["sdk"].PCO_CleanupLib()
                dll_close(self.libraries["sdk"]._handle)

        except Exception as exc:
            logger.error("FreeLibrary: {}".format(exc))


    def libs(self):
        return self.libraries

shared_library_loader = SharedLibrayLoader()