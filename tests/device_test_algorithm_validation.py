# File: "device_test_algorithm_validation.py"
# This file is designed to test and demonstrate the validity of the built in 
#   algorithms designed to discover various properties of the signals. We
#   circumvent signal generation and validation by using hard coded values.
#   Instead, we aim to check the soundness of the tests. The lines in this file
#   mirror the lines in "device_tests.py".


# For each test, we comment out signal generation and behavioral validation
# At the end of this script, we call an example of each algorithm

# class ResponseTimeTest(DeviceTest):
#     test_name = 'Response Time'

#     relevant_inputs = [
#         TestIOMapping('Input trigger')
        
#     ]
#     relvant_outputs = [
#         TestIOMapping('Output trigger')
#     ]

#     def run(self, inputs, outputs):
#         i = self.relevant_input_values[0]
#         o = self.relevant_output_values[0]

#         self.send_inputs(inputs, outputs)

#         input_groups = i.signal.find_groups(False, 8)
#         output_groups = o.signal.find_groups(False, 8)

#         response_start_time = output_groups[0][0]

#         for input_group in input_groups[::-1]:
#             if input_group[1] < response_start_time:
#                 break

#         return response_start_time - input_group[1]

# class ClockRateTest(DeviceTest):
#     test_name = 'Clock Rate'

#     parameters = [
#         TestParameter('Minimum Frequency', ('Hz', 'kHz', 'MHz'), parse_rate),
#         TestParameter('Maximum Frequency', ('Hz', 'kHz', 'MHz'), parse_rate),
#         TestParameter('Precision', ('Hz', '%'), float),
#     ]

#     relevant_inputs = [
#         TestIOMapping('Reset', optional=True),
#         TestIOMapping('Clock', required_mode='clock')
#     ]

# def run(self, inputs, outputs, numRuns=10):
def runClockRateTest(freq_min,freq_max,range_min,range_max,numRuns=10):
#     freq_min = self.parameter_values[0]
#     freq_max = self.parameter_values[1]


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
#     reset = self.relevant_input_values[0]
#     clock = self.relevant_input_values[1]

#     if reset.signal is None:
#         reset.signal = signal.Pulse(signal.LOW, 0.100, 0.100, 1.0)

  freq = (freq_min + freq_max)/2.0
  minBounds = [-1, -1]
  maxBounds = [-1, -1]
  print("Checking the overall frequency range of [{},{}]".format(freq_min,freq_max))
    #Consider preliminary check for freq_min/freq_max

    #Check if middle is valid, otherwise find an valid start freq
#     clock.signal = signal.Clock(freq, duty_cycle=clock.signal.duty_cycle)
#     self.send_inputs(inputs, outputs)
#     if self.behavior_model.validate(inputs, outputs):
  if freq >= range_min and freq <= range_max:
    minBounds = [freq_min, freq]
    maxBounds = [freq, freq_max]
    print("Found starting frequency value of {}".format(freq))
  else:
    found = False
    iters = 2
    for i in range(numRuns):
      if found:
        break
      else:
        scale = (freq_max - freq_min)/(iters + 1)
        for j in range(1,iters+1,1):
            freq = freq_min + j*scale
#           clock.signal = signal.Clock(freq, duty_cycle=clock.signal.duty_cycle)
#                     self.send_inputs(inputs, outputs)
#                     if self.behavior_model.validate(inputs, outputs):
            if freq >= range_min and freq <= range_max:
              minBounds = [freq_min, freq]
              maxBounds = [freq, freq_max]
              print("Found starting frequency value of {}".format(freq))
              found = True
              break
      iters *= 2
        
  if minBounds[0] == -1:
    print("Unable to find a valid start frequency. Possible reasons:\n1.) Given region too large or number of iterations too low.\n2.) No valid freqencies inside given region.")
    
    # Expand acceptable clock frequency range with binary search
  for i in range(numRuns):
    freq1 = (minBounds[0] + minBounds[1])/2.0
