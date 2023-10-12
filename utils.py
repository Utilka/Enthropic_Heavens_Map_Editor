import math
from typing import NamedTuple, Union, Type, Tuple


class Pointer(NamedTuple):
    column: Union[int, str]
    row: int

    def __str__(self):
        if isinstance(self.column, int):
            return f'R{self.row}C{self.column}'
        else:
            return f'{self.column}{self.row}'


class Coordinates(NamedTuple):
    q: int
    r: int

    @classmethod
    def from_tuple(cls, tuple_coords):
        return cls(*tuple_coords)


class TurnPageNotFoundError(Exception):
    pass


def alphabetic_to_numeric_column(column_letters) -> int:
    return sum([(ord(column_letter.upper()) - 64) * ((ord("Z") - 64) ** i) for i, column_letter in
                enumerate(column_letters[::-1])])


def numeric_to_alphabetic_column(column_number) -> str:
    result = ''
    while column_number > 0:
        column_number, remainder = divmod(column_number - 1, 26)
        result = chr(65 + remainder) + result
    return result


def distance(a: Union[Coordinates, Tuple[int, int]],
             b: Union[Coordinates, Tuple[int, int]]) -> int:
    a = Coordinates(*a)
    b = Coordinates(*b)
    return int((abs(a.q - b.q) + abs(a.q + a.r - b.q - b.r) + abs(a.r - b.r)) / 2)


def get_system_sheet_pointer(system_index: int, relative_pointer: Pointer) -> Pointer:
    """
    Convert a relative pointer to a cell in a system to an absolute pointer on the system sheet.

    Args:
    - system_index (int): System index.
    - relative_pointer (Pointer): The relative pointer.

    Returns:
    - Pointer: The absolute pointer.
    """
    return Pointer(row=relative_pointer.row + 3 + system_index * 16, column=relative_pointer.column)

def get_fleet_sheet_pointer(fleet_index: int, relative_pointer: Pointer) -> Pointer:
    """
    Convert a relative pointer to a cell in a system to an absolute pointer on the system sheet.

    Args:
    - system_index (int): System index.
    - relative_pointer (Pointer): The relative pointer.

    Returns:
    - Pointer: The absolute pointer.
    """
    return Pointer(row=relative_pointer.row + 3 + fleet_index * 16, column=relative_pointer.column)
