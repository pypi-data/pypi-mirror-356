from sq_midi.channel import Channel

class FXSend(Channel):
    """ FX Send Class """

    FILE_NAME = 'fx_sends'
    CHANNEL_TYPE = 'FX Send'
    CHANNEL_PREFIX = "FxSnd"
    CHANNEL_PARAMETERS = [
        "levels"
    ]
    NUMBER_OF_CHANNELS = 4

if __name__ == '__main__':
    from sq_midi import Mixer

    test = FXSend(Mixer(), 1)

    print(test)