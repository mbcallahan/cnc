from . import test
from . import signal
from .exceptions import PlaybackDeviceException
from .utils import parse_duration

class ButtonPulseWidthTest(test.DeviceTest):
    test_name = 'Button Pulse Width'

    parameters = [
        test.TestParameter('Minimum Pulse', ('s', 'ms', 'us'), parse_duration),
        test.TestParameter('Maximum Pulse', ('s', 'ms', 'us'), parse_duration),
    ]

    relevant_inputs = [
        test.TestIOMapping('Reset'),
        test.TestIOMapping('Button')
    ]

    def run(self, inputs, outputs, precision=10e-6, duration=0.30, setup_time=0.06):  # old prevision = 40e-9

        pulses = []
    
        #number of iterations
        iters = 70
        #iters = 30
        for i in range(iters):
            pulse_min = self.parameter_values[0]
            pulse_max = self.parameter_values[1]

            #precision = 40e-9

            # Initialization
            reset = self.relevant_input_values[0]
            button = self.relevant_input_values[1]
            val = (pulse_min + pulse_max) / 2
            search_size = val
            found_end = False

            pulse_bad_max = pulse_min  # Biggest value that didn't work
            pulse_good_min = pulse_max # Smallest vlaue that worked
            err_bad = 0
            err_good = 0

            # Find min pulse width
            while 1:
                search_size = search_size / 2
                # We can of course only send integer samples, and we must also send an integer as a sample rate. This means there will be some error
                # in the duration of the pulse we produce, due to limited precision in the sample rate on one side,
                # and in limited precision of sampling on the other. 
                # So we must ensure our error is less than our desired precision
                sr = 1/val
                while 1:
                    pulse_sample_count = round(round(sr) * val)
                    real_val = (pulse_sample_count / round(sr))
                    err = abs(val - real_val)
                    total_sample_count = round(round(sr) * duration)

                    if err < precision and sr > 1000:
                        break
                    
                    if total_sample_count > 2**15:
                        # Can't get any better precision
                        break

                    sr = sr * 2

                print("In iteration %d of %d"%(i, iters)) 
                print('Requested pulse duration: {:02f} s'.format(val))
                print('Real pulse duration: {:02f} s'.format(real_val))
                print('Sample count total:', total_sample_count)
                print('Sample count used for pulse:', pulse_sample_count)
                print('Sample rate:', round(sr))

                button.signal = signal.Pulse(signal.LOW, setup_time, val, duration - setup_time - val, sample_rate=sr)
                self.send_inputs(inputs, outputs)

                if self.behavior_model.validate(inputs, outputs):
                    if val < pulse_good_min:
                        pulse_good_min = real_val

                    val -= search_size
                else:
                    if val > pulse_bad_max:
                        pulse_bad_max = real_val

                    found_end = True
                    val += search_size

                #TODO: remove
                #self.environment.plot(['all'])

                if search_size * 2 < precision:
                    break

                if found_end:
                    pulse_min = val

            print('Minimum pulse duration in range:', pulse_bad_max, pulse_good_min)
            pulses.append(pulse_good_min)

        print(pulses)
        return {
            'invalid_pulse_max': pulse_bad_max,
            'valid_pulse_min': pulse_good_min
        }