#         clock.signal = signal.Clock(freq1, duty_cycle=clock.signal.duty_cycle)
#         self.send_inputs(inputs, outputs)
#         if self.behavior_model.validate(inputs, outputs):
    if freq1 >= range_min and freq1 <= range_max:
      minBounds[1] = freq1
    else:
      minBounds[0] = freq1
        
    freq2 = (maxBounds[0] + maxBounds[1])/2.0
    print("Checking MIN value of {} Checking MAX value of {}".format(freq1,freq2))
#         clock.signal = signal.Clock(freq2, duty_cycle=clock.signal.duty_cycle)
#         self.send_inputs(inputs, outputs)
#         if self.behavior_model.validate(inputs, outputs):
    if freq2 >= range_min and freq2 <= range_max:
      maxBounds[0] = freq2
    else:
      maxBounds[1] = freq2
  print("After {} iterations, the acceptable consistent clock range is [{}, {}]. The entire acceptable range is encompassed within the range of [{} {}]".format(numRuns, minBounds[1], maxBounds[0],minBounds[0],maxBounds[1]))
  if minBounds[0] == freq_min:
    print("NOTE: the minimum clock speed may be less than {}".format(freq_min))
  if maxBounds[1] == freq_max:
    print("NOTE: the maximum clock speed may be greater than {}".format(freq_max))

# class DutyCycleTest(DeviceTest):
#     test_name = 'Duty Cycle Test'

#     parameters = [
#         TestParameter('Minimum Duty Cycle', ('%'), parse_percent),
#         TestParameter('Maximum Duty Cycle', ('%'), parse_percent),
#     ]

#     relevant_inputs = [
#         TestIOMapping('Reset', optional=True),
#         TestIOMapping('Clock', required_mode='clock')
#     ]

#def runDutyCycleTest(self, inputs, outputs, numRuns=10):
def runDutyCycleTest(duty_min,duty_max,range_min,range_max,numRuns=10):
#   duty_min = self.parameter_values[0]
#   duty_max = self.parameter_values[1]

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

#   if reset.signal is None:
#     reset.signal = signal.Pulse(signal.LOW, 0.100, 0.100, 1.0)

  duty = (duty_min + duty_max)/2.0
  minBounds = [-1, -1]
  maxBounds = [-1, -1]

  #Check if middle is valid, otherwise find an valid start freq
#   clock.signal = signal.Clock(clock.signal.clock_rate, duty_cycle=duty, sample_rate=clock.signal.sample_rate)
#   self.send_inputs(inputs, outputs)
#   if self.behavior_model.validate(inputs, outputs):
  if duty >= range_min and duty <= range_max:
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
#           clock.signal = signal.Clock(clock.signal.clock_rate, duty_cycle=duty, sample_rate=clock.signal.sample_rate)
#           self.send_inputs(inputs, outputs)
#           if self.behavior_model.validate(inputs, outputs):
          if duty >= range_min and duty <= range_max:
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
#     clock.signal = signal.Clock(clock.signal.clock_rate, duty_cycle=duty1, sample_rate=clock.signal.sample_rate)
#     self.send_inputs(inputs, outputs)
#     if self.behavior_model.validate(inputs, outputs):
    if duty1 >= range_min and duty1 <= range_max:
      minBounds[1] = duty1
    else:
      minBounds[0] = duty1
            
    duty2 = (maxBounds[0] + maxBounds[1])/2.0
    print("Checking MIN value of {} Checking MAX value of {}".format(duty1,duty2))
#     clock.signal = signal.Clock(clock.signal.clock_rate, duty_cycle=duty2, sample_rate=clock.signal.sample_rate)
#     self.send_inputs(inputs, outputs)
#     if self.behavior_model.validate(inputs, outputs):
    if duty2 >= range_min and duty2 <= range_max:
      maxBounds[0] = duty2
    else:
      maxBounds[1] = duty2

  print("After {} iterations, the acceptable consistent duty cycle range is [{}, {}]. The entire acceptable range is encompassed within the range of [{} {}]".format(numRuns, minBounds[1], maxBounds[0],minBounds[0],maxBounds[1]))
  if minBounds[0] == duty_min and duty_min != 0:
    print("NOTE: the minimum duty cycle may be less than {}".format(duty_min))
  if maxBounds[1] == duty_max and duty_max != 100:
    print("NOTE: the maximum duty cycle may be greater than {}".format(duty_max))

