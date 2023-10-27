import logging
import pprint
import time
from copy import deepcopy
from itertools import chain, groupby
from typing import Dict, List

import gspread
import numpy
from oauth2client.service_account import ServiceAccountCredentials

from Forces import Fleet, SystemForce
from Star_System_utils import LocalAction, extract_project, get_project, Project, merge_project_pools, merge_edit_pools
from System_DB_handler import load_systems
from utils import numeric_to_alphabetic_column, distance, \
    Highlight, highlight_color_translation, acell_relative_reference, \
    ThingToGet, RangePointer, Pointer, get_cells, convert_coords_s_2_t, ThingToWrite, write_cells, acell

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

# same important cells but in R1C1


def get_system_cell(sheet, system_index, cell_name) -> gspread.Cell:
    relative_Pointer = acell_relative_reference[cell_name]
    absolute_Pointer = relative_Pointer.make_absolute_pointer(system_index)
    returned_cell = sheet.acell(str(absolute_Pointer))
    # time.sleep(1)
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
        # time.sleep(1)
        self.turn_sheet: gspread.Spreadsheet = client.open(self.turn_sheet_name)
        # time.sleep(1)
        if current_turn != -1:
            self.turn_page: gspread.Worksheet = self.find_the_current_turn_page(current_turn)
            # time.sleep(1)
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

        # time.sleep(1)
        logging.info(
            f"setting AP budget for {player_spreadsheet.title},{(systems_sheet.row_count - 3) // 16} systems indexed")
        for i in range((systems_sheet.row_count - 3) // 16):

            AP_net_cell = get_system_cell(systems_sheet, i, "AP net")
            # time.sleep(1)
            AP_net = AP_net_cell.numeric_value
            if AP_net is None:
                continue
            if AP_net < 0:
                systems_sheet.insert_note(AP_net_cell.address, "Negative AP net, needs fix")
                # time.sleep(1)
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
        # time.sleep(1)
        for i in range((systems_sheet.row_count - 3) // 16):

            WU_Progress_next_T_cell = get_system_cell(systems_sheet, i, "WU Progress next T")
            # time.sleep(1)
            WU_Progress_next_T = WU_Progress_next_T_cell.numeric_value
            if WU_Progress_next_T is None:
                continue
            if WU_Progress_next_T < 1:
                logging.info(
                    f"{player_spreadsheet.title},{systems_sheet.title},{WU_Progress_next_T_cell.address} WU Progress "
                    f"is being set to bellow 1 ({WU_Progress_next_T}) might need LM attention")
            WU_Progress_cell = get_system_cell(systems_sheet, i, "WU Progress")
            # time.sleep(1)
            systems_sheet.update_acell(WU_Progress_cell.address, WU_Progress_next_T)
            # time.sleep(1)

    def set_IP_budget(self):
        player_spreadsheet = self.player_sheet
        global_sheet: gspread.Worksheet = player_spreadsheet.worksheet('Global')
        logging.debug(f"setting IP budget for {player_spreadsheet.title}")
        IP_prod_cell = global_sheet.acell("L4")
        # time.sleep(1)
        IP_prod = int(IP_prod_cell.numeric_value)
        IP_budget_cell = global_sheet.acell("M4")
        # time.sleep(1)
        global_sheet.update_acell(IP_budget_cell.address, IP_prod)
        # time.sleep(1)

    def set_turn_counter(self, new_value):
        player_spreadsheet = self.player_sheet
        global_sheet: gspread.Worksheet = player_spreadsheet.worksheet('Global')
        # time.sleep(1)
        logging.debug(f"setting turn counter for {player_spreadsheet.title}")
        global_sheet.update_acell("A2", new_value)
        logging.info(f"set turn counter to {new_value} for {self.player_id} {self.player_name}")
        # time.sleep(1)

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
        # time.sleep(1)

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
        # time.sleep(3)

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
        # time.sleep(1)
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
        # time.sleep(1)

        system_forces_read_pointers = [
            (str(acell_relative_reference["System q"].make_absolute_pointer(index)),
             str(acell_relative_reference["System r"].make_absolute_pointer(index)),
             str(acell_relative_reference["SF Unit count"].make_absolute_pointer(index)),)
            for index in range(number_of_systems)
        ]
        system_forces_read_pointers = list(chain.from_iterable(system_forces_read_pointers))  # flatten the list
        system_forces_raw = systems_sheet.batch_get(system_forces_read_pointers)
        # time.sleep(1)
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
            raw_fleet_moves = self.turn_page.batch_get(["C3:11"], major_dimension="COLUMNS")[0]
            raw_fleet_moves = [move[0:1] + move[2:4] + move[5:7] + move[7:8] for move in raw_fleet_moves]
            pass

        # special handling for drako
        elif self.player_id == "117":
            raw_fleet_moves = self.turn_page.batch_get(["C3:9"], major_dimension="COLUMNS")[0]
            # TODO add civilian fleet movement

        else:
            raw_fleet_moves = self.turn_page.batch_get(["C3:9"], major_dimension="COLUMNS")[0]
        # time.sleep(1)

        for i, raw_fleet_move in enumerate(raw_fleet_moves):
            raw_fleet_moves[i] = raw_fleet_move + [""] * (7 - len(raw_fleet_move))

        logging.info(f"Player {self.player_id}: fetched {len(raw_fleet_moves)} raw fleet moves")

        return raw_fleet_moves

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
        # time.sleep(1)
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
        notes = {cell_range.split(":")[-1]: highlight.reason
                 for cell_range, highlight in cells_to_highlight.items()}
        target_page.insert_notes(notes)
        pass

    def process_system_actions(self):
        # check if turn page was found
        if self.turn_page is None:
            logging.warning(f"Player {self.player_id}: player has no turn page, cant process system actions")
            return 1

        system_actions = self.get_current_system_actions()
        logging.info(f"Player {self.player_id}: fetched {len(list(chain(system_actions)))} system actions")

        existing_project_pool = self.load_relevant_existing_projects(system_actions)
        logging.info(
            f"Player {self.player_id}: fetched {len(list(chain(existing_project_pool)))} existing projects pool")

        resource_pool = self.get_relevant_resources(system_actions)
        logging.info(f"Player {self.player_id}: fetched {len(list(chain(resource_pool)))} resources")

        new_project_pool = self.execute_actions(resource_pool, system_actions)
        logging.info(f"Player {self.player_id}: created {len(list(chain(new_project_pool)))} new projects")

        project_pool = merge_project_pools(existing_project_pool, new_project_pool)
        logging.info(f"Player {self.player_id}: {len(list(chain(project_pool)))} projects remained after merging")

        self.fetch_data_for_projects_verification(project_pool)

        # complete projects and accumulate deltas
        deltas = {}
        self.complete_projects_and_acumulate_deltas(deltas, project_pool)

        # convert relative deltas to absolute updates
        edits, originals = self.deltas_to_absolute_changes(deltas)

        # compile changes that will store projects and add them to edits
        # fetch all rows in system which had projects
        carry_over_info = self.fetch_mod_proj_rows(project_pool)

        # remove projects with 0 investment
        saved_projects_str = self.remove_proj_with_0_investment(project_pool)

        # add updated projects in empty spaces
        self.add_current_projects_to_carry(carry_over_info, saved_projects_str)

        # add carry over info to edit list
        self.add_carry_to_edits(carry_over_info, edits)

        # add resources to the edit list
        self.add_actual_resourses_to_edit(edits, resource_pool)

        pass
        pp = pprint.PrettyPrinter()
        pp.pprint(edits)
        self.do_feedback_on_actions(system_actions)

        things_to_write = []
        for system_coord, local_edits in edits.items():
            for cell_name, value in local_edits.items():
                things_to_write.append(ThingToWrite(target_category="Star Systems",
                                                    index=convert_coords_s_2_t(system_coord),
                                                    cell_name=cell_name,
                                                    new_value=value))
        write_cells(self.player_sheet,things_to_write)

        # apply the edits

    def deltas_to_absolute_changes(self, deltas):
        things_to_get = []
        for system_coords, local_delta in deltas.items():
            for cell_name, change in local_delta.items():
                pointer = acell[cell_name]
                things_to_get.append(ThingToGet(target_category=pointer.sheet_name,
                                                index=convert_coords_s_2_t(system_coords),
                                                cell_name=cell_name))
        response = get_cells(self.player_sheet, things_to_get)
        raw_values_pool = {}
        for thing, value in response:
            if f"{thing.index[0]}, {thing.index[1]}" not in raw_values_pool:
                raw_values_pool[f"{thing.index[0]}, {thing.index[1]}"] = {}
            raw_values_pool[f"{thing.index[0]}, {thing.index[1]}"][thing.cell_name] = value
        edits = merge_edit_pools(raw_values_pool, deltas)
        return edits, raw_values_pool

    def complete_projects_and_acumulate_deltas(self, deltas, project_pool):
        for system_coords, projects in project_pool.items():
            deltas[system_coords] = {}
            for project_name, project in projects.items():
                completions = project.complete()
                changes = deepcopy(project.on_completion)
                for cell, change in changes.items():
                    for i, row in enumerate(change):
                        for j, value in enumerate(row):
                            if isinstance(value, int):
                                changes[cell][i][j] = value * completions

                    if completions > 0:
                        # Merge with existing edits of same cell
                        if cell in deltas[system_coords]:
                            deltas[system_coords][cell] = Project.merge_changes(deltas[system_coords][cell],
                                                                                changes[cell])
                        else:
                            deltas[system_coords][cell] = changes[cell]

    def add_actual_resourses_to_edit(self, edits, resource_pool):
        Unit_to_cell_translations = {
            "AP": "AP Budget",
            "WU": "WU Progress"
        }
        for coordinate, resources in resource_pool.items():
            if coordinate not in edits:
                edits[coordinate] = {}
            for resource, quantity in resources.items():
                cell_name = Unit_to_cell_translations[resource]
                edits[coordinate][cell_name] = [[quantity]]

    def add_carry_to_edits(self, carry_over_info, edits):
        for coord, proj_section in carry_over_info.items():
            if coord not in edits:
                edits[coord] = {}
            edits[coord]["System modifiers / projects"] = proj_section

    def add_current_projects_to_carry(self, carry_over_info, saved_projects_str):
        proj_section_length = 6
        for coord in carry_over_info:
            carry_over_info[coord].extend(saved_projects_str.get(coord, []))
            # trim the list to len proj_section_length (6) forced
            carry_over_info[coord] = carry_over_info[coord][:proj_section_length]
            carry_over_info[coord].extend([['']] * (proj_section_length - len(carry_over_info[coord])))

    def remove_proj_with_0_investment(self, project_pool):
        saved_projects = {}
        for system_coord in project_pool:
            saved_projects[system_coord] = []
            for proj_name in project_pool[system_coord]:
                if sum(project_pool[system_coord][proj_name].progress_made.values()) > 0:
                    saved_projects[system_coord].append(project_pool[system_coord][proj_name])

            saved_projects[system_coord].sort(key=lambda project: sum(project.progress_made.values()))
        saved_projects_str = {system_coord: [[project.sheet_save_form] for project in proj_list]
                              for system_coord, proj_list in saved_projects.items()}
        return saved_projects_str

    def fetch_mod_proj_rows(self, project_pool):
        things_to_check = []
        for system_coords in project_pool.keys():
            things_to_check.append(ThingToGet(target_category="Star Systems",
                                              index=convert_coords_s_2_t(system_coords),
                                              cell_name="System modifiers / projects"))
        response = get_cells(self.player_sheet, things_to_check)
        # remove from response
        raw_mod_proj_pool = {f"{item[0].index[0]}, {item[0].index[1]}": item[1] for item in
                             response}
        carry_over_info: Dict[str, List[List[str]]] = {}
        for coord, rows in raw_mod_proj_pool.items():
            new_rows = []
            for i, row in enumerate(rows):
                if len(row) == 0:
                    continue
                cell = row[0]
                if cell.startswith("Project"):
                    continue
                elif cell == "":
                    continue
                else:
                    new_rows.append([cell])
            carry_over_info[coord] = new_rows
        return carry_over_info

    # def update_resourses(self, resource_pool):
    #
    #     things_to_write = []
    #     for coordinate, resources in resource_pool.items():
    #         for resource, quantity in resources.items():
    #             cell_name = Unit_to_cell_translations[resource]
    #             things_to_write.append(
    #                 ThingToWrite(target_category="Star Systems", index=coordinate,
    #                              cell_name=cell_name, new_value=[[quantity]]))
    #     write_cells(self.player_sheet, things_to_write)

    def fetch_data_for_projects_verification(self, project_pool):
        things_to_check = []
        for system_coords, projects in project_pool.items():
            for project_name, project in projects.items():
                for cell in project.validate_data_needed:
                    things_to_check.append(ThingToGet(target_category="Star Systems",
                                                      index=convert_coords_s_2_t(system_coords),
                                                      cell_name=cell))
        response = get_cells(self.player_sheet, things_to_check)
        # compile to system resources
        resource_pool = {f"{key[0]}, {key[1]}": {item[0].cell_name: item[1] for item in group}
                         for key, group in groupby(response, lambda item: item[0].index)}
        for system_coords, projects in project_pool.items():
            for project_name, project in projects.items():
                project.validate_data = {resource: resource_pool[system_coords][resource]
                                         for resource in project.validate_data_needed}

    def execute_actions(self, resource_pool, system_actions) -> Dict[str, Dict[str, Project]]:
        new_project_pool = {}
        for action in system_actions:
            if action.status != "Valid":
                continue
            resources_sufficient = all([resource_pool[action.coordinates_s][resource] >= quantity
                                        for resource, quantity in action.expenditure_coded.items()])
            resources_partially_sufficient = any([resource_pool[action.coordinates_s][resource] > 0
                                                  for resource, quantity in action.expenditure_coded.items()])
            resources_zero = all([resource_pool[action.coordinates_s][resource] == 0
                                  for resource, quantity in action.expenditure_coded.items()])
            if resources_sufficient:
                prev_quantities = deepcopy(resource_pool[action.coordinates_s])
                proj = self.add_project_and_progress_to_it(action, new_project_pool, resource_pool)

                action.status = "Executed"
                action.status_explanation = f"Resourses were sufficient in the target system, values before excecution: {prev_quantities}\n" \
                                            f"Resources successfully expended on a project in {action.coordinates_s}: {proj.progress_made}" \
                                            f"\nProject is now in the resolution queue"
                continue
            elif resources_partially_sufficient:
                prev_quantities = deepcopy(resource_pool[action.coordinates_s])
                proj = self.add_project_and_progress_to_it(action, new_project_pool, resource_pool)

                action.status = "Partially Executed"
                action.status_explanation = f"Resourses were not sufficient in the target system, values before excecution: {prev_quantities}\n" \
                                            f"Resources successfully expended on a project in {action.coordinates_s}: {proj.progress_made}" \
                                            f"\nProject is now in the resolution queue"
                continue
            elif resources_zero:
                prev_quantities = deepcopy(resource_pool[action.coordinates_s])
                action.status = "Failed"
                action.status_explanation = f"No resources to do this action. Values before action: {prev_quantities}"
                continue
        return new_project_pool

    def add_project_and_progress_to_it(self, action, new_project_pool, resource_pool):
        if action.coordinates_s not in new_project_pool:
            new_project_pool[action.coordinates_s] = {}
        proj_name = action.action_type
        proj = get_project(proj_name)
        for resource, quantity in action.expenditure_coded.items():
            proj.progress_made[resource] = min(quantity, resource_pool[action.coordinates_s][resource])
            resource_pool[action.coordinates_s][resource] -= proj.progress_made[resource]
        if proj_name in new_project_pool.get(action.coordinates_s, {}):
            # Create a merged project
            merged_progress = {
                resource: new_project_pool[action.coordinates_s][proj_name].progress_made.get(resource, 0)
                          + proj.progress_made.get(resource, 0)
                for resource in
                set(new_project_pool[action.coordinates_s][proj_name].progress_made) | set(
                    proj.progress_made)}

            # Create a merged project
            merged_project = Project(
                name=new_project_pool[action.coordinates_s][proj_name].name,
                progress_made=merged_progress,
                cost=new_project_pool[action.coordinates_s][proj_name].cost,
                validate_data_needed=new_project_pool[action.coordinates_s][proj_name].validate_data_needed,
                validate_func=new_project_pool[action.coordinates_s][proj_name].validate_func,
                on_completion=proj.on_completion,
                on_completion_custom=proj.on_completion_custom,
                validate_data=new_project_pool[action.coordinates_s][proj_name].validate_data
            )

            new_project_pool[action.coordinates_s][proj_name] = merged_project

        else:
            new_project_pool[action.coordinates_s][proj_name] = proj
        return proj

    def get_relevant_resources(self, system_actions):
        Unit_to_cell_translations = {
            "AP": "AP Budget",
            "WU": "WU Progress"
        }
        things_to_check = []
        for action in system_actions:
            used_units = action.expenditure_coded.keys()
            cells_containing_units = [Unit_to_cell_translations.get(unit) for unit in used_units]
            for cell in cells_containing_units:
                things_to_check.append(
                    ThingToGet(target_category="Star Systems", index=action.coordinates, cell_name=cell))
        response = get_cells(self.player_sheet, things_to_check)
        response.sort(key=lambda item: item[0].index)
        resource_pool = {f"{key[0]}, {key[1]}": {item[0].cell_name: item[1] for item in group}
                         for key, group in groupby(response, lambda item: item[0].index)}
        # unpack values for convenience
        for coordinate, resources in resource_pool.items():
            for resource, quantity in resources.items():
                if (resource == "AP Budget") or (resource == "WU Progress"):
                    resources[resource] = float(quantity[0][0])
        # Reverse names back to keys from Unit_to_cell_translations
        reverse_translation = {v: k for k, v in Unit_to_cell_translations.items()}
        for coordinate, resources in resource_pool.items():
            new_resources = {}
            for resource, quantity in resources.items():
                new_key = reverse_translation.get(resource, resource)  # Get the reverse translation if it exists
                new_resources[new_key] = quantity
            resource_pool[coordinate] = new_resources
        return resource_pool

    def load_relevant_existing_projects(self, system_actions) -> Dict[str, Dict[str, Project]]:
        things_to_check = []
        for action in system_actions:
            if action.status == "Valid":
                things_to_check.append(ThingToGet(target_category="Star Systems",
                                                  index=action.coordinates,
                                                  cell_name="System modifiers / projects"))
        response = get_cells(self.player_sheet, things_to_check)
        # create coord - list[project] for for ease of search for relevant projects
        raw_project_pool = {f"{item[0].index[0]}, {item[0].index[1]}": item[1] for item in response}
        project_pool = {}
        for coord, rows in raw_project_pool.items():
            project_pool[coord] = {}
            for row in rows:
                if len(row) == 0:
                    continue
                cell = row[0]
                if cell.startswith("Project"):
                    proj = extract_project(cell)
                    project_pool[coord][proj.name] = proj
        return project_pool

    def get_current_system_actions(self):
        system_actions_range = f"C{self.system_action_first_row}:{self.system_action_last_row}"
        raw_system_actions = self.turn_page.batch_get([system_actions_range], major_dimension="COLUMNS")[0]
        logging.info(f"Player {self.player_id}: fetched {len(raw_system_actions)} systems actions")

        for i, raw_system_action in enumerate(raw_system_actions):
            raw_system_actions[i] = raw_system_action + [""] * (8 - len(raw_system_action))

        system_actions = [LocalAction(system_q=raw_action[0], system_r=raw_action[1],
                                      action_type=raw_action[2], description=raw_action[3],
                                      expenditure=raw_action[6],
                                      status=raw_action[7],
                                      turn_sheet_origin=RangePointer(
                                          start=Pointer(numeric_to_alphabetic_column(3 + i),
                                                        self.system_action_first_row),
                                          end=Pointer(numeric_to_alphabetic_column(3 + i),
                                                      self.system_action_last_row)
                                      ))
                          for i, raw_action in enumerate(raw_system_actions)]
        return system_actions

    def do_feedback_on_actions(self, system_actions):
        status_coloring = {
            "Failed": "red",
            "Invalid": "red",
            "Partially Executed": "yellow",
            "Executed": "green",
            "Valid": "cyan",
            "Need Manual Execution": "cyan",
        }
        high_cells = {}
        for action in system_actions:
            high_cells[str(action.turn_sheet_origin)] = Highlight(status_coloring[action.status],
                                                                  action.status_explanation)

        self.highlight_cells(self.turn_page, high_cells)
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
