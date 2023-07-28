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


def print_systems_of_interest():
    spawns = [
        # ["Xaltios", [19, -24], ],
        # ["Toxiq", [-33, 29], ],
        # ["nwlr_tv", [-24, 8], ],
        # ["constantinos2", [33, -30], ],
        # ["georgell", [-11, 30], ],
        # ["jaguar162", [11, 6], ],
        # ["sppucke", [-17, -3], ],
        # ["brianofthewoods", [30, -3], ],
        # ["Storm_3210", [10, -25], ],
        # ["thatonefoxy", [19, 14], ],
        # ["rhysonasi", [-24, -12], ],
        ["triple_zero", [23, -15], ],
        # ["Mortron42", [0, 21], ],
        # ["Lizardwizard__", [-38, 4], ],
        # ["the_flying_meme", [9, -6], ],
        ["drakos", [-6, -4], ],
        ["Hirisu", [-7, -23], ],
    ]
    all_systems = load_systems()

    for i in range(len(spawns)):
        print("_______________")
        print(f"{101 + i}\n{spawns[i][0]}")
        print(f"{101 + i} {spawns[i][0]}")
        print(f"{101 + i}\t{spawns[i][0]}")
        print(f"{spawns[i][1][0] - 42}\t{spawns[i][1][1] - 42}")
        print(all_systems[(spawns[i][1][0] + 42, spawns[i][1][1] + 42)].description)
    pass


def name_star_systems():
    all_systems = load_systems()
    for i in range(all_systems.shape[0]):
        for j in range(all_systems.shape[1]):
            if all_systems[i, j] is not None:
                if (all_systems[i, j].name is None) or (all_systems[i, j].name == ""):
                    all_systems[i, j].name = system_generator.star_name_gen()
                all_systems[i, j].name = all_systems[i, j].name.title()
                # all_systems[i, j].planets.sort(key=lambda planet: temperature_order[planet.temperature])
    save_systems(all_systems)


def resort_planets():
    all_systems = load_systems()
    for i in range(all_systems.shape[0]):
        for j in range(all_systems.shape[1]):
            if all_systems[i, j] is not None:
                all_systems[i, j].planets.sort(key=lambda planet: temperature_order[planet.temperature])
    save_systems(all_systems)


def add_peli():
    peli_coords = (-11, 18)
    all_systems = load_systems()
    peli_system = all_systems[(peli_coords[0] + 42, peli_coords[1] + 42)]

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
    peli_system.rare_resource = None
    peli_system.rare_resource_quantity = None
    peli_system.modifier = None
    peli_system.name = "Persephone"
    peli_system.stars = [system_generator.StarType.all_stars["Red dwarf"]]
    peli_system.planets = []
    peli_system.planets.append(system_generator.Planet("Sterile", "Hot", "Small"))
    peli_system.planets.append(system_generator.Planet("Sterile", "Hot", "Large"))
    peli_system.planets[-1].moons.append(system_generator.Planet("Sterile", "Temperate", "Small"))
    peli_system.planets.append(system_generator.Planet("Gas giant", "Temperate", "Large"))
    peli_system.planets[-1].moons.append(system_generator.Planet("Moderate", "Temperate", "Medium"))
    peli_system.planets[-1].moons.append(system_generator.Planet("Moderate", "Temperate", "Medium"))
    peli_system.planets[-1].moons.append(system_generator.Planet("Moderate", "Temperate", "Medium"))
    peli_system.planets[-1].moons.append(system_generator.Planet("Sterile", "Temperate", "Small"))
    peli_system.planets[-1].moons.append(system_generator.Planet("Sterile", "Temperate", "Small"))
    peli_system.planets.append(system_generator.Planet("Gas giant", "Cold", "Large"))
    peli_system.planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    peli_system.planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Medium"))
    peli_system.planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    peli_system.planets.sort(key=lambda planet: temperature_order[planet.temperature])
    save_systems(all_systems)
    pass


def add_maid():
    maid_coords = (30, -3)
    all_systems = load_systems()
    maid_system = all_systems[(maid_coords[0] + 42, maid_coords[1] + 42)]

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
    maid_system.rare_resource = None
    maid_system.rare_resource_quantity = None
    maid_system.modifier = None
    maid_system.name = "Perch"
    maid_system.stars = [system_generator.StarType.all_stars["Red dwarf"]]
    maid_system.planets = []
    maid_system.planets.append(system_generator.Planet("Sterile", "Hot", "Small"))
    maid_system.planets.append(system_generator.Planet("Gas giant", "Hot", "Large"))
    maid_system.planets[-1].moons.append(system_generator.Planet("Sterile", "Hot", "Medium"))
    maid_system.planets[-1].moons.append(system_generator.Planet("Sterile", "Hot", "Medium"))
    maid_system.planets[-1].moons.append(system_generator.Planet("Moderate", "Hot", "Small"))
    maid_system.planets.append(system_generator.Planet("Gas giant", "Temperate", "Large"))
    maid_system.planets[-1].moons.append(system_generator.Planet("Moderate", "Temperate", "Medium"))
    maid_system.planets[-1].moons.append(system_generator.Planet("Moderate", "Temperate", "Medium"))
    maid_system.planets[-1].moons.append(system_generator.Planet("Moderate", "Temperate", "Medium"))
    maid_system.planets[-1].moons.append(system_generator.Planet("Moderate", "Temperate", "Small"))
    maid_system.planets[-1].moons.append(system_generator.Planet("Sterile", "Temperate", "Small"))
    maid_system.planets.append(system_generator.Planet("Moderate", "Cold", "Medium"))
    maid_system.planets.append(system_generator.Planet("Sterile", "Cold", "Small"))
    maid_system.planets.append(system_generator.Planet("Sterile", "Cold", "Small"))
    maid_system.planets.append(system_generator.Planet("Sterile", "Cold", "Large"))
    maid_system.planets.append(system_generator.Planet("Sterile", "Cold", "Small"))
    maid_system.planets.sort(key=lambda planet: temperature_order[planet.temperature])
    save_systems(all_systems)
    pass


