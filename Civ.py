import logging
import time
from itertools import chain
from typing import Dict

import gspread
import numpy
from oauth2client.service_account import ServiceAccountCredentials

from Forces import Fleet, SystemForce
from Star_System_utils import LocalAction
from System_DB_handler import load_systems
from utils import numeric_to_alphabetic_column, distance, \
    Highlight, highlight_color_translation, acell_relative_reference, \
    ThingToGet, RangePointer, Pointer

logging.basicConfig(level=logging.INFO,
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

# same important cells but in R1C1


def get_system_cell(sheet, system_index, cell_name) -> gspread.Cell:
    relative_Pointer = acell_relative_reference[cell_name]
    absolute_Pointer = relative_Pointer.make_absolute_pointer(system_index)
    returned_cell = sheet.acell(str(absolute_Pointer))
    time.sleep(1)
    return returned_cell


class Civ:
    def __init__(self, player_id: str, player_name: str, name: str, color: str, doctrine=None, fleets=None,
                 system_forces=None):
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
        self.turn_page = None

    def __str__(self):
        return f"Civ(\"{self.player_id}\",\"{self.player_name}\",\"{self.name}\",\"{self.color}\")"

    def __repr__(self):
        return f"Civ(\"{self.player_id}\",\"{self.player_name}\",\"{self.name}\",\"{self.color}\")"

    @property
    def player_sheet_name(self):
        return f"{self.player_id} {self.player_name} Player Sheet"

    @property
    def turn_sheet_name(self):
        return f"{self.player_id} {self.player_name} Turn Sheet"

    def explore_star_system(self, coordinates):
        self.explored_space[(coordinates[0] + 42, coordinates[1] + 42)] = True

    def open_gspread_connection(self, current_turn=-1):
        self.player_sheet: gspread.Spreadsheet = client.open(self.player_sheet_name)
        time.sleep(1)
        self.turn_sheet: gspread.Spreadsheet = client.open(self.turn_sheet_name)
        time.sleep(1)
        if current_turn != -1:
            self.turn_page: gspread.Worksheet = self.find_the_current_turn_page(current_turn)
            time.sleep(1)
        pass

    def close_gspread_connection(self):
        self.player_sheet = None
        self.turn_sheet = None
        self.turn_page = None

    def __reduce__(self):
        self.close_gspread_connection()
        return super().__reduce__()

    @property
    def system_action_first_row(self):
        if self.player_id == "117":
            return 28
        elif self.player_id == "120":
            return 23
        else:
            return 20

    @property
    def system_action_last_row(self):
        return self.system_action_first_row + 7

    def find_the_current_turn_page(self, current_turn) -> gspread.Worksheet:
        try:
            return next(page for page in self.turn_sheet.worksheets() if str(current_turn) in page.title)
        except StopIteration:
            logging.warning(f"Player {self.player_id} No turn page for turn {current_turn}")

    def set_AP_budgets(self):
        # TODO make batch update
        player_spreadsheet = self.player_sheet
        systems_sheet: gspread.Worksheet = player_spreadsheet.worksheet('Star Systems')

        time.sleep(1)
        logging.info(
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
        # TODO make batch update
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
        logging.info(f"set turn counter to {new_value} for {self.player_id} {self.player_name}")
        time.sleep(1)

    def update_explores(self):

        exploration_sheet: gspread.Worksheet = self.player_sheet.worksheet('Explored Systems')
        logging.debug(f"updating explores for {self.player_id} {self.player_name}")

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

        logging.info(f"uploaded {len(new_data)} explores for {self.player_id} {self.player_name}")
        time.sleep(1)

    def read_forces(self):
        logging.debug(f"Starting Fetching forces from sheet to DB for Player {self.player_id} {self.player_name}")

        self._read_fleets()
        if self.player_id == "117":
            self.system_forces = []
        else:
            self._read_system_forces()
        logging.info(f"Fetched forces from sheet to DB for Player {self.player_id} {self.player_name}")
        return 0

    def _read_fleets(self):
        fleet_sheet: gspread.Worksheet = self.player_sheet.worksheet('Fleets')
        number_of_fleets: int = len([fleet_name for fleet_name
                                     in self.player_sheet.sheet1.batch_get(["P8:P"], major_dimension="COLUMNS")[0]
                                     if fleet_name != ""])
        time.sleep(3)

        fleets_read_pointers = [
            (str(acell_relative_reference["Fleet q"].make_absolute_pointer(index)),
             str(acell_relative_reference["Fleet r"].make_absolute_pointer(index)),
             str(acell_relative_reference["Fleet Name"].make_absolute_pointer(index)),
             str(acell_relative_reference["Fleet Unit count"].make_absolute_pointer(index)),
             str(acell_relative_reference["Fleet Jump range"].make_absolute_pointer(index)),)
            for index in range(number_of_fleets)
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
        logging.info(f"Player {self.player_id}: fetched {len(fleets)} fleets from sheet to object")
        return 0

    def _read_system_forces(self):

        player_spreadsheet: gspread.Spreadsheet = self.player_sheet
        systems_sheet: gspread.Worksheet = player_spreadsheet.worksheet('Star Systems')
        number_of_systems: int = int(player_spreadsheet.sheet1.get("E4")[0][0])
        time.sleep(1)

        system_forces_read_pointers = [
            (str(acell_relative_reference["System q"].make_absolute_pointer(index)),
             str(acell_relative_reference["System r"].make_absolute_pointer(index)),
             str(acell_relative_reference["SF Unit count"].make_absolute_pointer(index)),)
            for index in range(number_of_systems)
        ]
        system_forces_read_pointers = list(chain.from_iterable(system_forces_read_pointers))  # flatten the list
        system_forces_raw = systems_sheet.batch_get(system_forces_read_pointers)
        time.sleep(1)
        system_forces = [
            SystemForce(int(system_forces_raw[i * 3 + 2][0][0]),
                        (int(system_forces_raw[i * 3 + 0][0][0]), int(system_forces_raw[i * 3 + 1][0][0])))
            for i in range(number_of_systems)]
        self.system_forces = system_forces
        logging.info(f"Player {self.player_id}: fetched {len(system_forces)} system forces from sheet to object")
        return 0

    def tick_fleets(self, current_turn):
        if self.turn_page is None:
            logging.warning(f"Player {self.player_id}: player has no turn page, cant perform Fleet Move")
            return 1

        logging.info(f"Player {self.player_id}: Performing Fleet Move")
        # special handling for misfitaid
        fleet_moves = self._get_fleet_moves()
        self._move_fleets(fleet_moves, current_turn)

        self._update_fleets()
        return 0

    def _get_fleet_moves(self):
        if self.player_id == "120":
            fleet_moves = self.turn_page.batch_get(["C3:10"], major_dimension="COLUMNS")[0]
            fleet_moves = [move[0:1] + move[2:4] + move[5:7] + move[7:8] for move in fleet_moves]
            pass

        # special handling for drako
        elif self.player_id == "117":
            fleet_moves = self.turn_page.batch_get(["C3:8"], major_dimension="COLUMNS")[0]
            # TODO add civilian fleet movement

        else:
            fleet_moves = self.turn_page.batch_get(["C3:8"], major_dimension="COLUMNS")[0]
        time.sleep(1)
        return fleet_moves

    def _move_fleets(self, fleet_moves, current_turn):
        cumulate_cells_to_highlight = {}
        for i, move in enumerate(fleet_moves):
            non_convertible_to_int_items = list(
                filter(lambda item: (not item[1].lstrip('-').isdigit()), enumerate(move[1:6])))
            if len(non_convertible_to_int_items) > 0:
                if len(list(filter(lambda item: item[1] != "", non_convertible_to_int_items))) > 0:
                    logging.info(f"Player {self.player_id} has strings in the in the cells "
                                 f"{numeric_to_alphabetic_column(3 + i)}{3}:{8 + (self.player_id == '120') * 2} = "
                                 f"{non_convertible_to_int_items}")
                    cell_column = numeric_to_alphabetic_column(i + 3)
                    problem_cells_index = f"{cell_column}3:{cell_column}{8 + (2 * (self.player_id == '120'))}"
                    cumulate_cells_to_highlight[problem_cells_index] = Highlight("red", "Failed to parse coordinates")
                    # TODO discord notification to GM
                continue

            move[1:5] = [int(val) for val in move[1:5]]

            try:
                fleet_moved: Fleet = next(fleet for fleet in self.fleets if str(move[0]) == fleet.name)
            except StopIteration:
                logging.error(
                    f"Player {self.player_id} Tried to move fleet {move[0]} but it wasnt found in the civ object ")
                # if player inputted some weird fleet name that is not in their fleet list, just ignore it and carry on
                cell_column = numeric_to_alphabetic_column(i + 3)
                problem_cells_index = f"{cell_column}3:{cell_column}{8 + (2 * (self.player_id == '120'))}"
                cumulate_cells_to_highlight[problem_cells_index] = Highlight("red", "Fleet not found in civ")
                # TODO discord notification to the player
                continue

            target_coordinates = (int(move[3]), int(move[4]))
            if distance(fleet_moved.coordinates, target_coordinates) > fleet_moved.jump_range:
                logging.error(
                    f"Player {self.player_id} Tried to move fleet {fleet_moved.name} further then jump range allows")
                cell_column = numeric_to_alphabetic_column(i + 3)
                problem_cells_index = f"{cell_column}3:{cell_column}{8 + (2 * (self.player_id == '120'))}"
                cumulate_cells_to_highlight[problem_cells_index] = Highlight("red", "Insufficient jump range")
                # TODO discord notification to the player
                continue

            if fleet_moved.turn_last_moved >= current_turn:
                logging.error(
                    f"Player {self.player_id} Tried to move fleet {fleet_moved.name} but it already moved this turn")
                cell_column = numeric_to_alphabetic_column(i + 3)
                problem_cells_index = f"{cell_column}3:{cell_column}{8 + (2 * (self.player_id == '120'))}"
                cumulate_cells_to_highlight[problem_cells_index] = Highlight("red", "Fleet moved this turn")
                # TODO discord notification to the player
                continue

            fleet_moved.coordinates = target_coordinates
            fleet_moved.turn_last_moved = current_turn
            cell_column = numeric_to_alphabetic_column(i + 3)
            problem_cells_index = f"{cell_column}3:{cell_column}{8 + (2 * (self.player_id == '120'))}"
            cumulate_cells_to_highlight[problem_cells_index] = Highlight("green", "Fleet moved")

        self.highlight_cells(self.turn_page, cumulate_cells_to_highlight)

    def _update_fleets(self):
        fleet_sheet: gspread.Worksheet = self.player_sheet.worksheet('Fleets')

        fleets_write_pointers = [{
            "range":
                f"{acell_relative_reference['Fleet q'].make_absolute_pointer(index)}:" +
                f"{acell_relative_reference['Fleet r'].make_absolute_pointer(index)}",
            'values': [fleet.coordinates]
        } for index, fleet in enumerate(self.fleets)]
        fleets_write_pointers += [{
            "range": f"{acell_relative_reference['Fleet Turn Last Moved'].make_absolute_pointer(index)}",
            'values': [[fleet.turn_last_moved]]
        } for index, fleet in enumerate(self.fleets)]
        fleet_sheet.batch_update(fleets_write_pointers)
        time.sleep(1)
        return 0

    @staticmethod
    def highlight_cells(target_page: gspread.Worksheet, cells_to_highlight: Dict[str, Highlight]):
        if len(cells_to_highlight) < 1:
            return
        # highlight
        formats = [{"range": cell_range, "format": highlight_color_translation[highlight.color]}
                   for cell_range, highlight in cells_to_highlight.items()]
        target_page.batch_format(formats)

        # add error notes
        # if a range was highlighted, insert note only in top-left most cell of it
        # (by cutting the range definition up to ":")
        notes = {cell_range.split(":")[0]: highlight.reason
                 for cell_range, highlight in cells_to_highlight.items()}
        target_page.insert_notes(notes)
        pass

    def process_system_actions(self):
        # check if turn page was found
        if self.turn_page is None:
            logging.warning(f"Player {self.player_id}: player has no turn page, cant process system actions")
            return 1

        cumulate_cells_to_highlight = {}
        # get actions
        raw_system_actions = []

        # special handling for misfitaid

        system_actions_range = f"C{self.system_action_first_row}:{self.system_action_last_row}"
        raw_system_actions = self.turn_page.batch_get([system_actions_range], major_dimension="COLUMNS")[0]

        logging.info(f"Player {self.player_id}: fetched {len(raw_system_actions)} systems actions")

        for i, raw_system_action in enumerate(raw_system_actions):
            raw_system_actions[i] = raw_system_action + [""]*(8-len(raw_system_action))


        system_actions = [LocalAction(system_q=raw_action[0], system_r=raw_action[1],
                                      action_type=raw_action[2], action_description=raw_action[3],
                                      action_expenditure=raw_action[6],
                                      action_status=raw_action[7],
                                      sheet_origin=RangePointer(
                                          start=Pointer(numeric_to_alphabetic_column(3 + i),
                                                        self.system_action_first_row),
                                          end=Pointer(numeric_to_alphabetic_column(3 + i),
                                                      self.system_action_last_row)
                                      ))
                          for i, raw_action in enumerate(raw_system_actions)]
        # ((self.player_id == "117") * 9) + ((self.player_id == "120") * 4)
        # verify resource expenditure
        # find needed cells

        Unit_to_cell_translations = {
            "AP": "AP Budget",
            "WU": "WU Progress"
        }
        things_to_check = []
        for action in system_actions:
            used_units = action.action_expenditure_coded.keys()
            cells_containing_units = [Unit_to_cell_translations.get(unit) for unit in used_units]
            for cell in cells_containing_units:
                things_to_check.append(
                    ThingToGet(target_category="Star Systems", index=(action.coordinates), cell_name=cell))

        # load previous projects

        # verify project completion conditions
        # project changes and resource subtraction
        pass


# 00 = {list: 7} ['19', '-24', 'build sci dev', 'Start Sci dev project with rest of capital AP', '', '', '40 + Capital AP Remains']
# 01 = {list: 7} ['19', '-24', 'build sus dev', '', '', '', '20']
# 02 = {list: 7} ['19', '-24', 'build ind dev', 'Use 7/10 project', '', '', '13']
# 03 = {list: 7} ['18', '-23', 'build sci dev', '', '', '', '40']
# 04 = {list: 7} ['18', '-23', 'build sus dev', '', '', '', '20']
# 05 = {list: 7} ['18', '-23', 'build ind dev', '', '', '', '16']
# 06 = {list: 7} ['17', '-22', 'build sci dev', '', '', '', '52']
# 07 = {list: 7} ['17', '-22', 'build ind dev', '', '', '', '20']
# 08 = {list: 7} ['16', '-21', 'build sci dev', '', '', '', '27']
# 09 = {list: 7} ['19', '-26', 'build sus dev', '', '', '', '10']
# 10 = {list: 7} ['17', '-24', 'build sus dev', '', '', '', '10']
# 11 = {list: 7} ['16', '-22', 'build sus dev', '', '', '', '10']
# 12 = {list: 7} ['19', '-26', 'build ind dev', 'Continue project', '', '', '7']
# 13 = {list: 7} ['17', '-24', 'build ind dev', 'Continue project', '', '', '7']
# 14 = {list: 7} ['16', '-22', 'build ind dev', 'Continue project', '', '', '7']

