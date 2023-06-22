import pickle


class Civ:
    def __init__(self, player_id, name, color: str, fleets=None, system_forces=None):
        if system_forces is None:
            system_forces = []
        if fleets is None:
            fleets = []
        self.player_id = player_id
        self.name = name
        self.color = color
        self.fleets = fleets
        self.system_forces = system_forces

    def __str__(self):
        return  f"Civ({self.player_id},{self.name},{self.color})"

    def __repr__(self):
        return f"Civ({self.player_id},{self.name},{self.color},{self.fleets},{self.system_forces})"


class Fleet:
    def __init__(self, name, units: int, coordinates):
        self.name = name
        self.units = units
        self._q, self._r = coordinates

    @property
    def coordinates(self):
        return self._q, self._r

    @coordinates.setter
    def coordinates(self, value):
        self._q, self._r = value

    @coordinates.deleter
    def coordinates(self):
        del self._q, self._r

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"Fleet({self.name},{self.units},{self.coordinates})"


class SystemForce:
    def __init__(self, units: int, coordinates):
        self.units = units
        self._q, self._r = coordinates

    @property
    def coordinates(self):
        return self._q, self._r

    @coordinates.setter
    def coordinates(self, value):
        self._q, self._r = value

    @coordinates.deleter
    def coordinates(self):
        del self._q, self._r

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"SystemForce({self.units},{self.coordinates})"


def get_civs():
    with open('Player_DB.pickle', 'rb') as f:
        return pickle.load(f)


def save_civs(all_civs):
    with open('Player_DB.pickle', 'wb') as f:
        pickle.dump(all_civs, f)


def main():
    all_civs = [
        Civ("11", "jij1", "#292cb8",
            [Fleet("Fleet1", 20, (-17, 3)), Fleet("Fleet2", 20, (-17, 5))],
            [SystemForce(20, (-17, 4)), SystemForce(20, (-16, 4)), SystemForce(20, (-16, 3))]
            ),
        Civ("12", "jij2", "#a029b8",
            [Fleet("Fleet1", 10, (-7, -7))],
            [SystemForce(20, (-7, -7)), ]
            ),

        Civ("101", "pjij1", "#1574a0",
            [Fleet("Fleet1", 20, (-7, -7)), Fleet("Fleet2", 20, (-3, -7))],
            [SystemForce(20, (-8, -4))]
            ),
        Civ("102", "pjij2", "#15a026",
            [Fleet("Fleet1", 20, (-8, -4)), ],
            [SystemForce(20, (-4, -7)), SystemForce(20, (-3, -7))]
            ),
    ]

    save_civs(all_civs)
    print(get_civs())


if __name__ == '__main__':
    main()
