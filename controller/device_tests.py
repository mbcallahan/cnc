import string
import time
import numpy as np

from . import test
from . import signal
from .exceptions import PlaybackDeviceException
from .utils import parse_rate, parse_duration, parse_percent, binary_search

from .basic_playback import BasicPlayback
from .response_time import ResponseTimeTest
from .clock_rate import ClockRateTest
from .duty_cycle import DutyCycleTest
from .max_drift import MaxDriftTest
from .max_glitch import MaxGlitchDuration
from .max_num_glitch import MaxNumGlitchTest
from .button_pulse import ButtonPulseWidthTest
from .single_inst_glitch import SingleInstructionGlitch
from .serial_fuzzer import SerialFuzzer
from .can_bus import CanBusDeviceTest
from .serial_test import SerialTest
from .pic_single_inst import PICSingleInstructionGlitch
from .clock_glitch import ClockGlitchDev


tests = [
    BasicPlayback, 
    ClockRateTest, 
    MaxGlitchDuration, 
    ResponseTimeTest, 
    MaxNumGlitchTest, 
    MaxDriftTest, 
    CanBusDeviceTest,
    ButtonPulseWidthTest, 
    PICSingleInstructionGlitch,
    SerialFuzzer, 
    SerialTest,
    ClockGlitchDev
    ]
