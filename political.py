import math
import pickle
from itertools import groupby

import numpy as numpy
from PIL import Image, ImageDraw, ImageFont

import map_to_hex_index
from hex_poligon_generator import HexagonCreator

from Player_DB_handler import *

forces_types = ["space", "system"]


class MicroHexagonCreator(HexagonCreator):
    def __init__(self, size: int, offset: (int, int), border: int):
        super().__init__(size, offset, border)

    def __call__(self, coord):
        # jij = [angle_deg for angle_deg in range(30, 390, 60)]
        p_center = self.hex_center(coord)

        hexus = []
        for angle_deg in range(30, 390, 60):
            angle_rad = math.radians(angle_deg)
            p_x = p_center[0] + round(math.cos(angle_rad) * self.size / 2)
            p_y = p_center[1] + round(math.sin(angle_rad) * self.size / 2)
            hexus.append((p_x, p_y))

        return hexus


class Force:
    def __init__(self, owner, units, force_type):
        self.owner = owner
        self.units = units
        self.force_type = force_type

    def __str__(self):
        return f"(\"{self.owner.player_id}\",\"{self.owner.name}\",{self.units},\"{self.force_type}\")"

    def __repr__(self):
        return f"Force({self.owner},{self.units},\"{self.force_type}\")"


def get_hex_forces(coordinates, all_civs):
    forces = []
    for civ in all_civs:
        for fleet in civ.fleets:
            if fleet.coordinates == coordinates:
                forces.append(Force(civ, fleet.units, forces_types[0]))
        for system_force in civ.system_forces:
            if system_force.coordinates == coordinates:
                forces.append(Force(civ, system_force.units, forces_types[1]))

    return forces


def group_forces(forces):
    grouped_forces = {}
    forces.sort(
        key=lambda x: (x.owner.player_id, x.force_type))  # Sort the list by owner player_id and type for grouping

    for key, group in groupby(forces, key=lambda x: (x.owner, x.force_type)):
        owner, force_type = key
        total_units = sum(f.units for f in group)

        if force_type == forces_types[1]:
            if owner.doctrine == 'defense':
                # Check if there's an existing group for space forces, otherwise create a new group
                space_key = (owner, forces_types[0])
                if space_key in grouped_forces:
                    grouped_forces[space_key] += total_units
                else:
                    grouped_forces[space_key] = total_units

        grouped_forces[key] = total_units

    return grouped_forces


def find_doms(forces):
    doms = {"space": None, "system": None}
    grouped_forces = group_forces(forces)

    system_keys = [key for key in grouped_forces.keys() if key[1] == forces_types[1]]

    if len(system_keys) != 0:
        system_key_with_max_value = max(system_keys, key=lambda k: grouped_forces[k])
        total_system_force = sum([grouped_forces[key] for key in system_keys])
        biggest_system_force = grouped_forces[system_key_with_max_value]

        if biggest_system_force / total_system_force >= 0.75:
            doms["system"] = system_key_with_max_value[0]


    space_keys = [key for key in grouped_forces.keys() if key[1] == forces_types[0]]

    if len(space_keys) != 0:
        space_key_with_max_value = max(space_keys, key=lambda k: grouped_forces[k])
        total_space_force = sum([grouped_forces[key] for key in space_keys])
        biggest_space_force = grouped_forces[space_key_with_max_value]

        if biggest_space_force / total_space_force >= 0.75:
            doms["space"] = space_key_with_max_value[0]
    else:
        doms["space"] = doms["system"]

    return doms


def generate_pol_index(in_filepath,all_civs):
    hex_index = numpy.load(in_filepath, allow_pickle=True)
    political_index = numpy.empty(hex_index.shape, dtype=object)
    del hex_index

    for i in range(political_index.shape[0]):
        for j in range(political_index.shape[1]):
            coordinates = (i - 42, j - 42)
            forces = get_hex_forces(coordinates, all_civs)
            doms = find_doms(forces)
            political_index[i, j] = doms

    return political_index


def main():
    all_civs = get_civs()
    print(generate_pol_index(all_civs))


if __name__ == '__main__':
    main()
