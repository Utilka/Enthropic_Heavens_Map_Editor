import pickle
import random

import numpy

import system_generator

temperature_order = {"Hot": 0, "Temperate": 1, "Cold": 2}


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


def load_systems() -> numpy.ndarray:
    with open('databases/System_DB.pickle', 'rb') as f:
        return pickle.load(f)


def save_systems(all_syst: numpy.ndarray):
    with open('databases/System_DB.pickle', 'wb') as f:
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


def editingus1():
    spawns = [
        ["Xaltios", [19, -24], ],
        ["Toxiq", [-33, 29], ],
        ["nwlr_tv", [-24, 8], ],
        ["constantinos2", [33, -30], ],
        ["georgell", [-11, 30], ],
        ["jaguar162", [11, 6], ],
        ["sppucke", [-17, -3], ],
        ["brianofthewoods", [30, -3], ],
        ["mr._saul_goodman", [-11, 18], ],
        ["Storm_3210", [10, -25], ],
        ["thatonefoxy", [19, 14], ],
        ["rhysonasi", [-24, -12], ],
        ["triple_zero", [23, -15], ],
        ["Mortron42", [0, 21], ],
        ["Lizardwizard__", [-38, 4], ],
        ["the_flying_meme", [9, -6], ],
        ["drakos", [-6, -4], ],
        ["Hirisu", [-7, -23], ],
    ]
    all_systems = load_systems()
    starting_systems = []
    for i in range(len(spawns)):
        spawns[i][1] = spawns[i][1][0] + 42, spawns[i][1][1] + 42
        st: system_generator.StarSystem = all_systems[spawns[i][1]]
        starting_systems.append(st)

    # starting_systems[-].rare_resource = None
    # starting_systems[-].rare_resource_quantity = None
    # starting_systems[-].modifier = None
    # starting_systems[-].name = None
    # starting_systems[-].stars = [system_generator.StarType.all_stars["Red dwarf"]]
    # starting_systems[-].planets = []
    # starting_systems[-].planets.append(system_generator.Planet("Fertile", "Temperate", "Medium", name=None))
    # starting_systems[-].planets.append(system_generator.Planet("Moderate", "Hot", "Medium"))
    # starting_systems[-].planets.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[-].planets.append(system_generator.Planet("Sterile", "Temperate", "Medium"))
    # starting_systems[-].planets[-1].moons.append(system_generator.Planet("Sterile", "Temperate", "Small"))
    # starting_systems[-].planets.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[-].planets.append(system_generator.Planet("Gas giant", "Temperate", "Large"))
    # starting_systems[-].planets[-1].moons.append(system_generator.Planet("Moderate", "Temperate", "Small"))
    # starting_systems[-].planets[-1].moons.append(system_generator.Planet("Sterile", "Temperate", "Medium"))
    # starting_systems[-].planets.append(system_generator.Planet("Gas giant", "Cold", "Large"))
    # starting_systems[-].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[-].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Medium"))
    # starting_systems[-].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[-].planets.sort(key=lambda planet: temperature_order[planet.temperature])
    pass


def main():
    all_systems = load_systems()
    counter = 0
    for i in range(all_systems.shape[0]):
        for j in range(all_systems.shape[0]):
            counter += int(all_systems[i, j] != None)
    print(counter)
    # print(all_systems[59, 55].description)
    # changes = {
    # "Mortron42": (0, 21), # rename
    # "Toxiq": (-33, 29),# add 2 sterile cold, 4 sterile moderate
    # }
    pass
    # save_systems(all_systems)


def c(coords):
    return (coords[0] + 42, coords[1] + 42)


def name_duplication_fix():
    all_systems = load_systems()
    uniq_names = []
    duplicates = False
    for i_1 in range(all_systems.shape[0]):
        for j_1 in range(all_systems.shape[1]):
            for i_2 in range(i_1 + 1, all_systems.shape[0]):
                for j_2 in range(j_1 + 1, all_systems.shape[1]):
                    if (all_systems[(i_1, j_1)] is not None) and (all_systems[(i_2, j_2)] is not None):
                        uniq_names.append(all_systems[(i_1, j_1)].name)
                        if (all_systems[(i_1, j_1)].name == all_systems[(i_2, j_2)].name):
                            print(
                                f"Systems {(i_1, j_1)} and {(i_2, j_2)} have same name {all_systems[(i_2, j_2)].name}")
                            duplicates = True
                            new_name = system_generator.star_name_gen()
                            while new_name in uniq_names:
                                new_name = system_generator.star_name_gen()
                            all_systems[(i_2, j_2)].name = new_name

    save_systems(all_systems)
    return duplicates


def make_sterile(system):
    for planet in system.planets:
        if planet.sterility == 'Moderate' or planet.sterility == 'Fertile':
            planet.sterility = 'Sterile'
        for moon in planet.moons:
            if moon.sterility == 'Moderate' or moon.sterility == 'Fertile':
                moon.sterility = 'Sterile'

    return system


if __name__ == "__main__":
    # add_maid()
    # add_flowers()
    # add_ameba()
    # main()
    # resort_planets()
    # name_duplication_search()
    # while True:
    #     has_dplicates = name_duplication_fix()
    #     if has_dplicates == False:
    #         break

    all_systems = load_systems()
    pass
