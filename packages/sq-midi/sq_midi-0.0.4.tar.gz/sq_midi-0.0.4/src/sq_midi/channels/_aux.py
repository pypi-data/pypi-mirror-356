from sq_midi.channel import Channel


class Aux(Channel):
    """ Auxiliary output channel"""

    FILE_NAME = 'auxes'
    CHANNEL_TYPE = CHANNEL_PREFIX =  'Aux'
    NUMBER_OF_CHANNELS = 12