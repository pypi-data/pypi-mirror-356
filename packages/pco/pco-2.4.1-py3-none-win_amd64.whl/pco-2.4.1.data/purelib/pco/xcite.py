# -*- coding: utf-8 -*-
"""
This module wraps the pco.recorder to python data structures.

Copyright @ Excelitas PCO GmbH 2005-2023

The a instance of the Recorder class is part of pco.Camera
"""


import ctypes as C
import sys
import os
from pathlib import Path
import platform
import time
from datetime import datetime
import warnings
import logging
from pco.loader import shared_library_loader
from pco.camera_exception import XCiteException
from pco.sdk import Sdk

logger = logging.getLogger(__name__)
if not logger.hasHandlers():
    logger.addHandler(logging.NullHandler())

class XCite_Ch(C.Structure):
    _pack_ = 1
    _fields_ = [
        ("szLedName", C.c_char * 16),
        ("iWaveLength", C.c_int),
        ("iBelongToWheelNum", C.c_int),
        ("iIntensity", C.c_int),
        ("iIntensityMin", C.c_int),
        ("iIntensityMax", C.c_int),
        ("iIntensityStep", C.c_int),
        ("iExtTriggerNum", C.c_int),
        ("iLedTemp", C.c_int),
        ("dwLEDState", C.c_uint32),
        ("ZZdwdummy", C.c_uint32 * 16),
    ]

class XCiteStruct(C.Structure):
    _pack_ = 1
    _fields_ = [
        ("wSize", C.c_uint16),
        ("szLightSourceName", C.c_char * 30),
        ("hdevice", C.c_void_p),
        ("hcamera", C.c_void_p),
        ("iNumChannels", C.c_int),
        ("iNumWheels", C.c_int),
        ("dwSystemState", C.c_uint32),
        ("dwSerialNumber", C.c_uint32),
        ("dwSystemCaps", C.c_uint32),
        ("iLastChannelOnWheel", C.c_int * 5),
        ("ZZdwdummy", C.c_uint32 * 16),
        ("Channels", XCite_Ch * 16),
    ]

#############################################################################
#                        Wrapper for C-Library functions                    #
#############################################################################

