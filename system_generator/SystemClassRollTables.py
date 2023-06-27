from . import RollTable



syst_modifiers = [
    "Strong Magnetic Field", "Cyber Flora", "Low Gravity", "Molten Springs",
    "High Gravity", "Behemoth Song", "Talking World", ]


class RareResource:
    def __init__(self, name, effect, description):
        self.name = name
        self.effect = effect
        self.description = description

    def __str__(self):
        return self.name

    # def __repr__(self):
    #     return self.name


class SystemModifier:
    def __init__(self, name, effect, description):
        self.name = name
        self.effect = effect
        self.description = description

    def __str__(self):
        return self.name

    # def __repr__(self):
    #     return self.name

universal_rr = [
    RareResource("Ionic Crystal", "", ""),
    RareResource("Giga Lattice", "", ""),
    RareResource("Amianthoid", "", ""),
    RareResource("Mercurite", "", ""),
    RareResource("Beryllium", "", ""),
]
unique_bio_rr = [
    RareResource("RedSang", "", ""),
    RareResource("Bluecap Mold", "", ""),
    RareResource("Eden Incense", "", ""),
    RareResource("Transvine", "", ""),
    RareResource("Superspuds", "", ""),
    RareResource("Proto-Orchid", "", ""),
    RareResource("Proto-Spores", "", ""),
    RareResource("placeholder 01", "", ""),
    RareResource("placeholder 02", "", ""),
]
red_rr = [
    RareResource("placeholder 11", "", ""),
    RareResource("placeholder 12", "", ""),
]
grey_rr = [
    RareResource("placeholder 21", "", ""),
    RareResource("placeholder 22", "", ""),
]

def create_rr_rolltables():


    universal_rr_rolltable = RollTable.RollTable(options=[RollTable.Option(i, 1) for i in universal_rr])
    unique_bio_rr_rolltable = RollTable.RollTable(options=[RollTable.Option(i, 1) for i in unique_bio_rr])
    red_rr_rolltable = RollTable.RollTable(options=[RollTable.Option(i, 1) for i in red_rr])
    grey_rr_rolltable = RollTable.RollTable(options=[RollTable.Option(i, 1) for i in grey_rr])

    fertile_planet_rolltable = RollTable.RollTable(options=[
        RollTable.Option(None, 40)],
        rolltables=[
            RollTable.Option(unique_bio_rr_rolltable, 39),
            RollTable.Option(universal_rr_rolltable, 1),
        ])

    green_class_rolltable = RollTable.RollTable(options=[
        RollTable.Option(None, 40)],
        rolltables=[
            RollTable.Option(universal_rr_rolltable, 1),
        ])

    orange_class_rolltable = RollTable.RollTable(options=[
        RollTable.Option(None, 20)],
        rolltables=[
            RollTable.Option(universal_rr_rolltable, 1),
        ])

    red_class_rolltable = RollTable.RollTable(options=[
        RollTable.Option(None, 10)],
        rolltables=[
            RollTable.Option(red_rr_rolltable, 1),
        ])

    grey_class_rolltable = RollTable.RollTable(options=[
        RollTable.Option(None, 5)],
        rolltables=[
            RollTable.Option(grey_rr_rolltable, 2),
        ])

    rr_rolltables = {
        "fertile": fertile_planet_rolltable,
        "green": green_class_rolltable,
        "orange": orange_class_rolltable,
        "red": red_class_rolltable,
        "grey": grey_class_rolltable,
    }
    return rr_rolltables
    pass


