import System_DB_handler

import system_generator
import numpy as numpy
from PIL import Image, ImageDraw, ImageFont
from hex_poligon_generator import HexagonCreator

hex_outer_radius = 35
pixel_offset_of_00_hex = (20, 20)
border_size = 2


def draw_hexes(base, data: dict):
    hex_index = base

    hex_cr = HexagonCreator(hex_outer_radius, pixel_offset_of_00_hex, border_size)

    giga_canvas_size = hex_cr.hex_center(hex_index.shape)
    crop_size = hex_cr.hex_center((0, hex_index.shape[1]))
    canvas_size = giga_canvas_size[0] - crop_size[0], giga_canvas_size[1]
    hex_cr.offset = (round(-crop_size[0] / 2), 0)

    hex_map = Image.new('RGBA', canvas_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(hex_map)

    color_tpl = (100, 100, 100, 100)  # the neutral color
    for i in range(hex_index.shape[0]):
        for j in range(hex_index.shape[1]):
            if hex_index[i, j] != None:
                hexagon = hex_cr((i, j))

                draw.polygon(hexagon, fill=color_tpl)

    font = ImageFont.truetype("courbd.ttf", size=12)

    for key in data:
        color_tpl = data[key][0]
        hexagon = hex_cr(key)
        draw.polygon(hexagon, fill=color_tpl)
        draw.text(hex_cr.hex_center(key), data[key][1],
                  anchor="mm", font=font, fill="black", align='center', stroke_width=0)

    hex_map.show()


#
#     hex_map.show()
#
color_map = {}
for rr in system_generator.universal_rr:
    color_map[rr.name] = "#324b76"
for rr in system_generator.unique_bio_rr:
    color_map[rr.name] = "#2b471f"
for rr in system_generator.red_rr:
    color_map[rr.name] = "#924d4d"
for rr in system_generator.grey_rr:
    color_map[rr.name] = "#505050"

for sm in system_generator.universal_modifiers:
    color_map[sm.name] = "#324b76"
for sm in system_generator.fertile_modifiers:
    color_map[sm.name] = "#2b471f"
for sm in system_generator.unique_modifiers:
    color_map[sm.name] = "#734b5f"
for sm in system_generator.young_modifiers:
    color_map[sm.name] = "#924d4d"
for sm in system_generator.extreme_modifiers:
    color_map[sm.name] = "#7e4413"

color_map["grey"] = "#505050"
color_map["red"] = "#924d4d"
color_map["orange"] = "#7e4413"
color_map["green"] = "#2b471f"
color_map["fertile"] = (50, 200, 0, 255)
color_map["infertile"] = "#505050"

f_d = {True: "fertile", False: "infertile"}


def main():
    all_systems = System_DB_handler.load_systems()
    base = numpy.empty(all_systems.shape, dtype=object)
    rare_resourse = {}
    system_mod = {}
    system_type = {}
    system_fert = {}

    for i in range(all_systems.shape[0]):
        for j in range(all_systems.shape[1]):
            sys: system_generator.StarSystem = all_systems[i, j]
            if sys is None:
                continue
            coordinates = (i, j)
            if sys.rare_resource != None:
                rare_resourse[coordinates] = (color_map[sys.rare_resource.name], str(sys.rare_resource_quantity))
            if sys.modifier != None:
                system_mod[coordinates] = (color_map[sys.modifier.name], "")

            system_type[coordinates] = (color_map[sys.system_class],
                                        f"f{sum([p.size_def[p.size] for p in sys.planets if p.sterility == 'Fertile']):.1f} \n" +
                                        f"m{sum([p.size_def[p.size] for p in sys.planets if p.sterility == 'Moderate']):.1f} \n" +
                                        f"s{sum([p.size_def[p.size] for p in sys.planets if p.sterility == 'Sterile']):.1f} \n" +
                                        f"g{sum([p.size_def[p.size] for p in sys.planets if p.sterility == 'Gas giant']):.1f}"
                                        )

            system_fert[coordinates] = (color_map[f_d[sys.has_fertile]],
                                        f"f{sum([p.size_def[p.size] for p in sys.planets if p.sterility == 'Fertile']):.1f}"
                                        )

    # data_to_anal = system_fert
    # draw_hexes(all_systems, data_to_anal)

    draw_hexes(all_systems, system_type)

    draw_hexes(all_systems, system_fert)

    pass


if __name__ == "__main__":
    main()