# class MaxDriftTest(DeviceTest):
#     test_name = 'Max Drift Test'
    
#     relevant_inputs = [
#         TestIOMapping('Signal 1'),
#         TestIOMapping('Signal 2'),
#         TestIOMapping('Reset', optional=True)
#     ]

#     parameters = [
#         TestParameter('Max delay on Signal 1', ('s', 'ms', 'us'), parse_duration),
#         TestParameter('Max delay on Signal 2', ('s', 'ms', 'us'), parse_duration),
#     ]

# def runMaxDriftTest(self, inputs, outputs, numRuns=10):
def runMaxDriftTest(pos_delay_max, neg_delay_max, range_pos, range_neg, numRuns=10):
#   pos_delay_max = self.parameter_values[0]
#   neg_delay_max = self.parameter_values[1]

  if(pos_delay_max < 0):
    print("Invalid positive delay, please enter a positive number in seconds")
    return
  if(neg_delay_max < 0):
    print("Invalid negative delay, please enter a positive number in seconds")
    return

  # Parameter Validation Check
#   og_signals = [self.relevant_input_values[0].signal.clone(), self.relevant_input_values[1].signal.clone()]

#   self.send_inputs(inputs, outputs)
#   if not self.behavior_model.validate(inputs, outputs):
  if range_pos < 0 or range_neg < 0: 
    print("Unable to validate signals before attempting to drift")
    return

  pos_bounds = [0, pos_delay_max]
  neg_bounds = [0, neg_delay_max]

  for i in range(numRuns):
           
    delay_pos = (pos_bounds[0] + pos_bounds[1])/2.0

#     s_pos = og_signals[1].insert_delay(delay_pos)
#     self.relevant_input_values[0].signal = og_signals[0]
#     self.relevant_input_values[1].signal = s_pos
#     self.send_inputs(inputs,outputs)
#     if self.behavior_model.validate(inputs, outputs):
    if delay_pos < range_pos:
      pos_bounds[0] = delay_pos
    else:
      pos_bounds[1] = delay_pos

    delay_neg = (neg_bounds[0] + neg_bounds[1])/2.0
    print("Checking POS value of {} Checking NEG value of {}".format(delay_pos,delay_neg))
#     s_neg = og_signals[0].insert_delay(delay_neg)
#     self.relevant_input_values[0].signal = s_neg
#     self.relevant_input_values[1].signal = og_signals[1]
#     self.send_inputs(inputs,outputs)
#     if self.behavior_model.validate(inputs, outputs):
    if delay_neg < range_neg:
      neg_bounds[0] = delay_neg
    else:
      neg_bounds[1] = delay_neg

  if pos_bounds[0] == 0 and neg_bounds[0] == 0:
    print("Unable to find any drift values with valid signals. Possible reasons:\n1.) Given region too large or number of iterations too low.\n2.) System too precise to allow drift.")
  else: 
    print("After {} iterations, the range of acceptable delay allowed on signal 2 is [-{}, {}].\nThe total acceptable range is encompassed in [-{}, {}]".format(numRuns, neg_bounds[0], pos_bounds[0],neg_bounds[1],pos_bounds[1]))
    if neg_bounds[1] == neg_delay_max:
      print("NOTE: the negative drift may be greater than -{}".format(neg_delay_max))
    if pos_bounds[1] == pos_delay_max:
      print("NOTE: the positive drift may be greater than {}".format(pos_delay_max))


# class MaxGlitchDuration(DeviceTest):
#     test_name = 'Max Glitch Duration'

#     parameters = [
#         TestParameter('Duration', ('s', 'cycles'), float)
#     ]

#     relevant_inputs = [
#         TestIOMapping('Reset', optional=True),
#         TestIOMapping('Clock', required_mode='clock')
#     ]

