from . import test
from . import signal
from .exceptions import PlaybackDeviceException
#Test to see what timing parameters the reset of the pic has

class PICReset(test.DeviceTest):
    test_name = 'PIC Reset Test'

    parameters = [
        #TestParameter('Duration', ('s', 'cycles'), float)
    ]

    relevant_inputs = [
        test.TestIOMapping('Reset'),
       # test.TestIOMapping('Button'),
        test.TestIOMapping('Clock')
    ]

    relevant_outputs = [
    ]

    def run(self, inputs, outputs):
        #Reminder: these are the zybo pins
        reset = self.relevant_input_values[0]
        #button = self.relevant_input_values[1]
        clock = self.relevant_input_values[1]

        clock_rate = 4000000
        #clock_rate = 50000
        print("start reset")
        #run reset signal
        reset.signal = signal.Signal(initial_value=signal.LOW, sample_rate=2*clock_rate, duration=16/clock_rate)
        reset.signal = reset.signal.append(signal.Signal(initial_value=signal.HIGH, sample_rate=2*clock_rate, duration=16/clock_rate))


      
        #Empirically measured that we should glitch at 20 cycles after the
        #button press
        #glitch_location=button_high+(20/clock_rate)
        #glitch_location_samples = int(glitch_location*clock.signal.sample_rate)
        #print('glitch_location (seconds): ', glitch_location)
        #print('glitch_location (samples): ', glitch_location_samples)

        sample_rate=40*clock_rate
        #glitch_start = 82.71
        #glitch_start = 84.00

        #for glitch_start in range(165,170):
        

            #Manually generate a clock        
        clock.signal = signal.Signal(initial_value=signal.LOW, duration=0.5/clock_rate, sample_rate=sample_rate)
        
        
        for i in range(50):
            if i % 2 == 0:
                signal_value = signal.HIGH
            else:
                signal_value = signal.LOW

            #add the up or down step 
            clock.signal = clock.signal.append(signal.Signal(initial_value=signal_value, sample_rate=sample_rate, duration=4/clock_rate))

            #self.environment.plot(['inputs'])
        self.send_inputs(inputs, outputs)

        if not self.behavior_model.validate(inputs, outputs):
                    print("---")
                    print("Behavior model not validated")
                    print("glitch_start: ", glitch_start)
                    print("glitch_size: ", glitch_size)
                    print("---")


                    print("---")
