import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from main import Signal, FPGAPlaybackDevice

playback = FPGAPlaybackDevice(baud_rate=19200)
preloaded_signal = playback.dump_signal().plot()

# Play pre-loaded signal
input('Enter to play signal')
playback.play()

input('')

# Accept and play user signal
while 1:
	samples = input("Enter a signal (1's and 0's): ")
	if samples.count('1') + samples.count('0') == len(samples) and len(samples) < 100:
		break

	print('Invalid signal, try again')

signal = Signal.from_samples(100, [int(c) for c in samples])
signal.plot()

input('Enter to load & play signal')
playback.load_signal(signal)