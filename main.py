# monke patch the gspread lib to have 1 second delay after every request
# in order to comply with my 60 request per min quota
import time
from gspread import client

old_request = client.Client.request


def slow_request(*args, **kwargs):
    time.sleep(1)
    return old_request(*args, **kwargs)


client.Client.request = slow_request

import logging
from typing import List

import map_painter
from Player_DB_handler import load_civs, save_civs
from System_DB_handler import load_systems
from utils import get_cells, ThingToGet

# these imports are needed for load_civs pickle thing
from Civ import Civ
from Forces import Fleet, SystemForce

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler('my_log_file.log'),
                        logging.StreamHandler()
                    ])


def c(coords):
    return (coords[0] + 42, coords[1] + 42)


def check_first_contacts(explored_systems):
    # check for exploration encounters
    for explorer_id in explored_systems:
        for explored_id in explored_systems:
            for explorer_coord in explored_systems[explorer_id]:
                for explored_coord in explored_systems[explored_id]:
                    if explored_coord == explorer_coord and explorer_id != explored_id:
                        print(f"player {explorer_id} has encountered {explored_id} science ships in {explorer_coord}")

    all_civs = load_civs()
    # check for encounters with forces
    for explorer_id in explored_systems:
        for explored_civ in all_civs:
            for explorer_coord in explored_systems[explorer_id]:
                for SF in explored_civ.system_forces:
                    if (explorer_coord == SF.coordinates) and (explorer_id != explored_civ.player_id):
                        print(
                            f"player {explorer_id} has encountered {explored_civ.player_id} system forces in {explorer_coord}")
                for Fleet in explored_civ.fleets:
                    if (explorer_coord == Fleet.coordinates) and (explorer_id != explored_civ.player_id):
                        print(
                            f"player {explorer_id} has encountered {explored_civ.player_id} fleet in {explorer_coord}")

    # check for encounters with remnants of exploration
    for explorer_id in explored_systems:
        for explored_civ in all_civs:
            for explorer_coord in explored_systems[explorer_id]:
                if (explored_civ.explored_space[c(explorer_coord)]) and explorer_id != explored_civ.player_id:
                    print(
                        f"player {explorer_id} has encountered {explored_civ.player_id} remnants of exploration activity in {explorer_coord}")
    pass


def explore_and_print(explored_systems):
    counter = 0
    for civ_id in explored_systems:
        counter += len(explored_systems[civ_id])
    print(counter)

    check_first_contacts(explored_systems)

    all_civs = load_civs()
    all_systems = load_systems()
    for civ in all_civs:
        if civ.player_id in explored_systems.keys():
            print(f"{'':_<40}\n{civ.player_id:<3} {civ.player_name}")
            for coords in explored_systems[civ.player_id]:
                civ.explore_star_system(coords)
                shifted_coords = coords[0] + 42, coords[1] + 42
                if all_systems[shifted_coords] is not None:
                    print(f"{coords[0]}\t{coords[1]}")
                    print(all_systems[shifted_coords].description)
                else:
                    print(f"Player {civ.player_id} explored {coords[0]}\t{coords[1]} but it is None")

                print(f"{'':_<20}")
    pass
    save_civs(all_civs)


# explored_systems = {
#         "101": [],
#         "102": [],
#         "104": [],
#         "105": [],
#         "106": [],
#         "110": [],
#         "112": [],
#         "113": [],
#         "114": [],
#         "117": [],
#         "118": [],
#         "120": [],
#     }

def phase_2(turn):
    all_civs = load_civs()
    all_civs = all_civs[:-2]  # remove test players
    explored_systems = {
        "101": [],
        "102": [],
        "104": [],
        "106": [],
        "110": [],
        "112": [(-14, -12), ],
        "113": [],
        "114": [(7, 12),
                (8, 13),
                (6, 15),
                (6, 14),
                (7, 14),
                (7, 13),
                (8, 12),
                (9, 12), ],
        "117": [],
        "118": [],
        "120": [],
    }

    # explore_and_print(explored_systems)
    # for civ in all_civs:
    #     civ.open_gspread_connection(turn)
    #     # civ.process_system_actions()
    #     civ.read_forces()
    #     civ.update_explores()
    #     civ.close_gspread_connection()
    #
    # save_civs(all_civs)

    map_painter.color_political("maps/hex_political.png", all_civs)

    map_painter.color_explored("maps/hex_explored.png", all_civs)

    map_painter.color_politicals(turn, all_civs)


def phase_1(turn):
    logging.info(f"Started executing turn {turn + 0.1}")
    all_civs = load_civs()

    logging.info(f"Fetched {len(all_civs)} civs from civ database")
    all_civs = all_civs[:-2]  # remove test players
    for civ in all_civs:
        logging.info(f"working on {civ.player_id} {civ.player_name} Player Sheet")
        civ.open_gspread_connection(turn)

        # time.sleep(1)
        if civ.player_sheet.sheet1.acell("D2").numeric_value == 1:
            logging.info(f"skipping {civ.player_id} {civ.player_name} Player Sheet, no touch flag detected")
            continue
        # time.sleep(1)

        if civ.player_sheet.sheet1.acell("A2").numeric_value >= turn + 0.1:
            logging.info(
                f"skipping {civ.player_id} {civ.player_name} Player Sheet, turn counter indicates that turn was already excecuted")
            continue
        # time.sleep(1)

        civ.tick_fleets(turn)
        civ.set_AP_budgets()
        civ.tick_WU_growth()
        civ.set_IP_budget()
        civ.update_explores()
        civ.set_turn_counter(turn + 0.1)
        civ.close_gspread_connection()

        # time.sleep(10)

    map_painter.color_political("maps/hex_political.png", all_civs)

    map_painter.color_explored("maps/hex_explored.png", all_civs)

    map_painter.color_politicals(turn, all_civs)


def test():
    all_players = load_civs()
    all_players = all_players[:-2]

    all_players = all_players[:1]
    for test_player in all_players:
        test_player.open_gspread_connection(32)
        test_player.process_system_actions()
    # jij = get_cells(test_player.player_sheet, [ThingToGet("Star Systems", "Pleisdag", "AP Budget"),
    #                                            ThingToGet("Star Systems", (17, -22), "WU Progress")])
    pass


if __name__ == '__main__':
    pass
    # if not os.path.exists("./maps"):
    #     os.makedirs("./maps")
    # all_civs = load_civs()
    # pass
    # test()
    # executed_turn = 31
    # phase_1(executed_turn)
    # phase_2(executed_turn)