#def run(self, inputs, outputs, glitch_loc=0.5, numRuns=10):
def runMaxGlitchDurationTest(glitch_loc,range_min,range_max,period=1,numRuns=10,scaled=False):
#   clock = self.relevant_input_values[0]
#   reset = self.relevant_input_values[1]

#   if reset.signal is None:
#     reset.signal = signal.Pulse(signal.LOW, 0.100, 0.100, 1.0)


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

#   clock.signal = signal.Clock(freq, duty_cycle=clock.signal.duty_cycle)

#   self.send_inputs(inputs, outputs)
#   if not self.behavior_model.validate(inputs, outputs):
  if glitch_loc > range_max or glitch_loc < range_min:
    print("Initial signal not valid.\n")
    return

#   scale = 0.5*clock.signal.period*0.01
  lowBound = [glitch_loc, 0] # PERIOD CALC===================
  highBound = [glitch_loc, 100] # PERIOD CALC===================
  spreadBound = [0, max_spread] # PERIOD CALC===================

  for i in range(numRuns):

    # Step 1: Expand towards rising edge

    # Rebuild the clock without glitches
#     clock.signal = signal.Clock(clock_rate=clock.signal.clock_rate,duration=clock.signal.duration)

    glitch_size_1 = (lowBound[0] + lowBound[1])/2.0 
    #TODO: GENERATE SIGNAL THAT IS LOW FROM (glitchloc - glitch_size_1, glitch_loc) MAYBE SCALE DOWN BY 0.5 TO ACCOUNT FOR PERIOD
#     self.send_inputs(inputs, outputs)
#     if self.behavior_model.validate(inputs, outputs):
    #print(glitch_size_1)
    if glitch_size_1 > range_min:
      lowBound[0] = glitch_size_1
    else:
      lowBound[1] = glitch_size_1
    
    # Step 2: Expand towards negative edge

    # Rebuild the clock without glitches
#     clock.signal = signal.Clock(clock_rate=clock.signal.clock_rate,duration=clock.signal.duration)
    glitch_size_2 = (highBound[0] + highBound[1])/2.0
    #TODO: GENERATE SIGNAL THAT IS LOW FROM (glitchloc, glitch_loc + glitch_size_2)
#     self.send_inputs(inputs, outputs)
#     if self.behavior_model.validate(inputs, outputs):
    if glitch_size_2 < range_max:
      highBound[0] = glitch_size_2
    else:
      highBound[1] = glitch_size_2

    # Step 3: Expand outward in both directions

    # Rebuild the clock without glitches
#     clock.signal = signal.Clock(clock_rate=clock.signal.clock_rate,duration=clock.signal.duration)
    glitch_size_3 = (spreadBound[0] + spreadBound[1])/2.0
    print("Checking LOW value of -{}   Checking HIGH value of {}   Checking SPREAD value of +/-{}".format((glitch_loc-glitch_size_1),(glitch_size_2-glitch_loc),glitch_size_3))
    #TODO: GENERATE SIGNAL THAT IS LOW FROM (glitchloc - glitch_size_3, glitch_loc + glitch_size_3)
#     self.send_inputs(inputs, outputs)
#     if self.behavior_model.validate(inputs, outputs):
    if (glitch_loc - glitch_size_3) > range_min and (glitch_loc + glitch_size_3) < range_max:
      spreadBound[0] = glitch_size_3
    else:
      spreadBound[1] = glitch_size_3

  print("After {} iterations,".format(numRuns))
  print("A glitch towards the rising edge of the signal extended [{},{}] for a maximum of {} [found to not exceed {}]".format(lowBound[0],glitch_loc,(glitch_loc-lowBound[0]),lowBound[1]))
  print("A glitch towards the falling edge of the signal extended [{},{}] for a maximum of {} [found to not exceed {}]".format(glitch_loc,highBound[0],(highBound[0]-glitch_loc),highBound[1]))
  print("A glitch spreading equally in both directions extended [{},{}] for a maximum of {} [found to not exceed {}]".format((glitch_loc-spreadBound[0]),(glitch_loc+spreadBound[0]),(2*spreadBound[0]),(2*spreadBound[1])))
  if scaled == True:
    # scale = 0.5*clock.signal.period*0.01
    scale = 0.5*period*0.01
    print("\nScaled based on a period of {} seconds.\nAfter {} iterations,".format(period,numRuns))
    print("A glitch towards the rising edge of the signal extended [{},{}] for a maximum of {} seconds [found to not exceed {} seconds]".format(lowBound[0]*scale,glitch_loc*scale,(glitch_loc-lowBound[0])*scale,lowBound[1]*scale))
    print("A glitch towards the falling edge of the signal extended [{},{}] for a maximum of {} seconds [found to not exceed {} seconds]".format(glitch_loc*scale,highBound[0]*scale,(highBound[0]-glitch_loc)*scale,highBound[1]*scale))
    print("A glitch spreading equally in both directions extended [{},{}] for a maximum of {} seconds [found to not exceed {} seconds]".format((glitch_loc-spreadBound[0])*scale,(glitch_loc+spreadBound[0])*scale,(2*spreadBound[0])*scale,(2*spreadBound[1])*scale))


