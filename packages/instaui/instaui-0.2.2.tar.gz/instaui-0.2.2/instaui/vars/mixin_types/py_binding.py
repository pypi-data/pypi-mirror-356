from abc import ABC, abstractmethod
from typing import Sequence


class CanInputMixin(ABC):
    @abstractmethod
    def _to_input_config(self):
        pass


class CanOutputMixin(ABC):
    @abstractmethod
    def _to_output_config(self):
        pass


def _assert_outputs_be_can_output_mixin(outputs: Sequence):
    for output in outputs:
        if not isinstance(output, CanOutputMixin):
            raise TypeError("The outputs parameter must be a `ui.state`")
