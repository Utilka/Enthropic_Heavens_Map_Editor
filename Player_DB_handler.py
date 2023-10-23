import pickle
from typing import List

from Civ import Civ
from Forces import Fleet, SystemForce

def load_civs() -> List[Civ]:
    with open('databases/Player_DB.pickle', 'rb') as f:
        return pickle.load(f)


def save_civs(all_civs: List[Civ]):
    with open('databases/Player_DB.pickle', 'wb') as f:
        pickle.dump(all_civs, f)


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
    save_civs(all_civs)
    test_civ: Civ = all_civs[0]
    test_civ.open_gspread_connection(29)
    test_civ.process_system_actions()
    pass


if __name__ == '__main__':
    # test()
    all_civs = load_civs()
    test_civ: Civ = all_civs[-1]
    test_civ.open_gspread_connection(1)
    pass
    # all_civs[-1].player_id = "888"
    # all_civs[-2].player_id = "999"
    # all_civs.append(Civ(str(888), "Test", "jija", "#ffDDff",
    #                     system_forces=[SystemForce(5, (222, 111))]))
    # all_civs.append(Civ(str(999), "Default", "jija", "#ffDDff",
    #                     system_forces=[SystemForce(5, (111, 222))]))
    #
    # save_civs(all_civs)
    pass