#for period_index in range(0, round(clock.signal.duration / clock.signal.period)):
  #clock.signal.glitch((glitch_loc + period_index) * clock.signal.period, glitch_size)
# clock.signal.plot()

# class MaxNumGlitchTest(DeviceTest):
#     test_name = 'Max Num Glitch Test'

#     parameters = [
#         TestParameter('Duration', ('s', 'cycles'), float)
#     ]

def runMaxNumGlitchTest(self, inputs, outputs, locs, limit=10):
  clock = self.relevant_input_values[0]
  reset = self.relevant_input_values[1]

  if reset.signal is None:
    reset.signal = signal.Pulse(signal.LOW, 0.100, 0.100, 1.0)

  glitch_locations = [0, 0.25, 0.5, 0.75]
  for loc in glitch_locations:
    # TODO: Binary search of glitch sizes would be way better

    for glitch_size in (0.25/glitch_size_count * i for i in range(1, glitch_size_count)):
      # Rebuild the clock without glitches
      clock.signal = signal.Clock(clock_rate=clock.signal.clock_rate, duration=clock.signal.duration)

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


# class ButtonPulseWidthTest(DeviceTest):
#     test_name = 'Button Pulse Width'

#     parameters = [
#         TestParameter('Minimum Pulse', ('s', 'ms', 'us'), parse_duration),
#         TestParameter('Maximum Pulse', ('s', 'ms', 'us'), parse_duration),
#     ]

#     relevant_inputs = [
#         TestIOMapping('Reset'),
#         TestIOMapping('Button')
#     ]

#     def run(self, inputs, outputs, numRuns=10):
#         pulse_min = self.parameter_values[0]
#         pulse_max = self.parameter_values[1]

#         precision = 40e-9

        # Initialization
#         reset = self.relevant_input_values[0]
#         button = self.relevant_input_values[1]

#         val = (pulse_min + pulse_max) / 2
#         search_size = val
#         found_end = False

        # Find min pulse width
#         while 1:
#             if search_size < precision:
#                 break

#             search_size = search_size / 2
#             print('Trying pulse duration: {:02f} s'.format(val))
#             self.send_inputs(inputs, outputs)
#             button.signal = signal.Pulse(signal.LOW, 1.0, val, 1.0, sample_rate=1/val)

#             if self.behavior_model.validate(inputs, outputs):
#                 val -= search_size
#             else:
#                 found_end = True
#                 val += search_size

#         if found_end:
#             pulse_min = val

        # Find max pulse width
#         val = (pulse_min + pulse_max) / 2
#         search_size = val

#         found_end = False
#         while 1:
#             if search_size < precision:
#                 break

#             search_size = search_size / 2
#             print('Trying pulse duration: {:02f} s'.format(val))
#             self.send_inputs(inputs, outputs)
#             button.signal = signal.Pulse(signal.LOW, 1.0, val, 1.0, sample_rate=1/val)

#             if self.behavior_model.validate(inputs, outputs):
#                 val += search_size
#             else:
#                 found_end = True
#                 val -= search_size

#         if found_end:
#             pulse_max = val

#         print(pulse_min, pulse_max)


