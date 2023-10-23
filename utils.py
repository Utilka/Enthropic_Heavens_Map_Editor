import math
import re
from typing import NamedTuple, Union, Type, Tuple, List, TypedDict

import gspread
import numpy


class Pointer(NamedTuple):
    column: Union[int, str]
    row: int

    def __str__(self):
        if isinstance(self.column, int):
            return f'R{self.row}C{self.column}'
        else:
            return f'{self.column}{self.row}'


class RangePointer(NamedTuple):
    start: Pointer
    end: Pointer


class Coordinates(NamedTuple):
    q: int
    r: int

    @classmethod
    def from_tuple(cls, tuple_coords):
        return cls(*tuple_coords)


class TurnPageNotFoundError(Exception):
    pass


highlight_color_translation = {
    "green": {"backgroundColorStyle": {"rgbColor": {"red": 0.714, "green": 0.843, "blue": 0.659, "alpha": 1, }}},
    "yellow": {"backgroundColorStyle": {"rgbColor": {"red": 1, "green": 0.851, "blue": 0.400, "alpha": 1, }}},
    "red": {"backgroundColorStyle": {"rgbColor": {"red": 0.918, "green": 0.600, "blue": 0.600, "alpha": 1, }}},
}


class Highlight(NamedTuple):
    color: str
    reason: str


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


UNITS = [
    "AP", "SP", "IP", "WU", "Space Habitat",
    "Ionic Crystal", "Giga Lattice", "Amianthoid", "Mercurite",
    "Beryllium", "Glascore", "Adamantian", "Noviarium",
    "Rhodochrosite", "RedSang", "Bluecap Mold", "Eden Incense",
    "Starlings", "Superspuds", "Proto-Orchid", "Proto-spores",
    "Glassteel", "Bioforge Moss"
]

# Create a regular expression pattern
PATTERN = r'(?:(\d+)\s*)?\b(' + '|'.join([re.escape(unit) for unit in UNITS]) + r')s?\b'
CASE_INSENSITIVE_PATTERN = re.compile(PATTERN, re.IGNORECASE)

# Pattern for standalone numbers
NUMBER_PATTERN = re.compile(r'^\s*(\d+)\s*$')


def extract_units_quantity(s: str) -> Dict[str, int]:
    matches = CASE_INSENSITIVE_PATTERN.findall(s)

    # Convert matches to the desired dictionary format
    result = {}
    for match in matches:
        # If no quantity provided, default to 1
        quantity = int(match[0]) if match[0] else 1
        unit = match[1]
        result[unit] = quantity

    # Check for the default case
    if not result:
        number_match = NUMBER_PATTERN.match(s)
        if number_match:
            result["AP"] = int(number_match.group(1))

    return result


acell_relative_reference = {
    "AP net": Pointer("K", 15),
    "AP Budget": Pointer("H", 11),
    "WU Progress": Pointer("G", 13),
    "WU Progress next T": Pointer("H", 13),
    "SF Unit count": Pointer("P", 13),
    "System q": Pointer("B", 2),
    "System r": Pointer("C", 2),
    "System Name": Pointer("F", 2),
    "Fleet q": Pointer("B", 2),
    "Fleet r": Pointer("C", 2),
    "Fleet Name": Pointer("F", 2),
    "Fleet Unit count": Pointer("F", 5),
    "Fleet Jump range": Pointer("K", 5),
    "Fleet Turn Last Moved": Pointer("J", 7),
    "System modifiers / projects": RangePointer(Pointer("M", 4), Pointer("M", 9))
}

Unit_to_cell_translations = {
    "AP": "AP Budget",
}


class ThingToGet(TypedDict):
    target_category: str  # "System" or "Fleet" or "Espionage"
    index: Union[str, int, Tuple[int, int]]
    # system index, or system coordinates (Tuple[int,int]) or fleet coordinates or whatever relevant in the category
    cell_name: str  # key in acell_relative_reference


def get_cells(player_sheet: gspread.Spreadsheet, things_to_get: List[ThingToGet]) -> List[Tuple[ThingToGet, str]]:
    pass


def is_integer(s: str) -> bool:
    if s[0] in ('-', '+'):  # Check for optional sign at the beginning
        return s[1:].isdigit()
    return s.isdigit()


def is_coordinate_on_map(coordinates: Tuple[int, int], map_shape: numpy.ndarray.shape) -> bool:
    is_q_on_map = ((coordinates[0] + 42) < map_shape[0]) and ((coordinates[0] + 42) > 0)
    is_r_on_map = ((coordinates[1] + 42) < map_shape[1]) and ((coordinates[1] + 42) > 0)
    return is_q_on_map and is_r_on_map
