import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from main import Signal, FPGAPlaybackDevice, MHZ

playback = FPGAPlaybackDevice(baud_rate=19200)
playback.play()
#playback.dump_signal().plot()