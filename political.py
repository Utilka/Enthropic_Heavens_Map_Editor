import math
import pickle

import numpy as numpy
from PIL import Image, ImageDraw, ImageFont

import map_to_hex_index
from hex_poligon_generator import HexagonCreator

from Player_DB_handler import *


class Force():
    def __init__(self, owner, units, type):
        self.owner = owner
        self.units = units
        self.type = type

    def __str__(self):
        return f"({self.owner.player_id},{self.owner.name},{self.units},{self.type})"

    def __repr__(self):
        return f"Force({self.owner},{self.units},{self.type})"


def get_hex_forces(coordinates, all_civs):
    forces = []
    for civ in all_civs:
        for fleet in civ.fleets:
            if fleet.coordinates == coordinates:
                forces.append(Force(civ, fleet.units, "fleet"))
        for system_force in civ.system_forces:
            if system_force.coordinates == coordinates:
                forces.append(Force(civ, system_force.units, "systemforce"))

    return forces

def find_dom(forces, type):
    f_forces = list(filter(lambda x: x.type == type, forces))
    f_forces.sort(key= lambda x: x.units, reverse=True)
    grouped_forces =
    for force in f_forces:
        pass




def main():
    hex_index = numpy.load("data/hex_types.npy", allow_pickle=True)
    political_map = numpy.empty(hex_index.shape, dtype=object)
    del hex_index
    all_civs = get_civs()

    # for i in range(political_map.shape[0]):
    #     for j in range(political_map.shape[1]):
    #         forces = get_hex_forces((i, j), all_civs)
    #         space_dom = find_dom(forces, "fleet")
    #         local_dom = find_dom(forces,"systemforce")

    forces = get_hex_forces((-7, -7), all_civs)
    space_dom = find_dom(forces, "fleet")
    local_dom = find_dom(forces, "systemforce")

    pass


if __name__ == '__main__':
    main()