# tests = [BasicPlayback, ClockRateTest, MaxGlitchDuration, ResponseTimeTest, MaxNumGlitchTest, MaxDriftTest, ButtonPulseWidthTest]
print("-----Testing Clock Rate-----\n")

f_min = 10000
f_max = 40000
r_min = 20000
r_max = 22000
n_runs = 10
print("Test 1:\nChecking Frequency Range: [{},{}], Actual Hardcoded Range: [{},{}], Iterations = {}\n".format(f_min,f_max,r_min,r_max,n_runs))
runClockRateTest(f_min,f_max,r_min,r_max,numRuns=n_runs)
print("\nEnd Test 1\n\n")

f_min = 10000
f_max = 40000
r_min = 20000
r_max = 20010
n_runs = 60
print("\nTest 2:\nChecking Frequency Range: [{},{}], Actual Hardcoded Range: [{},{}], Iterations = {}\n".format(f_min,f_max,r_min,r_max,n_runs))
runClockRateTest(f_min,f_max,r_min,r_max,numRuns=n_runs)
print("\nEnd Test 2\n")

f_min = 10000
f_max = 40000
r_min = 5000
r_max = 15000
n_runs = 10
print("\nTest 3:\nChecking Frequency Range: [{},{}], Actual Hardcoded Range: [{},{}], Iterations = {}\n".format(f_min,f_max,r_min,r_max,n_runs))
runClockRateTest(f_min,f_max,r_min,r_max,numRuns=n_runs)
print("\nEnd Test 3\n")

f_min = 40000
f_max = 10000
r_min = 20000
r_max = 22000
n_runs = 10
print("\nTest 4:\nChecking Frequency Range: [{},{}], Actual Hardcoded Range: [{},{}], Iterations = {}\n".format(f_min,f_max,r_min,r_max,n_runs))
runClockRateTest(f_min,f_max,r_min,r_max,numRuns=n_runs)
print("\nEnd Test 4\n")


print("\n-----End Test Clock Rate-----\n\n\n")




print("\n-----Testing Duty Cycle-----\n")

d_min = 0
d_max = 100
r_min = 43.8
r_max = 100
n_runs = 10
print("Test 1:\nChecking Duty Cycle Range: [{},{}], Actual Hardcoded Range: [{},{}], Iterations = {}\n".format(d_min,d_max,r_min,r_max,n_runs))
runDutyCycleTest(d_min,d_max,r_min,r_max,numRuns=n_runs)
print("\nEnd Test 1\n\n")

d_min = 0
d_max = 100
r_min = 11.4321
r_max = 70.1234
n_runs = 60
print("\nTest 2:\nChecking Duty Cycle Range: [{},{}], Actual Hardcoded Range: [{},{}], Iterations = {}\n".format(d_min,d_max,r_min,r_max,n_runs))
runDutyCycleTest(d_min,d_max,r_min,r_max,numRuns=n_runs)
print("\nEnd Test 2\n")

d_min = 0
d_max = 90
r_min = 0
r_max = 100
n_runs = 10
print("\nTest 3:\nChecking Duty Cycle Range: [{},{}], Actual Hardcoded Range: [{},{}], Iterations = {}\n".format(d_min,d_max,r_min,r_max,n_runs))
runDutyCycleTest(d_min,d_max,r_min,r_max,numRuns=n_runs)
print("\nEnd Test 3\n")

d_min = -1
d_max = 90
r_min = 43.8
r_max = 100
n_runs = 10
print("\nTest 4:\nChecking Duty Cycle Range: [{},{}], Actual Hardcoded Range: [{},{}], Iterations = {}\n".format(d_min,d_max,r_min,r_max,n_runs))
runDutyCycleTest(d_min,d_max,r_min,r_max,numRuns=n_runs)
print("\nEnd Test 4\n")

print("\n-----End Test Duty Cycle-----\n\n\n")






print("\n-----Testing Maximum Drift-----\n")

