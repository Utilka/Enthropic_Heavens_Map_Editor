import random


class Planet:
    sterility_options = ["Gas giant", "Sterile", "Moderate", "Fertile"]
    temperature_options = ["Cold", "Temperate", "Hot"]
    size_options = ["Small", "Medium", "Large"]
    size_def = {"Small": 0.8, "Medium": 1, "Large": 1.4}

    def __init__(self, sterility=None, temperature=None, size=None, moons=None, name=None, description=None):
        if moons is None:
            moons = []
        assert sterility in self.sterility_options
        self.sterility = sterility
        assert temperature in self.temperature_options
        self.temperature = temperature
        assert size in self.size_options
        self.size = size
        self.moons = moons
        self.name = name
        self._description = description

    def __str__(self):
        return f"{self.sterility}:{self.temperature}:{self.size}:moons{[str(m) for m in self.moons]}"

    def __repr__(self):
        return f"Planet({self.sterility},{self.temperature},{self.size},{[repr(m) for m in self.moons]}"


# [Gas giant,Sterile,Moderate,Fertile][Cold,Temperate,Hot][Small,Medium,Large]
weights_table = {
    "grey": [[0.2, 0.8, 0, 0], [0.9, 0.1, 0], [0.2, 0.4, 0.2]],
    "red": [[0.5, 0.5, 0, 0], [0.2, 0.3, 0.5], [0.2, 0.25, 0.35]],
    "orange": [[0.5, 0.25, 0.25, 0], [0.5, 0.4, 0.2], [0.2, 0.25, 0.35]],
    "green": [[0.5, 0.4, 0.3, 0.025], [0.5, 0.4, 0.2], [0.2, 0.25, 0.35]],
}

normal_planet_moons = [[0, 1, 2, 3], [0.6, 0.22, 0.11, 0.07]]
gas_giant_moons = [[0, 1, 2, 3, 4, 5], [0.08, 0.17, 0.25, 0.25, 0.17, 0.08]]

moon_amount = {
    "Gas giant": gas_giant_moons,
    "Sterile": normal_planet_moons,
    "Moderate": normal_planet_moons,
    "Fertile": normal_planet_moons
}


def create_planet(system_class):
    sterility = random.choices(Planet.sterility_options, weights=weights_table[system_class][0])[0]
    temperature = random.choices(Planet.temperature_options, weights=weights_table[system_class][1])[0]
    size = random.choices(Planet.size_options, weights=weights_table[system_class][2])[0]

    planet = Planet(sterility, temperature, size)

    if planet.size != "Small":
        m_am = random.choices(moon_amount[sterility][0], weights=moon_amount[sterility][1])[0]
        for i in range(m_am):
            planet.moons.append(create_moon(system_class, temperature, planet.size))

    return planet


def create_moon(system_class, temperature, max_size):
    sterility = random.choices(Planet.sterility_options[1:], weights=weights_table[system_class][0][1:])[0]

    size = random.choices(Planet.size_options[:Planet.size_options.index(max_size)],
                          weights=weights_table[system_class][2][:Planet.size_options.index(max_size)])[0]
    moon = Planet(sterility, temperature, size)
    return moon


def main():
    for i in range(10):
        print(create_planet("green"))
    pass


if __name__ == '__main__':
    main()
