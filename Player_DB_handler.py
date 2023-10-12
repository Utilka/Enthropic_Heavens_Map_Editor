import logging
import pickle
import time
from itertools import chain
from typing import Tuple

import gspread
import numpy
from oauth2client.service_account import ServiceAccountCredentials

from System_DB_handler import load_systems
from utils import Pointer, TurnPageNotFoundError, alphabetic_to_numeric_column, numeric_to_alphabetic_column, distance, \
    get_system_sheet_pointer

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler('my_log_file.log'),
                        logging.StreamHandler()
                    ])

hex_index = numpy.load("data/hex_types.npy", allow_pickle=True)

all_systems = load_systems()
CREDENTIALS_FILE = 'smiling-spider-398713-aee239712464.json'
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
client = gspread.authorize(creds)

# reference of all important cells in a block (system or fleet) with a A1 excel notation
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
}

# same important cells but in R1C1
cell_relative_reference = {
    cell_name: Pointer(
        row=cell_pointer.row,
        column=alphabetic_to_numeric_column(cell_pointer.column)
    )
    for cell_name, cell_pointer in acell_relative_reference.items()
}


def get_system_cell(sheet, system_index, cell_name) -> gspread.Cell:
    relative_row, relative_col = cell_relative_reference[cell_name]
    absolute_row, absolute_col = get_system_sheet_pointer(system_index, Pointer(relative_row, relative_col))
    returned_cell = sheet.cell(absolute_row, absolute_col)
    time.sleep(1)
    return returned_cell