p_d_max = 0.5
n_d_max = 0.5
r_pos = 0.013
r_neg = 0.24
n_runs = 10
print("Test 1:\nChecking Drift Range: [-{},{}], Actual Hardcoded Range: [-{},{}], Iterations = {}\n".format(p_d_max,n_d_max,r_pos,r_neg,n_runs))
runMaxDriftTest(p_d_max,n_d_max,r_pos,r_neg,numRuns=n_runs)
print("\nEnd Test 1\n\n")

p_d_max = 0.1
n_d_max = 0.100
r_pos = 0.01743
r_neg = 0.89234
n_runs = 60
print("Test 2:\nChecking Drift Range: [-{},{}], Actual Hardcoded Range: [-{},{}], Iterations = {}\n".format(p_d_max,n_d_max,r_pos,r_neg,n_runs))
runMaxDriftTest(p_d_max,n_d_max,r_pos,r_neg,numRuns=n_runs)
print("\nEnd Test 2\n\n")

p_d_max = -0.1
n_d_max = 0.1
r_pos = 0.05
r_neg = 0.05
n_runs = 10
print("Test 3:\nChecking Drift Range: [-{},{}], Actual Hardcoded Range: [-{},{}], Iterations = {}\n".format(p_d_max,n_d_max,r_pos,r_neg,n_runs))
runMaxDriftTest(p_d_max,n_d_max,r_pos,r_neg,numRuns=n_runs)
print("\nEnd Test 3\n\n")

p_d_max = 0.4
n_d_max = 0.1
r_pos = 0.4
r_neg = 0.1
n_runs = 10
print("Test 4:\nChecking Drift Range: [-{},{}], Actual Hardcoded Range: [-{},{}], Iterations = {}\n".format(p_d_max,n_d_max,r_pos,r_neg,n_runs))
runMaxDriftTest(p_d_max,n_d_max,r_pos,r_neg,numRuns=n_runs)
print("\nEnd Test 4\n\n")

print("\n-----End Test Maximum Drift-----\n\n\n")






print("\n-----Testing Maximum Glitch Duration-----\n")

g_loc = 50
r_min = 43.8
r_max = 100
p = 1 #seconds
n_runs = 10
print("Test 1:\nChecking Glitch Location: {}, Actual Hardcoded Range: [{},{}], Iterations = {}\n".format(g_loc,r_min,r_max,n_runs))
runMaxGlitchDurationTest(g_loc,r_min,r_max,numRuns=n_runs)
print("\nEnd Test 1\n\n")

g_loc = 50
r_min = 43.8
r_max = 100
p = 1 #seconds
n_runs = 10
print("Test 2:\nChecking Glitch Location: {}, Actual Hardcoded Range: [{},{}], Period = {}, Iterations = {}\n".format(g_loc,r_min,r_max,p,n_runs))
runMaxGlitchDurationTest(g_loc,r_min,r_max,period=p,numRuns=n_runs,scaled=True)
print("\nEnd Test 2\n\n")

g_loc = 50
r_min = 27.951
r_max = 70.063
n_runs = 60
print("\nTest 3:\nChecking Glitch Location {}, Actual Hardcoded Range: [{},{}], Iterations = {}\n".format(g_loc,r_min,r_max,n_runs))
runMaxGlitchDurationTest(g_loc,r_min,r_max,numRuns=n_runs)
print("\nEnd Test 3\n")

g_loc = 101
r_min = 100
r_max = 102
n_runs = 10
print("\nTest 4:\nChecking Glitch Location {}, Actual Hardcoded Range: [{},{}], Iterations = {}\n".format(g_loc,r_min,r_max,n_runs))
runMaxGlitchDurationTest(g_loc,r_min,r_max,numRuns=n_runs)
print("\nEnd Test 4\n")


g_loc = 100
r_min = 88.9
r_max = 100
n_runs = 10
print("\nTest 5:\nChecking Glitch Location {}, Actual Hardcoded Range: [{},{}], Iterations = {}\n".format(g_loc,r_min,r_max,n_runs))
runMaxGlitchDurationTest(g_loc,r_min,r_max,numRuns=n_runs)
print("\nEnd Test 5\n")

print("\n-----End Test Maximum Glitch Duration-----\n\n\n")

