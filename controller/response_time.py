from . import test
from . import signal
from .exceptions import PlaybackDeviceException

class ResponseTimeTest(test.DeviceTest):
    test_name = 'Response Time'

    relevant_inputs = [
        test.TestIOMapping('Input trigger')
        
    ]
    relvant_outputs = [
        test.TestIOMapping('Output trigger')
    ]

    def run(self, inputs, outputs):
        i = self.relevant_input_values[0]
        o = self.relevant_output_values[0]

        self.send_inputs(inputs, outputs)

        input_groups = i.signal.find_groups(False, 8)
        output_groups = o.signal.find_groups(False, 8)

        response_start_time = output_groups[0][0]

        for input_group in input_groups[::-1]:
            if input_group[1] < response_start_time:
                break

        return response_start_time - input_group[1]