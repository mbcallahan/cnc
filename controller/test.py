import string
import time
import numpy as np

from . import signal
from .exceptions import PlaybackDeviceException
from .utils import parse_rate, parse_duration, parse_percent, binary_search

class TestParameter:
    def __init__(self, display_name, units, obj_cast=float):
        self.display_name = display_name
        self.units = units
        self.obj_cast = obj_cast

class TestIOMapping:
    def __init__(self, display_name, optional=False):
        self.display_name = display_name
        self.optional = optional

class DeviceTestMeta(type):
    def __str__(self):
        return self.test_name

class DeviceTest(metaclass=DeviceTestMeta):
    test_name = None
    parameters = []
    relevant_inputs = []
    relevant_outputs = []

    def __init__(self, environment):
        self.environment = environment
        self.parameter_values = []
        self.relevant_input_values = []
        self.relevant_output_values = []

    @property
    def behavior_model(self):
        return self.environment.behavior_model

    @property
    def device(self):
        return self.environment.playback_device

    def __str__(self):
        text = '{}\n'.format(self.test_name)

        if len(self.parameters):
            text += '    ' + (', '.join('{}: {}'.format(p.display_name, str(val)) \
                    for p, val in zip(self.parameters, self.parameter_values)))
            text += '\n'

        if len(self.relevant_inputs):
            text += '    ' + (', '.join('{}: {}'.format(ri.display_name, str(val)) \
                    for ri, val in zip(self.relevant_inputs, self.relevant_input_values)))
            text += '\n'

        if len(self.relevant_outputs):
            text += '    ' + (', '.join('{}: {}'.format(ro.display_name, str(val)) \
                    for ro, val in zip(self.relevant_outputs, self.relevant_output_values)))
            text += '\n'
        
        return text

    def run_configure_ui(self):
        self.parameter_values = []
        self.relevant_input_values = []
        self.relevant_output_values = []

        if len(self.parameters):
            print('============================================')
            print('Test parameters:')
            for p in self.parameters:
                text = p.display_name + ' (' + ', '.join(u for u in p.units) + '): '

                while True:
                    try:
                        value = p.obj_cast(input(text))
                        break
                    except ValueError:
                        print('Invalid value, try again')

                self.parameter_values.append(value)
            print()

        if len(self.relevant_inputs) + len(self.relevant_outputs):
            print('============================================')
            print('Identify the signals to be used by the test: (inputs first)')
            for ri in self.relevant_inputs:
                text = ri.display_name + ': '
                while True:
                    value = input(text)

                    # TODO: Don't let the user set inputs as outputs and vice versa
                    io = self.environment.get_io(value)

                    # TODO: We should probably be able to tell the difference between a user wanted to set it to None,
                    # and when a user just gives a invalid input name
                    if ri.optional and io is None:
                        self.relevant_input_values.append(None)
                    elif io is None:
                        print('Invalid IO name, try again')
                    else:
                        self.relevant_input_values.append(io)
                        break

            for ro in self.relevant_outputs:
                text = ro.display_name + ': '
                while True:
                    value = input(text)

                    # TODO: Don't let the user set inputs as outputs and vice versa
                    io = self.environment.get_io(value)

                    # TODO: We should probably be able to tell the difference between a user wanted to set it to None,
                    # and when a user just gives a invalid input name
                    if ro.optional and io is None:
                        self.relevant_output_values.append(None)
                    elif io is None:
                        print('Invalid IO name, try again')
                    else:
                        self.relevant_output_values.append(io)
                        break
            print()

    def send_inputs(self, inputs, outputs):
        print('    Send inputs...')
        signals = [i.signal if i.enabled else None for i in inputs]

        if self.device is None:
            raise PlaybackDeviceException('No playback peripheral connected.')

        self.device.load_signals(signals)

        # TODO: remove duration calcs; device should auto-stop when playback done
        #if all(s.repeat for s in signals):
        #    duration = self.device.MAX_LENGTH / max(s.sample_rate for s in signals)
        #else:
        #    duration = min((s.sample_count / s.sample_rate for s in signals if not s.repeat))

        #print('Recording for duration:', duration)

        # TODO: USE ONLY SUPPORTED SAMPLE RATES
        session = signal.Signal.start_recording(
                sample_rate=self.environment.recording_sample_rate, 
                outputs=[o for o in outputs if o.enabled])

        # TODO: Use device stop capabilities
        # Wait for duration of shortest signal
        print('Playing...')
        self.device.play() 
            
        #time.sleep(duration)
        #self.device.stop()

        signals = session.finish_recording()

        # Save output signals
        i = 0
        for o in outputs:
            if o.enabled:
                o.signal = signals[i]
                i += 1

    def run(self, inputs, outputs):
        pass