def add_sin():
    sin_coords = (-39, 19)
    all_systems = load_systems()
    sin_system = all_systems[(sin_coords[0] + 42, sin_coords[1] + 42)]

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
    sin_system.rare_resource = None
    sin_system.rare_resource_quantity = None
    sin_system.modifier = None
    sin_system.name = "Avon"
    sin_system.stars = [system_generator.StarType.all_stars["Red dwarf"]]
    sin_system.planets = []
    sin_system.planets.append(system_generator.Planet("Sterile", "Hot", "Small"))
    sin_system.planets.append(system_generator.Planet("Sterile", "Hot", "Large"))
    sin_system.planets.append(system_generator.Planet("Moderate", "Hot", "Medium"))
    sin_system.planets.append(system_generator.Planet("Gas giant", "Hot", "Large"))
    sin_system.planets[-1].moons.append(system_generator.Planet("Sterile", "Hot", "Medium"))
    sin_system.planets[-1].moons.append(system_generator.Planet("Sterile", "Hot", "Medium"))
    sin_system.planets[-1].moons.append(system_generator.Planet("Moderate", "Hot", "Small"))
    sin_system.planets.append(system_generator.Planet("Gas giant", "Temperate", "Large"))
    sin_system.planets[-1].moons.append(system_generator.Planet("Moderate", "Temperate", "Medium"))
    sin_system.planets[-1].moons.append(system_generator.Planet("Moderate", "Temperate", "Medium"))
    sin_system.planets[-1].moons.append(system_generator.Planet("Moderate", "Temperate", "Medium"))
    sin_system.planets[-1].moons.append(system_generator.Planet("Moderate", "Temperate", "Small"))
    sin_system.planets[-1].moons.append(system_generator.Planet("Sterile", "Temperate", "Small"))
    sin_system.planets.append(system_generator.Planet("Moderate", "Cold", "Medium"))
    sin_system.planets[-1].moons.append(system_generator.Planet("Moderate", "Cold", "Small"))
    sin_system.planets.append(system_generator.Planet("Sterile", "Cold", "Small"))
    sin_system.planets.append(system_generator.Planet("Sterile", "Cold", "Small"))
    sin_system.planets.append(system_generator.Planet("Sterile", "Cold", "Large"))
    sin_system.planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    sin_system.planets.sort(key=lambda planet: temperature_order[planet.temperature])
    pass
    save_systems(all_systems)


def add_ameba():
    ameba_coords = (9, 11)
    all_systems = load_systems()
    ameba_system = all_systems[(ameba_coords[0] + 42, ameba_coords[1] + 42)]

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
    ameba_system.rare_resource = None
    ameba_system.rare_resource_quantity = None
    ameba_system.modifier = None
    ameba_system.name = "Waub"
    ameba_system._description = "Waub system is lush with spaceborn life, with numbers of Space Ameba dominating the ecosystem, gathered around the gas giants "
    ameba_system.stars = [system_generator.StarType.all_stars["Red dwarf"],
                          system_generator.StarType.all_stars["Red dwarf"]]
    ameba_system.planets = []
    ameba_system.planets.append(system_generator.Planet("Sterile", "Hot", "Small"))
    ameba_system.planets.append(system_generator.Planet("Gas giant", "Hot", "Large"))
    ameba_system.planets[-1].moons.append(system_generator.Planet("Sterile", "Hot", "Medium"))
    ameba_system.planets[-1].moons.append(system_generator.Planet("Sterile", "Hot", "Medium"))
    ameba_system.planets[-1].moons.append(system_generator.Planet("Sterile", "Hot", "Small"))
    ameba_system.planets.append(system_generator.Planet("Gas giant", "Temperate", "Medium",
                                                        description="There is a small, clearly artificial satelite orbiting around this planet"))
    ameba_system.planets[-1].moons.append(system_generator.Planet("Moderate", "Temperate", "Small"))
    ameba_system.planets[-1].moons.append(system_generator.Planet("Fertile", "Temperate", "Small",
                                                                  description="There are clearly artifical formations on the surface of this planet, they may very well be structures"))
    ameba_system.planets[-1].moons.append(system_generator.Planet("Sterile", "Temperate", "Small"))
    ameba_system.planets.append(system_generator.Planet("Gas giant", "Hot", "Small"))
    ameba_system.planets.append(system_generator.Planet("Gas giant", "Temperate", "Large"))
    ameba_system.planets[-1].moons.append(system_generator.Planet("Moderate", "Temperate", "Medium"))
    ameba_system.planets.append(system_generator.Planet("Gas giant", "Temperate", "Medium"))
    ameba_system.planets[-1].moons.append(system_generator.Planet("Moderate", "Temperate", "Medium"))
    ameba_system.planets[-1].moons.append(system_generator.Planet("Moderate", "Temperate", "Medium"))
    ameba_system.planets.append(system_generator.Planet("Gas giant", "Cold", "Small"))
    ameba_system.planets.append(system_generator.Planet("Gas giant", "Cold", "Medium"))
    ameba_system.planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    ameba_system.planets.append(system_generator.Planet("Moderate", "Cold", "Small"))
    ameba_system.planets.append(system_generator.Planet("Sterile", "Cold", "Small"))
    ameba_system.planets.append(system_generator.Planet("Sterile", "Cold", "Small"))
    ameba_system.planets.sort(key=lambda planet: temperature_order[planet.temperature])
    print(ameba_system.description)
    save_systems(all_systems)
    pass


