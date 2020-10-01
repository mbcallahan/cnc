from . import test
from . import signal
from .exceptions import PlaybackDeviceException

class ClockGlitchDev(test.DeviceTest):
    test_name = 'Clock Glitching Development'

    parameters = [
        #TestParameter('Duration', ('s', 'cycles'), float)
    ]

    relevant_inputs = [
        test.TestIOMapping('Reset'),
        test.TestIOMapping('Manual Clock'),
        test.TestIOMapping('Clock') #Kept clock on 3 to line up with PIC test
    ]

    relevant_outputs = [
    ]

    def run(self, inputs, outputs):
        #Reminder: these are the zybo pins
        reset = self.relevant_input_values[0]
        manual_clock = self.relevant_input_values[1]
        clock = self.relevant_input_values[2]

        clock_rate = 50000
        #Give a signal so this ends
        reset.signal = signal.Signal(initial_value=signal.LOW, sample_rate=2*clock_rate, duration=16/clock_rate)
        reset.signal = reset.signal.append(signal.Signal(initial_value=signal.HIGH, sample_rate=2*clock_rate, duration=16/clock_rate))

        glitch_size=0.25/clock_rate
        #glitch_size=0.0050/
        glitch_start=10.0

        #Manually generate a clock        
        manual_clock.signal = signal.Signal(initial_value=signal.LOW, duration=0.5/clock_rate, sample_rate=4*clock_rate)
        for i in range(280):
            if i % 2 == 0:
                signal_value = signal.HIGH
            else:
                signal_value = signal.LOW

            if i == glitch_start:
                #Insert glitch
                duration=glitch_size
            else:
                duration=0.5/clock_rate
            manual_clock.signal = manual_clock.signal.append(signal.Signal(initial_value=signal_value, sample_rate=4*clock_rate, duration=duration))

        print("Trying a glitch of %g at %g "%(glitch_size,glitch_start))
        clock.signal = signal.Clock(clock_rate)
        clock.signal = clock.signal \
            .unroll(140) \
            .glitch(glitch_start/clock_rate, glitch_size)\

        #self.environment.plot(['inputs'])

        self.send_inputs(inputs, outputs)

        #self.environment.plot(['outputs'])