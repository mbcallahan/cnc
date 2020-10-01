from . import test
from . import signal
from .exceptions import PlaybackDeviceException

class MaxGlitchDuration(test.DeviceTest):
    test_name = 'Max Glitch Duration'

    parameters = [
        test.TestParameter('Duration', ('s', 'cycles'), float)
    ]

    relevant_inputs = [
        test.TestIOMapping('Reset', optional=True),
        test.TestIOMapping('Clock')
    ]

    def run(self, inputs, outputs, glitch_loc=50,numRuns=10, scaled=False):
        clock = self.relevant_input_values[0]
        reset = self.relevant_input_values[1]

        if reset.signal is None:
            reset.signal = signal.Pulse(signal.LOW, 0.100, 0.100, 1.0)

        if glitch_loc > 100 or glitch_loc < 0:
            print("Invalid location, input a percentage value in the range of 0 to 100")
            return

        if numRuns <= 0:
            print("Number of iterations too low.")
            return

        if glitch_loc > 50:
            max_spread = 100 - glitch_loc
        else:
            max_spread = glitch_loc

        clock.signal = signal.Clock(freq, duty_cycle=clock.signal.duty_cycle)

        self.send_inputs(inputs, outputs)
        if not self.behavior_model.validate(inputs, outputs):
            print("Initial signal not valid.\n")
            return

        scale = 0.5*clock.signal.period*0.01
        lowBound = [glitch_loc, 0] # PERIOD CALC===================
        highBound = [glitch_loc, 100] # PERIOD CALC===================
        spreadBound = [0, max_spread] # PERIOD CALC===================

        for i in range(numRuns):

            # Step 1: Expand towards rising edge

            # Rebuild the clock without glitches
            clock.signal = signal.Clock(clock_rate=clock.signal.clock_rate,duration=clock.signal.duration)

            glitch_size_1 = (lowBound[0] + lowBound[1])/2.0 
            #TODO: GENERATE SIGNAL THAT IS LOW FROM (glitchloc - glitch_size_1, glitch_loc) MAYBE SCALE DOWN BY 0.5 TO ACCOUNT FOR PERIOD
            self.send_inputs(inputs, outputs)
            if self.behavior_model.validate(inputs, outputs):
                lowBound[0] = glitch_size_1
            else:
                lowBound[1] = glitch_size_1

    
            # Step 2: Expand towards negative edge

            # Rebuild the clock without glitches
            clock.signal = signal.Clock(clock_rate=clock.signal.clock_rate,duration=clock.signal.duration)
            glitch_size_2 = (highBound[0] + highBound[1])/2.0
            #TODO: GENERATE SIGNAL THAT IS LOW FROM (glitchloc, glitch_loc + glitch_size_2)
            self.send_inputs(inputs, outputs)
            if self.behavior_model.validate(inputs, outputs):
                highBound[0] = glitch_size_2
            else:
                highBound[1] = glitch_size_2

            # Step 3: Expand outward in both directions

            # Rebuild the clock without glitches
            clock.signal = signal.Clock(clock_rate=clock.signal.clock_rate,duration=clock.signal.duration)
            glitch_size_3 = (spreadBound[0] + spreadBound[1])/2.0
            print("Checking LOW value of -{} Checking HIGH value of {} Checking SPREAD value of +/-{}".format(glitch_size_1,glitch_size_2,glitch_size_3))
            #TODO: GENERATE SIGNAL THAT IS LOW FROM (glitchloc - glitch_size_3, glitch_loc + glitch_size_3)
            self.send_inputs(inputs, outputs)
            if self.behavior_model.validate(inputs, outputs):
                highBound[0] = glitch_size_3
            else:
                highBound[1] = glitch_size_3

        print("After {} iterations,".format(numRuns))
        print("A glitch towards the rising edge of the signal extended [{},{}] for a maximum of {} [found to not exceed {}]".format(lowBound[0],glitch_loc,(glitch_loc-lowBound[0]),lowBound[1]))
        print("A glitch towards the falling edge of the signal extended [{},{}] for a maximum of {} [found to not exceed {}]".format(glitch_loc,highBound[0],(highBound[0]-glitch_loc),highBound[1]))
        print("A glitch spreading equally in both directions extended [{},{}] for a maximum of {} [found to not exceed {}]".format((glitch_loc-spreadBound[0]),(glitch_loc+spreadBound[0]),(2*spreadBound[0]),(2*spreadBound[1])))
        if scaled == True:
            print("\nScaled based on a period of {} seconds.\nAfter {} iterations,".format(clock.signal.period,numRuns))
            print("A glitch towards the rising edge of the signal extended [{},{}] for a maximum of {} seconds [found to not exceed {} seconds]".format(lowBound[0]*scale,glitch_loc*scale,(glitch_loc-lowBound[0])*scale,lowBound[1]*scale))
            print("A glitch towards the falling edge of the signal extended [{},{}] for a maximum of {} seconds [found to not exceed {} seconds]".format(glitch_loc*scale,highBound[0]*scale,(highBound[0]-glitch_loc)*scale,highBound[1]*scale))
            print("A glitch spreading equally in both directions extended [{},{}] for a maximum of {} seconds [found to not exceed {} seconds]".format((glitch_loc-spreadBound[0])*scale,(glitch_loc+spreadBound[0])*scale,(2*spreadBound[0])*scale,(2*spreadBound[1])*scale))

        # TODO: return result dict (see ButtonPulseWidthTest... used in TestEnviornment.run for multi-iteration runs)