def add_flowers():
    flower_coords = (-28, 1)
    all_systems = load_systems()
    flower_system = all_systems[(flower_coords[0] + 42, flower_coords[1] + 42)]

    pass
    flower_system.rare_resource = None
    flower_system.rare_resource_quantity = None
    flower_system.modifier = None
    flower_system.name = "Wenlai"
    flower_system._description = "Wenlai is houses entire ecosystem of spaceborn alien life, home to magneficent Space Flowers"
    flower_system.stars = [system_generator.StarType.all_stars["Red dwarf"],
                           system_generator.StarType.all_stars["Orange dwarf"],
                           system_generator.StarType.all_stars["Orange dwarf"],
                           system_generator.StarType.all_stars["Yellow dwarf"],
                           system_generator.StarType.all_stars["Red dwarf"]]
    flower_system.planets = []
    flower_system.planets.append(system_generator.Planet("Gas giant", "Temperate", "Large",
                                                         description="There is a small, clearly artificial satelite orbiting around this planet"))
    flower_system.planets[-1].moons.append(system_generator.Planet("Moderate", "Temperate", "Medium"))
    flower_system.planets[-1].moons.append(system_generator.Planet("Moderate", "Temperate", "Medium"))
    flower_system.planets[-1].moons.append(system_generator.Planet("Fertile", "Temperate", "Medium",
                                                                   description="There are clearly artifical formations on the surface of this planet, they may very well be structures"))
    flower_system.planets[-1].moons.append(system_generator.Planet("Moderate", "Temperate", "Small"))
    flower_system.planets[-1].moons.append(system_generator.Planet("Sterile", "Temperate", "Small"))
    flower_system.planets.append(system_generator.Planet("Sterile", "Hot", "Small"))
    flower_system.planets.append(system_generator.Planet("Gas giant", "Hot", "Large"))
    flower_system.planets[-1].moons.append(system_generator.Planet("Sterile", "Hot", "Medium"))
    flower_system.planets[-1].moons.append(system_generator.Planet("Sterile", "Hot", "Medium"))
    flower_system.planets[-1].moons.append(system_generator.Planet("Moderate", "Hot", "Small"))
    flower_system.planets.append(system_generator.Planet("Moderate", "Cold", "Medium"))
    flower_system.planets.append(system_generator.Planet("Sterile", "Cold", "Small"))
    flower_system.planets.append(system_generator.Planet("Sterile", "Cold", "Small"))
    flower_system.planets.append(system_generator.Planet("Sterile", "Cold", "Large"))
    flower_system.planets.append(system_generator.Planet("Sterile", "Cold", "Small"))
    flower_system.planets.sort(key=lambda planet: temperature_order[planet.temperature])
    print(flower_system.description)
    save_systems(all_systems)
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
            for i_2 in range(i_1+1,all_systems.shape[0]):
                for j_2 in range(j_1+1,all_systems.shape[1]):
                    if (all_systems[(i_1, j_1)] is not None) and (all_systems[(i_2, j_2)] is not None):
                        uniq_names.append(all_systems[(i_1, j_1)].name)
                        if (all_systems[(i_1, j_1)].name == all_systems[(i_2, j_2)].name):
                            print(f"Systems {(i_1, j_1)} and {(i_2, j_2)} have same name {all_systems[(i_2, j_2)].name}")
                            duplicates = True
                            new_name = system_generator.star_name_gen()
                            while new_name in uniq_names:
                                new_name = system_generator.star_name_gen()
                            all_systems[(i_2, j_2)].name = new_name

    save_systems(all_systems)
    return duplicates


def make_sterile(system):
    for planet in system.planets:
        if planet.sterility == 'Moderate' or planet.sterility =='Fertile':
            planet.sterility = 'Sterile'
        for moon in planet.moons:
            if moon.sterility == 'Moderate' or moon.sterility =='Fertile':
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
