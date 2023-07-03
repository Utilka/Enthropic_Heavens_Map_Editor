import pickle
import random

import numpy

import system_generator


def get_system_types():
    hex_color_index = numpy.load("data/hex_types.npy", allow_pickle=True)
    mapping = {
        "green": "stellar_nursery",
        "yellow": "galactic_arm",
        "blue-ish": "inter_arm",
        "red": "core",
        "purple": "manual",
        None: None,
    }

    hex_type_index = numpy.copy(hex_color_index)
    for k, v in zip(mapping.keys(), mapping.values()): hex_type_index[hex_color_index == k] = v
    return hex_type_index


def load_systems():
    with open('System_DB.pickle', 'rb') as f:
        return pickle.load(f)


def save_systems(all_syst):
    with open('System_DB.pickle', 'wb') as f:
        pickle.dump(all_syst, f)


def generate_systems(hex_type_index):
    systems = numpy.empty(hex_type_index.shape, dtype=object)
    system_coords = []
    for i in range(systems.shape[0]):
        for j in range(systems.shape[1]):
            if hex_type_index[i, j] is not None:
                system_coords.append((i, j))

    order = random.sample(range(len(system_coords)), k=len(system_coords))
    for i in order:
        systems[system_coords[i]] = system_generator.generate_system(hex_type_index[system_coords[i]])

    return systems


def main():
    all_systems = generate_systems(get_system_types())
    save_systems(all_systems)


if __name__ == "__main__":
    main()
