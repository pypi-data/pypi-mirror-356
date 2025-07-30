from sq_midi.parameter_wrapper import ParameterWrapper

class ParameterHandler:
    """ Handle setting / getting parameters """
    def __init__(self, wrapper: ParameterWrapper, parameter_name):
        self._mixer = wrapper.__getattribute__("mixer")
        self._list = wrapper.__getattribute__("channel").info[
            wrapper.__getattribute__("parameter_category")
        ][parameter_name]
        #print(self._list)
        self._data_type = wrapper.__getattribute__("parameter_type")
        self._data_range = wrapper.__getattribute__("parameter_range")
        self._data_map = wrapper.__getattribute__("parameter_map")

    def __getitem__(self, key: int):
        """ Get a parameter """
        if key not in range(1, len(self._list) + 1):
            raise IndexError(f"Parameter index out of range [1, {len(self._list)}]")
        #print(self._list[key-1])
        return self._mixer.get_param(self._list[key-1])

    def __setitem__(self, key, value):
        """ Set a parameter
            1-indexed, e.g. aux[1] => Aux1
        """
        if type(key) is not int:
            raise TypeError("Parameter key must be an integer")
        if key not in range(1, len(self._list) + 1):
            raise IndexError(f"Parameter index out of range [1, {len(self._list)}]")
        if (
            type(value) is not self._data_type
            and not (
                self._data_type is bool
                and isinstance(value, int)
                and value in [0, 1]
            )
        ):
            raise ValueError(f"Value must be of type {str(self._data_type)}")
        if value not in self._data_range:
            raise ValueError("Value must be in range " + str(self._data_range[0]) + " to " + str(self._data_range[-1]))
        value = self._data_map(value)
        coarse = value >> 7
        fine = value & 0x7F
        #print("Coarse: " + str(coarse), "Fine: " + str(fine))
        self._mixer.set_param(self._list[key - 1], coarse, fine)