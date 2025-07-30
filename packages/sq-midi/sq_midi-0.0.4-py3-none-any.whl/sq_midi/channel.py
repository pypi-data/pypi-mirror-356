from sq_midi.mixer import Mixer
from sq_midi.data.loader import load_data, decode


class Channel:
    """ Channel class
        Must be inherited by subclass to set FILE_NAME
    """

    FILE_NAME = None
    CHANNEL_TYPE = ""
    CHANNEL_PREFIX = ""
    NUMBER_OF_CHANNELS = -1
    CHANNEL_PARAMETERS = [
        "assignments",
        "levels",
        "panning"
    ]

    _level = 0
    _info = []
    _number = None
    __freeze = False

    def __init__(self, mixer: Mixer, number: int = None):
        self._mixer = mixer
        self._number = number
        if self.number is not None and self.number not in range(1, self.NUMBER_OF_CHANNELS + 1):
            raise ValueError(f"Channel number must be between 1 and {self.NUMBER_OF_CHANNELS}")
        self._info = self._load_info()
        self.__decode_info()
        self.__freeze = True

    def __str__(self):
        return f"{self.__class__.__name__} object [{self.CHANNEL_PREFIX}{self.number}]"

    def __decode_info(self):
        self._info = decode(self._info)
        try:
            self._info["levels"]["lr"] = [self._info["levels"]["lr"]]
            self._info["panning"]["lr"] = [self._info["panning"]["lr"]]
            self._info["assignments"]["lr"] = [self._info["assignments"]["lr"]]
        except KeyError:
            pass

    def _load_info(self):
        info = load_data(self.FILE_NAME)
        if self.number > len(info):
            raise ValueError("Channel number out of range")
        else:
            return info[self.number-1]

    @property
    def info(self):
        """ Channel commands & info """
        return self._info

    @property
    def number(self):
        """ Channel number"""
        return self._number

    @property
    def name(self):
        return self.info['name']

    """MUTE"""
    @property
    def mute(self):
        """ Get channel mute """
        return self._mixer.get_param(self.info["mute"])

    @mute.setter
    def mute(self, value: bool):
        """ Set channel mute """
        if type(value) is not bool and value not in [0, 1]:
            raise ValueError("Channel mute must be a boolean")
        self._mixer.set_param(self.info["mute"], int(value))

    def unmute(self):
        self.mute = False

    """LEVEL"""
    @property
    def level(self):
        """ Get current channel master level """
        return self.levels.lr

    @level.setter
    def level(self, value):
        """ Set channel master level """
        self.levels.lr = value

    """PANNING"""
    @property
    def pan(self):
        """ Get current channel master panning """
        return self.panning.lr

    @pan.setter
    def pan(self, value):
        """ Set channel master panning """
        self.panning.lr = value

    def center(self):
        self.panning.lr = 0

    def __getattr__(self, item):
        """ Handle other parameters as defined in JSON
            e.g. assignments / panning
            e.g. [channel].levels
                 [channel].panning
        """
        if item not in self.CHANNEL_PARAMETERS:
            raise AttributeError(f"{self.CHANNEL_TYPE} channel does not have parameter {item}"
                                 f"\nAvailable parameters: {", ".join(self.CHANNEL_PARAMETERS)}")
        t = None # Value data type
        r = None # Range of values
        m = lambda val: val # Map value to correct range
        match item:
            case "levels":
                t = int
                r = range(0, 110+1)
                # Map [0, 100] to [0, 12544] and [100, 110] to [12544, 16320]
                # according to MIDI datasheet [-inf, 0dB] and [0dB, +10dB]
                m = lambda val: int(
                        125.44 * val
                        if 0 <= val <= 100 else
                        (377.6 * (val - 100) + 12544 )
                    )
            case "assignments":
                t = bool
                r = [True, False]
            case "panning":
                t = int
                r = range(-100, 100+1)
                # Map [-100, 100] to [0, 16383]
                m = lambda val: int(((val + 100) / 200) * 16383)
        if t is not None:
            # Avoid circular dependency
            from .parameter_wrapper import ParameterWrapper
            # Use parameter wrapper class
            return ParameterWrapper(
                mixer = self._mixer,
                channel = self,
                parameter_category=item,
                parameter_type = t,
                parameter_range = r,
                parameter_map = m
            )
        else:
            # If parameter name does not exist, use normal attribute error message
            return super().__getattribute__(item)

    def __setattr__(self, key, value):
        if (self.__freeze or key in self.CHANNEL_PARAMETERS) and key not in ["level", "mute", "pan"]:
            raise TypeError("Cannot edit instance of Channel"
                            "\n[Attributes] \nInfo: name, number\nControl: level, mute, pan\nRouting: levels, assignments, panning"
                            "\n[Methods]: \nunmute(), center()")
        object.__setattr__(self, key, value)


if __name__ == "__main__":
    _mixer = Mixer(
            input_name="MIDI Control 1",
            output_name="MIDI Control 1",
            debug = True
        )

    print(_mixer.inputs[1].mute)
    _mixer.inputs[1].levels = 100
    print(_mixer.inputs[1].levels)
    print(_mixer.inputs.ip133)