class XCiteWrapper:
    """
    This class provides the basic methods for using etc xcite.
    """
    # -------------------------------------------------------------------------
    class exception(Exception):
        def __str__(self):
            return "Exception: {0} {1:08x}".format(
                self.args[0], self.args[1] & (2**32 - 1)
            )
    # -------------------------------------------------------------------------
    def __init__(self):    
        if platform.architecture()[0] != "64bit":
            logger.error("Python Interpreter not x64")
            raise OSError
    
        self.ETC_XCite = shared_library_loader.libs()["xcite"]

        self.sdk = Sdk()

        self.ETC_XCite.XCITE_ScanDevices.argtypes = [
            C.POINTER(C.c_void_p),
            C.c_uint32,
            C.POINTER(C.c_uint32),
        ]

        self.ETC_XCite.XCITE_GetDeviceInfo.argtypes = [
            C.c_void_p,
            C.POINTER(C.c_int),
            C.POINTER(C.c_char),
            C.c_uint32,
            C.POINTER(C.c_uint32),
        ]

        self.ETC_XCite.XCITE_OpenDevice.argtypes = [
            C.POINTER(C.c_void_p),
            C.c_int,
            C.POINTER(C.c_char),
            C.c_uint32,
        ]

        self.ETC_XCite.XCITE_OpenDeviceEx.argtypes = [
            C.c_void_p,
        ]

        self.ETC_XCite.XCITE_CloseDevice.argtypes = [
            C.c_void_p,
        ]

        # Commands available after open
        self.ETC_XCite.XCITE_ExecuteCommandWithValue.argtypes = [
            C.c_void_p,
            C.POINTER(C.c_char),
            C.POINTER(C.c_char),
            C.c_uint32,
            C.POINTER(C.c_char),
        ]

        self.ETC_XCite.XCITE_ExecuteCommand.argtypes = [
            C.c_void_p,
            C.POINTER(C.c_char),
            C.POINTER(C.c_char),
            C.c_uint32,
        ]

        self.ETC_XCite.XCITE_SetXCStruct.argtypes = [
            C.c_void_p,
            C.POINTER(XCiteStruct),
        ]

        self.ETC_XCite.XCITE_GetXCStruct.argtypes = [
            C.c_void_p,
            C.POINTER(XCiteStruct),
        ]

        self.ETC_XCite.XCITE_SwitchXCite.argtypes = [
            C.c_void_p,
            C.c_bool,
            C.c_bool,
        ]

        self.ETC_XCite.XCITE_GetVersion.argtypes = [
            C.POINTER(C.c_int),
            C.POINTER(C.c_int),
            C.POINTER(C.c_int),
            C.POINTER(C.c_int),
        ]


        # logging setup
        self.ETC_XCite.XCITE_SetLogBits.argtypes = [
            C.c_uint32,
        ]

        self.ETC_XCite.XCITE_GetLogBits.argtypes = [
        ]

        self.ETC_XCite.XCITE_SetLogMode.argtypes = [
            C.c_int,
        ]

        self.ETC_XCite.XCITE_GetLogMode.argtypes = [
        ]

        self.ETC_XCite.XCITE_SetLogFile.argtypes = [
            C.POINTER(C.c_char),
        ]

        self.xcite_types = {
            "XC_120PC": 0,
            "XC_exacte": 1,
            "XC_120LED": 2,
            "XC_110LED": 3,
            "XC_mini": 4,
            "XC_XYLIS": 5,
            "XC_XR210": 6,
            "XC_XLED1": 7,
            "XC_XT600": 8,
            "XC_XT900": 9,
            "Any": 0xFFFF
        }

    # ---------------------------------------------------------------------
    
    def scan_devices(self):
        """Identify number of connected xcite devices

        Raises:
            XCiteException: On error of the sdk function call

        Returns:
            dict: Dictionary containing the device count and handles to available devices
        """
        # Now get devices
        max_devices = C.c_uint32(16)
        xcite_handles = (C.c_void_p * 16)()
        xcite_handles_ptr = C.cast(xcite_handles, C.POINTER(C.c_void_p))
        num_devices = C.c_uint32(0)

        time_start = time.perf_counter()
        error = self.ETC_XCite.XCITE_ScanDevices(xcite_handles_ptr, max_devices, num_devices)
        duration = time.perf_counter() - time_start
        error_msg = self.get_error_text(error)

        ret = {}
        if error == 0:
            handles = []
            for i in range(0, num_devices.value):
                handles.append(xcite_handles[i])
            ret.update({"device count": num_devices.value})
            ret.update({"handle list": handles})

        logger.info("[{:5.3f} s] [xcite] {}: {}".format(duration, sys._getframe().f_code.co_name, error_msg))
        if error:
            raise XCiteException(sdk=self.sdk, code=error)

        return ret


    def get_device_info(self, handle):
        """Get info of a xcite device referenced by the transferred handle


        Args:
            handle (int): Handle of the device to query info from (doesn't need to be opened before)

        Raises:
            XCiteException: On error of the sdk function call

        Returns:
            dict: Dictionary with the device info
        """

        h = handle  
        xcite_type = C.c_int(0)
        port_len = C.c_uint32(500)
        port = (C.c_char * port_len.value)()
        port_ptr = C.cast(port, C.POINTER(C.c_char))
        open_count = C.c_uint32(0)

        time_start = time.perf_counter()
        error = self.ETC_XCite.XCITE_GetDeviceInfo(h, xcite_type, port_ptr, port_len, open_count)
        duration = time.perf_counter() - time_start
        error_msg = self.get_error_text(error)

        ret = {}
        if error == 0:
            temp_list = []
            for i in range(port_len.value):
                if port[i] == b'\x00':
                    break
                if port[i] != b'\xfe':
                    temp_list.append(port[i])
            output_string = bytes.join(b"", temp_list).decode("ascii")

            type_name = list(self.xcite_types.keys())[list(self.xcite_types.values()).index(xcite_type.value)]
            ret.update({"type": type_name})
            ret.update({"port": output_string})
            ret.update({"open count": open_count.value})

        logger.info("[{:5.3f} s] [xcite] {}: {}".format(duration, sys._getframe().f_code.co_name, error_msg))
        if error:
            raise XCiteException(sdk=self.sdk, code=error)

        return ret


    def open_device(self, port="", xcite_type="Any", speed=9600):
        """Open a xcite device at a given port, according to the specified device and speed

        Args:
            port (str): Port of the device to open
            xcite_type (str, optional): Required xcite type. Defaults to "Any".
            speed (int, optional): COM port speed. Defaults to 9600.

        Returns:
            dict: Dictionary containing error code information
        """

        xcite_type_c = C.c_int32(self.xcite_types[xcite_type])
        port_cstr = C.c_char_p(port.encode("utf-8"))
        speed_c = C.c_uint32(speed)
        xcite_handle = C.c_void_p(0)
        time_start = time.perf_counter()
        error = self.ETC_XCite.XCITE_OpenDevice(xcite_handle, xcite_type_c, port_cstr, speed_c)
        duration = time.perf_counter() - time_start
        error_msg = self.get_error_text(error)

        logger.info("[{:5.3f} s] [xcite] {}: {}".format(duration, sys._getframe().f_code.co_name, error_msg))

        return {
            "handle": xcite_handle,
            "error": error}


    def open_device_ex(self, handle):
        """Open the specified device

        Args:
            handle (HANDLE): Handle of the device to open (typically comes from a previous scan_devices call)

        Returns:
            dict: Dictionary containing error code information
        """
        h = C.c_void_p(handle)

        time_start = time.perf_counter()
        error = self.ETC_XCite.XCITE_OpenDeviceEx(h)
        duration = time.perf_counter() - time_start
        error_msg = self.get_error_text(error)

        logger.info("[{:5.3f} s] [xcite] {}: {}".format(duration, sys._getframe().f_code.co_name, error_msg))

        return {
            "handle": h,
            "error": error}
    
    def close_device(self, xcite_handle):
        """Close the currently opened device
        """

        time_start = time.perf_counter()
        self.ETC_XCite.XCITE_CloseDevice(xcite_handle)
        duration = time.perf_counter() - time_start

        xcite_handle = C.c_void_p(0)

        logger.info("[{:5.3f} s] [xcite] {}".format(duration, sys._getframe().f_code.co_name))

    
    def execute_command(self, xcite_handle, cmd, in_value=""):
        """
        send command with optional response
        """
        
        sz_cmd = C.c_char_p(cmd.encode("utf-8"))
        answer = (C.c_char * 1024)()
        buflen = C.c_uint32(1024)
        time_start = time.perf_counter()
        if in_value == "":
            error = self.ETC_XCite.XCITE_ExecuteCommand(xcite_handle, sz_cmd, answer, buflen)
        else:
            sz_invalue = C.c_char_p(in_value.encode("utf-8"))
            error = self.ETC_XCite.XCITE_ExecuteCommandWithValue(xcite_handle, sz_cmd, answer, buflen, sz_invalue)
        duration = time.perf_counter() - time_start
        error_msg = self.get_error_text(error)

        temp_list = []
        for i in range(1024):
            if answer[i] == b'\x00':
                break
            if answer[i] != b'\xfe':
                temp_list.append(answer[i])
        output_string = bytes.join(b"", temp_list).decode("ascii")

        logger.info("[{:5.3f} s] [xcite] {}: {}".format(duration, sys._getframe().f_code.co_name, error_msg))

        if error:
            raise XCiteException(sdk=self.sdk, code=error)
        
        return {"answer" : output_string}
    
    def get_xc_struct(self, xcite_handle):
        """
        Gets XCite data, and returns struct values as a dict

        :rtype: dict
        """
        strXCite = XCiteStruct()
        strXCite.wSize = C.sizeof(XCiteStruct)

        time_start = time.perf_counter()
        error = self.ETC_XCite.XCITE_GetXCStruct(
            xcite_handle, strXCite
        )
        duration = time.perf_counter() - time_start

        if error:
            raise XCiteException(sdk=self.sdk, code=error)

        temp_list = []
        for i in range(30):
            if strXCite.szLightSourceName[i] != b'\x00':
                break
            if strXCite.szLightSourceName[i] != b'\xfe':
                temp_list.append(strXCite.szLightSourceName[i])
        output_string = bytes.join(b"", temp_list).decode("ascii")

        ret = {}
        ret.update({"light source name" : output_string})
        ret.update({"device handle" : strXCite.hdevice})
        ret.update({"camera handle" : strXCite.hcamera})
        ret.update({"number of channels" : strXCite.iNumChannels})
        ret.update({"number of wheels" : strXCite.iNumWheels})
        ret.update({"system state" : strXCite.dwSystemState})
        ret.update({"serial number" : strXCite.dwSerialNumber})
        ret.update({"dwSystemCaps" : strXCite.dwSystemCaps})

        lcw_tuple = (
            strXCite.iLastChannelOnWheel[0],
            strXCite.iLastChannelOnWheel[1],
            strXCite.iLastChannelOnWheel[2],
            strXCite.iLastChannelOnWheel[3],
            strXCite.iLastChannelOnWheel[4],
        )

        ret.update({"last channel on wheel" : list(lcw_tuple)})
        
        channel_list = []
        for i in range(strXCite.iNumChannels):
            channel = {}
            temp_list = []
            for j in range(16):
                if len(strXCite.Channels[i].szLedName) == 0:
                    break
                if strXCite.Channels[i].szLedName[j] != b'\x00':
                    break
                if strXCite.Channels[i].szLedName[j] != b'\xfe':
                    temp_list.append(strXCite.Channels[i].szLedName[j])
            output_string = bytes.join(b"", temp_list).decode("ascii")

            channel.update({"index": i})
            channel.update({"led name": output_string})   
            channel.update({"wavelength": strXCite.Channels[i].iWaveLength})   
            channel.update({"belong to wheel": strXCite.Channels[i].iBelongToWheelNum})   
            channel.update({"intensity": strXCite.Channels[i].iIntensity})   
            channel.update({"intensity min": strXCite.Channels[i].iIntensityMin})   
            channel.update({"intensity max": strXCite.Channels[i].iIntensityMax})   
            channel.update({"intensity step": strXCite.Channels[i].iIntensityStep})   
            channel.update({"external trigger num": strXCite.Channels[i].iExtTriggerNum})   
            channel.update({"led temperature": strXCite.Channels[i].iLedTemp})   
            channel.update({"led state": bool(strXCite.Channels[i].dwLEDState & 0x1)})   
            channel_list.append(channel)

        ret.update({"channels" : channel_list})

        logger.info("[{:5.3f} s] [xcite] {}".format(duration, sys._getframe().f_code.co_name))

        return ret

    def set_xc_struct(self, xcite_handle, setup_dict):
        """
        Sets XCite data, and returns struct values as a dict
        """
        strXCite = XCiteStruct()
        strXCite.wSize = C.sizeof(XCiteStruct)

        if "camera handle" in setup_dict:
            strXCite.hcamera = setup_dict["camera handle"]
        if "channels"  in setup_dict:
            strXCite.iNumChannels = C.c_int(len(setup_dict["channels"]))
            for i in range(len(setup_dict["channels"])):
                strXCite.Channels[i] = XCite_Ch()
                strXCite.Channels[i].iIntensity = C.c_int(setup_dict["channels"][i]["intensity"])
                strXCite.Channels[i].dwLEDState = C.c_uint32(int(setup_dict["channels"][i]["led state"]))

        time_start = time.perf_counter()
        error = self.ETC_XCite.XCITE_SetXCStruct(
            xcite_handle, strXCite
        )
        duration = time.perf_counter() - time_start
        error_msg = self.get_error_text(error)

        logger.info("[{:5.3f} s] [xcite] {}: {}".format(duration, sys._getframe().f_code.co_name, error_msg))

        if error:
            raise XCiteException(sdk=self.sdk, code=error)
        
    def switch_xcite(self, xcite_handle, use_common_onoff, on):
        """configuration for common switch"""

        c_common = C.c_bool(use_common_onoff)
        c_on = C.c_bool(on)
        
        time_start = time.perf_counter()
        error = self.ETC_XCite.XCITE_SwitchXCite(xcite_handle, c_common, c_on)
        duration = time.perf_counter() - time_start
        error_msg = self.get_error_text(error)

        logger.info("[{:5.3f} s] [xcite] {}: {}".format(duration, sys._getframe().f_code.co_name, error_msg))
        if error:
            raise XCiteException(sdk=self.sdk, code=error)

    def get_version(self):
        """
        Returns the version info about the sdk dll
        """

        iMajor = C.c_int()
        iMinor = C.c_int()
        iPatch = C.c_int()
        iBuild = C.c_int()

        time_start = time.perf_counter()
        error = self.ETC_XCite.XCITE_GetVersion(iMajor, iMinor, iPatch, iBuild)
        duration = time.perf_counter() - time_start
        error_msg = self.get_error_text(error)

        ret = {}

        if error == 0:
            ret.update(
                {
                    "name": "XCite",
                    "major": iMajor.value,
                    "minor": iMinor.value,
                    "patch": iPatch.value,
                    "build": iBuild.value,
                }
            )

        logger.info("[{:5.3f} s] [xcite] {}: {}".format(duration, sys._getframe().f_code.co_name, error_msg))
        if error:
            raise XCiteException(sdk=self.sdk, code=error)

        return ret

    def get_error_text(self, error):
        return self.sdk.get_error_text(error)


    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass

    def set_log_bits(self, level_list):
        level_map = {
            "ERROR_M" : 0x0001,
            "INIT_M" : 0x0002,
            "BUFFER_M" : 0x0004,
            "PROCESS_M" : 0x0008,
            "WARNING_M" : 0x0010,
            "INFO_M" : 0x0020,
            "COMMAND_M" : 0x0040,
            "PCI_M" : 0x0080,
            "HANDLE_M" : 0x0800,
            "TIME_M" : 0x1000,
            "TIME_MD" : 0x2000,
            "THREAD_ID" : 0x4000,
        }

        bits = 0
        for level in level_list:
            bits = bits | level_map[level]
        
        c_bits = C.c_uint32(bits)
        time_start = time.perf_counter()
        self.ETC_XCite.XCITE_SetLogBits(c_bits)
        duration = time.perf_counter() - time_start
    
    def get_log_bits(self):
        level_map = {
            "ERROR_M" : 0x0001,
            "INIT_M" : 0x0002,
            "BUFFER_M" : 0x0004,
            "PROCESS_M" : 0x0008,
            "WARNING_M" : 0x0010,
            "INFO_M" : 0x0020,
            "COMMAND_M" : 0x0040,
            "PCI_M" : 0x0080,
            "HANDLE_M" : 0x0800,
            "TIME_M" : 0x1000,
            "TIME_MD" : 0x2000,
            "THREAD_ID" : 0x4000,
        }

        c_bits = C.c_uint32(0)
        time_start = time.perf_counter()
        self.ETC_XCite.XCITE_GetLogBits(c_bits)
        duration = time.perf_counter() - time_start

        ret = []
        for bit in list(level_map.values()):
            if c_bits & bit:
                ret.append(list(level_map.keys())[list(level_map.values()).index(bit)])
        return ret
    
    def set_log_mode(self, mode):
        mode_map = {
            "LOGMETHOD_STDOUT" : 0,
            "LOGMETHOD_FILE" : 1,
            "LOGMETHOD_CALLBACK" : 2,
            "LOGMETHOD_NULL" : 4,
        }

        c_mode = C.c_int(mode_map[mode])
        self.ETC_XCite.XCITE_SetLogMode(c_mode)
    
    def get_log_mode(self):
        mode_map = {
            "LOGMETHOD_STDOUT" : 0,
            "LOGMETHOD_FILE" : 1,
            "LOGMETHOD_CALLBACK" : 2,
            "LOGMETHOD_NULL" : 4,
        }

        c_mode = C.c_int(0)
        self.ETC_XCite.XCITE_GetLogMode(c_mode)

        return list(mode_map.keys())[list(mode_map.values()).index(c_mode)]
    
    def set_log_file(self, name):

        name_cstr = C.c_char_p(name.encode("utf-8"))
        self.ETC_XCite.XCITE_SetLogFile(name_cstr)


