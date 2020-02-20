from .utils import display_rate

class SignalException(Exception):
    """General class for Signal-related exceptions"""
    pass

class SignalIncompatibleException(SignalException):
    """Raised when two signals of different sample clock rates attempt to be appended"""
    pass

class ClockException(SignalException):
    """General class for Clock-related exceptions"""
    pass

class ClockTooFast(ClockException):
    """Raised when the clock rate is too fast to represent with the sample rate"""
    def __init__(self, clock_rate, sample_rate):
        super().__init__(
            'Clock is too fast; cannot construct a {} clock sampled at {}'\
                .format(display_rate(clock_rate), display_rate(sample_rate)))

class ClockInvalidDutyCycle(ClockException):
    """Raised when the clock duty cycle is out of range (< 0.0 or > 1.0)"""
    def __init__(self, duty_cycle):
        super().__init__('Duty cycle must be between 0.00 and 1.00, not {}'.format(duty_cycle))

class PlaybackDeviceException(Exception):
    pass

