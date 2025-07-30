import time
import click
import math
import warnings
import pydicom

from pydicom.uid import (
    ExplicitVRLittleEndian, ImplicitVRLittleEndian, ExplicitVRBigEndian
)

warnings.filterwarnings("ignore", message="Invalid value for VR UI:", category=UserWarning)


def current_time_in_milliseconds() -> int:
    return int(round(time.time() * 1000))


def current_time_in_seconds() -> int:
    return int(round(current_time_in_milliseconds() / 1000.0))


def elapsed_time_in_milliseconds(start_time_in_milliseconds: int) -> int:
    return current_time_in_milliseconds() - start_time_in_milliseconds


def elapsed_time_in_seconds(start_time_in_seconds: int) -> int:
    return current_time_in_seconds() - start_time_in_seconds


def duration(seconds: int) -> str:
    h = int(math.floor(seconds/3600.0))
    remainder = seconds - h * 3600
    m = int(math.floor(remainder/60.0))
    remainder = remainder - m * 60
    s = int(math.floor(remainder))
    return '{} hours, {} minutes, {} seconds'.format(h, m, s)


def input_dict_from_input(input):
    input_dict = {}
    for item in input:
        if '=' not in item:
            raise click.BadParameter('Inputs must be in the format "name=path"')
        name, path = item.split('=', 1)
        input_dict[name] = path
    return input_dict


def param_dict_from_params(params):
    param_dict = {}
    for item in params:
        if '=' not in item:
            raise click.BadParameter('Parameters must be in the format "name=value"')
        name, value = item.split('=', 1)
        param_dict[name] = value
    return param_dict


def is_dicom(f):
    try:
        pydicom.dcmread(f, stop_before_pixels=True)
        return True
    except pydicom.errors.InvalidDicomError:
        return False
    

def load_dicom(f, stop_before_pixels=False):
    if is_dicom(f):
        return pydicom.dcmread(f, stop_before_pixels=stop_before_pixels)
    return None


def is_jpeg2000_compressed(p):
    return p.file_meta.TransferSyntaxUID not in [ExplicitVRLittleEndian, ImplicitVRLittleEndian, ExplicitVRBigEndian]