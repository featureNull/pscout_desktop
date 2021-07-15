'''
Ids Usb 2 Kamera
'''
from camview.camera_abc import AbstractCam, Resolution
from pyueye import ueye
import numpy as np
import cv2
import time

bits_per_pixel = ueye.INT(32)


class _IdsException(Exception):
    pass


class IdsCam(AbstractCam):
    def __init__(self):
        self.hcam = ueye.HIDS(0)
        self.membuf = ueye.c_mem_p()
        self.memid = ueye.int()
        self.pitch = -1
        self.framerate = -1
        self.imgwidth = None
        self.imgheight = None

    def open(self, res: Resolution, framerate):
        ueye_init_camera(self.hcam, None)

        # check handleable cams
        if not ueye_get_camera_info(self.hcam).Type & ueye.IS_INTERFACE_TYPE_USB:
            raise _IdsException('only Usb Cameras are supported')
        if ueye_get_sensor_info(self.hcam).SensorID != ueye.IS_SENSOR_XS:
            raise _IdsException('only IS_SENSOR_XS Camera is supported')

        # set image format and frame rate
        # image_formats = ueye_get_image_formats(self.hcam)
        ueye_set_image_format(self.hcam, formatid=4)
        ueye_set_frame_rate(self.hcam, framerate)
        self.framerate = framerate

        # get image aoi and alloc and init buffers
        aoi = ueye_get_aoi(self.hcam)
        ueye_alloc_image_mem(self.hcam, aoi.s32Width, aoi.s32Height, self.membuf, self.memid)
        ueye_set_image_mem(self.hcam, self.membuf, self.memid)
        ueye_set_color_mode(self.hcam, ueye.IS_CM_BGRA8_PACKED)

        # start and weiss nicht was das tut
        ueye_capture_video(self.hcam, ueye.IS_DONT_WAIT)
        self.pitch = ueye_inquire_image_mem(self.hcam, self.membuf, self.memid,
            aoi.s32Width, aoi.s32Height)
        self.imgwidth = aoi.s32Width.value
        self.imgheight = aoi.s32Height.value

    def close(self):
        # let grab throw
        self.pitch = -1
        # wait at least one frame
        time.sleep(500)
        ueye_free_image_mem(self.hcam, self.membuf, self.memid)
        ueye_exit_camera(self.hcam)

    def pause(self):
        ueye_stop_live_video(self.hcam)

    def resume(self):
        ueye_capture_video(self.hcam, ueye.IS_DONT_WAIT)

    def grab(self):
        time.sleep(1 / self.framerate)
        array = ueye.get_data(self.membuf,
                              self.imgwidth,
                              self.imgheight,
                              bits_per_pixel,
                              self.pitch, copy=False)
        bytes_per_pixel = int(bits_per_pixel / 8)
        frame = np.reshape(array, (self.imgheight, self.imgwidth, bytes_per_pixel))
        # this is bgra so convert it in qt compatible rgb
        b, g, r, a = cv2.split(frame)
        rgbframe = cv2.merge((r, g, b))
        return rgbframe


def ueye_init_camera(hcam, weissnicht):
    err = ueye.is_InitCamera(hcam, weissnicht)
    _throw_if_err(hcam, err)


def ueye_get_camera_info(hcam):
    caminfo = ueye.CAMINFO()
    err = ueye.is_GetCameraInfo(hcam, caminfo)
    _throw_if_err(hcam, err)
    return caminfo


def ueye_get_sensor_info(hcam) -> ueye.SENSORINFO:
    sensor_info = ueye.SENSORINFO()
    err = ueye.is_GetSensorInfo(hcam, sensor_info)
    _throw_if_err(hcam, err)
    return sensor_info


def ueye_get_image_formats(hcam):
    fcnt = ueye.UINT()
    cmd = ueye.IMGFRMT_CMD_GET_NUM_ENTRIES
    err = ueye.is_ImageFormat(hcam, cmd, fcnt, ueye.sizeof(fcnt))
    _throw_if_err(hcam, err)

    fl = ueye.IMAGE_FORMAT_LIST((ueye.IMAGE_FORMAT_INFO * fcnt))
    fl.nSizeOfListEntry = ueye.sizeof(ueye.IMAGE_FORMAT_INFO)
    fl.nNumListElements = fcnt
    cmd = ueye.IMGFRMT_CMD_GET_LIST
    err = ueye.is_ImageFormat(hcam, cmd, fl, ueye.sizeof(fl))
    # aufschluesseln auf human readable
    fl2 = {fi.nFormatID.value: fi for fi in fl.FormatInfo}
    ret = {}
    for k, v in sorted(fl2.items()):
        ret[k] = v.strFormatName.decode("utf-8")
    return ret


def ueye_set_image_format(hcam, formatid) -> None:
    fid = ueye.int(formatid)
    cmd = ueye.IMGFRMT_CMD_SET_FORMAT
    err = ueye.is_ImageFormat(hcam, cmd, fid, ueye.sizeof(fid))
    _throw_if_err(hcam, err)


def ueye_set_frame_rate(hcam, framerate) -> None:
    frr = ueye.double(framerate)
    dummy = ueye.double(0)
    err = ueye.is_SetFrameRate(hcam, frr, dummy)
    _throw_if_err(hcam, err)


def ueye_get_aoi(hcam) -> ueye.IS_RECT:
    aoi = ueye.IS_RECT()
    cmd = ueye.IS_AOI_IMAGE_GET_AOI
    err = ueye.is_AOI(hcam, cmd, aoi, ueye.sizeof(aoi))
    _throw_if_err(hcam, err)
    return aoi


def ueye_alloc_image_mem(hcam, width, height, membuf, memid):
    f = ueye.is_AllocImageMem
    err = f(hcam, width, height, bits_per_pixel, membuf, memid)
    _throw_if_err(hcam, err)


def ueye_set_image_mem(hcam, membuf, memid):
    err = ueye.is_SetImageMem(hcam, membuf, memid)
    _throw_if_err(hcam, err)


def ueye_set_color_mode(hcam, mode):
    err = ueye.is_SetColorMode(hcam, mode)
    _throw_if_err(hcam, err)


def ueye_capture_video(hcam, mode):
    err = ueye.is_CaptureVideo(hcam, mode)
    _throw_if_err(hcam, err)


def ueye_stop_live_video(hcam):
    err = ueye.is_StopLiveVideo(hcam, ueye.IS_WAIT)
    _throw_if_err(hcam, err)


def ueye_inquire_image_mem(hcam, membuf, memid, width, height) -> int:
    pitch = ueye.INT()
    f = ueye.is_InquireImageMem
    err = f(hcam, membuf, memid, width, height, bits_per_pixel, pitch)
    _throw_if_err(hcam, err)
    return pitch


def ueye_free_image_mem(hcam, membuf, memid) -> None:
    ueye.is_FreeImageMem(hcam, membuf, memid)


def ueye_exit_camera(hcam) -> None:
    ueye.is_ExitCamera(hcam)


def _throw_if_err(hcam, err):
    if err != ueye.IS_SUCCESS:
        ueye_err = ueye.int(err)
        txt = ueye.c_char_p()
        ret = ueye.is_GetError(hcam, ueye_err, txt)
        msg = str(txt.value) if ret == ueye.IS_SUCCESS else 'camera not availible'
        raise _IdsException(msg)
