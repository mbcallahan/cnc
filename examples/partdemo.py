import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from main import Signal, FPGAPlaybackDevice, MHZ

playback = FPGAPlaybackDevice(baud_rate=19200)
while 1:
	samples = input("Enter a signal (1's and 0's): ")
	if samples.count('1') + samples.count('0') == len(samples) and len(samples) < 100:
		break

	print('Invalid signal, try again')

signal = Signal.from_samples(100, [int(c) for c in samples])
signal.plot()

input('Enter to load signal')
playback.load_signal(signal)

# Play user signal
input('Enter to play signal')
playback.play()
