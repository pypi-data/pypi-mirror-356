from sq_midi.channel import Channel
from sq_midi.mixer import Mixer


class FXReturn(Channel):
    """ FX Return Mix Class """

    FILE_NAME = 'fx_returns'
    CHANNEL_TYPE = 'FX Return'
    CHANNEL_PREFIX = "FxRtn"
    NUMBER_OF_CHANNELS = 8

if __name__ == '__main__':
    _mixer = Mixer(debug=True)
    fx = FXReturn(_mixer, 8)

    print(fx.assignments.groups[1])
