import time
import mido
from mido import Message

from sq_midi.channel_wrapper import ChannelWrapper


class Mixer:
    """ Main Mixer class """

    _input_port = None
    _output_port = None
    _current_state = []
    _connected = False
    # noinspection PyTypeChecker
    _channels = {
        "lr": None,
        "inputs": [],
        "groups": [],
        "aux": [],
        "dcas": [],
        "mute_groups": [],
        "fx_returns": [],
        "fx_sends": [],
        "matrices": [],
    }

    def __init__(self, input_name="MIDI Control 1", output_name="MIDI Control 1", channel=0, debug=False):
        self._input = input_name
        self._output = output_name
        self._channel = channel
        self._debug = debug
        self._connect()
        self.init_channels()

    def _print_debug(self, msg):
        if self._debug:
            print("DEBUG [Mixer] => " + str(msg))

    def _connect(self):
        input_name = None
        output_name = None
        # Input
        self._print_debug("Connecting to input ...")
        self._print_debug(mido.get_input_names())
        for port in mido.get_input_names():
            if self._input in port:
                input_name = port
        # Output
        self._print_debug("Connecting to output ...")
        self._print_debug(mido.get_output_names())
        for port in mido.get_output_names():
            if self._output in port:
                output_name = port

        self._print_debug("Selected Input: " + str(input_name))
        self._print_debug("Selected Output: " + str(output_name))
        if input_name is None or output_name is None:
            return False
        # Connect
        try:
            self._input_port = mido.open_input(input_name)
            self._output_port = mido.open_output(output_name)
            self._print_debug("Connected to Input: '" + input_name + "' Output: '" + output_name + "'")
        except Exception as e:
            self._print_debug(e)
            return False
        self._connected = True
        return True

    @property
    def connected(self):
        """ Whether connected to the mixer (via MIDI) """
        return self._connected

    def __send_command(self, msb: int, lsb: int, data1: list[int], data2: list[int] = None):
        """ Send an NRPN command to the mixer """
        if not self.connected and not self._connect():
            return False
        temp = " ".join(map(str, data2)) if data2 else "[None]"
        self._print_debug("Sending command: MSB: " + str(msb) + " LSB: " + str(lsb) + " Data1: " + " ".join(
            map(str, data1)) + " Data2: " + temp)
        ch = 'B' + str(self._channel)
        # MSB & LSB
        msg_msb = Message.from_bytes([int(ch, 16), 99, msb])
        msg_lsb = Message.from_bytes([int(ch, 16), 98, msb])
        # Data
        msg_data1 = Message.from_bytes([int(ch, 16), *data1])
        # Send command
        self._output_port.send(msg_msb)
        self._output_port.send(msg_lsb)
        self._output_port.send(msg_data1)
        # If data2
        if data2 is not None:
            msg_data2 = Message.from_bytes([int(ch, 16), *data2])
            self._output_port.send(msg_data2)
        return True

    def set_param(self, msb_lsb: list[int], coarse: int, fine: int = None):
        """ Send a 'set' NRPN command with 'coarse' and 'fine' values """
        msb = msb_lsb[0]
        lsb = msb_lsb[1]
        # If only sending single parameter (e.g. mute)
        if fine is None:
            fine = coarse
            coarse = 0
        return self.__send_command(
            msb=msb,
            lsb=lsb,
            data1=[6, coarse],
            data2=[38, fine]
        )

    def get_param(self, msb_lsb: list[int]):
        """ Get a parameter from the mixer """
        if not self.connected and not self._connect():
            return None
        self.__send_command(
            msb=msb_lsb[0],
            lsb=msb_lsb[1],
            data1=[90, 127]
        )
        start = time.time_ns()
        msg = None
        while time.time_ns() - start < 5000 * 1000:
            if not self._input_port.closed:
                msg = self._input_port.poll()
        return msg if msg is not None else False

    def increment_param(self, msb, lsb):
        """ Increment a parameter """
        return self.__send_command(
            msb=msb,
            lsb=lsb,
            data1=[96, 0]
        )

    def decrement_param(self, msb, lsb):
        """ Decrement a parameter """
        return self.__send_command(
            msb=msb,
            lsb=lsb,
            data1=[97, 0]
        )

    """ Handle channels """

    def init_channels(self):
        """ Initialize all channels """
        # Avoid circular loop
        import sq_midi.channels as channels
        """ Initialize channels """
        # Inputs
        for i in range(channels.Input.NUMBER_OF_CHANNELS):
            self._channels["inputs"].append(channels.Input(self, i + 1))
        # Groups
        for i in range(channels.Group.NUMBER_OF_CHANNELS):
            self._channels["groups"].append(channels.Group(self, i + 1))
        # Auxes
        for i in range(channels.Aux.NUMBER_OF_CHANNELS):
            self._channels["aux"].append(channels.Aux(self, i + 1))
        # Matrices
        for i in range(channels.Matrix.NUMBER_OF_CHANNELS):
            self._channels["matrices"].append(channels.Matrix(self, i + 1))
        # LR
        # noinspection PyTypeChecker
        self._channels["lr"] = channels.LR(self)
        # FX Sends
        for i in range(channels.FXSend.NUMBER_OF_CHANNELS):
            self._channels["fx_sends"].append(channels.FXSend(self, i + 1))
        # FX Returns
        for i in range(channels.FXReturn.NUMBER_OF_CHANNELS):
            self._channels["fx_returns"].append(channels.FXReturn(self, i + 1))

    # Channels
    @property
    def inputs(self):
        """ List of input channels"""
        return ChannelWrapper(self._channels["inputs"])

    @property
    def groups(self):
        """ List of groups """
        return ChannelWrapper(self._channels["groups"])

    @property
    def lr(self):
        """ Main LR channel"""
        from sq_midi.channels import LR
        return LR(self)

    @property
    def aux(self):
        """ List of aux channels """
        return ChannelWrapper(self._channels["aux"])

    @property
    def matrices(self):
        """ List of matrices """
        return ChannelWrapper(self._channels["matrices"])

    @property
    def fxsends(self):
        """ List of FX Sends """
        return ChannelWrapper(self._channels["fx_sends"])

    @property
    def fxreturns(self):
        """ List of FX Returns """
        return ChannelWrapper(self._channels["fx_returns"])


if __name__ == "__main__":
    mixer = Mixer(
        input_name="MIDI Control 1",
        output_name="MIDI Control 1",
        debug=True
    )
    print(mixer.inputs[48].levels.lr)
    print(mixer.groups[1])
    #print(mixer.fxsends[1].panning)
    print(mixer.fxsends[1].assignments)
