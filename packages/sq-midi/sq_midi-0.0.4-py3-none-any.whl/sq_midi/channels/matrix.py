from sq_midi.channel import Channel


class Matrix(Channel):
    """ Matrix class """

    FILE_NAME = "matrices"
    CHANNEL_TYPE = "Matrices"
    CHANNEL_PREFIX = "Mtx"
    NUMBER_OF_CHANNELS = 3

    def _load_info(self):
        return {
            "name": self.CHANNEL_PREFIX + str(self.number),
            "mute": ["00", "5" + str(self.number+4)], # [00 55] -> [00 57]
            "levels": {
                "lr": ["4F", "1" + str(self.number)], # [4F 11] -> [4F 13]
            },
            "panning": {
                "lr": ["5F", "1" + str(self.number)], # [5F 11] -> [5F 13]
            }
        }

if __name__ == "__main__":
    from sq_midi import Mixer
    c = Matrix(Mixer(), 1)
    print(c.info)