# The duty cycle test takes a range of duty cycles, and uses binary search to
#   determine how much flexibility there is in the different duty cycles that
#   can be used. The test assumes that duty cycles will behave consistently when
#   in the valid range, and there is some threshold that, once crossed,
#   will result in behavior that does not reflect that outlined in the behavioral
#   model. The configurable inputs are the range of of input duty cycles and the
#   number of iterations the test will run.

from . import test
from . import signal
from .exceptions import PlaybackDeviceException
from .utils import parse_percent

class DutyCycleTest(test.DeviceTest):
    test_name = 'Duty Cycle Test'

    parameters = [
        test.TestParameter('Minimum Duty Cycle', ('%'), parse_percent),
        test.TestParameter('Maximum Duty Cycle', ('%'), parse_percent),
    ]

    relevant_inputs = [
        test.TestIOMapping('Reset', optional=True),
        test.TestIOMapping('Clock')
    ]

    def run(self, inputs, outputs, numRuns=10):
        duty_min = self.parameter_values[0]
        duty_max = self.parameter_values[1]

        #Input integrity validation    
        if duty_min < 0:
            print("Invalid minimum duty cycle value.")
            return
        if duty_max < 0:
            print("Invalid maximum duty cycle value.")
            return
        if duty_max > 100:
            print("Duty cycle value too high. Please use a duty cycle of 0.0 - 100.0")
            return
        if duty_min > duty_max:
            print("Maximum duty cycle value less than minimum duty cycle value.")
            return
        if numRuns <= 0:
            print("Number of iterations too low.")
            return

        # Initialization
        reset = self.relevant_input_values[0]
        clock = self.relevant_input_values[1]
        if reset.signal is None:
            reset.signal = signal.Pulse(signal.LOW, 0.100, 0.100, 1.0)

        duty = (duty_min + duty_max)/2.0
        minBounds = [-1, -1]
        maxBounds = [-1, -1]

        #Check if middle is valid, otherwise find an valid start duty cycle
        clock.signal = signal.Clock(clock.signal.clock_rate, duty_cycle=duty, sample_rate=clock.signal.sample_rate)
        self.send_inputs(inputs, outputs)
        if self.behavior_model.validate(inputs, outputs):
            minBounds = [duty_min, duty]
            maxBounds = [duty, duty_max]
            print("Found starting duty cycle value of {}".format(duty))
        else:
            found = False
            iters = 2
            for i in range(numRuns):
                if found:
                    break
                else:
                    scale = (duty_max - duty_min)/(iters + 1)
                    for j in range(1,iters+1,1):
                        duty = duty_min + j*scale
                        clock.signal = signal.Clock(clock.signal.clock_rate, duty_cycle=duty, sample_rate=clock.signal.sample_rate)
                        self.send_inputs(inputs, outputs)
                        if self.behavior_model.validate(inputs, outputs):
                            minBounds = [duty_min, duty]
                            maxBounds = [duty, duty_max]
                            print("Found starting duty cycle value of {}".format(duty))
                            found = True
                            break
                iters *= 2
        
        if minBounds[0] == -1:
            print("Unable to find a valid start duty cycle. Possible reasons:\n1.) Given region too large or number of iterations too low.\n2.) No valid duty cycles inside given region.")
        
        # Expand acceptable duty cycle range with binary search
        for i in range(numRuns):
            duty1 = (minBounds[0] + minBounds[1])/2.0
            clock.signal = signal.Clock(clock.signal.clock_rate, duty_cycle=duty1, sample_rate=clock.signal.sample_rate)
            self.send_inputs(inputs, outputs)
            if self.behavior_model.validate(inputs, outputs):
                minBounds[1] = duty1
            else:
                minBounds[0] = duty1
            
            duty2 = (maxBounds[0] + maxBounds[1])/2.0
            print("Checking MIN value of {} Checking MAX value of {}".format(duty1,duty2))
            clock.signal = signal.Clock(clock.signal.clock_rate, duty_cycle=duty2, sample_rate=clock.signal.sample_rate)
            self.send_inputs(inputs, outputs)
            if self.behavior_model.validate(inputs, outputs):
                maxBounds[0] = duty2
            else:
                maxBounds[1] = duty2
        print("After {} iterations, the acceptable consistent duty cycle range is [{}, {}]. The entire acceptable range is encompassed within the range of [{} {}]".format(numRuns, minBounds[1], maxBounds[0],minBounds[0],maxBounds[1]))
        if minBounds[0] == duty_min and duty_min != 0:
            print("NOTE: the minimum duty cycle may be less than {}".format(duty_min))
        if maxBounds[1] == duty_max and duty_max != 100:
            print("NOTE: the maximum duty cycle may be greater than {}".format(duty_max))

        # TODO: return result dict (see ButtonPulseWidthTest... used in TestEnviornment.run for multi-iteration runs)