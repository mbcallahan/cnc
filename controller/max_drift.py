from . import test
from . import signal
from .exceptions import PlaybackDeviceException
from .utils import parse_duration

class MaxDriftTest(test.DeviceTest):
    test_name = 'Max Drift Test'
    
    relevant_inputs = [
        test.TestIOMapping('Signal 1'),
        test.TestIOMapping('Signal 2'),
        test.TestIOMapping('Reset', optional=True)
    ]

    parameters = [
        test.TestParameter('Max delay on Signal 1', ('s', 'ms', 'us'), parse_duration),
        test.TestParameter('Max delay on Signal 2', ('s', 'ms', 'us'), parse_duration),
    ]

    def run(self, inputs, outputs, numRuns=10):
        pos_delay_max = self.parameter_values[0]
        neg_delay_max = self.parameter_values[1]

        if(pos_delay_max < 0):
            print("Invalid positive delay, please enter a positive number in seconds")
        if(neg_delay_max < 0):
            print("Invalid negative delay, please enter a positive number in seconds")


        # Parameter Validation Check
        og_signals = [self.relevant_input_values[0].signal.clone(), self.relevant_input_values[1].signal.clone()]

        self.send_inputs(inputs, outputs)
        if not self.behavior_model.validate(inputs, outputs):
            print("Unable to validate signals before attempting to drift")
            return

        
        pos_bounds = [0, pos_delay_max]
        neg_bounds = [0, neg_delay_max]

        for i in range(numRuns):
            
            delay_pos = (pos_bounds[0] + pos_bounds[1])/2.0

            s_pos = og_signals[1].insert_delay(delay_pos)
            self.relevant_input_values[0].signal = og_signals[0]
            self.relevant_input_values[1].signal = s_pos

            self.send_inputs(inputs,outputs)
            if self.behavior_model.validate(inputs, outputs):
                pos_bounds[0] = delay_pos
            else:
                pos_bounds[1] = delay_pos

            delay_neg = (neg_bounds[0] + neg_bounds[1])/2.0
            print("Checking POS value of {} Checking NEG value of {}".format(delay_pos,delay_neg))
            s_neg = og_signals[0].insert_delay(delay_neg)
            self.relevant_input_values[0].signal = s_neg
            self.relevant_input_values[1].signal = og_signals[1]

            self.send_inputs(inputs,outputs)
            if self.behavior_model.validate(inputs, outputs):
                neg_bounds[0] = delay_neg
            else:
                neg_bounds[1] = delay_neg

        if pos_bounds[0] == 0 and neg_bounds[0] == 0:
            print("Unable to find any drift values with valid signals. Possible reasons:\n1.) Given region too large or number of iterations too low.\n2.) System too precise to allow drift.")
        else: 
            print("After {} iterations, the range of acceptable delay allowed on signal 2 is [-{}, {}]. The total acceptable range is encompassed in [-{}, {}]".format(numRuns, neg_bounds[0], pos_bounds[0],neg_bounds[1],pos_bounds[1]))
            if neg_bounds[0] == neg_delay_max:
                print("NOTE: the negative drift may be greater than -{}".format(delay_neg))
            if pos_bounds[0] == pos_delay_max:
                print("NOTE: the positive drift may be greater than {}".format(delay_pos))

        # TODO: return result dict (see ButtonPulseWidthTest... used in TestEnviornment.run for multi-iteration runs)
