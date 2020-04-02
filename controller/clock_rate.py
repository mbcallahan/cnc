# The clock rate test takes a range of frequencies, and uses binary search to
#   determine how much flexibility there is in the different clock speeds that
#   can be used. The test assumes that frequencies will behave consistently when
#   in the valid clock range, and there is some threshold that, once crossed,
#   will result in behavior that does not reflect that outlined in the behavioral
#   model. The configurable inputs are the range of of input frequencies and the
#   number of iterations the test will run.

from . import test
from . import signal
from .exceptions import PlaybackDeviceException
from .utils import parse_rate

class ClockRateTest(test.DeviceTest):
    test_name = 'Clock Rate'

    parameters = [
        test.TestParameter('Minimum Frequency', ('Hz', 'kHz', 'MHz'), parse_rate),
        test.TestParameter('Maximum Frequency', ('Hz', 'kHz', 'MHz'), parse_rate),
        # TestParameter('Precision', ('Hz', '%'), float),
    ]

    relevant_inputs = [
        test.TestIOMapping('Reset', optional=True),
        test.TestIOMapping('Clock')
    ]

    def run(self, inputs, outputs, numRuns=10):
        freq_min = self.parameter_values[0]
        freq_max = self.parameter_values[1]

        #Input integrity validation
        if freq_min < 0:
            print("Invalid minimum frequency value.")
            return
        if freq_max < 0:
            print("Invalid maximum frequency value.")
            return
        if freq_min > freq_max:
            print("Maximum frequency value less than minimum frequency value.")
            return
        if numRuns <= 0:
            print("Number of iterations too low.")
            return

        # Initialization
        reset = self.relevant_input_values[0]
        clock = self.relevant_input_values[1]

        if reset.signal is None:
            reset.signal = signal.Pulse(signal.LOW, 0.100, 0.100, 1.0)

        freq = (freq_min + freq_max)/2.0
        minBounds = [-1, -1]
        maxBounds = [-1, -1]
        print("Checking the overall frequency range of [{},{}]".format(freq_min,freq_max))

        #Consider preliminary check for freq_min/freq_max

        #Check if middle is valid, otherwise find an valid start freq
        clock.signal = signal.Clock(freq, duty_cycle=clock.signal.duty_cycle)
        self.send_inputs(inputs, outputs)
        if self.behavior_model.validate(inputs, outputs):
            minBounds = [freq_min, freq]
            maxBounds = [freq, freq_max]
            print("Found starting frequency value of {}".format(freq))
        else:
            found = False
            iters = 2
            
            # With no information on the signal, we must use depth first search
            # in attempts to find a valid start location.
            for i in range(numRuns):
                if found:
                    break
                else:
                    scale = (freq_max - freq_min)/(iters + 1)
                    for j in range(1,iters+1,1):
                        freq = freq_min + j*scale
                        clock.signal = signal.Clock(freq, duty_cycle=clock.signal.duty_cycle)
                        self.send_inputs(inputs, outputs)
                        if self.behavior_model.validate(inputs, outputs):
                            minBounds = [freq_min, freq]
                            maxBounds = [freq, freq_max]
                            print("Found starting frequency value of {}".format(freq))
                            
                            found = True    #Need to break 2 loops
                            break
                iters *= 2
        
        if minBounds[0] == -1:
            print("Unable to find a valid start frequency. Possible reasons:\n1.) Given region too large or number of iterations too low.\n2.) No valid freqencies inside given region.")
        
        # Expand acceptable clock frequency range with binary search
        for i in range(numRuns):
            # Expanding towards rising clock edge
            freq1 = (minBounds[0] + minBounds[1])/2.0
            clock.signal = signal.Clock(freq1, duty_cycle=clock.signal.duty_cycle)
            self.send_inputs(inputs, outputs)
            if self.behavior_model.validate(inputs, outputs):
                minBounds[1] = freq1
            else:
                minBounds[0] = freq1
            
            # Expanding toward falling clock edge
            freq2 = (maxBounds[0] + maxBounds[1])/2.0
            print("Checking MIN value of {} Checking MAX value of {}".format(freq1,freq2))
            clock.signal = signal.Clock(freq2, duty_cycle=clock.signal.duty_cycle)
            self.send_inputs(inputs, outputs)
            if self.behavior_model.validate(inputs, outputs):
                maxBounds[0] = freq2
            else:
                maxBounds[1] = freq2
        
        print("After {} iterations, the acceptable consistent clock range is [{}, {}]. The entire acceptable range is encompassed within the range of [{} {}]".format(numRuns, minBounds[1], maxBounds[0],minBounds[0],maxBounds[1]))
        if minBounds[0] == freq_min:
            print("NOTE: the minimum clock speed may be less than {}".format(freq_min))
        if maxBounds[1] == freq_max:
            print("NOTE: the maximum clock speed may be greater than {}".format(freq_max))

        # TODO: return result dict (see ButtonPulseWidthTest... used in TestEnviornment.run for multi-iteration runs)