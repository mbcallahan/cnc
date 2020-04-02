from . import test
from . import signal
from .exceptions import PlaybackDeviceException

class SerialTest(test.DeviceTest):
    test_name = 'Serial Glitching Test'

    parameters = [
    ]

    relevant_inputs = [
        test.TestIOMapping('Serial')
    ]
    relevant_outputs = [
        test.TestIOMapping('SerialLoopback')
    ]

    def run(self, inputs, outputs): 
        serialout = self.relevant_input_values[0]    
        serialloop = self.relevant_output_values[0]
 
        for c in string.digits:
            serialout.signal = signal.RS232Signal(data=c, baud_rate=9600, duration=0.1).resample_factor(10).glitch(15.5/9600, 0.1/9600)

            self.environment.plot(['inputs'])
            self.send_inputs(inputs, outputs)
            self.environment.plot(['outputs'])