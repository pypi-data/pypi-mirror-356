from sq_midi import Channel


class DCA(Channel):
    """ DCA channel class """

    CHANNEL_TYPE = CHANNEL_PREFIX = "DCA"
    NUMBER_OF_CHANNELS = 8

    def _load_info(self):
        return {
            "name": self.CHANNEL_PREFIX + str(self.number),
            "mute": ["02", "0" + str(self.number-1)], # [02 00] -> [02 07]
            "levels": {
                "lr": ["4F", "2" + str(self.number-1)], # [4F 20] -> [4F 27]
            }
        }

if __name__ == '__main__':
    from sq_midi import Mixer
    channel = DCA(Mixer(debug=1), 8)
    #print(channel.level)
    channel.mute = 1
    #print(channel.mute)
    #channel.mute = False
    #print(channel.info)
