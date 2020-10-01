from . import test
from . import signal
from .exceptions import PlaybackDeviceException

class CanBusDeviceTest(test.DeviceTest):
    test_name = 'Can Bus Device'

    relevant_inputs = [
        test.TestIOMapping('CAN Input Loopback')
    ]
    def run(self, inputs, outputs):
        serialout = self.relevant_input_values[0]
        my_data = "01100011000100000101000101011011111010011011111"
        serialout.signal = signal.CANSignal(data=my_data, baud_rate=125000, duration=0.01)
        self.send_inputs(inputs, outputs)
        self.behavior_model.validate(inputs, outputs)
        self.environment.plot(['inputs'])
        self.environment.plot(['outputs'])

        print("Done")