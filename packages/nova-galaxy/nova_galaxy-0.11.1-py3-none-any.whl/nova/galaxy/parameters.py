"""Parameters are input values for Galaxy tools."""

from typing import Any, Dict


class Parameters:
    """Specialized map wrapper used as an input to a Galaxy tool."""

    def __init__(self) -> None:
        self.inputs: Dict[str, Any] = {}

    def add_input(self, name: str, value: Any) -> None:
        self.inputs[name] = value

    def change_input_value(self, name: str, new_value: Any) -> None:
        if self.inputs[name]:
            self.inputs[name] = new_value

    def remove_input(self, name: str) -> None:
        self.inputs.pop(name)
