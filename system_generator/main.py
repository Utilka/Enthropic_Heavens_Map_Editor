import numpy as numpy

from .SystemClassRollTables import *
from .StarRollTable import *
from .PlanetTable import *
import random
import pickle

# IF there are no rare resources or syst_modifiers available, insert a "placeholder", as the code no likey when rare resources or system modifiers are empty.

final_result = ["Star Type", "placehold", "Star Amount", "0", "Rare Resources", "none", "System Modifier", "none",
                "No. of Planets", "0", "No. of Moons", "0"]


class StarSystem:

    def __init__(self, name=None, stars: [StarType] = None, planets=None, modifier=None, rare_resource=None,
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
        return None

    @property
    def has_fertile(self):
        for planet in self.planets:
            if planet.sterility == "Fertile":
                return True
            for moon in planet.moons:
                if planet.sterility == "Fertile":
                    return True
        return False


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
temperature_order = {"Cold": 0, "Temperate": 1, "Hot": 2}


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
        star_system.planets.append(create_planet(star_system.system_class))
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
    filename = 'system.pickle'  # Replace 'object.pickle' with your desired filename

    with open(filename, 'wb') as file:
        pickle.dump(listus, file)

    file.close()
    with open(filename, 'rb') as file:
        loaded_object = pickle.load(file)

    file.close()
    n = numpy.array(loaded_object)
    print(loaded_object)


if __name__ == '__main__':
    main()
