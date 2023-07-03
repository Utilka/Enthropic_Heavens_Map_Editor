import System_DB_handler

import system_generator
import numpy as numpy
from PIL import Image, ImageDraw, ImageFont
from hex_poligon_generator import HexagonCreator

hex_outer_radius = 35
pixel_offset_of_00_hex = (20, 20)
border_size = 2

caps_natr_matrix = {
    "Fertile": {"Cold": [30, 20, 5, 8],
                "Temperate": [30, 30, 10, 5],
                "Hot": [30, 20, 15, 4],
                },
    "Moderate": {"Cold": [2, 1, 4, 6],
                 "Temperate": [4, 2, 8, 4],
                 "Hot": [2, 1, 10, 3],
                 },
    "Sterile": {"Cold": [1, 0, 1, 3],
                "Temperate": [2, 0, 2, 2],
                "Hot": [1, 0, 2, 2],
                },
    "Gas giant": {"Cold": [0, 0, 0, 0],
                  "Temperate": [0, 0, 0, 0],
                  "Hot": [0, 0, 0, 0],
                  }, }


def draw_hexes(base, data: dict,out_filepath):
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
        draw.text(hex_cr.hex_center(key), f"{key[0] - 42}:{key[1]  - 42}\n"+data[key][1],
                  anchor="mm", font=font, fill="black", align='center', stroke_width=0)

    # hex_map.show()
    hex_map.save(out_filepath)


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
    sys_matrixs = {}

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
                                        f"f{sum([p.size_def[p.size] for p in sys.planets if p.sterility == 'Fertile']):.1f} " +
                                        f"m{sum([p.size_def[p.size] for p in sys.planets if p.sterility == 'Moderate']):.1f} \n" +
                                        f"s{sum([p.size_def[p.size] for p in sys.planets if p.sterility == 'Sterile']):.1f} " +
                                        f"g{sum([p.size_def[p.size] for p in sys.planets if p.sterility == 'Gas giant']):.1f}"
                                        )

            system_fert[coordinates] = (color_map[f_d[sys.has_fertile]],
                                        f"f{sum([p.size_def[p.size] for p in sys.planets if p.sterility == 'Fertile']):.1f}"
                                        )
            matrx = {
                "Fertile": {"Cold": sum([p.size_def[p.size] for p in sys.planets if
                                         (p.sterility == 'Fertile' and p.temperature == 'Cold')]),
                            "Temperate": sum([p.size_def[p.size] for p in sys.planets if
                                              (p.sterility == 'Fertile' and p.temperature == 'Temperate')]),
                            "Hot": sum([p.size_def[p.size] for p in sys.planets if
                                        (p.sterility == 'Fertile' and p.temperature == 'Hot')]),
                            },
                "Moderate": {"Cold": sum([p.size_def[p.size] for p in sys.planets if
                                          (p.sterility == 'Moderate' and p.temperature == 'Cold')]),
                             "Temperate": sum([p.size_def[p.size] for p in sys.planets if
                                               (p.sterility == 'Moderate' and p.temperature == 'Temperate')]),
                             "Hot": sum([p.size_def[p.size] for p in sys.planets if
                                         (p.sterility == 'Moderate' and p.temperature == 'Hot')]),
                             },
                "Sterile": {"Cold": sum([p.size_def[p.size] for p in sys.planets if
                                         (p.sterility == 'Sterile' and p.temperature == 'Cold')]),
                            "Temperate": sum([p.size_def[p.size] for p in sys.planets if
                                              (p.sterility == 'Sterile' and p.temperature == 'Temperate')]),
                            "Hot": sum([p.size_def[p.size] for p in sys.planets if
                                        (p.sterility == 'Sterile' and p.temperature == 'Hot')]),
                            },
                "Gas giant": {"Cold": sum([p.size_def[p.size] for p in sys.planets if
                                           (p.sterility == 'Gas giant' and p.temperature == 'Cold')]),
                              "Temperate": sum([p.size_def[p.size] for p in sys.planets if
                                                (p.sterility == 'Gas giant' and p.temperature == 'Temperate')]),
                              "Hot": sum([p.size_def[p.size] for p in sys.planets if
                                          (p.sterility == 'Gas giant' and p.temperature == 'Hot')]),
                              }, }
            sys_matrixs[coordinates] = matrx

    nat_system_prod = {}

    maxs = (0, 0, 0, 0)
    for coord in sys_matrixs:
        jij = (
            sum([
                sum([sys_matrixs[coord][f_key][t_key] * caps_natr_matrix[f_key][t_key][0]
                     for t_key in sys_matrixs[coord][f_key]
                     ]) for f_key in sys_matrixs[coord]]
            ), sum([
                sum([sys_matrixs[coord][f_key][t_key] * caps_natr_matrix[f_key][t_key][1]
                     for t_key in sys_matrixs[coord][f_key]
                     ]) for f_key in sys_matrixs[coord]]
            ), sum([
                sum([sys_matrixs[coord][f_key][t_key] * caps_natr_matrix[f_key][t_key][2]
                     for t_key in sys_matrixs[coord][f_key]
                     ]) for f_key in sys_matrixs[coord]]
            ), sum([
                sum([sys_matrixs[coord][f_key][t_key] * caps_natr_matrix[f_key][t_key][3]
                     for t_key in sys_matrixs[coord][f_key]
                     ]) for f_key in sys_matrixs[coord]]
            ),
        )
        maxs = (max(jij[0], maxs[0]), max(jij[1], maxs[1]), max(jij[2], maxs[2]), max(jij[3], maxs[3]))
        nat_system_prod[coord] = jij

    pass
    nat_system_prod_prt = {}
    for coord in nat_system_prod:
        nat_system_prod_prt[coord] = ((
                                       int(nat_system_prod[coord][2]/maxs[2]*255),
                                       int(nat_system_prod[coord][1]/maxs[1]*255),
                                       int(nat_system_prod[coord][3]/maxs[3]*255),
                                       int(nat_system_prod[coord][0]/maxs[0]*255)),
                                      f"{nat_system_prod[coord][0]:.1f} {nat_system_prod[coord][1]:.1f}\n{nat_system_prod[coord][2]:.1f} {nat_system_prod[coord][3]:.1f}")

    # data_to_anal = system_fert
    # draw_hexes(all_systems, data_to_anal)

    draw_hexes(all_systems, system_fert, "maps/fert.png")
    draw_hexes(all_systems, nat_system_prod_prt,"maps/nat_prod.png")
    #
    draw_hexes(all_systems, rare_resourse,"maps/rare.png")
    draw_hexes(all_systems, system_mod,"maps/mod.png")
    draw_hexes(all_systems, system_type,"maps/type.png")




    pass


if __name__ == "__main__":
    main()
