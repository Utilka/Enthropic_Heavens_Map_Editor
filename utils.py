import math
import re
from itertools import groupby
from typing import NamedTuple, Union, Type, Tuple, List, TypedDict, Optional, Dict

import gspread
import numpy

from System_DB_handler import load_systems

star_systems = load_systems()


class Pointer(NamedTuple):
    column: Union[int, str]
    row: int

    # this annotates name of the google sheets page on which this pointer should exist
    sheet: Optional[str] = None

    def __str__(self):
        if isinstance(self.column, int):
            return f'R{self.row}C{self.column}'
        else:
            return f'{self.column}{self.row}'

    def make_absolute_pointer(self, index: int, sheet: str = None) -> 'Pointer':
        if sheet is None:
            if self.sheet is None:
                raise ValueError("sheet value was undefined both in object and in function call, cant determine page "
                                 "to which indexing to convert Pointer")
            else:
                sheet = self.sheet

        if sheet == "Star Systems":
            return Pointer(column=self.column, row=self.row + 3 + index * 16, sheet=sheet)
        elif sheet == "Fleets":
            return Pointer(column=self.column, row=self.row + 3 + index * 16, sheet=sheet)
        else:
            NotImplementedError("absolute indexing conversion for sheet types other then "
                                "'Star Systems' and 'Fleets' is not implemented")


class RangePointer(NamedTuple):
    start: Pointer
    end: Pointer

    # this annotates name of the google sheets page on which this pointer should exist
    sheet: Optional[str] = None

    def __str__(self):
        return f"{str(self.start)}:{str(self.end)}"


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
    "AP net": Pointer("K", 15, "Star Systems"),
    "AP Budget": Pointer("H", 11, "Star Systems"),
    "WU Progress": Pointer("G", 13, "Star Systems"),
    "WU Progress next T": Pointer("H", 13, "Star Systems"),
    "SF Unit count": Pointer("P", 13, "Star Systems"),
    "System q": Pointer("B", 2, "Star Systems"),
    "System r": Pointer("C", 2, "Star Systems"),
    "System Name": Pointer("F", 2, "Star Systems"),
    "Fleet q": Pointer("B", 2, "Fleets"),
    "Fleet r": Pointer("C", 2, "Fleets"),
    "Fleet Name": Pointer("F", 2, "Fleets"),
    "Fleet Unit count": Pointer("F", 5, "Fleets"),
    "Fleet Jump range": Pointer("K", 5, "Fleets"),
    "Fleet Turn Last Moved": Pointer("J", 7, "Fleets"),
    "System modifiers / projects": RangePointer(Pointer("M", 4), Pointer("M", 9), "Star Systems")
}

Unit_to_cell_translations = {
    "AP": "AP Budget",
}


class ThingToGet(NamedTuple):
    target_category: str  # "Star Systems" or "Fleets" or "Espionage"
    index: Union[str, int, Tuple[int, int]]
    # system index, or system coordinates (Tuple[int,int]) or fleet coordinates or whatever relevant in the category

    cell_name: str  # key in acell_relative_reference


def to_numeric_index(reference, index: Union[str, int, Tuple[int, int]]) -> int:
    if isinstance(index, str):
        return reference.name_ref[index]
    elif isinstance(index, tuple):
        return reference.coord_ref[f"{index[0]}, {index[1]}"]
    elif isinstance(index, int):
        return index
    else:
        raise TypeError


def get_coords_of_star_systems(names: List[str]) -> Dict[str, Tuple[int, int]]:
    # Using numpy's vectorized functions to compare the names and retrieve indices
    matches = numpy.vectorize(lambda x: x is not None and x.name in names)(star_systems)
    raw_coords = list(zip(*matches.nonzero()))

    return {star_systems[coord].name:(coord[0]-42,coord[1]-42) for coord in raw_coords}


def create_reference(player_sheet: gspread.Spreadsheet, target_category: str):
    reference = NamedTuple("reference", [("name_ref", Dict), ("coord_ref", Dict)])

    if target_category == "Star Systems":
        global_page = player_sheet.worksheet("Global")

        name_ref_raw = global_page.batch_get(["D8:E"], major_dimension="ROWS")[0]
        name_ref = {row[1]: int(row[0])-1 for row in name_ref_raw if len(row) == 2}

        name_coord_ref = get_coords_of_star_systems(list(name_ref.keys()))

        coordinate_ref = {f"{coords[0]}, {coords[1]}": int(name_ref[name]) for name, coords in name_coord_ref.items()}

        reference.name_ref = name_ref
        reference.coord_ref = coordinate_ref

    elif target_category == "Fleets":
        global_page = player_sheet.worksheet("Global")

        ref_raw = global_page.batch_get(["N8:P"], major_dimension="ROWS")

        name_ref = {row[2]: int(row[0]) for row in ref_raw if row[2] != ""}
        coordinate_ref = {row[1]: int(row[0]) for row in ref_raw if row[2] != ""}

        reference.name_ref = name_ref
        reference.coord_ref = coordinate_ref
    else:
        raise NotImplementedError

    return reference


def get_cells(player_sheet: gspread.Spreadsheet, things_to_get: List[ThingToGet]) -> List[Tuple[ThingToGet, str]]:
    results = []

    # Create a dictionary with ThingToGet objects as keys and their positions as values.
    # Will need later to return to user provided order
    original_positions = {thing: index for index, thing in enumerate(things_to_get)}

    # Group things_to_get by target_category
    things_to_get_sorted = sorted(things_to_get, key=lambda x: x.target_category)
    for target_category, group in groupby(things_to_get_sorted, key=lambda x: x.target_category):
        group_to_get = list(group)
        reference = create_reference(player_sheet, target_category)

        # Convert each index in the group to a cell pointer
        cell_pointers = [str(
            acell_relative_reference[item.cell_name].make_absolute_pointer(
                to_numeric_index(
                    reference,
                    item.index
                )
            )
        )
            for item in group_to_get]

        worksheet = player_sheet.worksheet(target_category)
        cell_values = worksheet.batch_get(cell_pointers)

        # Pair the original request with the cell value
        for thing, value in zip(group_to_get, cell_values):
            results.append((thing, value))

    # Sort the results by the original positions to return to user provided order
    results.sort(key=lambda x: original_positions[x[0]])

    return results


def is_integer(s: str) -> bool:
    if s[0] in ('-', '+'):  # Check for optional sign at the beginning
        return s[1:].isdigit()
    return s.isdigit()


def is_coordinate_on_map(coordinates: Tuple[int, int], map_shape: numpy.ndarray.shape) -> bool:
    is_q_on_map = ((coordinates[0] + 42) < map_shape[0]) and ((coordinates[0] + 42) > 0)
    is_r_on_map = ((coordinates[1] + 42) < map_shape[1]) and ((coordinates[1] + 42) > 0)
    return is_q_on_map and is_r_on_map
