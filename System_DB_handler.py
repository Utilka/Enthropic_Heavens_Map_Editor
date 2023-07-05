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

    # starting_systems[0].rare_resource = None
    # starting_systems[0].rare_resource_quantity = None
    # starting_systems[0].modifier = None
    # starting_systems[0].name = "Kenvorus"
    # starting_systems[0].stars = [system_generator.StarType.all_stars["Orange dwarf"]]
    # starting_systems[0].planets = []
    # starting_systems[0].planets.append(system_generator.Planet("Fertile", "Temperate", "Medium", name=None))
    # starting_systems[0].planets.append(system_generator.Planet("Moderate", "Hot", "Medium"))
    # starting_systems[0].planets.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[0].planets.append(system_generator.Planet("Sterile", "Temperate", "Medium"))
    # starting_systems[0].planets[-1].moons.append(system_generator.Planet("Sterile", "Temperate", "Small"))
    # starting_systems[0].planets.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[0].planets.append(system_generator.Planet("Gas giant", "Temperate", "Large"))
    # starting_systems[0].planets[-1].moons.append(system_generator.Planet("Moderate", "Temperate", "Small"))
    # starting_systems[0].planets[-1].moons.append(system_generator.Planet("Sterile", "Temperate", "Medium"))
    # starting_systems[0].planets.append(system_generator.Planet("Gas giant", "Cold", "Large"))
    # starting_systems[0].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[0].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Medium"))
    # starting_systems[0].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[0].planets.sort(key=lambda planet: temperature_order[planet.temperature])
    #
    # starting_systems[1].rare_resource = None
    # starting_systems[1].rare_resource_quantity = None
    # starting_systems[1].modifier = None
    # starting_systems[1].name = "Kandidose"
    # starting_systems[1].planets = []
    # starting_systems[1].planets.append(system_generator.Planet("Sterile", "Hot", "Medium"))
    # starting_systems[1].planets.append(system_generator.Planet("Fertile", "Temperate", "Medium"))
    # starting_systems[1].planets.append(system_generator.Planet("Moderate", "Temperate", "Medium"))
    # starting_systems[1].planets.append(system_generator.Planet("Gas giant", "Cold", "Small"))
    # starting_systems[1].planets.append(system_generator.Planet("Gas giant", "Cold", "Medium"))
    # starting_systems[3].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[3].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[3].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[1].planets.append(system_generator.Planet("Gas giant", "Cold", "Medium"))
    # starting_systems[3].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[3].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[1].planets.append(system_generator.Planet("Gas giant", "Cold", "Small"))
    # starting_systems[1].planets.sort(key=lambda planet: temperature_order[planet.temperature])
    #
    # starting_systems[2].rare_resource = None
    # starting_systems[2].rare_resource_quantity = None
    # starting_systems[2].modifier = None
    # starting_systems[2].planets = []
    # starting_systems[2].planets.append(system_generator.Planet("Fertile", "Hot", "Medium", name="Lóquetz"))
    # starting_systems[2].planets.append(system_generator.Planet("Moderate", "Hot", "Medium"))
    # starting_systems[2].planets.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[2].planets.append(system_generator.Planet("Sterile", "Temperate", "Medium"))
    # starting_systems[2].planets[-1].moons.append(system_generator.Planet("Sterile", "Temperate", "Small"))
    # starting_systems[2].planets.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[2].planets.append(system_generator.Planet("Gas giant", "Temperate", "Large"))
    # starting_systems[2].planets[-1].moons.append(system_generator.Planet("Moderate", "Temperate", "Small"))
    # starting_systems[2].planets[-1].moons.append(system_generator.Planet("Sterile", "Temperate", "Medium"))
    # starting_systems[2].planets.append(system_generator.Planet("Gas giant", "Cold", "Large"))
    # starting_systems[2].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[2].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Medium"))
    # starting_systems[2].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[2].planets.sort(key=lambda planet: temperature_order[planet.temperature])
    #
    # starting_systems[2].rare_resource = None
    # starting_systems[2].rare_resource_quantity = None
    # starting_systems[2].modifier = None
    # starting_systems[3].name = "The Nest"
    # starting_systems[3].stars = [system_generator.StarType.all_stars["Red dwarf"]]
    # starting_systems[3].planets = []
    # starting_systems[3].planets.append(system_generator.Planet("Fertile", "Hot", "Medium", name="Silkheart"))
    # starting_systems[3].planets[-1].moons.append(
    #     system_generator.Planet("Sterile", "Temperate", "Small", name="Luna Prime"))
    # starting_systems[3].planets[-1].moons.append(
    #     system_generator.Planet("Sterile", "Temperate", "Small", name="Nestia"))
    # starting_systems[3].planets[-1].moons.append(system_generator.Planet("Sterile", "Temperate", "Small"))
    # starting_systems[3].planets.append(system_generator.Planet("Moderate", "Hot", "Medium"))
    # starting_systems[3].planets.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[3].planets.append(system_generator.Planet("Gas giant", "Temperate", "Large"))
    # starting_systems[3].planets[-1].moons.append(system_generator.Planet("Moderate", "Temperate", "Small"))
    # starting_systems[3].planets[-1].moons.append(system_generator.Planet("Sterile", "Temperate", "Medium"))
    # starting_systems[3].planets.append(system_generator.Planet("Gas giant", "Cold", "Large"))
    # starting_systems[3].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[3].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Medium"))
    # starting_systems[3].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[3].planets.sort(key=lambda planet: temperature_order[planet.temperature])
    #
    # starting_systems[4].rare_resource = None
    # starting_systems[4].rare_resource_quantity = None
    # starting_systems[4].modifier = None
    # starting_systems[4].name = "Bloody Sunset"
    # starting_systems[4].stars = [system_generator.StarType.all_stars["Red dwarf"]]
    # starting_systems[4].planets = []
    # starting_systems[4].planets.append(system_generator.Planet("Fertile", "Temperate", "Medium", name="Xo"))
    # starting_systems[4].planets[-1].moons.append(system_generator.Planet("Sterile", "Temperate", "Small"))
    # starting_systems[4].planets[-1].moons.append(system_generator.Planet("Sterile", "Temperate", "Small"))
    # starting_systems[4].planets[-1].moons.append(system_generator.Planet("Sterile", "Temperate", "Small"))
    # starting_systems[4].planets[-1].moons.append(system_generator.Planet("Sterile", "Temperate", "Small"))
    # starting_systems[4].planets[-1].moons.append(system_generator.Planet("Sterile", "Temperate", "Small"))
    # starting_systems[4].planets.append(system_generator.Planet("Moderate", "Hot", "Medium"))
    # starting_systems[4].planets.append(system_generator.Planet("Sterile", "Temperate", "Medium"))
    # starting_systems[4].planets.append(system_generator.Planet("Gas giant", "Cold", "Large"))
    # starting_systems[4].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[4].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Medium"))
    # starting_systems[4].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[4].planets.sort(key=lambda planet: temperature_order[planet.temperature])
    #
    # starting_systems[5].rare_resource = None
    # starting_systems[5].rare_resource_quantity = None
    # starting_systems[5].modifier = None
    # starting_systems[5].name = None
    # starting_systems[5].stars = [system_generator.StarType.all_stars["Red dwarf"]]
    # starting_systems[5].planets = []
    # starting_systems[5].planets.append(system_generator.Planet("Fertile", "Temperate", "Medium", name=None))
    # starting_systems[5].planets.append(system_generator.Planet("Moderate", "Hot", "Medium"))
    # starting_systems[5].planets.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[5].planets.append(system_generator.Planet("Sterile", "Temperate", "Medium"))
    # starting_systems[5].planets[-1].moons.append(system_generator.Planet("Sterile", "Temperate", "Small"))
    # starting_systems[5].planets.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[5].planets.append(system_generator.Planet("Gas giant", "Temperate", "Large"))
    # starting_systems[5].planets[-1].moons.append(system_generator.Planet("Moderate", "Temperate", "Small"))
    # starting_systems[5].planets[-1].moons.append(system_generator.Planet("Sterile", "Temperate", "Medium"))
    # starting_systems[5].planets.append(system_generator.Planet("Gas giant", "Cold", "Large"))
    # starting_systems[5].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[5].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Medium"))
    # starting_systems[5].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[5].planets.sort(key=lambda planet: temperature_order[planet.temperature])
    #
    # starting_systems[6].rare_resource = None
    # starting_systems[6].rare_resource_quantity = None
    # starting_systems[6].modifier = None
    # starting_systems[6].name = None
    # starting_systems[6].stars = [system_generator.StarType.all_stars["Red dwarf"]]
    # starting_systems[6].planets = []
    # starting_systems[6].planets.append(system_generator.Planet("Fertile", "Temperate", "Medium", name=None))
    # starting_systems[6].planets.append(system_generator.Planet("Moderate", "Hot", "Medium"))
    # starting_systems[6].planets.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[6].planets.append(system_generator.Planet("Sterile", "Temperate", "Medium"))
    # starting_systems[6].planets[-1].moons.append(system_generator.Planet("Sterile", "Temperate", "Small"))
    # starting_systems[6].planets.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[6].planets.append(system_generator.Planet("Gas giant", "Temperate", "Large"))
    # starting_systems[6].planets[-1].moons.append(system_generator.Planet("Moderate", "Temperate", "Small"))
    # starting_systems[6].planets[-1].moons.append(system_generator.Planet("Sterile", "Temperate", "Medium"))
    # starting_systems[6].planets.append(system_generator.Planet("Gas giant", "Cold", "Large"))
    # starting_systems[6].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[6].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Medium"))
    # starting_systems[6].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[6].planets.sort(key=lambda planet: temperature_order[planet.temperature])
    #
    # starting_systems[7].rare_resource = None
    # starting_systems[7].rare_resource_quantity = None
    # starting_systems[7].modifier = None
    # starting_systems[7].name = "Shell"
    # starting_systems[7].stars = [system_generator.StarType.all_stars["Yellow dwarf"],
    #                              system_generator.StarType.all_stars["Orange dwarf"],
    #                              system_generator.StarType.all_stars["Yellow dwarf"], ]
    # starting_systems[7].planets = []
    # starting_systems[7].planets.append(system_generator.Planet("Fertile", "Temperate", "Medium"))
    # starting_systems[7].planets.append(system_generator.Planet("Moderate", "Temperate", "Large"))
    # starting_systems[7].planets.append(system_generator.Planet("Moderate", "Temperate", "Medium"))
    # starting_systems[7].planets.append(system_generator.Planet("Moderate", "Temperate", "Large"))
    # starting_systems[7].planets.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[7].planets.append(system_generator.Planet("Sterile", "Hot", "Small"))
    # starting_systems[7].planets.append(system_generator.Planet("Sterile", "Temperate", "Medium"))
    # starting_systems[7].planets.append(system_generator.Planet("Moderate", "Hot", "Small"))
    # starting_systems[7].planets.append(system_generator.Planet("Sterile", "Temperate", "Medium"))
    # starting_systems[7].planets.append(system_generator.Planet("Gas giant", "Cold", "Large"))
    # starting_systems[7].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[7].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Medium"))
    # starting_systems[7].planets.sort(key=lambda planet: temperature_order[planet.temperature])
    #
    # starting_systems[8].rare_resource = None
    # starting_systems[8].rare_resource_quantity = None
    # starting_systems[8].modifier = None
    # starting_systems[8].name = "Alpherian"
    # starting_systems[8].stars = [system_generator.StarType.all_stars["Red dwarf"]]
    # starting_systems[8].planets = []
    # starting_systems[8].planets.append(system_generator.Planet("Fertile", "Temperate", "Medium", name="Alpheria"))
    # starting_systems[8].planets.append(system_generator.Planet("Sterile", "Hot", "Large"))
    # starting_systems[8].planets[-1].moons.append(system_generator.Planet("Sterile", "Hot", "Small"))
    # starting_systems[8].planets[-1].moons.append(system_generator.Planet("Sterile", "Hot", "Small"))
    # starting_systems[8].planets.append(system_generator.Planet("Sterile", "Hot", "Small"))
    # starting_systems[8].planets.append(system_generator.Planet("Sterile", "Temperate", "Small"))
    # starting_systems[8].planets.append(system_generator.Planet("Moderate", "Cold", "Small"))
    # starting_systems[8].planets.append(system_generator.Planet("Gas giant", "Cold", "Medium"))
    # starting_systems[8].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[8].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[8].planets.sort(key=lambda planet: temperature_order[planet.temperature])
    #
    # starting_systems[9].rare_resource = None
    # starting_systems[9].rare_resource_quantity = None
    # starting_systems[9].modifier = None
    # starting_systems[9].stars = [system_generator.StarType.all_stars["Yellow dwarf"]]
    # starting_systems[9].planets = []
    # starting_systems[9].planets.append(system_generator.Planet("Fertile", "Hot", "Medium", name="Jezus"))
    # starting_systems[9].planets.append(system_generator.Planet("Fertile", "Hot", "Medium",
    #                                                            name="Eye of the Lord's most holy son given to us 6 times, Nekar"))
    # starting_systems[9].planets.append(system_generator.Planet("Sterile", "Temperate", "Small"))
    # starting_systems[9].planets.append(system_generator.Planet("Gas giant", "Cold", "Large"))
    # starting_systems[9].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Medium"))
    # starting_systems[9].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[9].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[9].planets.append(system_generator.Planet("Gas giant", "Cold", "Medium"))
    # starting_systems[9].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[9].planets.append(system_generator.Planet("Gas giant", "Cold", "Medium"))
    # starting_systems[9].planets.append(system_generator.Planet("Gas giant", "Cold", "Small"))
    # starting_systems[9].planets.sort(key=lambda planet: temperature_order[planet.temperature])
    #
    # starting_systems[10].rare_resource = None
    # starting_systems[10].rare_resource_quantity = None
    # starting_systems[10].modifier = None
    # starting_systems[10].name = None
    # starting_systems[10].stars = [system_generator.StarType.all_stars["Red dwarf"]]
    # starting_systems[10].stars = [system_generator.StarType.all_stars["Orange dwarf"]]
    # starting_systems[10].stars = [system_generator.StarType.all_stars["Red dwarf"]]
    # starting_systems[10].planets = []
    # starting_systems[10].planets.append(system_generator.Planet("Fertile", "Hot", "Medium", name="Synchronicity I"))
    # starting_systems[10].planets.append(
    #     system_generator.Planet("Sterile", "Hot", "Medium", description="Planet covered in purple mist"))
    # starting_systems[10].planets.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[10].planets.append(system_generator.Planet("Moderate", "Temperate", "Medium"))
    # starting_systems[10].planets[-1].moons.append(system_generator.Planet("Moderate", "Temperate", "Small"))
    # starting_systems[10].planets.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[10].planets.append(system_generator.Planet("Gas giant", "Temperate", "Large"))
    # starting_systems[10].planets[-1].moons.append(system_generator.Planet("Moderate", "Temperate", "Small"))
    # starting_systems[10].planets[-1].moons.append(system_generator.Planet("Sterile", "Temperate", "Medium"))
    # starting_systems[10].planets.append(system_generator.Planet("Gas giant", "Cold", "Large"))
    # starting_systems[10].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[10].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Medium"))
    # starting_systems[10].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[10].planets.sort(key=lambda planet: temperature_order[planet.temperature])
    #
    # starting_systems[11].rare_resource = None
    # starting_systems[11].rare_resource_quantity = None
    # starting_systems[11].modifier = None
    # starting_systems[11].name = None
    # starting_systems[11].stars = [system_generator.StarType.all_stars["Yellow dwarf"]]
    # starting_systems[11].planets = []
    # starting_systems[11].planets.append(system_generator.Planet("Fertile", "Hot", "Medium", name="Nischiyeh"))
    # starting_systems[11].planets.append(system_generator.Planet("Moderate", "Hot", "Medium"))
    # starting_systems[11].planets.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[11].planets.append(system_generator.Planet("Sterile", "Temperate", "Medium"))
    # starting_systems[11].planets[-1].moons.append(system_generator.Planet("Sterile", "Temperate", "Small"))
    # starting_systems[11].planets.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[11].planets.append(system_generator.Planet("Gas giant", "Temperate", "Large"))
    # starting_systems[11].planets[-1].moons.append(system_generator.Planet("Moderate", "Temperate", "Small"))
    # starting_systems[11].planets[-1].moons.append(system_generator.Planet("Sterile", "Temperate", "Medium"))
    # starting_systems[11].planets.append(system_generator.Planet("Gas giant", "Cold", "Large"))
    # starting_systems[11].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[11].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Medium"))
    # starting_systems[11].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[11].planets.sort(key=lambda planet: temperature_order[planet.temperature])
    #
    # starting_systems[12].rare_resource = None
    # starting_systems[12].rare_resource_quantity = None
    # starting_systems[12].modifier = None
    # starting_systems[12].name = "Vekta"
    # starting_systems[12].stars = [system_generator.StarType.all_stars["Yellow dwarf"]]
    # starting_systems[12].stars = [system_generator.StarType.all_stars["Orange dwarf"]]
    # starting_systems[12].stars = [system_generator.StarType.all_stars["Red dwarf"]]
    # starting_systems[12].planets = []
    # starting_systems[12].planets.append(system_generator.Planet("Fertile", "Hot", "Medium", name="Vracronica"))
    # starting_systems[12].planets.append(system_generator.Planet("Moderate", "Temperate", "Medium"))
    # starting_systems[12].planets.append(system_generator.Planet("Sterile", "Hot", "Small"))
    # starting_systems[12].planets.append(system_generator.Planet("Sterile", "Hot", "Small"))
    # starting_systems[12].planets.append(system_generator.Planet("Sterile", "Hot", "Small"))
    # starting_systems[12].planets.append(system_generator.Planet("Sterile", "Hot", "Small"))
    # starting_systems[12].planets.append(system_generator.Planet("Sterile", "Hot", "Small"))
    # starting_systems[12].planets.append(system_generator.Planet("Sterile", "Hot", "Small"))
    # starting_systems[12].planets.append(system_generator.Planet("Sterile", "Hot", "Small"))
    # starting_systems[12].planets.sort(key=lambda planet: temperature_order[planet.temperature])
    #
    # starting_systems[13].rare_resource = None
    # starting_systems[13].rare_resource_quantity = None
    # starting_systems[13].modifier = None
    # starting_systems[13].name = None
    # starting_systems[13].stars = [system_generator.StarType.all_stars["Red dwarf"]]
    # starting_systems[13].planets = []
    # starting_systems[13].planets.append(system_generator.Planet("Fertile", "Temperate", "Medium", name=None))
    # starting_systems[13].planets.append(system_generator.Planet("Moderate", "Hot", "Medium"))
    # starting_systems[13].planets.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[13].planets.append(system_generator.Planet("Sterile", "Temperate", "Medium"))
    # starting_systems[13].planets[-1].moons.append(system_generator.Planet("Sterile", "Temperate", "Small"))
    # starting_systems[13].planets.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[13].planets.append(system_generator.Planet("Gas giant", "Temperate", "Large"))
    # starting_systems[13].planets[-1].moons.append(system_generator.Planet("Moderate", "Temperate", "Small"))
    # starting_systems[13].planets[-1].moons.append(system_generator.Planet("Sterile", "Temperate", "Medium"))
    # starting_systems[13].planets.append(system_generator.Planet("Gas giant", "Cold", "Large"))
    # starting_systems[13].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[13].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Medium"))
    # starting_systems[13].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[13].planets.sort(key=lambda planet: temperature_order[planet.temperature])
    #
    # starting_systems[14].rare_resource = None
    # starting_systems[14].rare_resource_quantity = None
    # starting_systems[14].modifier = None
    # starting_systems[14].name = None
    # starting_systems[14].stars = [system_generator.StarType.all_stars["Red dwarf"]]
    # starting_systems[14].planets = []
    # starting_systems[14].planets.append(system_generator.Planet("Fertile", "Hot", "Medium", name=None))
    # starting_systems[14].planets[-1].moons.append(system_generator.Planet("Sterile", "Temperate", "Medium"))
    # starting_systems[14].planets[-1].moons.append(system_generator.Planet("Sterile", "Temperate", "Medium"))
    # starting_systems[14].planets.append(system_generator.Planet("Moderate", "Hot", "Medium"))
    # starting_systems[14].planets.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[14].planets.append(system_generator.Planet("Sterile", "Temperate", "Medium"))
    # starting_systems[14].planets[-1].moons.append(system_generator.Planet("Sterile", "Temperate", "Small"))
    # starting_systems[14].planets.append(system_generator.Planet("Sterile", "Cold", "Medium"))
    # starting_systems[14].planets[-1].moons.append(system_generator.Planet("Sterile", "Temperate", "Small"))
    # starting_systems[14].planets.append(system_generator.Planet("Gas giant", "Cold", "Large"))
    # starting_systems[14].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[14].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Medium"))
    # starting_systems[14].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[14].planets.sort(key=lambda planet: temperature_order[planet.temperature])
    #
    # starting_systems[15].rare_resource = None
    # starting_systems[15].rare_resource_quantity = None
    # starting_systems[15].modifier = None
    # starting_systems[15].name = "Imperial Center"
    # starting_systems[15].stars = [system_generator.StarType.all_stars["Red dwarf"],
    #                               system_generator.StarType.all_stars["Red dwarf"],
    #                               system_generator.StarType.all_stars["Red dwarf"],
    #                               system_generator.StarType.all_stars["Red dwarf"]]
    # starting_systems[15].planets = []
    # starting_systems[15].planets.append(system_generator.Planet("Fertile", "Temperate", "Medium", name=None))
    # starting_systems[15].planets.append(system_generator.Planet("Moderate", "Temperate", "Small"))
    # starting_systems[15].planets.append(system_generator.Planet("Moderate", "Temperate", "Small"))
    # starting_systems[15].planets.append(system_generator.Planet("Moderate", "Temperate", "Small"))
    # starting_systems[15].planets.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[15].planets.append(system_generator.Planet("Sterile", "Hot", "Medium"))
    # starting_systems[15].planets.append(system_generator.Planet("Sterile", "Temperate", "Medium"))
    # starting_systems[15].planets[-1].moons.append(system_generator.Planet("Sterile", "Temperate", "Small"))
    # starting_systems[15].planets.append(system_generator.Planet("Gas giant", "Cold", "Medium"))
    # starting_systems[15].planets[-1].moons.append(system_generator.Planet("Sterile", "Temperate", "Small"))
    # starting_systems[15].planets[-1].moons.append(system_generator.Planet("Sterile", "Temperate", "Small"))
    # starting_systems[15].planets.append(system_generator.Planet("Gas giant", "Temperate", "Small"))
    # starting_systems[15].planets.append(system_generator.Planet("Gas giant", "Cold", "Medium"))
    # starting_systems[15].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[15].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[15].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[15].planets.sort(key=lambda planet: temperature_order[planet.temperature])
    #
    # starting_systems[16].rare_resource = None
    # starting_systems[16].rare_resource_quantity = None
    # starting_systems[16].modifier = None
    # starting_systems[16].name = None
    # starting_systems[16].stars = [system_generator.StarType.all_stars["Red dwarf"]]
    # starting_systems[16].planets = []
    # starting_systems[16].planets.append(system_generator.Planet("Fertile", "Temperate", "Medium", name=None))
    # starting_systems[16].planets.append(system_generator.Planet("Moderate", "Hot", "Medium"))
    # starting_systems[16].planets.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[16].planets.append(system_generator.Planet("Sterile", "Temperate", "Medium"))
    # starting_systems[16].planets[-1].moons.append(system_generator.Planet("Sterile", "Temperate", "Small"))
    # starting_systems[16].planets.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[16].planets.append(system_generator.Planet("Gas giant", "Temperate", "Large"))
    # starting_systems[16].planets[-1].moons.append(system_generator.Planet("Moderate", "Temperate", "Small"))
    # starting_systems[16].planets[-1].moons.append(system_generator.Planet("Sterile", "Temperate", "Medium"))
    # starting_systems[16].planets.append(system_generator.Planet("Gas giant", "Cold", "Large"))
    # starting_systems[16].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[16].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Medium"))
    # starting_systems[16].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[16].planets.sort(key=lambda planet: temperature_order[planet.temperature])
    #
    # starting_systems[17].rare_resource = None
    # starting_systems[17].rare_resource_quantity = None
    # starting_systems[17].modifier = None
    # starting_systems[17].name = "Evontal"
    # starting_systems[17].stars = [system_generator.StarType.all_stars["Red dwarf"]]
    # starting_systems[17].planets = []
    # starting_systems[17].planets.append(system_generator.Planet("Fertile", "Hot", "Medium", name="Darven'tal"))
    # starting_systems[17].planets.append(system_generator.Planet("Sterile", "Hot", "Medium", name="Mafum"))
    # starting_systems[17].planets.append(system_generator.Planet("Sterile", "Cold", "Small", name="Scrumpa"))
    # starting_systems[17].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[17].planets.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[17].planets.append(system_generator.Planet("Gas giant", "Temperate", "Large", name="Alper"))
    # starting_systems[17].planets[-1].moons.append(system_generator.Planet("Moderate", "Temperate", "Small"))
    # starting_systems[17].planets[-1].moons.append(system_generator.Planet("Sterile", "Temperate", "Medium"))
    # starting_systems[17].planets[-1].moons.append(system_generator.Planet("Sterile", "Temperate", "Small"))
    # starting_systems[17].planets.append(system_generator.Planet("Gas giant", "Cold", "Medium"))
    # starting_systems[17].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[17].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[17].planets[-1].moons.append(system_generator.Planet("Sterile", "Cold", "Small"))
    # starting_systems[17].planets.sort(key=lambda planet: temperature_order[planet.temperature])
    #


def print_systems_of_interest():
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

    for i in range(len(spawns)):
        print("_______________")
        print(f"{101+i}\n{spawns[i][0]}")
        print(f"{101+i} {spawns[i][0]}")
        print(f"{101+i}\t{spawns[i][0]}")
        print(f"{spawns[i][1][0]-42}\t{spawns[i][1][1]-42}")
        print(all_systems[spawns[i][1]].description)
    pass


def name_star_systems():
    all_systems = load_systems()
    for i in range(all_systems.shape[0]):
        for j in range(all_systems.shape[1]):
            if all_systems[i, j] is not None:
                if (all_systems[i, j].name is None) or (all_systems[i,j].name == ""):
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


def main():
    all_systems = load_systems()
    print(all_systems[59, 55].description)

    pass
    # save_systems(all_systems)


if __name__ == "__main__":
    editingus1()
    # main()
    # resort_planets()
