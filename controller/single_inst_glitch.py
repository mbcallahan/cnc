from . import test
from . import signal
from .exceptions import PlaybackDeviceException

class SingleInstructionGlitch(test.DeviceTest):
    test_name = 'Single Instruction Glitch'

    parameters = [
        #TestParameter('Duration', ('s', 'cycles'), float)
    ]

    relevant_inputs = [
        test.TestIOMapping('Reset'),
        test.TestIOMapping('Clock')
    ]

    def run(self, inputs, outputs):
        reset = self.relevant_input_values[0]
        clock = self.relevant_input_values[1]

        clock_rate = 1000000

        reset.signal = signal.Signal(initial_value=signal.LOW, sample_rate=2*clock_rate, duration=3/clock_rate)
        reset.signal = reset.signal.append(signal.Signal(initial_value=signal.HIGH, sample_rate=2*clock_rate, duration=13/clock_rate))

        clock.signal = signal.Clock(clock_rate)\
            .unroll(30)\
            .glitch(24.04 / clock_rate, 0.02 / clock_rate, resample=50)\
            .glitch(25.04 / clock_rate, 0.02 / clock_rate)\
            .glitch(26.04 / clock_rate, 0.02 / clock_rate)\
            .glitch(27.04 / clock_rate, 0.02 / clock_rate)

        #self.environment.plot('inputs')

        self.send_inputs(inputs, outputs)

        t1 = next(outputs[0].signal.edges('rising'))        # End of reset
        t2 = list(outputs[2].signal.edges('rising'))[-1]    # BSF complete
        

        t1b = t1 + 23 /clock_rate
        t3 = t2 + (t2 - t1b) / 4

        self.environment.plot(['outputs', str(t1b), str(t3)])
        print('Clock period count:', (t2 - t1) * clock_rate)