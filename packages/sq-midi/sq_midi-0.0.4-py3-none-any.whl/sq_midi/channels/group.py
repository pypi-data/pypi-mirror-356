from sq_midi.channel import Channel


class Group(Channel):
    """ Group Class """

    FILE_NAME = 'groups'
    CHANNEL_TYPE = 'Group Send'
    CHANNEL_PREFIX = 'Grp'
    NUMBER_OF_CHANNELS = 12

if __name__ == '__main__':
    from sq_midi import Mixer
    channel = Group(Mixer(debug=1), 1)
    print(channel.level)
