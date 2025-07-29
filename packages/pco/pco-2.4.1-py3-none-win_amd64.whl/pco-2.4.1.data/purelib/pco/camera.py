# -*- coding: utf-8 -*-
"""
This module main entry point for working with pco cameras.

Copyright @ Excelitas PCO GmbH 2005-2023

The class Camera is intended to be used the following way:

with pco.Camera() as cam:
    cam.record()
    image, meta = cam.image()
"""

import sys
import time
import copy
import numpy as np
import logging
import warnings
import os.path
import ctypes as C
from ctypes.wintypes import HMODULE
import platform

from pco.loader import shared_library_loader
from pco.sdk import Sdk
from pco.recorder import Recorder
from pco.convert import Convert
from pco.camera_exception import CameraException


logger = logging.getLogger(__name__)
if not logger.hasHandlers():
    logger.addHandler(logging.NullHandler())


class exception(Exception):
    def __str__(self):
        return ("pco.exception Exception:", self.args)
    
class Camera:

    # -------------------------------------------------------------------------
    def __init__(self, name="", interface=None, serial=None):
        '''Opening by serial takes longer without interface parameter'''

        logger.info("[-.--- s] [cam] {}".format(sys._getframe().f_code.co_name))
        shared_library_loader.increment()
        self._opened = True

        try:
            self.flim_config = None

            self.sdk = Sdk()

            self._image_number = 0
            self._interface = None

            self._auto_exposure = {"region": "balanced", "min exposure": 0.001, "max exposure": 0.1}
            self._auto_exp_state = False

            self._raw_format_mode = "Word"

            # self.sdk.open_camera()

            def _scanner_sn(sdk, interfaces, sn):
                if sys.platform.startswith('linux'):
                    if_type = None # 0 = all interfaces
                    if len(interfaces) == 1:  # if if was selected
                        if_type = interfaces[0]
                    ret = sdk.scan_cameras(if_type)
                    devices = ret["devices"]
                    for device in devices:
                        if device["serial number"] == sn:
                            ret = sdk.open_camera_device(device["id"])
                            if ret["error"] != 0:
                                raise CameraException(sdk=self.sdk, code=ret["error"])
                            return device["interface type"]
                else:
                    for interface in interfaces:
                        ret = sdk.open_camera_sn(interface=interface, serialnumber=sn)
                        if ret["error"] == 0:
                            return interface
                    
                raise CameraException(sdk=self.sdk, code=0xA0163013) # PCO_ERROR_HIGHLEVELSDK | PCO_ERROR_SDKDLL | PCO_ERROR_NOTAVAILABLE


            def _scanner(sdk, interfaces):
                if sys.platform.startswith('linux'):
                    ret = sdk.scan_cameras()
                    avail_devices = ret["devices"]
                    for device in avail_devices:
                        if_type = device["interface type"]
                        if if_type in interfaces:
                            ret = sdk.open_camera_device(id=device["id"])
                            if ret["error"] == 0:
                                return if_type
                            else:
                                break

                else:
                    for interface in interfaces:
                        for camera_number in range(64):
                            ret = sdk.open_camera_ex(interface=interface, camera_number=camera_number)
                            if ret["error"] == 0:
                                return interface
                            elif ret["error"] & 0x80002001 == 0x80002001:
                                continue
                            else:
                                break
                raise ValueError

            try:
                if interface is not None:
                    if isinstance(interface, list) and all(isinstance(s, str) for s in interface):
                        interfaces = interface
                    elif isinstance(interface, str):
                        interfaces = [interface]
                    else:
                        raise ValueError("Argument <interface> must be 'str' or 'list of str'")
                else:
                    interfaces = [
                        "FireWire",
                        "Camera Link MTX",
                        "GenICam",
                        "Camera Link NAT",
                        "GigE",
                        "USB 2.0",
                        "Camera Link ME4",
                        "USB 3.0",
                        "CLHS"]
                if serial is None:
                    self._interface = _scanner(self.sdk, interfaces)
                else:
                    self._interface = _scanner_sn(self.sdk, interfaces, serial)
            except CameraException:
                raise
            except ValueError as exc:
                error_msg = "No camera found. Please check the connection and close other processes which use the camera."
                logger.error("[---.- s] [cam] {}: {}".format(sys._getframe().f_code.co_name, error_msg))
                raise CameraException(sdk=self.sdk, message=error_msg, code=0x80162001)

            self.rec = Recorder(
                self.sdk,
                self.sdk.get_camera_handle()
            )

            self._camera_type = self.sdk.get_camera_type()
            if (serial):
                self._serial = serial
            else:
                self._serial = self._camera_type["serial number"]
            if (name):
                self._camera_name = name
            else:
                self._camera_name = self.sdk.get_camera_name()["camera name"]
            self._camera_description = self.sdk.get_camera_description()
            self.colorflag = self._camera_description["wSensorTypeDESC"] & 0x0001


            if self.colorflag:
                self.conv = {
                    "Mono8": Convert(self.sdk.get_camera_handle(), self.sdk, "bw", self._camera_description["bit resolution"]),
                    "BGR8": Convert(self.sdk.get_camera_handle(), self.sdk, "color", self._camera_description["bit resolution"]),
                    "BGR16": Convert(self.sdk.get_camera_handle(), self.sdk, "color16", self._camera_description["bit resolution"]),
                }
            else:
                self.conv = {
                    "Mono8": Convert(self.sdk.get_camera_handle(), self.sdk, "bw", self._camera_description["bit resolution"]),
                    "BGR8": Convert(self.sdk.get_camera_handle(), self.sdk, "pseudo", self._camera_description["bit resolution"]),
                }

            # get required infos for convert creation
            sensor_info = self._get_sensor_info()
            for key in self.conv:
                self.conv[key].create(sensor_info["data_bits"], sensor_info["dark_offset"],
                                      sensor_info["ccm"], sensor_info["sensor_info_bits"])
            
            self.default_configuration()

        except Exception:
            self.close() # delete constructed modules and decrement shared library loader
            raise


    # -------------------------------------------------------------------------

    def default_configuration(self):
        """
        Sets default configuration for the camera.

        :rtype: None

        >>> default_configuration()

        """

        logger.info("[-.--- s] [cam] {}".format(sys._getframe().f_code.co_name))

        if self.has_ram:
            self.switch_to_camram()

        if self.sdk.get_recording_state()["recording state"] == "on":
            self.sdk.set_recording_state("off")

        self.sdk.reset_settings_to_default()

        self.sdk.set_bit_alignment("LSB")

        if self._camera_description["dwGeneralCapsDESC1"] & 0x00004000:
            self.sdk.set_metadata_mode("on")

        self._arm_camera()

    # -------------------------------------------------------------------------
    def __str__(self):
        return "{}, serial: {}".format(self._camera_name, self._serial)

    # -------------------------------------------------------------------------
    def __repr__(self):
        return "pco.Camera"

    # -------------------------------------------------------------------------
    def __bool__(self):
        logger.debug("{}".format(self._opened))
        return self._opened

    # -------------------------------------------------------------------------
    @property
    def camera_name(self):
        logger.debug("{}".format(self._camera_name))
        return self._camera_name

    # -------------------------------------------------------------------------
    @property
    def raw_format(self):
        """
        identify current bit resolution setup of camera
        
        :rtype: str  <'Word' | 'Byte'>
        """
        raw_format = self._raw_format_mode
        if not self.rec.recorder_handle:
            if self._camera_description["dwGeneralCapsDESC3"] & 0x00020000:  # GENERALCAPS3_CAMERA_SETUP_PIXELFORMAT
                if self.sdk.get_camera_setup("pixel format")["setup"] == "8":
                    raw_format = "Byte"
                else:
                    raw_format = "Word"
            else:
                if self._camera_description["bit resolution"] > 8:
                    raw_format = "Word"
                else:
                    raw_format = "Byte"
        logger.debug("{}".format(raw_format))
        return raw_format

    # -------------------------------------------------------------------------
    @property
    def camera_serial(self):
        logger.debug("{}".format(self._serial))
        return self._serial
    
     # -------------------------------------------------------------------------
    @property
    def interface(self):
        logger.debug("{}".format(self._interface))
        return self._interface

    # -------------------------------------------------------------------------
    @property
    def is_recording(self):
        try:
            status = self.rec.get_status()["bIsRunning"]
        except ValueError:
            status = False
        logger.debug("{}".format(status))
        return bool(status)

    # -------------------------------------------------------------------------
    @property
    def is_color(self):
        return bool(self.colorflag)

    @property
    def recorded_image_count(self):
        try:
            recorded_images = self.rec.get_status()["dwProcImgCount"]
        except ValueError:
            recorded_images = 0
        logger.debug("{}".format(recorded_images))
        return recorded_images

    # -------------------------------------------------------------------------
    @property
    def configuration(self):
        logger.info("[-.--- s] [cam] {}".format(sys._getframe().f_code.co_name))

        conf = {}

        exp = self.sdk.get_delay_exposure_time()
        timebase = {"ms": 1e-3, "us": 1e-6, "ns": 1e-9}
        exp_time = exp["exposure"] * timebase[exp["exposure timebase"]]
        delay_time = exp["delay"] * timebase[exp["delay timebase"]]
        conf.update({"exposure time": exp_time})
        conf.update({"delay time": delay_time})

        roi = self.sdk.get_roi()
        x0, y0, x1, y1 = roi["x0"], roi["y0"], roi["x1"], roi["y1"]
        conf.update({"roi": (x0, y0, x1, y1)})

        conf.update({"timestamp": self.sdk.get_timestamp_mode()["timestamp mode"]})
        conf.update({"pixel rate": self.sdk.get_pixel_rate()["pixel rate"]})
        conf.update({"trigger": self.sdk.get_trigger_mode()["trigger mode"]})
        conf.update({"acquire": self.sdk.get_acquire_mode()["acquire mode"]})
        if self._camera_description["dwGeneralCapsDESC1"] & 0x00000001:  # GENERALCAPS1_NOISE_FILTER
            conf.update({"noise filter": self.sdk.get_noise_filter_mode()["noise filter mode"]})
        try:
            mdm = self.sdk.get_metadata_mode()["metadata mode"]
        except ValueError:
            mdm = "off"
        conf.update({"metadata": mdm})

        binning = self.sdk.get_binning()
        conf.update({"binning": (binning["binning x"], binning["binning y"], binning["binning mode"])})
        
        # Auto exposure tuple
        conf.update({"auto exposure": (self._auto_exposure["region"], self._auto_exposure["min exposure"], self._auto_exposure["max exposure"])})
        
        if self._camera_description["dwGeneralCapsDESC3"] & 0x00020000:  # GENERALCAPS3_CAMERA_SETUP_PIXELFORMAT
            conf.update({"pixel format": self.sdk.get_camera_setup("pixel format")["setup"]})
        else:
            conf.update({"pixel format": self._dynres_to_pixelformat(self._camera_description["bit resolution"])})

        return conf

    # -------------------------------------------------------------------------
    @configuration.setter
    def configuration(self, arg):
        """
        Configures the camera with the given values from a dictionary.

        :param arg: Arguments to configure the camera.
        :type arg: dict

        :rtype: None

        >>> configuration = {'exposure time': 10e-3,
                             'roi': (1, 1, 512, 512),
                             'timestamp': 'ascii'}

        """

        logger.info("[-.--- s] [cam] {}".format(sys._getframe().f_code.co_name))

        if type(arg) is not dict:
            logger.error("Argument is not a dictionary")
            raise TypeError

        config_keys = [
            'exposure time',
            'delay time',
            'roi',
            'timestamp',
            'pixel rate',
            'trigger',
            'acquire',
            'noise filter',
            'metadata',
            'binning',
            'auto exposure',
            'pixel format'
        ]

        for k in arg.keys():
            if not k in config_keys:
                raise KeyError(f'{"<"}{k}{"> is not a valid key for pco.Camera.configuration."}')

        if self.sdk.get_recording_state()["recording state"] == "on":
            raise ValueError  # self.sdk.set_recording_state("off")

        if "exposure time" in arg:
            self.exposure_time = arg["exposure time"]

        if "delay time" in arg:
            self.delay_time = arg["delay time"]

        if "noise filter" in arg:
            if self._camera_description["dwGeneralCapsDESC1"] & 0x00000001:  # GENERALCAPS1_NOISE_FILTER
                self.sdk.set_noise_filter_mode(arg["noise filter"])

        if "roi" in arg:
            if any(x < 1 for x in arg["roi"]):
                raise ValueError(f'{"Value of roi: "}{arg["roi"]}{" is zero or negative. Minimum for x0, y0 is 1"}')

            # if (arg["roi"][2] - arg["roi"][0]) < self.description['min width']:
            #   raise ValueError(f'{"roi: "}{arg["roi"]}{" is below min width limit"}')

            # if (arg["roi"][3] - arg["roi"][1]) < self.description['min height']:
            #   raise ValueError(f'{"roi: "}{arg["roi"]}{" is below min height limit"}')

            # if arg["roi"][2] > self.description['max width']:
            #   raise ValueError(f'{"roi: "}{arg["roi"]}{" is above max width limit"}')

            # if arg["roi"][3] > self.description['max height']:
            #   raise ValueError(f'{"roi: "}{arg["roi"]}{" is above max height limit"}')

            self.sdk.set_roi(*arg["roi"])

        if "timestamp" in arg:
            if self._camera_description["dwGeneralCapsDESC1"] & 0x00000100:  # GENERALCAPS1_NO_TIMESTAMP
                if arg["timestamp"] != 'off':
                    raise ValueError("Camera does not support configured timestamp mode")
            else:
                if arg["timestamp"] == 'ascii':
                    # GENERALCAPS1_TIMESTAMP_ASCII_ONLY
                    if not (self._camera_description["dwGeneralCapsDESC1"] & 0x00000008):
                        raise ValueError("Camera does not support ascii-only timestamp mode")
                self.sdk.set_timestamp_mode(arg["timestamp"])

        if "pixel rate" in arg:
            self.sdk.set_pixel_rate(arg["pixel rate"])

        if "trigger" in arg:
            self.sdk.set_trigger_mode(arg["trigger"])

        if "acquire" in arg:
            self.sdk.set_acquire_mode(arg["acquire"])

        if "metadata" in arg:
            if self._camera_description["dwGeneralCapsDESC1"] & 0x00004000:
                self.sdk.set_metadata_mode(arg["metadata"])

        if "binning" in arg:
            if "roi" not in arg:
                logger.warning(
                    'ROI must be adjusted if binning is used. Please set a valid ROI by the "roi" parameter.'
                )
            self.sdk.set_binning(*arg["binning"])

        # Tuple format for 'auto exposure': (region, min, max)
        # Tuple types for 'auto exposure': (str, double, double)
        if "auto exposure" in arg:
            self._auto_exposure = {"region": arg["auto exposure"][0], "min exposure": arg["auto exposure"][1], "max exposure": arg["auto exposure"][2]}
            self._update_auto_exposure()

        if "pixel format" in arg:
            if self._camera_description["dwGeneralCapsDESC3"] & 0x00020000:  # GENERALCAPS3_CAMERA_SETUP_PIXELFORMAT
                self.sdk.set_camera_setup("pixel format", arg["pixel format"])
            else:
                if self._dynres_to_pixelformat(self._camera_description["bit resolution"]) != arg["pixel format"]:
                    raise ValueError("Camera does not support specified pixelformat")
                

        self._arm_camera()

    # -------------------------------------------------------------------------
    @property
    def has_ram(self):
        if self._camera_description["dwGeneralCapsDESC1"] & 0x00001000:  # GENERALCAPS1_NO_RECORDER
            return False
        return True

    # -------------------------------------------------------------------------
    @property
    def camram_segment(self):
        if not self.has_ram:
            raise ValueError("Camera does not support CamRam!")
        
        return self.sdk.get_active_ram_segment()


    # -------------------------------------------------------------------------
    @property
    def camram_max_images(self):
        if not self.has_ram:
            raise ValueError("Camera does not support CamRam!")
        
        if not self.rec.recorder_handle.value:
            return self.sdk.get_number_of_images_in_segment(self._segment)["max image count"]
        
        if self.rec.get_settings()["recorder mode"] == 0x3: # camram mode
            return self._recorder_buffer_size
        
        return self.sdk.get_number_of_images_in_segment(self._segment)["max image count"]
        
    # -------------------------------------------------------------------------
    @property
    def camram_num_images(self):
        if not self.has_ram:
            raise ValueError("Camera does not support CamRam!")

        if not self.rec.recorder_handle.value:
            return 0
        
        if self.rec.get_settings()["recorder mode"] == 0x3: # camram mode
            return self.sdk.get_number_of_images_in_segment(self._segment)["images in segment"]
        
        return self.rec.get_status()["dwProcImgCount"]

    # -------------------------------------------------------------------------
    @property
    def lightsheet_configuration(self):
        logger.info("[-.--- s] [cam] {}".format(sys._getframe().f_code.co_name))

        conf = {}

        conf.update({"scmos readout": self.sdk.get_interface_output_format("edge")["format"]})
        line_time = self.sdk.get_cmos_line_timing()
        conf.update({"line timing parameter": line_time["parameter"]})
        conf.update({"line time": line_time["line time"]})

        lines_exp_delay = self.sdk.get_cmos_line_exposure_delay()
        conf.update({"lines exposure": lines_exp_delay["lines exposure"]})
        conf.update({"lines delay": lines_exp_delay["lines delay"]})

        return conf

    # -------------------------------------------------------------------------
    @lightsheet_configuration.setter
    def lightsheet_configuration(self, arg):
        """
        Configures the camera with the given values from a dictionary.

        :param arg: Arguments to configure the camera for lightsheet measurement
        :type arg: dict

        :rtype: None
        """
        logger.info("[-.--- s] [cam] {}".format(sys._getframe().f_code.co_name))

        if type(arg) is not dict:
            logger.error("Argument is not a dictionary")
            raise TypeError

        lightsheet_config_keys = [
            "scmos readout",
            "line time",
            "lines exposure",
            "lines exposure delay"
        ]

        for k in arg.keys():
            if not k in lightsheet_config_keys:
                raise KeyError(f'{"<"}{k}{"> is not a valid key for pco.Camera.lightsheet_configuration."}')

        if self.sdk.get_recording_state()["recording state"] == "on":
            raise ValueError  # self.sdk.set_recording_state("off")

        if "scmos readout" in arg:
            self.sdk.set_interface_output_format("edge", arg["scmos readout"])
            # self.sdk.set_transfer_parameters_auto()
            self.sdk.get_transfer_parameter()

        if "line time" in arg:
            self.sdk.set_cmos_line_timing("on", arg["line time"])
            if "lines exposure" in arg:
                logger.warning(
                    '!!! Exposure time might change: "line time" * "lines exposure" !!!'
                )

        if "lines exposure" in arg:
            self.sdk.set_cmos_line_exposure_delay(arg["lines exposure"], 0)

        if "lines exposure delay" in arg:
            exposure, delay = arg["lines exposure delay"]
            self.sdk.set_cmos_line_exposure_delay(exposure, delay)

        self._arm_camera()

    # -------------------------------------------------------------------------
    @property
    def flim_configuration(self):
        logger.info("[---.- s] [cam] {}".format(sys._getframe().f_code.co_name))

        conf = {}

        master_modulation_frequency = self.sdk.get_flim_master_modulation_frequency()
        conf.update({"frequency": master_modulation_frequency["frequency"]})

        phase_sequence_parameter = self.sdk.get_flim_phase_sequence_parameter()
        conf.update({"phase_number": phase_sequence_parameter["phase number"]})
        conf.update({"phase_symmetry": phase_sequence_parameter["phase symmetry"]})
        conf.update({"phase_order": phase_sequence_parameter["phase order"]})
        conf.update({"tap_select": phase_sequence_parameter["tap select"]})

        modulation_parameter = self.sdk.get_flim_modulation_parameter()
        conf.update({"source_select": modulation_parameter["source select"]})
        conf.update({"output_waveform": modulation_parameter["output waveform"]})

        image_processing_flow = self.sdk.get_flim_image_processing_flow()
        conf.update({"asymmetry_correction": image_processing_flow["asymmetry correction"]})
        conf.update({"output_mode": image_processing_flow["output mode"]})

        # width = (self._roi['x1'] - self._roi['x0'] + 1)
        # height = (self._roi['y1'] - self._roi['y0'] + 1)
        # conf.update({'resolution': (width, height)})

        # conf.update({'stack_size': self.stack_size})

        return conf

    # -------------------------------------------------------------------------
    @flim_configuration.setter
    def flim_configuration(self, arg):

        logger.info("[---.- s] [cam] {}".format(sys._getframe().f_code.co_name))

        if type(arg) is not dict:
            logger.error("Argument is not a dictionary")
            raise TypeError

        flim_config_keys = [
            "frequency",
            "phase_number",
            "phase_symmetry",
            "phase_order",
            "tap_select",
            "source_select",
            "output_waveform",
            "asymmetry_correction",
            "output_mode"
        ]

        for k in arg.keys():
            if not k in flim_config_keys:
                raise KeyError(f'{"<"}{k}{"> is not a valid key for pco.Camera.flim_configuration."}')

        conf = {}

        if "frequency" in arg:
            conf.update({"frequency": arg["frequency"]})

        if "phase_number" in arg:
            conf.update({"phase_number": arg["phase_number"]})

        if "phase_symmetry" in arg:
            conf.update({"phase_symmetry": arg["phase_symmetry"]})

        if "phase_order" in arg:
            conf.update({"phase_order": arg["phase_order"]})

        if "tap_select" in arg:
            conf.update({"tap_select": arg["tap_select"]})

        if "source_select" in arg:
            conf.update({"source_select": arg["source_select"]})

        if "output_waveform" in arg:
            conf.update({"output_waveform": arg["output_waveform"]})

        if "asymmetry_correction" in arg:
            conf.update({"asymmetry_correction": arg["asymmetry_correction"]})

        if "output_mode" in arg:
            conf.update({"output_mode": arg["output_mode"]})

        self.set_flim_configuration(**conf)

    # -------------------------------------------------------------------------
    def set_flim_configuration(
        self,
        frequency,
        phase_number,
        source_select="intern",
        output_waveform="sinusoidal",
        phase_symmetry="singular",
        phase_order="ascending",
        tap_select="both",
        asymmetry_correction="off",
        output_mode="default",
    ):
        """
        Sets all flim configuration values.

        >>> set_flim_configuration(**dict)

        """
        logger.info("[---.- s] [cam] {}".format(sys._getframe().f_code.co_name))

        self.flim_config = {
            "frequency": frequency,
            "phase_number": phase_number,
            "source_select": source_select,
            "output_waveform": output_waveform,
            "phase_symmetry": phase_symmetry,
            "phase_order": phase_order,
            "tap_select": tap_select,
            "asymmetry_correction": asymmetry_correction,
            "output_mode": output_mode,
        }

        self.sdk.set_flim_modulation_parameter(source_select, output_waveform)

        self.sdk.set_flim_master_modulation_frequency(frequency)

        self.sdk.set_flim_phase_sequence_parameter(
            phase_number, phase_symmetry, phase_order, tap_select
        )

        self.sdk.set_flim_image_processing_flow(asymmetry_correction, output_mode)

    # -------------------------------------------------------------------------
    def get_flim_configuration(self):
        """
        Returns the currently valid flim configuration. This configuration is
        used to initialize the flim calculation module. It contains all the
        required values to synchronize the camera settings and the flim
        calculation module.

        >>> get_flim_configuration()
        config

        """
        logger.info("[---.- s] [cam] {}".format(sys._getframe().f_code.co_name))

        frequency = self.sdk.get_flim_master_modulation_frequency()["frequency"]
        phase_number = self.sdk.get_flim_phase_sequence_parameter()["phase_number"]
        source_select = self.sdk.get_flim_modulation_parameter()["source_select"]
        output_waveform = self.sdk.get_flim_modulation_parameter()["output_waveform"]
        phase_symmetry = self.sdk.get_flim_phase_sequence_parameter()["phase_symmetry"]
        phase_order = self.sdk.get_flim_phase_sequence_parameter()["phase_order"]
        tap_select = self.sdk.get_flim_phase_sequence_parameter()["tap_select"]
        asymmetry_correction = self.sdk.get_flim_image_processing_flow()["asymmetry_correction"]
        output_mode = self.sdk.get_flim_image_processing_flow()["output_mode"]

        self.flim_config = {
            "frequency": frequency,
            "phase_number": phase_number,
            "source_select": source_select,
            "output_waveform": output_waveform,
            "phase_symmetry": phase_symmetry,
            "phase_order": phase_order,
            "tap_select": tap_select,
            "asymmetry_correction": asymmetry_correction,
            "output_mode": output_mode,
        }

        return self.flim_config

    # -------------------------------------------------------------------------
    @property
    def flim_stack_size(self):
        """
        Returns the currently valid stack size of flim images. This value is
        used to handle the readout form the fifo image buffer.
        The flim calculation needs image stacks, depending on the
        configuration, which have exactly this size.

        >>> get_stack_size()
        8

        """

        phase_number_to_int = {
            "manual shifting": 2,
            "2 phases": 2,
            "4 phases": 4,
            "8 phases": 8,
            "16 phases": 16,
        }

        phase_symmetry_to_int = {"singular": 1, "twice": 2}

        tap_select_to_int = {"tap A": 0.5, "tap B": 0.5, "both": 1}

        asymmetry_correction_to_int = {"off": 1, "average": 0.5}

        if self.flim_config is not None:
            rv = int(
                phase_number_to_int[self.flim_config["phase_number"]]
                * phase_symmetry_to_int[self.flim_config["phase_symmetry"]]
                * tap_select_to_int[self.flim_config["tap_select"]]
                * asymmetry_correction_to_int[self.flim_config["asymmetry_correction"]]
            )
        else:
            rv = 0

        logger.debug("stack size: {}".format(rv))
        return rv

    # -------------------------------------------------------------------------
    @property
    def description(self):
        logger.info("[-.--- s] [cam] {}".format(sys._getframe().f_code.co_name))

        desc = {}

        desc.update({"serial": self._serial})
        desc.update({"type": self._camera_type["camera type"]})
        desc.update({"sub type": self._camera_type["camera subtype"]})
        desc.update({"interface type": self._interface})

        cam_desc = self.sdk.get_camera_description()

        cam_desc3 = {}
        if cam_desc["dwGeneralCapsDESC1"] & 0x10000000:  # GENERALCAPS1_ENHANCED_DESCRIPTOR_3
            cam_desc3 = self.sdk.get_camera_description_3()

        desc.update({"min exposure time": (cam_desc["Min Expos DESC"] / 1e9)})
        desc.update({"max exposure time": (cam_desc["Max Expos DESC"] / 1e3)})
        desc.update({"min exposure step": (cam_desc["Min Expos Step DESC"] / 1e9)})
        desc.update({"min delay time": (cam_desc["Min Delay DESC"] / 1e9)})
        desc.update({"max delay time": (cam_desc["Max Delay DESC"] / 1e3)})
        desc.update({"min delay step": (cam_desc["Min Delay Step DESC"] / 1e9)})

        if cam_desc["ir"]:
            ir_sensitivity = self.sdk.get_ir_sensitivity()["ir sensitivity"]
            if ir_sensitivity == 1:
                desc.update({"min exposure time": (cam_desc["Min Expos IR DESC"] / 1e9)})
                desc.update({"max exposure time": (cam_desc["Max Expos IR DESC"] / 1e3)})

                desc.update({"min delay time": (cam_desc["Min Delay IR DESC"] / 1e9)})
                desc.update({"max delay time": (cam_desc["Max Delay IR DESC"] / 1e3)})

        sensor_format = self.sdk.get_sensor_format()["sensor format"]
        if sensor_format == 0:
            desc.update({"max width": cam_desc["max. horizontal resolution standard"]})
            desc.update({"max height": cam_desc["max. vertical resolution standard"]})
            if cam_desc["dwGeneralCapsDESC1"] & 0x10000000:  # GENERALCAPS1_ENHANCED_DESCRIPTOR_3
                desc.update({"min width": cam_desc3["min_horz_res_std"]})
                desc.update({"min height": cam_desc3["min_vert_res_std"]})
            else:
                desc.update({"min width": cam_desc["min size horz"]})
                desc.update({"min height": cam_desc["min size vert"]})
        else:
            desc.update({"max width": cam_desc["max. horizontal resolution extended"]})
            desc.update({"max height": cam_desc["max. vertical resolution extended"]})
            if cam_desc["dwGeneralCapsDESC1"] & 0x10000000:  # GENERALCAPS1_ENHANCED_DESCRIPTOR_3
                desc.update({"min width": cam_desc3["min_horz_res_ext"]})
                desc.update({"min height": cam_desc3["min_vert_res_ext"]})
            else:
                desc.update({"min width": cam_desc["min size horz"]})
                desc.update({"min height": cam_desc["min size vert"]})

        desc.update({"roi steps": (cam_desc["roi hor steps"], cam_desc["roi vert steps"])})
        desc.update({"bit resolution": cam_desc["bit resolution"]})

        roi_symmetric_vert = False
        if cam_desc["dwGeneralCapsDESC1"] & 0x00800000:  # GENERALCAPS1_ROI_VERT_SYMM_TO_HORZ_AXIS
            roi_symmetric_vert = True
        desc.update({"roi is vert symmetric": roi_symmetric_vert})

        roi_symmetric_horz = False
        if cam_desc["dwGeneralCapsDESC1"] & 0x01000000:  # GENERALCAPS1_ROI_HORZ_SYMM_TO_VERT_AXIS
            roi_symmetric_horz = True
        desc.update({"roi is horz symmetric": roi_symmetric_horz})

        has_timestamp_mode = True
        if cam_desc["dwGeneralCapsDESC1"] & 0x00000100:  # GENERALCAPS1_NO_TIMESTAMP
            has_timestamp_mode = False
        desc.update({"has timestamp": has_timestamp_mode})

        has_timestamp_mode_ascii_only = False
        if cam_desc["dwGeneralCapsDESC1"] & 0x00000008:  # GENERALCAPS1_TIMESTAMP_ASCII_ONLY
            has_timestamp_mode_ascii_only = True
        desc.update({"has ascii-only timestamp": has_timestamp_mode_ascii_only})

        has_trigger_mode_extexpctrl = True
        if cam_desc["dwGeneralCapsDESC1"] & 0x00000080:  # GENERALCAPS1_NO_EXTEXPCTRL
            has_trigger_mode_extexpctrl = False
        desc.update({"has trigger extexpctrl": has_trigger_mode_extexpctrl})

        has_acquire_mode = True
        if cam_desc["dwGeneralCapsDESC1"] & 0x00000200:  # GENERALCAPS1_NO_ACQUIREMODE
            has_acquire_mode = False
        desc.update({"has acquire": has_acquire_mode})

        has_ext_acquire_mode = False
        if cam_desc["dwGeneralCapsDESC1"] & 0x00200000:  # GENERALCAPS1_EXT_ACQUIRE
            has_ext_acquire_mode = True
        desc.update({"has extern acquire": has_ext_acquire_mode})

        has_metadata_mode = False
        if cam_desc["dwGeneralCapsDESC1"] & 0x00004000:  # GENERALCAPS1_METADATA
            has_metadata_mode = True
        desc.update({"has metadata": has_metadata_mode})

        has_ram = True
        if cam_desc["dwGeneralCapsDESC1"] & 0x00001000:  # GENERALCAPS1_NO_RECORDER
            has_ram = False
        desc.update({"has ram": has_ram})

        pixelrates = cam_desc["pixel rate"]
        desc.update({"pixelrates": [value for value in pixelrates if value != 0]})

        current_binning_x = 1
        binning_horz = []
        while (current_binning_x <= cam_desc["max. binning horizontal"]):
            binning_horz.append(current_binning_x)
            if cam_desc["binning horizontal stepping"] == 1:
                current_binning_x = current_binning_x + 1
            else:
                current_binning_x = current_binning_x * 2
        desc.update({"binning horz vec": binning_horz})

        current_binning_y = 1
        binning_vert = []
        while (current_binning_y <= cam_desc["max. binning vert"]):
            binning_vert.append(current_binning_y)
            if cam_desc["binning vert stepping"] == 1:
                current_binning_y = current_binning_y + 1
            else:
                current_binning_y = current_binning_y * 2
        desc.update({"binning vert vec": binning_vert})

        has_avg_binning = False
        if cam_desc["dwGeneralCapsDESC3"] & 0x00004000:  # GENERALCAPS3_BINNING_MODE_AVERAGE
            has_avg_binning = True
        desc.update({"has average binning": has_avg_binning})


        formats = []
        if self._camera_description["dwGeneralCapsDESC3"] & 0x00020000:  # GENERALCAPS3_CAMERA_SETUP_PIXELFORMAT
            formats.extend(self.sdk.get_camera_setup("pixel format")["supported pixel formats"])
        else:
            formats.append(self._dynres_to_pixelformat(self._camera_description["bit resolution"]))
        desc.update({"supported pixel formats": formats})

        return desc

    # -------------------------------------------------------------------------
    @property
    def exposure_time(self):
        """Returns the exposure time.

        >>> exp_time = cam.exposure_time
        """

        de = self.sdk.get_delay_exposure_time()

        exposure = de["exposure"]
        timebase = de["exposure timebase"]

        timebase_dict = {"ns": 1e-9, "us": 1e-6, "ms": 1e-3}

        exposure_time = timebase_dict[timebase] * exposure

        # logger.debug("exposure time: {}".format(exposure_time))
        logger.info("[---.- s] [cam] {}".format(sys._getframe().f_code.co_name))
        return exposure_time

    # -------------------------------------------------------------------------
    @exposure_time.setter
    def exposure_time(self, arg):
        """
        Sets the exposure time of the camera. The underlying values for the
        sdk.set_delay_exposure_time() function will be
        calculated automatically. The delay time does not change

        >>> cam.exposure_time = 0.001

        >>> cam.exposure_time = 1e-3

        """
        logger.info("[---.- s] [cam] {}: exposure time: {}".format(sys._getframe().f_code.co_name, arg))

        if type(arg) is not int and type(arg) is not float:
            logger.error("Argument is not an int or float")
            raise TypeError
        
        min_exposure_ns = self._camera_description["Min Expos DESC"]
        max_exposure_ms = self._camera_description["Max Expos DESC"]
        
        if self._camera_description["ir"] == 1:
            ir_sensititvity = self.sdk.get_ir_sensitivity()
            if ir_sensititvity["ir sensitivity"] == "on":
                min_exposure_ns = self._camera_description["Min Expos IR DESC"]
                max_exposure_ms = self._camera_description["Max Expos IR DESC"]
         

        if np.isnan(arg):
            logger.error("invalid exposure time: NaN")
            raise ValueError("invalid exposure time: NaN")
        
        if arg < (1e-9 * (float(min_exposure_ns) - float(self._camera_description["Min Expos Step DESC"]))):
            logger.error("invalid exposure time: smaller than min limit or negative")
            raise ValueError("invalid exposure time: smaller than min limit or negative")

        if arg > (1e-3 * float(max_exposure_ms)):
            logger.error("invalid exposure time: greater than max limit")
            raise ValueError("invalid exposure time: greater than max limit")

        _exposure_time = arg

        if _exposure_time <= 4e-3:
            time = int(_exposure_time * 1e9)
            timebase = "ns"

        elif _exposure_time <= 4:
            time = int(_exposure_time * 1e6)
            timebase = "us"

        elif _exposure_time > 4:
            time = int(_exposure_time * 1e3)
            timebase = "ms"

        else:
            raise AssertionError

        # Get delay time
        de = self.sdk.get_delay_exposure_time()
        delay = de["delay"]
        delay_timebase = de["delay timebase"]

        self.sdk.set_delay_exposure_time(delay, delay_timebase, time, timebase)

    # -------------------------------------------------------------------------

    @property
    def delay_time(self):
        """Returns the delay time.

        >>> del_time = cam.delay_time
        """

        de = self.sdk.get_delay_exposure_time()

        delay = de["delay"]
        timebase = de["delay timebase"]

        timebase_dict = {"ns": 1e-9, "us": 1e-6, "ms": 1e-3}

        delay_time = timebase_dict[timebase] * delay

        # logger.debug("delay time: {}".format(delay_time))
        logger.info("[---.- s] [cam] {}".format(sys._getframe().f_code.co_name))
        return delay_time

    # -------------------------------------------------------------------------
    @delay_time.setter
    def delay_time(self, arg):
        """
        Sets the delay time of the camera. The underlying values for the
        sdk.set_delay_exposure_time() function will be
        calculated automatically. The exposure time does not change.

        >>> cam.delay_time = 0.001

        >>> cam.delay_time= 1e-3

        """
        logger.info("[---.- s] [cam] {}: delay time: {}".format(sys._getframe().f_code.co_name, arg))

        if type(arg) is not int and type(arg) is not float:
            logger.error("Argument is not an int or float")
            raise TypeError

        min_delay_ns = self._camera_description["Min Delay DESC"]
        max_delay_ms = self._camera_description["Max Delay DESC"]
        
        if self._camera_description["ir"] == 1:
            ir_sensititvity = self.sdk.get_ir_sensitivity()
            if ir_sensititvity["ir sensitivity"] == "on":
                min_delay_ns = self._camera_description["Min Delay IR DESC"]
                max_delay_ms = self._camera_description["Max Delay IR DESC"]
         
        if np.isnan(arg):
            logger.error("invalid delay time: NaN")
            raise ValueError("invalid delay time: NaN")
        
        if arg < (1e-9 * (float(min_delay_ns) - float(self._camera_description["Min Delay Step DESC"]))):
            logger.error("invalid delay time: smaller than min limit or negative")
            raise ValueError("invalid delay time: smaller than min limit or negative")

        if arg > (1e-3 * float(max_delay_ms)):
            logger.error("invalid delay time: greater than max limit")
            raise ValueError("invalid delay time: greater than max limit")

        _delay_time = arg

        if _delay_time <= 4e-3:
            time = int(_delay_time * 1e9)
            timebase = "ns"

        elif _delay_time <= 4:
            time = int(_delay_time * 1e6)
            timebase = "us"

        elif _delay_time > 4:
            time = int(_delay_time * 1e3)
            timebase = "ms"

        else:
            raise AssertionError

        # Get delay time
        de = self.sdk.get_delay_exposure_time()
        exposure = de["exposure"]
        exposure_timebase = de["exposure timebase"]

        self.sdk.set_delay_exposure_time(time, timebase, exposure, exposure_timebase)

    # -------------------------------------------------------------------------

    def get_convert_control(self, data_format):
        """
        Get the current convert control settings for the specified data format

        :param data_format: Data format for which the convert settings should be queried
        :type data_format: string

        :return: convert_control
        :rtype: dict

        """
        logger.info("[-.--- s] [cam] {}".format(sys._getframe().f_code.co_name))

        _data_format = self._get_standard_dataformat(data_format)
        conv_ctrl = self.conv[_data_format].get_control_properties()

        return conv_ctrl

    # -------------------------------------------------------------------------
    def set_convert_control(self, data_format, convert_ctrl):
        """
        Set convert control settings for the specified data format.

        :param data_format: Data format for which the convert settings should be set.
        :type data_format: string

        :param convert_ctrl: Convert control settings that should be set.
        :type convert_ctrl: dict

        :rtype: None

        """
        logger.info("[-.--- s] [cam] {}".format(sys._getframe().f_code.co_name))

        _data_format = self._get_standard_dataformat(data_format)
        self.conv[_data_format].set_control_properties(convert_ctrl)

    # -------------------------------------------------------------------------
    def record(self, number_of_images=1, mode="sequence", file_path=None):  # file_type=None   mode=file & file non blocking
        """
        Generates and configures a new Recorder instance.

        :param number_of_images: Number of images allocated in the driver. The
                                 RAM of the PC is limiting the maximum value.
        :type number_of_images: int
        :param mode: Mode of the Recorder
            * 'sequence' - function is blocking while the number of images are
                           recorded. Recorder stops the recording when the
                           maximum number of images is reached.
            * 'sequence non blocking' - function is non blocking. Status must
                                        be checked before reading the image.
            * 'ring buffer' - function is non blocking. Status must be checked
                              before reading the image. Recorder did not stop
                              the recording when the maximum number of images
                              is reached. The first image is overwritten from
                              the next image.
            * 'fifo' - function is non blocking. Status must be checked before
                       reading the image.
        :type mode: string
        :param file_path: Path to save images
        :type file_path: string

        >>> record()

        >>> record(10)

        >>> record(number_of_images=10, mode='sequence')

        >>> record(10, 'ring buffer')

        >>> record(20, 'fifo')

        """

        logger.info(
            "[---.- s] [cam] {}: number_of_images: {}, mode: {}, file_path: {}".format(
                sys._getframe().f_code.co_name, number_of_images, mode, file_path
            )
        )

        self._image_number = 0

        if mode.startswith("camram"):
            if not mode in ["camram segment", "camram ring"]:
                raise ValueError("Unknown CamRam mode: " + mode)
            if not self.has_ram:
                raise ValueError("Camera does not support CamRam!")
            
            max_images = self.camram_max_images
            if (number_of_images != max_images):
                logger.warning("[---.- s] [cam] {}: record mode {} number_of_images is set automatically to maximum: {} --> {}",
                               sys._getframe().f_code.co_name, mode, number_of_images, max_images)
                number_of_images = max_images
            
            if self.description["has metadata"]:
                self.sdk.set_metadata_mode("on")
            
            self.sdk.set_storage_mode("recorder")

            if mode == "camram segment":
                self.sdk.set_recorder_submode("sequence")
            else:
                self.sdk.set_recorder_submode("ring buffer")
        
        if self._camera_description["dwGeneralCapsDESC3"] & 0x00020000:  # GENERALCAPS3_CAMERA_SETUP_PIXELFORMAT
            if self.sdk.get_camera_setup("pixel format")["setup"] == "8":
                self._raw_format_mode = "Byte"
            else:
                self._raw_format_mode = "Word"
        else:
            if self._camera_description["bit resolution"] > 8:
                self._raw_format_mode = "Word"
            else:
                self._raw_format_mode = "Byte"

        if not number_of_images:
            raise CameraException(sdk=self.sdk, message="number_of_images for record(...) must not be 0", code=0xA0163001)

        # if (self.sdk.get_camera_health_status()['status'] & 2) != 2:
        # workaround: camera edge -> set_binning
        self._arm_camera()

        self._roi = self.sdk.get_roi()
        self._width = (self._roi['x1'] - self._roi['x0'] + 1)
        self._height = (self._roi['y1'] - self._roi['y0'] + 1)
        self._double_image_factor = 1
        try:
            if self.sdk.get_camera_description()["wDoubleImageDESC"] == 1:
                if self.sdk.get_double_image_mode()["double image"] == "on":
                    self._double_image_factor = 2
        except ValueError:
            pass

        if self.rec.recorder_handle.value is not None: # == not nullptr
            self.rec.stop_record()
            self.rec.delete()

        # internal values for convert
        sensor_info = self._get_sensor_info()
        for key in self.conv:
            self.conv[key].set_sensor_info(sensor_info["data_bits"], sensor_info["dark_offset"],
                                           sensor_info["ccm"], sensor_info["sensor_info_bits"])

        # camram off
        segment = None

        #######################################################################
        rec_type = mode
        if mode == "sequence":
            if number_of_images <= 0:
                logger.error("Please use 1 or more image buffer")
                raise ValueError
            blocking = "on"
            if file_path is not None:
                raise ValueError('"file_path" is not available in "sequence" mode.')
            self._recorder_buffer_size = self.rec.create("memory")["maximum available images"]

        elif mode == "sequence non blocking":
            if number_of_images <= 0:
                logger.error("Please use 1 or more image buffer")
                raise ValueError
            rec_type = "sequence"
            blocking = "off"
            if file_path is not None:
                raise ValueError('"file_path" is not available in "sequence non blocking" mode.')
            self._recorder_buffer_size = self.rec.create("memory")["maximum available images"]

        elif mode == "ring buffer":
            if number_of_images < 4:
                logger.error("Please use 4 or more image buffer")
                raise ValueError
            blocking = "off"
            if file_path is not None:
                raise ValueError('"file_path" is not available in "ring buffer" mode.')
            self._recorder_buffer_size = self.rec.create("memory")["maximum available images"]

        elif mode == "fifo":
            if number_of_images < 4:
                logger.error("Please use 4 or more image buffer")
                raise ValueError
            blocking = "off"
            if file_path is not None:
                raise ValueError('"file_path" is not available in "fifo" mode.')
            self._recorder_buffer_size = self.rec.create("memory")["maximum available images"]

        #######################################################################
        elif mode == "sequence dpcore":
            if number_of_images <= 0:
                logger.error("Please use 1 or more image buffer")
                raise ValueError
            blocking = "on"
            rec_type = "sequence"
            if file_path is not None:
                raise ValueError('"file_path" is not available in "sequence dpcore" mode.')
            self._recorder_buffer_size = self.rec.create("memory", dpcore=True)["maximum available images"]

        elif mode == "sequence non blocking dpcore":
            if number_of_images <= 0:
                logger.error("Please use 1 or more image buffer")
                raise ValueError
            rec_type = "sequence"
            blocking = "off"
            if file_path is not None:
                raise ValueError('"file_path" is not available in "sequence non blocking dpcore" mode.')
            self._recorder_buffer_size = self.rec.create("memory", dpcore=True)["maximum available images"]

        elif mode == "ring buffer dpcore":
            rec_type = "ring buffer"
            if number_of_images < 4:
                logger.error("Please use 4 or more image buffer")
                raise ValueError
            blocking = "off"
            if file_path is not None:
                raise ValueError('"file_path" is not available in "ring buffer dpcore" mode.')
            self._recorder_buffer_size = self.rec.create("memory", dpcore=True)["maximum available images"]

        elif mode == "fifo dpcore":
            rec_type = "fifo"
            if number_of_images < 4:
                logger.error("Please use 4 or more image buffer")
                raise ValueError
            blocking = "off"
            if file_path is not None:
                raise ValueError('"file_path" is not available in "fifo dpcore" mode.')
            self._recorder_buffer_size = self.rec.create("memory", dpcore=True)["maximum available images"]

        #######################################################################
        elif (
                mode == "tif"
                or mode == "multitif"
                or mode == "pcoraw"
                or mode == "b16"
                or mode == "dicom"
                or mode == 'multidicom'):
            blocking = "off"
            if file_path is None:
                raise ValueError
            base_path = os.path.dirname(os.path.abspath(file_path))
            if not os.path.exists(base_path):
                base_path = file_path
                if not os.path.exists(base_path):
                    logger.error("Invalid file path, folder doesn't exist")
                    raise ValueError

            self._recorder_buffer_size = self.rec.create("file", file_path=base_path)["maximum available images"]

        elif mode.startswith("camram"):
            blocking = "off"
            segment = self.camram_segment
            rec_type = "camram sequential"
            self._recorder_buffer_size = self.rec.create("camram")["maximum available images"]
            
        else:
            raise ValueError("Unknown record mode: " + mode)

        if number_of_images > self._recorder_buffer_size:
            logger.warning("Not enough space for your application.")
            logger.warning("Required number of images get adapted to max possible:", self._recorder_buffer_size)
            number_of_images = self._recorder_buffer_size
        elif number_of_images > (0.5 * self._recorder_buffer_size) and not segment:
            logger.warning("You are above 50% of available space.")

        self.rec.init(number_of_images, rec_type, file_path, segment)

        #set auto exposure settings
        #Here we force set the auto exp state as we know that record gets started now
        self._update_auto_exposure(True)
        self.rec.start_record()

        if blocking == "on":
            while True:
                cur_status = self.rec.get_status()
                lastBufferError = cur_status["dwLastError"]
                if lastBufferError != 0:
                    raise CameraException(sdk=self.sdk, code=lastBufferError)
                running = cur_status["is running"]
                if running is False:
                    break
                time.sleep(0.001)

    # -------------------------------------------------------------------------
    def stop(self):
        """
        Stops the current recording. Is used in "ring buffer" mode or "fifo"
        mode.

        >>> stop()

        """
        logger.info("[---.- s] [cam] {}".format(sys._getframe().f_code.co_name))

        if self.rec.recorder_handle.value is not None:
            self.rec.stop_record()

    # -------------------------------------------------------------------------
    def close(self):
        """
        Closes the current active camera and releases the blocked resources.
        This function must be called before the application is terminated.
        Otherwise the resources remain occupied.

        This function is called automatically, if the camera object is
        created by the 'with' statement. An explicit call of 'close()' is no
        longer necessary.

        >>> close()

        >>> with pco.camera() as cam:
        ...:   # do some stuff

        """
        logger.info("[---.- s] [cam] {}".format(sys._getframe().f_code.co_name))

        if not self._opened:
          logger.warning("[---.- s] [cam] {} has not been open yet.".format(sys._getframe().f_code.co_name))
          return
            

        self._opened = False

        if hasattr(self, "conv"):
            for key in self.conv:
                try:
                    if self.conv[key].convert_handle.value is not None:
                        self.conv[key].delete()
                except ValueError:
                    pass
            self.conv.clear()

        if hasattr(self, "rec"):
            try:
                if self.rec.recorder_handle.value is not None:
                    self.rec.stop_record()
            except ValueError:
                pass

            try:
                if self.rec.recorder_handle.value is not None:
                    self.rec.delete()
            except ValueError:
                pass

        if hasattr(self, "sdk"):
            try:
                if self.sdk.lens_control.value is not None:
                    self.sdk.close_lens_control()
            except ValueError:
                pass

            try:
                if self.sdk.camera_handle.value is not None:
                    self.sdk.close_camera()
            except ValueError:
                pass

        shared_library_loader.decrement()

    def load_lut(self, data_format, lut_file):
        """
        Set the lut file for the convert control settings.

        This is just a convenience function, the lut file could also be set using setConvertControl

        :param data_format: Data format for which the lut file should be set.
        :type data_format: string

        :param lut_file: Actual lut file path to be set.
        :type lut_file: string

        :rtype: None

        >>> load_lut("RGBA8", "C:/Program Files/PCO Digital Camera Toolbox/pco.camware/Lut/LUT_blue.lt4")

        """
        logger.info("[---.- s] [cam] {}".format(sys._getframe().f_code.co_name))

        _data_format = self._get_standard_dataformat(data_format)
        if not _data_format == "BGR8":
            raise ValueError("{}: Invalid data format".format(data_format))

        if self.is_color:
            raise ValueError("Pseudo color not supported for color cameras!")

        conv_ctrl = self.conv[_data_format].get_control_properties()
        conv_ctrl["lut_file"] = lut_file

        self.conv[_data_format].set_control_properties(conv_ctrl)

    def adapt_white_balance(self, image, data_format, roi=None):
        """
        Do a white-balance according to a transferred image.

        :param image: Image that should be used for white-balance computation
        :type image: numpy array

        :param data_format: Data format for which the lut file should be set.
        :type data_format: string

        :param roi: Use only the specified roi for white-balance computation
        :type roi: tuple(int, int, int, int)

        :rtype: None

        """
        logger.info("[---.- s] [cam] {}".format(sys._getframe().f_code.co_name))

        _data_format = self._get_standard_dataformat(data_format)
        if not _data_format in ["BGR8", "BGR16"]:
            raise ValueError("{}: Invalid data format".format(data_format))

        wb_dict = self.conv[_data_format].get_white_balance(image, roi)

        conv_ctrl = self.conv[_data_format].get_control_properties()
        conv_ctrl["color_temperature"] = wb_dict["color_temp"]
        conv_ctrl["color_tint"] = wb_dict["color_tint"]

        self.conv[_data_format].set_control_properties(conv_ctrl)

    def configureHWIO_1_exposureTrigger(self, on, edgePolarity):
        """
        Configures the HWIO 1
        :param on: True for on, False for off
        :type on: bool

        :param edgePolarity: "rising edge" or "falling edge"
        :type edgePolarity: string

        :rtype: None
        """
        signal_index = 0
        if on:
            on_off = "on"
        else:
            on_off = "off"
        if not (edgePolarity == "rising edge" or edgePolarity == "falling edge"):
            # Error
            raise CameraException(sdk=self.sdk, message="HWIO 1 polarity is not \"rising edge\" or \"falling edge\"")
        if self.is_recording:
            # Error
            raise CameraException(sdk=self.sdk, message="HWIO can not be set during recording")
        if self._camera_description["dwGeneralCapsDESC1"] & 0x40000000 != 0x40000000:  # GENERALCAPS1_HW_IO_SIGNAL_DESCRIPTOR
            # Error
            raise CameraException(sdk=self.sdk, message="HWIO Configuration not supported for this camera!")

        settings = self.sdk.get_hwio_signal(signal_index)
        self.sdk.set_hwio_signal(signal_index, on_off, settings["type"], edgePolarity, settings["filter"], settings["selected"], settings["parameter"])
        self._arm_camera()

    def configureHWIO_2_acquireEnable(self, on, polarity):
        """
        Configures the HWIO 2
        :param on: True for on, False for off
        :type on: bool

        :param polarity: "high level" or "low level"
        :type polarity: string

        :rtype: None
        """
        signal_index = 1
        if on:
            on_off = "on"
        else:
            on_off = "off"
        if not (polarity == "high level" or polarity == "low level"):
            # Error
            raise CameraException(sdk=self.sdk, message="HWIO 2 polarity is not \"high level\" or \"low level\"")
        if self.is_recording:
            # Error
            raise CameraException(sdk=self.sdk, message="HWIO can not be set during recording")
        if self._camera_description["dwGeneralCapsDESC1"] & 0x40000000 != 0x40000000:  # GENERALCAPS1_HW_IO_SIGNAL_DESCRIPTOR
            # Error
            raise CameraException(sdk=self.sdk, message="HWIO Configuration not supported for this camera!")

        settings = self.sdk.get_hwio_signal(signal_index)
        self.sdk.set_hwio_signal(signal_index, on_off, settings["type"], polarity, settings["filter"], settings["selected"], settings["parameter"])
        self._arm_camera()
        pass

    def configureHWIO_3_statusBusy(self, on, polarity, signal_type):
        """
        Configures the HWIO 3
        If the signal_type is not available, it configures HWIO3 anyway, based on "on" and "polarity"
        The function returns true if the signal_type is available and false if it is not available
        :param on: True for on, False for off
        :type on: bool

        :param polarity: "high level" or "low level"
        :type polarity: string

        :param signal_type: "status busy" or "status line" or "status armed"
        :type signal_type: string

        :return: type_available 
        :rtype: bool 
        """
        signal_index = 2
        if on:
            on_off = "on"
        else:
            on_off = "off"
        if not (polarity == "high level" or polarity == "low level"):
            # Error
            raise CameraException(sdk=self.sdk, message="HWIO 3 polarity is not \"high level\" or \"low level\"")
        if self.is_recording:
            # Error
            raise CameraException(sdk=self.sdk, message="HWIO can not be set during recording")
        if self._camera_description["dwGeneralCapsDESC1"] & 0x40000000 != 0x40000000:  # GENERALCAPS1_HW_IO_SIGNAL_DESCRIPTOR
            # Error
            raise CameraException(sdk=self.sdk, message="HWIO Configuration not supported for this camera!")

        comp = {"status busy": 0x00,
                "status expos": 0x01,
                "status line": 0x02,
                "status armed": 0x03}
        if signal_type not in comp:
            raise CameraException(sdk=self.sdk, message="HWIO 3 signal_type is unknown")
        if signal_type == "status expos":
            raise CameraException(sdk=self.sdk, message="status expos is not supported by HWIO 3")

        settings = self.sdk.get_hwio_signal(signal_index)
        descriptor = self.sdk.get_hwio_signal_descriptor(signal_index)

        type_available = False
        if signal_type in (x.lower() for x in descriptor["signal name"]):
            index = [x.lower() for x in descriptor["signal name"]].index(signal_type)
            settings["selected"] = index
            type_available = True
        else:
            print("HWIO 3 signal_type is not supported by the camera")
            type_available = False

        self.sdk.set_hwio_signal(signal_index, on_off,  settings["type"], polarity, settings["filter"], settings["selected"], settings["parameter"])
        self._arm_camera()
        
        return type_available

    def configureHWIO_4_statusExpos(self, on, polarity, signal_type, signal_timing=None):
        """
        Configures the HWIO 4
        If the signal_type is not available, it configures HWIO4 anyway, based on "on" and "polarity"
        The function returns true if the signal_type is available and false if it is not available

        :param on: True for on, False for off
        :type on: bool

        :param polarity: "high level" or "low level"
        :type polarity: string

        :param signal_type: "status expos" or "status line" or "status armed"
        :type signal_type: string

        :param signal_timing: None if it should be ignored, 
            otherwise one of "first line" or "last line" or "global" or "all lines"
        :type signal_timing: string

        :return: type_available 
        :rtype: bool 
        """
        signal_index = 3
        if on:
            on_off = "on"
        else:
            on_off = "off"
        if not (polarity == "high level" or polarity == "low level"):
            # Error
            raise CameraException(sdk=self.sdk, message="HWIO 4 polarity is not \"high level\" or \"low level\"")
        if self.is_recording:
            # Error
            raise CameraException(sdk=self.sdk, message="HWIO can not be set during recording")
        if self._camera_description["dwGeneralCapsDESC1"] & 0x40000000 != 0x40000000:  # GENERALCAPS1_HW_IO_SIGNAL_DESCRIPTOR
            # Error
            raise CameraException(sdk=self.sdk, message="HWIO Configuration not supported for this camera!")

        comp = {"status busy": 0x00,
                "status expos": 0x01,
                "status line": 0x02,
                "status armed": 0x03}
        if not signal_type in comp:
            raise CameraException(sdk=self.sdk, message="HWIO 4 signal_type is unknown")
        if signal_type == "status busy":
            raise CameraException(sdk=self.sdk, message="status busy is not supported by HWIO 4")

        settings = self.sdk.get_hwio_signal(signal_index)
        descriptor = self.sdk.get_hwio_signal_descriptor(signal_index)
        
        type_available = False
        if signal_type in (x.lower() for x in descriptor["signal name"]):
            index = [x.lower() for x in descriptor["signal name"]].index(signal_type)
            settings["selected"] = index
            type_available = True

            if signal_timing is not None:
                timings = {"first line": 0x01,
                        "last line": 0x03,
                        "global": 0x02,
                        "all lines": 0x04}
                if not signal_timing in timings.keys():
                    raise CameraException(sdk=self.sdk, message="HWIO 4 signal_timing is unknown")
                if signal_type != "status expos":
                    raise CameraException(sdk=self.sdk, message="Signal Timing only supported for signal type status_expos!")
                if settings["signal functionality"][index] != 0x07:
                    raise CameraException(sdk=self.sdk, message="Signal Timing only supported for rolling shutter!")
                    
                settings["parameter"][index] = timings[signal_timing]
        else:
            print("HWIO 4 signal_type is not supported by the camera")
            type_available = False
        
        self.sdk.set_hwio_signal(signal_index, on_off,  settings["type"], polarity, settings["filter"], settings["selected"], settings["parameter"])
        self._arm_camera()
        
        return type_available


    # -------------------------------------------------------------------------
    def __enter__(self):
        logger.info("[---.- s] [cam] {}".format(sys._getframe().f_code.co_name))
        return self

    # -------------------------------------------------------------------------
    def __exit__(self, exc_type, exc_value, exc_traceback):
        logger.info("[---.- s] [cam] {}".format(sys._getframe().f_code.co_name))
        self.close()

    # -------------------------------------------------------------------------

    def image(self, image_index=0, roi=None, data_format="Undefined", comp_params=None):
        """
        Returns an image from the recorder and metadata.

        :param image_index:  Index of the image that should be queried, 
                             use PCO_RECORDER_LATEST_IMAGE for latest image 
                             (for recorder modes fifo/fifo_dpcore always use 0)
        :type image_index: int
        :param roi: Region of interest. Only this region is returned.
        :type roi: tuple(int, int, int, int)

        :param data_format: Data format the image should have
        :type data_format: string

        :param comp_params: Compression parameters, not implemented yet
        :type comp_params: dict

        :return: image, metadata
        :rtype: tuple<numpy array, dict>
                shape: (n, m) for monochrome formats, meta data: dict
                shape: (n, m, 3) for color formats without alpha channel, meta data: dict
                shape: (n, m, 4) for color formats with alpha channel, meta data: dict

        >>> image(image_index=0, roi=(1, 1, 512, 512))
        image, metadata

        >>> image(0xFFFFFFFF)
        image, metadata

        >>>image(data_format='rgb')
        image, metadata

        """

        logger.info(
            "[---.- s] [cam] {}: image_index: {}, argument roi: {}, data_format: {}".format(
                sys._getframe().f_code.co_name, image_index, roi, data_format
            )
        )

        if not self.rec.recorder_handle.value:
            if self.has_ram:
                raise CameraException(sdk=self.sdk, message="Camera has no memory allocated for the active segment", code=0x00160000|0x00003000|0xA0000006)
            raise CameraException(sdk=self.sdk, message="Camera has not recorded yet. Call \"record(...)\" before \"images(...)\"", code=0x00160000|0x00003000|0x80003024)


        _data_format = self._get_standard_dataformat(data_format)

        if self._raw_format_mode == "Byte" and _data_format != "Mono8":
            raise ValueError("data format is not supported with pixel format setup 'Byte'")
        
        if not self.is_color and _data_format == "BGR16":
            raise ValueError("data format BGR16 is not supported for mono cameras!")
        
        channel_order_rgb = True
        if data_format.lower().startswith('bgr'):
            channel_order_rgb = False

        if (_data_format == "CompressedMono8"):
            if comp_params == None:
                raise ValueError("Compression parameters are required for CompressedMono8 format")
            self.rec.set_compression_params(comp_params)

        if roi is None:
            if _data_format == "CompressedMono8":
                image = self.rec.copy_image_compressed(
                    image_index, 1, 1, self._width, (self._height * self._double_image_factor))
            else:
                image = self.rec.copy_image(
                    image_index, 1, 1, self._width, (self._height * self._double_image_factor), self._raw_format_mode)
            np_image = np.asarray(image["image"]).reshape((self._height * self._double_image_factor), self._width)
        else:
            if _data_format == "CompressedMono8":
                image = self.rec.copy_image_compressed(image_index, roi[0], roi[1], roi[2], roi[3])
            else:
                image = self.rec.copy_image(image_index, roi[0], roi[1], roi[2], roi[3], self._raw_format_mode)
            np_image = np.asarray(image["image"]).reshape((roi[3] - roi[1] + 1), (roi[2] - roi[0] + 1))

        meta = {}
        # meta.update({"raw format": self._raw_format_mode})
        meta.update({"data format": _data_format})

        if len(image["timestamp"]) > 0:
            meta.update({"timestamp": image["timestamp"]})  # cleared turned off

        meta.update(image["metadata"])  # cleared turned off

        meta.update({"recorder image number": image["recorder image number"]})
        self._image_number = image["recorder image number"]

        if _data_format in ["Mono16", "CompressedMono8"]:
            return np_image, meta

        if roi is not None:
            soft_offset_x = roi[0] - 1
            soft_offset_y = roi[1] - 1
        else:
            soft_offset_x = 0
            soft_offset_y = 0

        offset_x = self._roi["x0"] - 1 + soft_offset_x
        offset_y = self._roi["y0"] - 1 + soft_offset_y
        color_pattern = self._camera_description["Color Pattern DESC"]

        has_alpha = False
        if data_format in ["RGBA8", "BGRA8", "rgba8", "bgra8", "rgba", "bgra"]:
            has_alpha = True

        mode = self.conv[_data_format].get_mode_flags(with_alpha=has_alpha)

        if _data_format == "Mono8" and self._raw_format_mode == "Word":
            mono8image = self.conv["Mono8"].convert_16_to_8(np_image, mode, color_pattern, offset_x, offset_y)
            return mono8image, meta
        if _data_format == "Mono8" and self._raw_format_mode == "Byte":
            return np_image, meta

        if _data_format == "BGR8":
            if self.is_color:
                colorimage = self.conv["BGR8"].convert_16_to_col(np_image, mode, color_pattern, offset_x, offset_y)
            else:
                colorimage = self.conv["BGR8"].convert_16_to_pseudo(np_image, mode, color_pattern, offset_x, offset_y)

            if channel_order_rgb:
                img = np.flip(colorimage[:, :, 0:3], 2)  # rgb
                if colorimage.shape[2] == 4:
                    a = colorimage[:, :, 3:]  # a
                    img = np.concatenate((img, a), axis=2)  # rgb + a
            else:
                img = colorimage  # bgr, bgra
            return img, meta
        elif _data_format == "BGR16":
            colorimage = self.conv["BGR16"].convert_16_to_col16(np_image, mode, color_pattern, offset_x, offset_y)
            if channel_order_rgb:
                img = np.flip(colorimage, 2)
            else:
                img = colorimage
            return img, meta
        else:
            raise ValueError

    # -------------------------------------------------------------------------

    def images(
        self,
        roi=None,
        start_idx=0,
        blocksize=None,
        data_format="Undefined",
        comp_params=None
    ):
        """
        Returns all recorded images from the recorder.

        :param roi: Region of interest. Only this region is returned.
        :type roi: tuple(int, int, int, int)

        :param blocksize: The blocksize defines the number of images which are returned.
        :type blocksize: int

        :param start_idx: The index of the first image that should be queried
        :type start_idx: int

        :param data_format: Data format the image should have
        :type data_format: string

        :param comp_params: Compression parameters, not implemented yet
        :type comp_params: dict

        :return: images
        :rtype: list(numpy arrays)

        >>> images()
        image_list, metadata_list

        >>> images(blocksize=8, start_idx=6)
        image_list[:8], metadata_list[:8]

        """
        # logger.debug("argument roi: {}, blocksize: {}".format(roi, blocksize))
        logger.info("[---.- s] [cam] {}".format(sys._getframe().f_code.co_name))

        if not self.rec.recorder_handle.value:
            if self.has_ram:
                raise CameraException(sdk=self.sdk, message="Camera has no memory allocated for the active segment", code=0x00160000|0x00003000|0xA0000006)
            raise CameraException(sdk=self.sdk, message="Camera has not recorded yet. Call \"record(...)\" before \"images(...)\"", code=0x00160000|0x00003000|0x80003024)

        image_list = []
        meta_list = []

        status = self.rec.get_status()
        record_on = status["bIsRunning"]

        settings = self.rec.get_settings()
        if record_on and settings["recorder mode"] == 0x0002 and settings["recorder type"] == 0x0002:
            raise CameraException(sdk=self.sdk, message="images() does not support record mode ring_buffer during record.", code=0x00160000|0x00003000|0xA0000013)
        if blocksize is None:
            blocksize = status["dwReqImgCount"] - start_idx
        elif blocksize > (status["dwReqImgCount"] - start_idx):
            raise ValueError("Block size is too big to hold latest recorded images starting from start_index!")

        # wait for images to be recorded
        while record_on:
            status = self.rec.get_status()
            record_on = status["bIsRunning"]
            if (status["dwProcImgCount"] >= (blocksize + start_idx)):
                break

        if (self.rec.get_status()["dwProcImgCount"] < (blocksize + start_idx)):
            raise CameraException(sdk=self.sdk, message="Image vector is too big to hold currently recorded images and record has stopped!", code=0x00160000|0x00003000|0xA0000006)

        for index in range(start_idx, (start_idx + blocksize)):
            image, meta = self.image(index, roi, data_format, comp_params)

            meta_list.append(meta)
            image_list.append(image)

        return image_list, meta_list

    # -------------------------------------------------------------------------

    def image_average(self, roi=None, data_format="Undefined"):
        """
        Returns an averaged image from the recorder.

        :param roi: Region of interest. Only this region is returned.
        :type roi: tuple(int, int, int, int)

        :param data_format: Data format the image should have
        :type data_format: string

        :return: image
        :rtype: numpy array
                shape: (n, m) for monochrome formats,
                shape: (n, m, 3) for color formats without alpha channel
                shape: (n, m, 4) for color formats with alpha channel

        >>> image_average(roi=(1, 1, 512, 512))
        image

        """

        logger.info(
            "[---.- s] [cam] {}: argument roi: {}, data_format: {}".format(
                sys._getframe().f_code.co_name, roi, data_format
            )
        )

        if not self.rec.recorder_handle.value:
            if self.has_ram:
                raise CameraException(sdk=self.sdk, message="Camera has no memory allocated for the active segment", code=0x00160000|0x00003000|0xA0000006)
            raise CameraException(sdk=self.sdk, message="Camera has not recorded yet. Call \"record(...)\" before \"images(...)\"", code=0x00160000|0x00003000|0x80003024)

        _data_format = self._get_standard_dataformat(data_format)

        if self._raw_format_mode == "Byte" and _data_format != "Mono8":
            raise ValueError("data format is not supported with pixel format setup 'Byte'")
        
        if not self.is_color and _data_format == "BGR16":
            raise ValueError("data format BGR16 is not supported for mono cameras!")
        

        channel_order_rgb = True
        if data_format.lower().startswith('bgr'):
            channel_order_rgb = False

        if _data_format == "CompressedMono8":
            raise ValueError("DataFormat::CompressedMono8 is not supported for average images!")

        status = self.rec.get_status()
        start_idx = 0
        stop_idx = min(status["dwProcImgCount"], status["dwReqImgCount"]) - 1
        if roi is None:
            image = self.rec.copy_average_image(
                start_idx, stop_idx, 1, 1, self._width, (self._height * self._double_image_factor), self._raw_format_mode)
            np_image = np.asarray(image["average image"]).reshape((self._height * self._double_image_factor), self._width)
        else:
            image = self.rec.copy_average_image(start_idx, stop_idx, roi[0], roi[1], roi[2], roi[3], self._raw_format_mode)
            np_image = np.asarray(image["average image"]).reshape((roi[3] - roi[1] + 1), (roi[2] - roi[0] + 1))

        if _data_format == "Mono16":
            return np_image

        if roi is not None:
            soft_offset_x = roi[0] - 1
            soft_offset_y = roi[1] - 1
        else:
            soft_offset_x = 0
            soft_offset_y = 0

        offset_x = self._roi["x0"] - 1 + soft_offset_x
        offset_y = self._roi["y0"] - 1 + soft_offset_y
        color_pattern = self._camera_description["Color Pattern DESC"]

        has_alpha = False
        if data_format in ["RGBA8", "BGRA8", "rgba8", "bgra8", "rgba", "bgra"]:
            has_alpha = True

        mode = self.conv[_data_format].get_mode_flags(with_alpha=has_alpha)

        if _data_format == "Mono8" and self._raw_format_mode == "Word":
            mono8image = self.conv["Mono8"].convert_16_to_8(np_image, mode, color_pattern, offset_x, offset_y)
            return mono8image
        if _data_format == "Mono8" and self._raw_format_mode == "Byte":
            return np_image
        
        elif _data_format == "BGR8":
            if self.is_color:
                colorimage = self.conv["BGR8"].convert_16_to_col(np_image, mode, color_pattern, offset_x, offset_y)
            else:
                colorimage = self.conv["BGR8"].convert_16_to_pseudo(np_image, mode, color_pattern, offset_x, offset_y)

            if channel_order_rgb:
                img = np.flip(colorimage[:, :, 0:3], 2)  # rgb
                if colorimage.shape[2] == 4:
                    a = colorimage[:, :, 3:]  # a
                    img = np.concatenate((img, a), axis=2)  # rgb + a
            else:
                img = colorimage  # bgr, bgra
            return img
        elif _data_format == "BGR16":
            colorimage = self.conv["BGR16"].convert_16_to_col16(np_image, mode, color_pattern, offset_x, offset_y)
            if channel_order_rgb:
                img = np.flip(colorimage, 2)
            else:
                img = colorimage
            return img
        else:
            raise ValueError

    # -------------------------------------------------------------------------
    def wait_for_first_image(self, delay=True, timeout=None):
        """
        This function waits for the first available image. In recorder mode
        'sequence non blocking', 'ring buffer' and 'fifo' the record() function
        returns immediately. The user is responsible to wait for images from
        the camera before image() / images() is called.

        :param delay: This parameter reduces the frequency of the queries and
                      the maybe unnecessary utilization of the CPU.
        :type delay: bool

        :param timeout: If set, this parameter defines the timeout [s] for the waiting loop.
        :type timeout: float

        >>> wait_for_first_image(delay=True, timeout=5.0)

        >>> wait_for_first_image(delay=False)

        """
        # logger.debug("delay: {}".format(delay))
        logger.info("[---.- s] [cam] {}".format(sys._getframe().f_code.co_name))

        time_start = time.perf_counter()
        while True:
            if self.rec.get_status()["dwProcImgCount"] >= 1:
                break
            if delay:
                time.sleep(0.001)

            duration = time.perf_counter() - time_start
            if timeout is not None and duration > timeout:
                raise TimeoutError("Timeout ({} s) reached, no image acquired".format(timeout))

    # -------------------------------------------------------------------------
    def wait_for_new_image(self, delay=True, timeout=None):
        """
        This function waits for a newer image.

        The __init__() and stop() function set the value to zero. The image()
        function stores the last reded image number.

        :param delay: This parameter reduces the frequency of the queries and
                      the maybe unnecessary utilization of the CPU.
        :type delay: bool

        :param timeout: If set, this parameter defines the timeout [s] for the waiting loop.
        :type timeout: float

        >>> wait_for_new_image(delay=True, 5.0)

        >>> wait_for_new_image(delay=False)

        :return:
        """
        # logger.debug("delay: {}".format(delay))
        logger.info("[---.- s] [cam] {}".format(sys._getframe().f_code.co_name))

        # get recorder type
        time_start = time.perf_counter()
        settings = self.rec.get_settings()
        while True:
            status = self.rec.get_status()
            image_count = status["dwProcImgCount"]
            
            if not status["bIsRunning"]:
                break

            if settings["recorder mode"] == 0x0003 and self._image_number == 0xffffffff: # camram without metadata (recorder implementation)
                break

            if settings["recorder type"] == 0x0003:  # for fifo mode check only > 0
                if self.rec.get_status()["dwProcImgCount"] > 0:
                    break
            else:
                if image_count > self._image_number:
                    break
            if delay:
                time.sleep(0.001)

            duration = time.perf_counter() - time_start
            if timeout is not None and duration > timeout:
                raise TimeoutError("Timeout ({} s) reached, no new image acquired".format(timeout))

    def auto_exposure_on(self):
        """Switch on autoexposure
        """

        self._auto_exp_state = True 
        self._update_auto_exposure()

    def auto_exposure_off(self):
        """Switch off autoexposure
        """

        self._auto_exp_state = False 
        self._update_auto_exposure()
        
    def configure_auto_exposure(self, region_type, min_exposure_s, max_exposure_s):
        """Configure the auto exposure functionality
        :param region_type: Relevant region for auto exposure check. (valid are "balanced", "center based", "corner based", "full")
        :type region_type: string

        :param min_exposure_s: lowest exposure time in seconds that auto exposure is allowed to reach
        :type min_exposure_s: double

        :param max_exposure_s: highest exposure time in seconds that auto exposure is allowed to reach
        :type max_exposure_s: double
        """

        types = {
            "balanced": 0,
            "center based": 1,
            "corner based": 2,
            "full": 3,
        }
        if region_type not in types:
            raise CameraException(sdk=self.sdk, message="auto exposure region_type is unknown")
        if min_exposure_s is None or max_exposure_s is None:
            raise CameraException(sdk=self.sdk, message="Either min exposure or/and max exposure is None")
        else:
            if max_exposure_s < min_exposure_s:
                raise CameraException(sdk=self.sdk, message="auto exposure max exposure is smaller than min exposure")
        self._auto_exposure = {"region": region_type, "min exposure": min_exposure_s, "max exposure": max_exposure_s}
        self._update_auto_exposure()


    def switch_to_camram(self, segment=None):
        if not self.has_ram:
            raise ValueError("Camera does not support CamRam!")
        
        if not segment:
            segment = self.camram_segment

        logger.info("[-.--- s] [cam] {}".format(sys._getframe().f_code.co_name))

        if self.sdk.get_recording_state()["recording state"] == "on":
            self.sdk.set_recording_state("off")
        
        self.sdk.set_active_ram_segment(segment)
        self._segment = segment

        if self._camera_description["dwGeneralCapsDESC1"] & 0x00004000:
            self.sdk.set_metadata_mode("on")
        
        if self.rec.recorder_handle.value is not None:
            self.rec.stop_record()
            self.rec.delete()

        self.sdk.set_storage_mode("recorder")
        
        self.sdk.set_recorder_submode("ring buffer")

        try:
            self._arm_camera()
        except CameraException as exc:
            if (exc.error_code & 0x80001025) == 0x80001025:
                return
            raise

        max_images = self.rec.create("camram")["maximum available images"]

        type = "camram sequential"
        if max_images:
            self.rec.init(max_images, type)
        
        settings = self.rec.get_settings()

        self._image_number = 0

        self._roi = {
                "x0": 1,
                "y0": 1,
                "x1": settings["width"],
                "y1": settings["height"],
            }
        
        self._recorder_buffer_size = settings["maximum number of images"]

    def set_camram_allocation(self, percents):
        if not self.has_ram:
            raise ValueError("Camera does not support CamRam!")
        
        if not isinstance(percents, list):
            raise ValueError("percents is not list of numbers that assign sizes of CamRam allocation.")
        
        ps = percents[:4]
        sum_ps = sum(ps)

        if sum_ps > 100:
            raise ValueError("Sum of percentages is greater than 100%")
        
        if sum_ps <= 1.0 and sum_ps > 0.0:
            ps = [ x * 100 for x in ps ]
        
        storage = self.sdk.get_storage_struct()

        self.sdk.set_camera_ram_segment_size(
            [int(x) * int(storage["ram size"] / 100) for x in ps]
        )
        

