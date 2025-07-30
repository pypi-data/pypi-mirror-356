from gc import freeze


class ChannelWrapper:

    __freeze = False

    def __init__(self, channel_list: list):
        self.__channel_list = channel_list
        self.__prefix = self.__channel_list[0].CHANNEL_PREFIX
        self.__type = self.__channel_list[0].CHANNEL_TYPE
        __freeze = True

    def __str__(self):
        return "Mixer " + self.__type + " [total " + str(len(self.__channel_list)) + "]"

    def __dir__(self):
        return [f"{self.__prefix}{i}" for i in range(1, len(self.__channel_list)+1)]

    def __getitem__(self, key):
        """ Get channel by number """
        if key not in range(1, len(self.__channel_list) + 1):
            raise IndexError(f"Parameter index must be in range [1, {len(self.__channel_list)}]")
        return self.__channel_list[key - 1]

    def __getattr__(self, attr):
        """ Get channel by name """
        item = attr.capitalize()
        if item.startswith(self.__prefix.capitalize()) and item.replace(self.__prefix.capitalize(), '').isdigit():
            return self.__channel_list[int(item.replace(self.__prefix.capitalize(), '')) - 1]
        else:
            # Handle default
            return super().__getattribute__(item)

    def __setattr__(self, key, value):
        if self.__freeze:
            raise TypeError("Channel lists are read-only")
        object.__setattr__(self, key, value)