class Civ:
    def __init__(self, player_id, player_name, name, color: str, doctrine=None, fleets=None, system_forces=None):
        if system_forces is None:
            system_forces = []
        if fleets is None:
            fleets = []
        self.player_id = player_id
        self.player_name = player_name
        self.name = name
        self.color = color
        self.fleets = fleets
        self.system_forces = system_forces
        self.doctrine = doctrine
        self.explored_space = numpy.full(hex_index.shape, False)
        self.player_sheet = None
        self.turn_sheet = None

    def __str__(self):
        return f"Civ(\"{self.player_id}\",\"{self.player_name}\",\"{self.name}\",\"{self.color}\")"

    def __repr__(self):
        return f"Civ(\"{self.player_id}\",\"{self.player_name}\",\"{self.name}\",\"{self.color}\",\"{self.doctrine}\",{self.fleets},{self.system_forces})"

    @property
    def player_sheet_name(self):
        return f"{self.player_id} {self.player_name} Player Sheet"

    @property
    def turn_sheet_name(self):
        return f"{self.player_id} {self.player_name} Turn Sheet"

    def explore_star_system(self, coordinates):
        self.explored_space[(coordinates[0] + 42, coordinates[1] + 42)] = True

    def open_gspread_connection(self):
        self.player_sheet = client.open(self.player_sheet_name)
        time.sleep(1)
        self.turn_sheet = client.open(self.turn_sheet_name)
        time.sleep(1)

    def close_gspread_connection(self):
        self.player_sheet = None
        self.turn_sheet = None

    def __reduce__(self):
        self.close_gspread_connection()
        # Return the reconstructing information.
        # I'm assuming all arguments for __init__ are picklable here.
        return (self.__class__, (
            self.player_id, self.player_name, self.name, self.color, self.doctrine, self.fleets, self.system_forces))

    def set_AP_budgets(self):
        player_spreadsheet = self.player_sheet
        systems_sheet: gspread.Worksheet = player_spreadsheet.worksheet('Star Systems')

        time.sleep(1)
        logging.debug(
            f"setting AP budget for {player_spreadsheet.title},{(systems_sheet.row_count - 3) // 16} systems indexed")
        for i in range((systems_sheet.row_count - 3) // 16):

            AP_net_cell = get_system_cell(systems_sheet, i, "AP net")
            time.sleep(1)
            AP_net = AP_net_cell.numeric_value
            if AP_net is None:
                continue
            if AP_net < 0:
                systems_sheet.insert_note(AP_net_cell.address, "Negative AP net, needs fix")
                time.sleep(1)
                logging.error(
                    f"{player_spreadsheet.title},{systems_sheet.title},{AP_net_cell.address} Negative AP net, needs fix")

            AP_budget_cell = get_system_cell(systems_sheet, i, "AP Budget")

            if AP_budget_cell.numeric_value > 0:
                logging.info(
                    f"{player_spreadsheet.title},{systems_sheet.title},{AP_net_cell.address} AP budget wasn't 0, but "
                    f"instead {AP_budget_cell.value}")
            systems_sheet.update_acell(AP_budget_cell.address, AP_net)

    def tick_WU_growth(self):
        player_spreadsheet = self.player_sheet
        systems_sheet: gspread.Worksheet = player_spreadsheet.worksheet('Star Systems')
        logging.debug(
            f"ticking WU growth for {player_spreadsheet.title},{(systems_sheet.row_count - 3) // 16} systems indexed")
        time.sleep(1)
        for i in range((systems_sheet.row_count - 3) // 16):

            WU_Progress_next_T_cell = get_system_cell(systems_sheet, i, "WU Progress next T")
            time.sleep(1)
            WU_Progress_next_T = WU_Progress_next_T_cell.numeric_value
            if WU_Progress_next_T is None:
                continue
            if WU_Progress_next_T < 1:
                logging.info(
                    f"{player_spreadsheet.title},{systems_sheet.title},{WU_Progress_next_T_cell.address} WU Progress "
                    f"is being set to bellow 1 ({WU_Progress_next_T}) might need LM attention")
            WU_Progress_cell = get_system_cell(systems_sheet, i, "WU Progress")
            time.sleep(1)
            systems_sheet.update_acell(WU_Progress_cell.address, WU_Progress_next_T)
            time.sleep(1)

    def set_IP_budget(self):
        player_spreadsheet = self.player_sheet
        global_sheet: gspread.Worksheet = player_spreadsheet.worksheet('Global')
        logging.debug(f"setting IP budget for {player_spreadsheet.title}")
        IP_prod_cell = global_sheet.acell("L4")
        time.sleep(1)
        IP_prod = int(IP_prod_cell.numeric_value)
        IP_budget_cell = global_sheet.acell("M4")
        time.sleep(1)
        global_sheet.update_acell(IP_budget_cell.address, IP_prod)
        time.sleep(1)

    def set_turn_counter(self, new_value):
        player_spreadsheet = self.player_sheet
        global_sheet: gspread.Worksheet = player_spreadsheet.worksheet('Global')
        time.sleep(1)
        logging.debug(f"setting turn counter for {player_spreadsheet.title}")
        global_sheet.update_acell("A2", new_value)
        time.sleep(1)

    def update_explores(self):
        exploration_sheet: gspread.Worksheet = self.player_sheet.worksheet('Explored Systems')

        indexes = numpy.where(self.explored_space)
        new_data = [["Short Coords", "q", "r", "Short Description", "Stellar Bodies Description"]]

        for i in range(indexes[0].size):
            new_data.append(
                [f"({indexes[0][i] - 42}, {indexes[1][i] - 42})", str(indexes[0][i] - 42), str(indexes[1][i] - 42),
                 all_systems[(indexes[0][i], indexes[1][i])].short_description,
                 all_systems[(indexes[0][i], indexes[1][i])].stellar_bod_description])

        # Adding data to the Google Sheet using batch operation
        # worksheet = sh.add_worksheet(title=f'Sheet{civ.player_id}', rows=len(new_data), cols=len(new_data[0]))
        # cell_list = exploration_sheet.range(1, 1, len(new_data), len(new_data[0]))

        exploration_sheet.batch_update([{
            "range": f"A1:{numeric_to_alphabetic_column(len(new_data[0]))}{len(new_data)}",
            'values': new_data,
        }])
        time.sleep(1)

    def read_forces(self):
        logging.info(f"Player {self.player_id} Fetching forces from sheet to DB")
        self._read_fleets()
        if self.player_id == "117":
            self.system_forces = []
        else:
            self._read_system_forces()
        return 0

    def _read_fleets(self):
        fleet_sheet: gspread.Worksheet = self.player_sheet.worksheet('Fleets')
        number_of_fleets: int = len([fleet_name for fleet_name
                                     in self.player_sheet.sheet1.batch_get(["P8:P"], major_dimension="COLUMNS")[0]
                                     if fleet_name != ""])
        time.sleep(3)

        fleets_read_pointers = [
            (str(get_system_sheet_pointer(i, acell_relative_reference["Fleet q"])),
             str(get_system_sheet_pointer(i, acell_relative_reference["Fleet r"])),
             str(get_system_sheet_pointer(i, acell_relative_reference["Fleet Name"])),
             str(get_system_sheet_pointer(i, acell_relative_reference["Fleet Unit count"])),
             str(get_system_sheet_pointer(i, acell_relative_reference["Fleet Jump range"])),)
            for i in range(number_of_fleets)
        ]
        fleets_read_pointers = list(chain.from_iterable(fleets_read_pointers))  # flatten the list
        fleets_raw = fleet_sheet.batch_get(fleets_read_pointers)
        time.sleep(1)
        fleets = [
            Fleet(fleets_raw[i * 3 + 2][0][0],
                  int(fleets_raw[i * 3 + 3][0][0]),
                  (int(fleets_raw[i * 3 + 0][0][0]), int(fleets_raw[i * 3 + 1][0][0])),
                  int(fleets_raw[i * 3 + 4][0][0]))
            for i in range(number_of_fleets)
        ]
        self.fleets = fleets
        return 0

    def _read_system_forces(self):

        player_spreadsheet: gspread.Spreadsheet = self.player_sheet
        systems_sheet: gspread.Worksheet = player_spreadsheet.worksheet('Star Systems')
        number_of_systems: int = int(player_spreadsheet.sheet1.get("E4")[0][0])
        time.sleep(1)

        system_forces_read_pointers = [
            (str(get_system_sheet_pointer(i, acell_relative_reference["System q"])),
             str(get_system_sheet_pointer(i, acell_relative_reference["System r"])),
             str(get_system_sheet_pointer(i, acell_relative_reference["SF Unit count"])),)
            for i in range(number_of_systems)
        ]
        system_forces_read_pointers = list(chain.from_iterable(system_forces_read_pointers))  # flatten the list
        system_forces_raw = systems_sheet.batch_get(system_forces_read_pointers)
        time.sleep(1)
        system_forces = [
            SystemForce(int(system_forces_raw[i * 3 + 2][0][0]),
                        (int(system_forces_raw[i * 3 + 0][0][0]), int(system_forces_raw[i * 3 + 1][0][0])))
            for i in range(number_of_systems)]
        self.system_forces = system_forces
        return 0

    def _find_the_current_turn_page(self, current_turn) -> gspread.Worksheet:
        try:
            return next(page for page in self.turn_sheet.worksheets() if str(current_turn) in page.title)
        except StopIteration:
            raise TurnPageNotFoundError(f"Turn Page for a turn '{current_turn}' was not found")

    def tick_fleets(self, current_turn):

        logging.info(f"Player {self.player_id} Performing Fleet Move")
        try:
            turn_page = self._find_the_current_turn_page(current_turn)
        except TurnPageNotFoundError:
            logging.error(f"Player {self.player_id} No Turn Sheet for turn {current_turn}")
            return 2  # i guess 2 can be error code for no turn sheet lol

        # special handling for misfitaid
        if self.player_id == "120":
            fleet_moves = turn_page.batch_get(["C3:10"], major_dimension="COLUMNS")[0]
            fleet_moves = [move[0:1] + move[2:4] + move[5:7] + move[7:8] for move in fleet_moves]
            pass

        # special handling for drako
        elif self.player_id == "117":
            fleet_moves = turn_page.batch_get(["C3:8"], major_dimension="COLUMNS")[0]
            # TODO add civilian fleet movement

        else:
            fleet_moves = turn_page.batch_get(["C3:8"], major_dimension="COLUMNS")[0]


        time.sleep(1)
        self._move_fleets(fleet_moves, current_turn)
        return 0

    def _move_fleets(self, fleet_moves, current_turn):
        cumulate_cells_to_highlight = []
        for i, move in enumerate(fleet_moves):
            non_convertible_to_int_items = list(filter(lambda item: not item[1].lstrip('-').isdigit(), enumerate(move[1:6])))
            if non_convertible_to_int_items:
                logging.info(f"Player {self.player_id} has strings in the in the cells "
                             f"{numeric_to_alphabetic_column(3 + i)}{3}:{8 + (self.player_id == '120') * 2} = "
                             f"{non_convertible_to_int_items}")
                # TODO add cell highlight in turn sheet and notification to GM
                continue

            move[1:6] = [int(val) for val in move[1:6]]

            try:
                fleet_moved: Fleet = next(fleet for fleet in self.fleets if str(move[0]) == fleet.name)
            except StopIteration:
                logging.error(
                    f"Player {self.player_id} Tried to move fleet {move[0]} but it wasnt found in the civ object ")
                # if player inputted some weird fleet name that is not in their fleet list, just ignore it and carry on
                # TODO add cell highlight in turn sheet and notification to the player
                continue

            target_coordinates = (int(move[3]), int(move[4]))
            if distance(fleet_moved.coordinates, target_coordinates) > fleet_moved.jump_range:
                logging.error(
                    f"Player {self.player_id} Tried to move fleet {fleet_moved.name} further then jump range allows")
                # TODO add cell highlight in turn sheet and notification to the player
                continue
            if fleet_moved.turn_last_moved >= current_turn:
                logging.error(
                    f"Player {self.player_id} Tried to move fleet {fleet_moved.name} but it already moved this turn")
                # TODO add cell highlight in turn sheet and notification to the player
                continue
            fleet_moved.coordinates = target_coordinates
            fleet_moved.turn_last_moved = current_turn

        self._highlight_turn_cells(cumulate_cells_to_highlight)
        self._update_fleets()

    def _update_fleets(self):
        fleet_sheet: gspread.Worksheet = self.player_sheet.worksheet('Fleets')

        fleets_write_pointers = [{
            "range": (
                f"{get_system_sheet_pointer(i, acell_relative_reference['Fleet q'])}:"
                f"{get_system_sheet_pointer(i, acell_relative_reference['Fleet r'])}",),
            'values': [fleet.coordinates]
        } for i, fleet in enumerate(self.fleets)]
        fleets_write_pointers += [{
            "range": (
                f"{get_system_sheet_pointer(i, acell_relative_reference['Fleet Turn Last Moved'])}",),
            'values': [fleet.turn_last_moved]
        } for i, fleet in enumerate(self.fleets)]
        fleet_sheet.batch_update(fleets_write_pointers)
        time.sleep(1)
        return 0

    def _highlight_turn_cells(self, cells_to_highlight):
        raise NotImplemented()


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


def load_civs():
    with open('Player_DB.pickle', 'rb') as f:
        return pickle.load(f)


def save_civs(all_civs):
    with open('Player_DB.pickle', 'wb') as f:
        pickle.dump(all_civs, f)


def start_game():
    spawns = [
        ("Xaltios", (19, -24), "The Arcturan Caliphate", "#A33084"),
        ("Toxiq", (-33, 29), "Steels Ambit", "#8c22b4"),
        ("nwlr_tv", (-24, 8), "Taxpm-Yyn Covenant", "#f2cc0d"),
        ("constantinos2", (33, -30), "Istionian Planetary Union", "#6A0D98"),
        ("georgell", (-11, 30), "Xerum Exploratory Republic", "#07a895"),
        ("jaguar162", (11, 6), None, "#326fa8"),
        ("sppucke", (-17, -3), "The Umbral Collective", "#0FAD3E"),
        ("brianofthewoods", (30, -3), "Resinalwahl", "#2cffdf"),
        ("mr._saul_goodman", (-11, 18), "Alpheria", "#B60000"),
        ("Storm_3210", (10, -25), "The Knights of Nekar", "#5496af"),
        ("thatonefoxy", (19, 14), "The Foundation", "#492C5D"),
        ("rhysonasi", (-24, -12), "Chosen of Nishchiyeh", "#00e600"),
        ("triple_zero", (23, -15), "Vracronica", "#851D2D"),
        ("Mortron42", (0, 21), "United Clans of the Sorzal", "#efeb2b"),
        ("Lizardwizard__", (-38, 4), "Cerin unity united", "#00ffff"),
        ("the_flying_meme", (9, -6), "Floof", "#3047cf"),
        ("drakos", (-6, -4), "Kalrani Startrate Cooperative", "#FFD700"),
        ("Hirisu", (-7, -23), "Second Eclipson Dominion", "#ffDDff"),
    ]
    all_civs = load_civs()
    for i in range(len(spawns)):
        civ = Civ(str(100 + 1 + i), spawns[i][0], spawns[i][2], spawns[i][3],
                  system_forces=[SystemForce(5, spawns[i][1])])
        civ.explore_star_system(spawns[i][1])
        all_civs.append(civ)

    save_civs(all_civs)
    print(load_civs())


def print_colors():
    all_civs = load_civs()
    print("[")
    for civ in all_civs:
        print(f'("{civ.player_id}","{civ.player_name}","{civ.color}"),')

    print("]")


def test():
    all_civs = load_civs()
    # xal_civ: Civ = all_civs[0]
    # xal_civ.open_gspread_connection()
    # for civ in all_civs:
    #     civ.open_gspread_connection()
    #     civ.read_forces()
    #     civ.close_gspread_connection()
    # save_civs(all_civs)
    # test_civ: Civ = all_civs[2]
    # test_civ.open_gspread_connection()
    # test_civ.tick_fleets(27)
    pass


if __name__ == '__main__':
    test()
    # all_civs = load_civs()
    # pass
    # save_civs(all_civs)
    # pass
