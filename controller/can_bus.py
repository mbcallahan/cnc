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
        my_data = "0011001100"#"1111110110001100010000010100010101101111111"
        serialout.signal = signal.CANSignal(data='0', baud_rate=125000, duration=0.01)
        for c in my_data:
            #serialout.signal = signal.CANSignal(data=c, baud_rate=125000, duration=0.01)
            serialout.signal.append_char(c)
        self.send_inputs(inputs, outputs)
        self.behavior_model.validate(inputs, outputs)
        #self.environment.plot(['inputs'])
        #self.environment.plot(['outputs'])

        print("Done")

        # self.send_inputs(inputs, outputs)

        # print('Analyzing...')
        # if self.behavior_model is not None:
        #     if self.behavior_model.validate(inputs, outputs):
        #         print('Device behavior validated!')
        #         print(outputs)

        #     else:
        #         print('Device behavior did not validate.')