import numpy as numpy

from .SystemClassRollTables import *
from .StarRollTable import *
from .PlanetTable import *
from .star_name_generator import *
import random
import pickle

star_indexes = ["a", "b", "c", "d", "e", "f"]
moon_indexes = ["I", "II", "III", "IV", "V"]


# IF there are no rare resources or syst_modifiers available, insert a "placeholder", as the code no likey when rare resources or system modifiers are empty.

class StarSystem:

    def __init__(self, name=None, stars: [StarType] = None, planets: [Planet] = None, modifier=None, rare_resource=None,
                 rare_resource_quantity=None):

        if stars is None:
            stars = []
        if planets is None:
            planets = []
        self.stars = stars
        self.name = name
        self.planets = planets
        self.modifier = modifier
        self.rare_resource = rare_resource
        self.rare_resource_quantity = rare_resource_quantity

    @property
    def system_class(self):
        for star_class in StarType.star_class_rank:
            for star in self.stars:
                if star.star_type == star_class:
                    return star_class
        return "grey"

    def __str__(self):
        return f"{self.system_class},{len(self.stars)}:{len(self.planets)},{self.modifier},{self.rare_resource}"

    def __repr__(self):
        return f"StarSystem({self.name},{self.stars},{self.planets},{self.modifier},{self.rare_resource},{self.rare_resource_quantity}"

    @property
    def description(self):
        title_str = f"{(self.name is not None) * str(self.name)} Star System, is of {self.system_class.capitalize()} class, has {len(self.stars)} stars and {self.total_planets} planets."
        mods_str = f"\nModifier:{self.modifier}; Rare Resourse: {self.rare_resource}; Rare Resourse quantity: {self.rare_resource_quantity} "

        star_str = f"\nStars:\n"
        for i in range(len(self.stars)):
            star_str += f"{star_indexes[i]:<4} {self.stars[i].description}\n"
        planets_str = f"\nPlanets:\n"
        for i in range(len(self.planets)):
            planets_str += f"{str(i):<4} {self.planets[i].description}\n"

        return title_str + mods_str + "\nPlanet type matrix:\n" + self.planet_type_matrix + star_str + planets_str

    @property
    def has_fertile(self):
        for planet in self.planets:
            if planet.sterility == "Fertile":
                return True
            for moon in planet.moons:
                if planet.sterility == "Fertile":
                    return True
        return False

    @property
    def total_planets(self):
        counter = 0
        for planet in self.planets:
            counter += len(planet.moons) + 1
        return counter

    @property
    def planet_type_matrix(self):
        tmp = {"Cold": 0, "Temperate": 1, "Hot": 2}
        ster = {"Gas giant": 0, "Sterile": 1, "Moderate": 2, "Fertile": 3}
        counter = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

        for planet in self.planets:
            counter[tmp[planet.temperature]][ster[planet.sterility]]+= planet.size_def[planet.size]
            for moon in planet.moons:
                counter[tmp[moon.temperature]][ster[moon.sterility]]+= moon.size_def[moon.size]
        retr_str = ""
        for tmp in counter:
            for ster in tmp:
                retr_str+= f"{ster:<4.1f}" + "\t"
            retr_str+= "\n"

        return retr_str


hex_types = ["stellar_nursery", "galactic_arm", "inter_arm", "core", "manual"]
star_rolltables = create_star_rolltables()
rr_rolltables = create_rr_rolltables()
mod_rolltables = create_mod_rolltables()
amount_of_stars_roll = [
    (1, 2, 3, 4, 5, 6),
    (0.15, 0.7, 0.14, 0.00665241, 0.00244728, 0.00090031)
]
max_amount_of_planets = {
    1: 10,
    2: 16,
    3: 16,
    4: 20,
    5: 20,
    6: 20,
}
temperature_order = {"Hot": 0, "Temperate": 1, "Cold": 2}


def generate_system(hex_type):
    if hex_type == hex_types[4]:
        return StarSystem()
    star_system = StarSystem()
    star_amount = random.choices(amount_of_stars_roll[0], weights=amount_of_stars_roll[1])[0]

    for i in range(star_amount):
        star_system.stars.append(star_rolltables[hex_type]())

    max_planet_amount = max_amount_of_planets[star_amount]

    if star_system.system_class == "grey" or star_system.system_class == "red":
        max_planet_amount = 3

    pl_c = random.randint(0, max_planet_amount)
    for i in range(pl_c):
        star_system.planets.append(
            create_planet(star_system.system_class,
                          spawn_fertile=
                          (2 >= (len([p for p in star_system.planets if p.sterility == "Fertile"]) +
                                 sum([len([m for m in p.moons if m.sterility == "Fertile"])
                                      for p in star_system.planets])
                                 ))
                          )  # dont spawn more then 2 fertile per system
        )
    star_system.planets.sort(key=lambda planet: temperature_order[planet.temperature])

    if star_system.has_fertile:
        star_system.modifier = mod_rolltables["fertile"]()
        star_system.rare_resource = rr_rolltables["fertile"]()
    else:
        star_system.modifier = mod_rolltables[star_system.system_class]()
        star_system.rare_resource = rr_rolltables[star_system.system_class]()

    if star_system.rare_resource is not None:
        if star_system.rare_resource in unique_bio_rr:
            star_system.rare_resource_quantity = random.randint(3, 5)
        else:
            star_system.rare_resource_quantity = random.randint(1, 5)

    return star_system


def main():
    listus = []
    for i in range(100):
        listus.append(generate_system(hex_types[2]))

    # filename = 'system.pickle'  # Replace 'object.pickle' with your desired filename
    # with open(filename, 'wb') as file:
    #     pickle.dump(listus, file)
    #
    # file.close()
    # with open(filename, 'rb') as file:
    #     loaded_object = pickle.load(file)
    #
    # file.close()
    # n = numpy.array(loaded_object)
    # print(loaded_object)
    pass


if __name__ == '__main__':
    main()
