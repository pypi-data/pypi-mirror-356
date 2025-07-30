from sq_midi import Channel

class MuteGroup(Channel):
    """ Mute groups """

    CHANNEL_TYPE = "Mute Group"
    CHANNEL_PREFIX = "MGRP"
    NUMBER_OF_CHANNELS = 8

    def _load_info(self):
        return {
            "name": self.CHANNEL_PREFIX + str(self.number),
            "mute": ["04", "0" + str(self.number-1)],
        }

if __name__ == "__main__":
    from sq_midi import Mixer
    c = MuteGroup(Mixer(), 8)
    print(c.info)