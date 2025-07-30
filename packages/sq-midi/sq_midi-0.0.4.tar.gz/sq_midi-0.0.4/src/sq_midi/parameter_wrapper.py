from typing import Callable

class ParameterWrapper:
    """ Parameter wrapper class
        handles parameters
    """

    from sq_midi import Mixer
    from sq_midi.channel import Channel

    channel: Channel = None
    mixer: Mixer = None
    parameter_category: str = None
    parameter_type: object = None
    parameter_range: list = None
    parameter_map: Callable = None


    def __init__(
            self,
            mixer: Mixer,
            channel: Channel,
            parameter_category: str,
            parameter_type: object,
            parameter_range: list,
            parameter_map: Callable
        ):
        self.channel = channel
        self.mixer = mixer
        self.parameter_category = parameter_category
        self.parameter_type = parameter_type
        self.parameter_range = parameter_range
        self.parameter_map = parameter_map
        #print("Initializing Parameter Wrapper with " + parameter_category)

    def __getattr__(self, item):
        """ Handle parameter destination by name
            e.g. mixer.inputs[1].aux
                 mixer.inputs[1].mtx
        """
        #print("__getattr__ called " + item)
        if item not in self.channel.info[self.parameter_category]:
            raise ValueError(
                f"'{self.parameter_category}' parameter does not have destination type '{item}'"
                f"\nAvailable values: { ", ".join(self.channel.info[self.parameter_category].keys())}"
            )
        # Load handler here (avoiding circular dependency)
        from sq_midi.parameter_handler import ParameterHandler
        handler = ParameterHandler(self, item)
        # Return handler
        # If LR, then return directly
        return handler[1] if item == "lr" else handler

    def __setattr__(self, key, value):
        """ Used to set LR parameters (not indexed) """
        if key == "lr":
            from sq_midi.parameter_handler import ParameterHandler
            ParameterHandler(self, key)[1] = value
        else:
            if getattr(ParameterWrapper, key, False) is not False:
                super().__setattr__(key, value)
            else:
                raise ValueError(
                    f"'{self.parameter_category}' parameter does not have destination type '{key}'"
                    f"\nAvailable values: {", ".join(self.channel.info[self.parameter_category].keys())}"
                )