from . import RollTable


class StarType:
    all_stars = {}
    star_classes = {
        "grey": [],
        "red": [],
        "orange": [],
        "green": [],
    }
    star_class_rank = ["grey", "red", "orange", "green"]

    def __init__(self, name=None, star_class=None, description=None):
        self.name = name
        self.description = description

        assert star_class in self.star_classes
        self.star_type = star_class

        StarType.star_classes[self.star_type].append(self)
        StarType.all_stars[self.name] = self

    def __del__(self):
        StarType.star_classes[self.star_type].remove(self)
        StarType.all_stars.pop(self.name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"StarType({self.name},{self.star_type},{self.description})"


def create_star_rolltables():
    StarType("Evaporating gaseous globule", star_class="red", description="")
    StarType("Pre-stellar core", star_class="red", description="")
    StarType("Giant molecular clouds", star_class="red", description="")
    StarType("Bok globule", star_class="red", description="")
    StarType("Herbig Ae/Be star", star_class="red", description="")
    StarType("T Tauri Star", star_class="red", description="")

    StarType("Red giant", star_class="orange", description="")
    StarType("Yellow giant", star_class="red", description="")
    StarType("Orange giant", star_class="red", description="")
    StarType("Blue giant", star_class="red", description="")
    StarType("White giant", star_class="red", description="")

    StarType("Red dwarf", star_class="green", description="")
    StarType("Orange dwarf", star_class="green", description="")
    StarType("Yellow dwarf", star_class="green", description="")
    StarType("A-type dwarf", star_class="orange", description="")
    StarType("Hot sub-dwarf", star_class="orange", description="")
    StarType("Brown dwarf", star_class="orange", description="")
    StarType("Yellow-White dwarf", star_class="orange", description="")
    StarType("Blue-White dwarf", star_class="orange", description="")
    StarType("White dwarf", star_class="grey", description="")

    StarType("Black hole", star_class="grey", description="")
    StarType("Neutron star", star_class="grey", description="")
    StarType("Wolf-Rayet star", star_class="grey", description="")

    giant_stars_table = RollTable.RollTable(
        options=[
            RollTable.Option(StarType.all_stars["Red giant"], 300),
            RollTable.Option(StarType.all_stars["Yellow giant"], 100),
            RollTable.Option(StarType.all_stars["Orange giant"], 100),
            RollTable.Option(StarType.all_stars["Blue giant"], 250),
            RollTable.Option(StarType.all_stars["White giant"], 250),
        ]
    )

    stellar_nursery_table = RollTable.RollTable(
        options=[
            RollTable.Option(StarType.all_stars["Evaporating gaseous globule"], 0.1),
            RollTable.Option(StarType.all_stars["Pre-stellar core"], 0.1),
            RollTable.Option(StarType.all_stars["Giant molecular clouds"], 0.1),
            RollTable.Option(StarType.all_stars["Bok globule"], 0.1),
            RollTable.Option(StarType.all_stars["Herbig Ae/Be star"], 0.25),
            RollTable.Option(StarType.all_stars["T Tauri Star"], 0.25),
        ]
    )

    galactic_arm_table = RollTable.RollTable(
        options=[
            RollTable.Option(StarType.all_stars["Red dwarf"], 0.454),
            RollTable.Option(StarType.all_stars["Orange dwarf"], 0.072),
            RollTable.Option(StarType.all_stars["Yellow dwarf"], 0.047),
            RollTable.Option(StarType.all_stars["Yellow-White dwarf"], 0.016),
            RollTable.Option(StarType.all_stars["A-type dwarf"], 0.004),
        ]
    )

    inter_arm_table = RollTable.RollTable(
        options=[
            RollTable.Option(StarType.all_stars["Hot sub-dwarf"], 5),
            RollTable.Option(StarType.all_stars["Brown dwarf"], 30),
            RollTable.Option(StarType.all_stars["White dwarf"], 15),
            RollTable.Option(StarType.all_stars["Red dwarf"], 689),
            RollTable.Option(StarType.all_stars["Orange dwarf"], 109),
            RollTable.Option(StarType.all_stars["Yellow dwarf"], 69),
            RollTable.Option(StarType.all_stars["A-type dwarf"], 5),
            RollTable.Option(StarType.all_stars["Yellow-White dwarf"], 27),
            RollTable.Option(StarType.all_stars["Blue-White dwarf"], 1),
            RollTable.Option(StarType.all_stars["Black hole"], 5),
            RollTable.Option(StarType.all_stars["Neutron star"], 5),
        ]
    )

    core_table = RollTable.RollTable(
        options=[
            RollTable.Option(StarType.all_stars["Black hole"], 10),
            RollTable.Option(StarType.all_stars["Neutron star"], 10),
            RollTable.Option(StarType.all_stars["Wolf-Rayet star"], 10),
        ]
    )

    stellar_nursery_table.rolltables.append(RollTable.Option(galactic_arm_table, 0.1))

    galactic_arm_table.rolltables.append(RollTable.Option(stellar_nursery_table, 0.1))
    galactic_arm_table.rolltables.append(RollTable.Option(giant_stars_table, 0.307))

    inter_arm_table.rolltables.append(RollTable.Option(giant_stars_table, 40))

    core_table.rolltables.append(RollTable.Option(giant_stars_table, 60))
    core_table.rolltables.append(RollTable.Option(galactic_arm_table, 20))

    star_rolltables = {
        "stellar_nursery": stellar_nursery_table,
        "galactic_arm": galactic_arm_table,
        "inter_arm": inter_arm_table,
        "core": core_table,
    }


    return star_rolltables


def main():
    star_rolltables = create_star_rolltables()
    print([str(star_rolltables["stellar_nursery"]()) for i in range(10)])
    print([str(star_rolltables["galactic_arm"]()) for i in range(10)])
    print([str(star_rolltables["inter_arm"]()) for i in range(10)])
    print([str(star_rolltables["core"]()) for i in range(10)])
    pass


if __name__ == '__main__':
    main()
