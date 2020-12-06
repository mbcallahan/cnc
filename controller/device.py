from itertools import zip_longest, repeat

import time
import serial
import serial.tools.list_ports
import saleae
import platform

from .signal import Signal
from .exceptions import PlaybackDeviceException

MHZ = 1000 * 1000
DO_ECHO = True

class FPGAPlaybackDevice:
    #STOP_SUPPORT = True
    MAX_LENGTH = 2**20

    def __init__(self, port=None):
        self.connected = False                              #Flag for playback device connection
        self.device_name = ''                               #Playback device name
        self.ser = serial.Serial(None, baudrate=115200)     #Serial port connection to playback device
        self.loaded_signal_mask = 0xF

        self.connect()                                      #Search for playback device

    def connect(self, port=None):
        device_found = False
        for comport in list(serial.tools.list_ports.comports()):    #Check if device is still connected
            if self.ser.port == comport[0]:
                self.connected = True
                device_found = True
        if not(device_found):
            self.connected = False
            self.ser = serial.Serial(None, baudrate=115200)
            self.device_name = ''

        if port is not None:                                #Override any connection if port is provided
            self.device_name = ''
            self.ser = serial.Serial(None, baudrate=115200)
            self.connected = False
            for comport in list(serial.tools.list_ports.comports()):
                if 'Linux' == platform.system():            # Check for Digilent Adept USB Device on Linux machine
                    if "Digilent Adept USB Device" in comport[1] and port == comport[0]:
                        self.device_name = comport[1]
                        self.ser = serial.Serial(port, baudrate=115200)
                        self.connected = True
                elif 'Windows' == platform.system():        #Check for FTDI on Windows machine
                    if "FTDI" in comport[2] and port == comport[0]:
                        self.device_name = comport[2]
                        self.ser = serial.Serial(port, baudrate=115200)
                        self.connected = True

            if self.ser.port is None:                       #List available ports if provided port is invalid
                print('Invalid port')
                for comport in list(serial.tools.list_ports.comports()):
                    if 'Linux' == platform.system():
                        print('{} available at {}'.format(comport[1],comport[0]))
                    elif 'Windows' == platform.system(): 
                        print('{} available at {}'.format(comport[2],comport[0]))

        elif self.connected is False:                       #Auto select port if not connected
            # Auto-select port
            for comport in reversed(list(serial.tools.list_ports.comports())):
                if 'Linux' == platform.system():	       # Check for Digilent Adept USB Device on Linux machine
                    if "Digilent Adept USB Device" in comport[1]:
                        #Assumption: this is the only FTDI device
                        port = comport[0]
                        self.device_name = comport[1]
                        self.ser = serial.Serial(port, baudrate=115200)
                        self.connected = True
                elif 'Windows' == platform.system():	   #Check for FTDI on Windows machine
                    if "FTDI" in comport[2]:
                        port = comport[0]
                        self.device_name = comport[2]
                        self.ser = serial.Serial(port, baudrate=115200)
                        self.connected = True

            # TODO: Some kind of handshake here to verify the device is actually *our* device would be good.
            if self.ser.port is None:
                print('Unable to find a playback device')
                
        if self.ser.port is not None:                       #Print valid connection
            print('Connected to {} on port {}\n'.format(self.device_name,self.ser.port))

    def await_resp(self, ersp='OK\n', echo=DO_ECHO):
        rsp = ''
        if echo:
            print('RSP:', end='')

        if ersp is not None:
            while not rsp.endswith(ersp):

                c = self.ser.read(1).decode('utf-8')
                if echo:
                    print(c, end='')
                rsp += c

            if rsp.startswith('ERROR'):
                raise PlaybackDeviceException(rsp)

        if echo:
            print('')

    def send_command(self, cmd, ersp='OK\n', echo=DO_ECHO):
        if echo:
            print('CMD:', repr(cmd))
        self.ser.write(cmd.encode('utf-8'))
        self.await_resp(ersp, echo)

    def load_signals(self, signals):
        for ch, s in enumerate(signals):

            if s is not None:
                self.send_command('set_freq {} {}\n'.format(ch, s.sample_rate))
                self.send_command('set_stop_addr {} {}\n'.format(ch, s.sample_count-1))

        ch_mask = 0
        loop_mask = 0
        repeat_signals = []
        single_signals = []

        for i, signal in enumerate(signals):
            if signal is None:
                continue
            
            ch_mask = ch_mask | (1 << i)
            loop_mask = loop_mask | (int(signal.repeat) << i)

            if signal.repeat:
                repeat_signals.append(signal)
            else:
                single_signals.append(signal)

        #if self.STOP_SUPPORT:
        #    short_ch, short_dur, short_count = min(((i, s.sample_count / s.sample_rate, s.sample_count) for i, s in enumerate(signals) if not s.repeat), key=lambda a: a[1])
        #    self.send_command('set_stop_addr {} {:X}\n'.format(short_ch, short_count))

        # If all signals are repeat signals, load the full memory with the signal
        if len(single_signals) == 0:
            count = self.MAX_LENGTH
        else:
            count = max((s.sample_count for s in signals if s is not None and not s.repeat))
            if count > self.MAX_LENGTH:
                raise PlaybackDeviceException('Signal too long to play back: {} is greater than {}'.format(count, self.MAX_LENGTH))

        self.send_command('load {:X} {:X} {}\n'.format(ch_mask, loop_mask, count), ersp=None)

        self.loaded_signal_mask = ch_mask

        # Write samples
        #print('Writing length {}'.format(count))
        #print('Samples:', end='')

        sent_count = 0
        gens = [s.samples(length=count) if s is not None else repeat(0) for s in signals]
        for vals in zip_longest(*gens, fillvalue=0):
            din = 0
            for i, val in enumerate(vals):
                din = din | (val << i)

            #print(din, end='')

            self.ser.write(bytes([din]))
            sent_count += 1

            if sent_count >= count:
                break

        if DO_ECHO:
            print('\n')
            print('Sent {} samples'.format(sent_count))

        # Wait for ACK
        self.await_resp()
        
    def play(self):
        self.send_command('play {:X}\n'.format(self.loaded_signal_mask))

    def stop(self):
        self.send_command('stop\n')