#############################################################################
#                        High level class implementation                    #
#############################################################################

class XCite:


    def __init__(self, xcite_type="Any", port=""):
        
        logger.info("[-.--- s] [xcite] {}".format(sys._getframe().f_code.co_name))
        shared_library_loader.increment()

        self._opened = True

        self.xc = XCiteWrapper()
        self.xcite_handle = C.c_void_p(0)

        self._setup_logging()

        ret = self.xc.open_device(port=port, xcite_type=xcite_type)

        if ret["error"] != 0:
            raise XCiteException(sdk=self.xc.sdk, code=ret["error"])

        self.xcite_handle = ret["handle"]
        if not self.xcite_handle.value:
            raise XCiteException(sdk=self.xc.sdk, code=0xA0163013) # PCO_ERROR_HIGHLEVELSDK | PCO_ERROR_SDKDLL | PCO_ERROR_NOTAVAILABLE
    # -------------------------------------------------------------------------
    def __enter__(self):
        logger.info("[---.- s] [xcite] {}".format(sys._getframe().f_code.co_name))
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        info = self.xc.get_device_info(self.xcite_handle)
        if info["open count"] > 0:
            if info["open count"] == 1:
                self.switchOff()
            self.close()
            
    def close(self):
        if self.xcite_handle.value:
            self.xc.close_device(self.xcite_handle)
        
        shared_library_loader.decrement()


    def xcite(self):
        return self.xcite_handle

    @property
    def description(self):
        logger.info("[-.--- s] [xcite] {}".format(sys._getframe().f_code.co_name))
        
        setup = self.xc.get_xc_struct(self.xcite_handle)
        info = self.xc.get_device_info(self.xcite_handle)
        desc = {}

        desc.update({"serial": setup["serial number"]})
        desc.update({"name": info["type"]})
        desc.update({"com port": info["port"]})

        wavelength_exclusivity = {}
        for ch in setup["channels"]:
            wavelength_exclusivity.update({ch["wavelength"] : ch["belong to wheel"]})
        
        desc.update({"wavelength exclusivity": wavelength_exclusivity})

        wavelength_intensity_limits = {}
        for ch in setup["channels"]:
            wavelength_intensity_limits.update({ch["wavelength"] : (ch["intensity min"], ch["intensity max"])})
        
        desc.update({"wavelength intensity limits": wavelength_intensity_limits})

        return desc
    
    @property
    def configuration(self):
        logger.info("[-.--- s] [xcite] {}".format(sys._getframe().f_code.co_name))

        setup = self.xc.get_xc_struct(self.xcite_handle)
        
        conf = {}


        # conf.update({"wavelength config" : []})
        for ch in setup["channels"]:
            conf.update({ch["wavelength"] : {
                "intensity" : ch["intensity"],
                "led state" : ch["led state"]
            }})

            # conf["wavelength config"].append([ch["wavelength"], ch["intensity"], ch["led state"]])

        return conf

    @configuration.setter
    def configuration(self, arg):
        logger.info("[-.--- s] [cam] {}".format(sys._getframe().f_code.co_name))

        if type(arg) is not dict:
            logger.error("Argument is not a dictionary")
            raise TypeError
        
        wave_keys = [
            "intensity",
            "led state"
        ]
        setup = self.xc.get_xc_struct(self.xcite_handle)
        current_conf = self.configuration
        for wavelength, conf_dict in arg.items():
            if wavelength not in current_conf.keys():
                raise KeyError(f'{"<"}{conf_dict}{"> is not a vaild wavelength for this XCite device"}')
            
            index = None
            for i in range(len(setup["channels"])):
                if setup["channels"][i]["wavelength"] == wavelength:
                    index = i
                    break
            for wave_key, value in conf_dict.items():
                if wave_key not in wave_keys:
                    raise KeyError(f'{"<["}{conf_dict}{"]["}{wave_key}{"]> is not a vaild key for wavelength configuration"}')
                setup["channels"][index][wave_key] = value
        
        self.xc.set_xc_struct(self.xcite_handle, setup)

    def default_configuration(self):
        self.xc.switch_xcite(self.xcite_handle, True, False)
        conf = self.configuration
        for wavelength, conf_dict in conf.items():
            conf[wavelength]["led state"] = False
        self.configuration = conf

    def switchOff(self):
        self.xc.switch_xcite(self.xcite_handle, True, False)

    def switchOn(self):
        self.xc.switch_xcite(self.xcite_handle, True, True)

    
######################### private functions #########################


    def _setup_logging(self):
        self.xc.set_log_bits(["ERROR_M", "INIT_M", "BUFFER_M", "PROCESS_M", "WARNING_M", "INFO_M", "COMMAND_M", "TIME_M", "TIME_MD"])

        pco_log_path = ""
        if sys.platform.startswith('win32'):
            pco_log_path = "C:\\ProgramData\\pco"
        elif sys.platform.startswith('linux'):
            pco_log_path = os.path.expanduser("~/.pco/pco_logging")
        else:
            logger.error("Python Interpreter not x64")
            raise OSError("Platform not supported")
        
        Path(pco_log_path).mkdir(parents=True, exist_ok=True)
        file_name = os.path.join(pco_log_path, "etc_xcite.log")
        with open(file_name, "a") as f:
            f.write("==================== pco.xcite logging started from high-level SDK pco.python ===============\n")

        self.xc.set_log_mode("LOGMETHOD_FILE")
        self.xc.set_log_file(file_name)


