import pickle
from typing import List

from Civ import Civ
from Forces import Fleet, SystemForce

def load_civs() -> List['Civ']:
    with open('databases/Player_DB.pickle', 'rb') as f:
        return pickle.load(f)


def save_civs(all_civs: List['Civ']):
    with open('databases/Player_DB.pickle', 'wb') as f:
        pickle.dump(all_civs, f)
