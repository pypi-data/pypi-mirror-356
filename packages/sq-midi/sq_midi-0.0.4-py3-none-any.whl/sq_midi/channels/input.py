from sq_midi import Mixer
from sq_midi.channel import Channel

class Input(Channel):
    """ Input Channel Class """

    FILE_NAME = 'inputs'
    CHANNEL_TYPE = 'Input'
    CHANNEL_PREFIX = 'Ip'
    NUMBER_OF_CHANNELS = 48

if __name__ == '__main__':
    channel = Input(Mixer(debug=1), 1)
    print(channel.level)
    channel.panning.groups[0] =1