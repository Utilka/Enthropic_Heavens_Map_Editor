from typing import Tuple


class Fleet:
    def __init__(self, name, units: int, coordinates: Tuple[int, int], jump_range: int = 0, turn_last_moved: int = 0):
        self.name = name
        self.units = units
        self._q, self._r = coordinates
        self.jump_range = jump_range
        self.turn_last_moved = turn_last_moved

    @property
    def coordinates(self):
        return self._q, self._r

    @coordinates.setter
    def coordinates(self, value):
        self._q, self._r = value

    @coordinates.deleter
    def coordinates(self):
        del self._q, self._r

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"Fleet(\"{self.name}\",{self.units},{self.coordinates},{self.jump_range})"


class SystemForce:
    def __init__(self, units: int, coordinates: Tuple[int, int]):
        self.units = units
        self._q, self._r = coordinates

    @property
    def coordinates(self):
        return self._q, self._r

    @coordinates.setter
    def coordinates(self, value):
        self._q, self._r = value

    @coordinates.deleter
    def coordinates(self):
        del self._q, self._r

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"SystemForce({self.units},{self.coordinates})"