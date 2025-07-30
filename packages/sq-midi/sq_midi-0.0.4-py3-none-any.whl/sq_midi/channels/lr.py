from typing import override

from sq_midi import Mixer
from sq_midi.channel import Channel
from sq_midi.data.loader import load_data

class LR(Channel):
    """ Main LR channel class """

    FILE_NAME = "lr"

    def __init__(self, mixer: Mixer):
        super().__init__(mixer)

    def __str__(self):
        return "LR object [Main LR]"

    def _load_info(self):
        return load_data(self.FILE_NAME)

if __name__ == "__main__":
    lr = LR(Mixer(debug=True))
    print(lr)
    lr.level = 1
