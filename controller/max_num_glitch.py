from . import test
from . import signal
from .exceptions import PlaybackDeviceException

class MaxNumGlitchTest(test.DeviceTest):
    test_name = 'Max Num Glitch Test'

    parameters = [
        test.TestParameter('Duration', ('s', 'cycles'), float)
    ]

    def run(self, inputs, outputs, limit=10):
        clock = self.relevant_input_values[0]
        reset = self.relevant_input_values[1]

        if reset.signal is None:
            reset.signal = signal.Pulse(signal.LOW, 0.100, 0.100, 1.0)

        glitch_locations = [0.125, 0.25, 0.75]
        for loc in glitch_locations:
            # TODO: Binary search of glitch sizes would be way better

            for glitch_size in (0.25/glitch_size_count * i for i in range(1, glitch_size_count)):
                # Rebuild the clock without glitches
                clock.signal = signal.Clock(
                        clock_rate=clock.signal.clock_rate, 
                        duration=clock.signal.duration)

                print('Trying glitch size {} at loc {}'.format(glitch_size, loc))
                for period_index in range(0, round(clock.signal.duration / clock.signal.period)):
                    clock.signal.glitch((loc + period_index) * clock.signal.period, glitch_size)

                clock.signal.plot()

                error_count = 0
                for i in range(3):
                    self.send_inputs(inputs, outputs)

                    if not self.behavior_model.validate(inputs, outputs):
                        error_count += 1

                if error_count == 3:
                    print('Not work')
                    break