######################### private functions #########################


    def _get_sensor_info(self):
        """
        get required infos for convert creation
        """
        logger.info("[---.- s] [cam] {}".format(sys._getframe().f_code.co_name))
        # get required infos for convert creation
        sensor_info_bits = 0
        bit_align = self.sdk.get_bit_alignment()["bit alignment"]
        if bit_align == "MSB":
            sensor_info_bits |= 0x0002
        if self._camera_description["sensor type"] & 0x0001:
            sensor_info_bits |= 0x0001

        ccm = (1, 0, 0, 0, 1, 0, 0, 0, 1)
        if self._camera_description["dwGeneralCapsDESC1"] & 0x00020000:  # GENERALCAPS1_CCM
            ccm = self.sdk.get_color_correction_matrix()["ccm"]

        data_bits = self._camera_description["bit resolution"]
        dark_offset = self.sdk.get_sensor_dark_offset()["dark offset"]

        sensor_info = {
            "sensor_info_bits": sensor_info_bits,
            "ccm": ccm,
            "data_bits": data_bits,
            "dark_offset": dark_offset
        }

        return sensor_info

    def _get_standard_dataformat(self, data_format):
        
        if data_format == "Undefined":
            if self._raw_format_mode == "Byte":
                return "Mono8"
            else:
                return "Mono16"

        df_dict = dict.fromkeys(["Mono8", "mono8"], "Mono8")
        df_dict.update(dict.fromkeys(["Mono16", "mono16", "raw16", "bw16"], "Mono16"))
        df_dict.update(dict.fromkeys(["rgb", "bgr", "RGB8", "BGR8", "RGBA8",
                       "BGRA8", "rgba8", "bgra8", "rgba", "bgra"], "BGR8"))
        df_dict.update(dict.fromkeys(["RGB16", "BGR16", "rgb16", "bgr16"], "BGR16"))
        df_dict.update(dict.fromkeys(["CompressedMono8", "compressed"], "CompressedMono8"))

        try:
            df = df_dict[data_format]
            return df
        except KeyError:
            raise ValueError(f'{"Invalid data_format. Available keys: "}{df_dict.keys()}')

    def _update_auto_exposure(self, force=False):
        """_summary_
        Update the current auto exposure region settings. 
        Update auto exposure setting when record is on or force is set
        
        Args:
            force (bool, optional): If set, the function always calls PCO_RecorderSetAutoExposure, 
                                    otherwise only when record is running. Defaults to False.
        """

        if self.rec.recorder_handle.value is not None: # == not nullptr
            err = self.rec.set_auto_exp_regions(self._auto_exposure["region"])
            if err:
                raise CameraException(sdk=self.sdk, code=err)

            if self.is_recording or force:    
                if self._auto_exp_state:
                    on_off = "on"
                else:
                    on_off = "off"           
                self.rec.set_auto_exposure(mode=on_off,
                                           smoothness=3,
                                           min_exposure_time=self._auto_exposure["min exposure"],
                                           max_exposure_time=self._auto_exposure["max exposure"])

    def _dynres_to_pixelformat(self, bit_resolution):
        if bit_resolution == 8:
            return "8"
        if bit_resolution == 10:
            return "10"
        if bit_resolution == 12:
            return "12"
        if bit_resolution == 14:
            return "14"
        if bit_resolution == 16:
            return "16"
        raise ValueError("Dynamic resolution is not supported")

    def _arm_camera(self):
        """
        Arm the camera
        """

        self.sdk.arm_camera()
        health_dict = self.sdk.get_camera_health_status()
        if (health_dict["status"] & 0x40000000) == 0x40000000:  # STATUS_DESCRIPTOR_MUST_BE_RELOADED
            self._camera_description = self.sdk.get_camera_description()
