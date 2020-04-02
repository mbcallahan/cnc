from . import test
from . import signal
from .exceptions import PlaybackDeviceException

class BasicPlayback(test.DeviceTest):
    """Plays back the loaded signals; does nothing else."""
    test_name = 'Basic Playback'

    def run(self, inputs, outputs):
        self.send_inputs(inputs, outputs)

        print('Analyzing...')
        if self.behavior_model is not None:
            if self.behavior_model.validate(inputs, outputs):
                print('Device behavior validated!')
                print(outputs)

            else:
                print('Device behavior did not validate.')