universal_modifiers = [
    SystemModifier("Mineral Rich", "", ""),
    SystemModifier("Antonov Rings", "", ""),
    SystemModifier("Huygens Rings", "", ""),
    SystemModifier("Hollow Planet", "", ""),
    SystemModifier("Strong Magnetic Field", "", ""),
    SystemModifier("Low Gravity", "", ""),
    SystemModifier("High Gravity", "", "", ),
    SystemModifier("Behemoth Song", "", ""),
    SystemModifier("Shattered Crust", "", ""),
    SystemModifier("Ice-10", "", ""),
]
fertile_modifiers = [
    SystemModifier("Psychoactive Air", "", ""),
    SystemModifier("Garden of Eden", "", ""),
    SystemModifier("Friendly Locals", "", ""),
    SystemModifier("Rich Soil", "", ""),
    SystemModifier("Hadopelagic Life", "", ""),
    SystemModifier("Permanent Monsoon", "", ""),
    SystemModifier("Long Season", "", ""),
    SystemModifier("Hostile Fauna", "", ""),
    SystemModifier("Poor Soil", "", ""),
    SystemModifier("Metallic Waters", "", ""),
    SystemModifier("Coral Reefs", "", ""),
    SystemModifier("Mutated Flora", "", ""),
    SystemModifier("Propitious Seasons", "", ""),
    SystemModifier("The Fallen Gardens", "", ""),
    SystemModifier("Tree of Worlds", "", ""),
]
unique_modifiers = [
    SystemModifier("Cyber Flora", "", ""),
    SystemModifier("Kessler Syndrome", "", ""),
    SystemModifier("Ancient Ruins", "", ""),
    SystemModifier("Deserted Cities", "", ""),
    SystemModifier("Guardian", "", ""),
    SystemModifier("The Platform of Ys", "", ""),
    SystemModifier("Strange Fossils", "", ""),
    SystemModifier("Humeris Insidentes", "", ""),
    SystemModifier("Fearful Symmetry", "", ""),
    SystemModifier("Talking World", "", ""),
]
young_modifiers = [
    SystemModifier("Molten Springs", "", ""),
    SystemModifier("Geothermic Activity", "", ""),
    SystemModifier("Seismic Activity", "", ""),
    SystemModifier("Komatiite Volcanoes", "", ""),
    SystemModifier("Acid Rains", "", ""),
    SystemModifier("Unstable Solar Winds", "", ""),
]
extreme_modifiers = [
    SystemModifier("Meteor Strikes", "", ""),
    SystemModifier("Irradiated", "", ""),
    SystemModifier("Chthonian World", "", ""),
    SystemModifier("Aurora Waves", "", ""),
    SystemModifier("Radiation Belts", "", ""),
    SystemModifier("Spatial Vortexes", "", ""),
    SystemModifier("Exotic Particle Emissions", "", ""),
]


def create_mod_rolltables():
    universal_m_rolltable = RollTable.RollTable(options=[RollTable.Option(i, 1) for i in universal_modifiers])
    fertile_m_rolltable = RollTable.RollTable(options=[RollTable.Option(i, 1) for i in fertile_modifiers])
    unique_m_rolltable = RollTable.RollTable(options=[RollTable.Option(i, 1) for i in unique_modifiers])
    young_m_rolltable = RollTable.RollTable(options=[RollTable.Option(i, 1) for i in young_modifiers])
    extreme_m_rolltable = RollTable.RollTable(options=[RollTable.Option(i, 1) for i in extreme_modifiers])

    fertile_planet_rolltable = RollTable.RollTable(options=[
        RollTable.Option(None, 10)],
        rolltables=[
            RollTable.Option(fertile_m_rolltable, 20),
            RollTable.Option(universal_m_rolltable, 2),
        ])

    green_class_rolltable = RollTable.RollTable(options=[
        RollTable.Option(None, 12)],
        rolltables=[
            RollTable.Option(universal_m_rolltable, 2),
            RollTable.Option(unique_m_rolltable, 1),
        ])

    orange_class_rolltable = RollTable.RollTable(options=[
        RollTable.Option(None, 12)],
        rolltables=[
            RollTable.Option(universal_m_rolltable, 2),
            RollTable.Option(unique_m_rolltable, 1),
        ])

    red_class_rolltable = RollTable.RollTable(options=[
        RollTable.Option(None, 10)],
        rolltables=[
            RollTable.Option(universal_m_rolltable, 1),
            RollTable.Option(young_m_rolltable, 4),
            RollTable.Option(extreme_m_rolltable, 2),
        ])

    grey_class_rolltable = RollTable.RollTable(options=[
        RollTable.Option(None, 8)],
        rolltables=[
            RollTable.Option(universal_m_rolltable, 1),
            RollTable.Option(extreme_m_rolltable, 6),
        ])

    modifier_rolltables = {
        "fertile": fertile_planet_rolltable,
        "green": green_class_rolltable,
        "orange": orange_class_rolltable,
        "red": red_class_rolltable,
        "grey": grey_class_rolltable,
    }
    return modifier_rolltables


def main():
    rr_rolltables = create_rr_rolltables()
    print([str(rr_rolltables["fertile"]()) for i in range(10)])
    print([str(rr_rolltables["green"]()) for i in range(10)])
    print([str(rr_rolltables["orange"]()) for i in range(10)])
    print([str(rr_rolltables["red"]()) for i in range(10)])
    print([str(rr_rolltables["grey"]()) for i in range(10)])

    mod_rolltables = create_mod_rolltables()
    print([str(mod_rolltables["fertile"]()) for i in range(10)])
    print([str(mod_rolltables["green"]()) for i in range(10)])
    print([str(mod_rolltables["orange"]()) for i in range(10)])
    print([str(mod_rolltables["red"]()) for i in range(10)])
    print([str(mod_rolltables["grey"]()) for i in range(10)])
    pass


if __name__ == '__main__':
    main()
