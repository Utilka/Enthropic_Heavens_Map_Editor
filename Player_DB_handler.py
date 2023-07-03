import pickle
import numpy

hex_index = numpy.load("data/hex_types.npy", allow_pickle=True)


class Civ:
    def __init__(self, player_id, player_name, name, color: str, doctrine=None, fleets=None, system_forces=None):
        if system_forces is None:
            system_forces = []
        if fleets is None:
            fleets = []
        self.player_id = player_id
        self.player_name = player_name
        self.name = name
        self.color = color
        self.fleets = fleets
        self.system_forces = system_forces
        self.doctrine = doctrine
        self.explored_space = numpy.full(hex_index.shape, False)

    def __str__(self):
        return f"Civ(\"{self.player_id}\",\"{self.player_name}\",\"{self.name}\",\"{self.color}\")"

    def __repr__(self):
        return f"Civ(\"{self.player_id}\",\"{self.player_name}\",\"{self.name}\",\"{self.color}\",\"{self.doctrine}\",{self.fleets},{self.system_forces})"

    def explore_star_system(self, coordinates):
        self.explored_space[(coordinates[0]+42,coordinates[1]+42)] = True


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
        return f"Fleet(\"{self.name}\",{self.units},{self.coordinates})"


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


def load_civs():
    with open('Player_DB.pickle', 'rb') as f:
        return pickle.load(f)


def save_civs(all_civs):
    with open('Player_DB.pickle', 'wb') as f:
        pickle.dump(all_civs, f)


def start_game():
    spawns = [
        ("Xaltios", (19, -24), "The Arcturan Caliphate", "#A33084"),
        ("Toxiq", (-33, 29), "Steels Ambit", "#8c22b4"),
        ("nwlr_tv", (-24, 8), "Taxpm-Yyn Covenant", "#f2cc0d"),
        ("constantinos2", (33, -30), "Istionian Planetary Union", "#6A0D98"),
        ("georgell", (-11, 30), "Xerum Exploratory Republic", "#07a895"),
        ("jaguar162", (11, 6), None, "#326fa8"),
        ("sppucke", (-17, -3), "The Umbral Collective", "#0FAD3E"),
        ("brianofthewoods", (30, -3), "Resinalwahl", "#2cffdf"),
        ("mr._saul_goodman", (-11, 18), "Alpheria", "#B60000"),
        ("Storm_3210", (10, -25), "The Knights of Nekar", "#5496af"),
        ("thatonefoxy", (19, 14), "The Foundation", "#492C5D"),
        ("rhysonasi", (-24, -12), "Chosen of Nishchiyeh", "#00e600"),
        ("triple_zero", (23, -15), "Vracronica", "#851D2D"),
        ("Mortron42", (0, 21), "United Clans of the Sorzal", "#efeb2b"),
        ("Lizardwizard__", (-38, 4), "Cerin unity united", "#00ffff"),
        ("the_flying_meme", (9, -6), "Floof", "#3047cf"),
    ]
    all_civs = [
        Civ("11", None, "", "#7800a0",
            ),
        Civ("21", None, "Galactic Concord 1", "#001e96",
            ),
        Civ("22", None, "Galactic Concord 2", "#001e96",
            ),
        Civ("23", None, "Galactic Concord 3", "#001e96",
            ),
        Civ("24", None, "Galactic Concord 4", "#001e96",
            ),
        Civ("25", None, "Galactic Concord 5", "#001e96",
            ),
    ]

    for i in range(len(spawns)):
        civ = Civ(str(100 + 1 + i), spawns[i][0], spawns[i][2], spawns[i][3],
                  system_forces=[SystemForce(5, spawns[i][1])])
        civ.explore_star_system(spawns[i][1])
        all_civs.append(civ)

    save_civs(all_civs)
    print(load_civs())


def main():
    # all_civs = [
    # ]
    #start_game()
    # save_civs(all_civs)
    print(load_civs())


if __name__ == '__main__':
    main()
