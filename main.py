import math
import os

import numpy as numpy
from PIL import Image, ImageDraw, ImageFont

import map_to_hex_index
import political
from hex_poligon_generator import HexagonCreator

from Player_DB_handler import *
from System_DB_handler import *

# from Player_DB_handler import *


hex_outer_radius = 35
pixel_offset_of_00_hex = (20, 20)
border_size = 2

color_map = {
    None: (50, 50, 50, 0),
    "blue-ish": (50, 100, 200, 255),
    "green": (50, 200, 0, 255),
    "purple": (200, 50, 200, 255),
    "red": (230, 0, 0, 255),
    "yellow": (250, 200, 0, 255),
    "s-green": (50, 230, 50, 255),
    "s-blue": (50, 100, 250, 255),
    "s-red": (250, 0, 0, 255),
    "s-orange": (250, 200, 0, 255),
    "p-blue": (0, 30, 150, 255),
    "p-purple": (120, 0, 160, 255),
    "neutral": (100, 100, 100, 100),
}


def color_hexes(in_filepath, out_filepath):
    hex_index = numpy.load(in_filepath, allow_pickle=True)

    hex_cr = HexagonCreator(hex_outer_radius, pixel_offset_of_00_hex, border_size)

    giga_canvas_size = hex_cr.hex_center(hex_index.shape)
    crop_size = hex_cr.hex_center((0, hex_index.shape[1]))
    canvas_size = giga_canvas_size[0] - crop_size[0], giga_canvas_size[1]
    hex_cr.offset = (round(-crop_size[0] / 2), 0)

    hex_types_img = Image.new('RGBA', canvas_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(hex_types_img)

    for i in range(hex_index.shape[0]):
        for j in range(hex_index.shape[1]):
            if hex_index[i, j] != None:
                hexagon = hex_cr((i, j))
                color_tpl = color_map[hex_index[i, j]]
                draw.polygon(hexagon, fill=color_tpl)

    # hex_types_img.show()
    hex_types_img.save(out_filepath)


def coordinate_hexes(in_filepath, out_filepath):
    hex_index = numpy.load(in_filepath, allow_pickle=True)

    hex_cr = HexagonCreator(hex_outer_radius, pixel_offset_of_00_hex, border_size)

    giga_canvas_size = hex_cr.hex_center(hex_index.shape)
    crop_size = hex_cr.hex_center((0, hex_index.shape[1]))
    canvas_size = giga_canvas_size[0] - crop_size[0], giga_canvas_size[1]
    hex_cr.offset = (round(-crop_size[0] / 2), 0)

    hex_coords_img = Image.new('RGBA', canvas_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(hex_coords_img)
    font = ImageFont.truetype("courbd.ttf", size=18)

    for i in range(hex_index.shape[0]):
        for j in range(hex_index.shape[1]):
            if hex_index[i, j] != None:
                draw.text(hex_cr.hex_center((i, j)), f"{i - 42}\n{j - 42}",
                          anchor="mm", font=font, fill="black", align='center', stroke_width=0)
    #
    # # hex_coords_img.show()
    hex_coords_img.save(out_filepath)


def grid_hexes(in_filepath, out_filepath):
    hex_index = numpy.load(in_filepath, allow_pickle=True)

    hex_cr = HexagonCreator(hex_outer_radius, pixel_offset_of_00_hex, border_size)
    giga_canvas_size = hex_cr.hex_center(hex_index.shape)
    crop_size = hex_cr.hex_center((0, hex_index.shape[1]))
    canvas_size = giga_canvas_size[0] - crop_size[0], giga_canvas_size[1]
    hex_cr.offset = (round(-crop_size[0] / 2), 0)
    hex_types_img = Image.new('RGBA', canvas_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(hex_types_img)
    color_tpl = color_map["neutral"]
    for i in range(hex_index.shape[0]):
        for j in range(hex_index.shape[1]):
            if hex_index[i, j] != None:
                hexagon = hex_cr((i, j))
                draw.polygon(hexagon, fill=color_tpl)

    # hex_types_img.show()
    hex_types_img.save(out_filepath)


def color_political(out_filepath):
    all_civs = load_civs()
    political_index = political.generate_pol_index("data/hex_types.npy", all_civs)

    hex_cr = HexagonCreator(hex_outer_radius, pixel_offset_of_00_hex, border_size)
    hex_cr_m = political.MicroHexagonCreator(hex_outer_radius, pixel_offset_of_00_hex, border_size)

    giga_canvas_size = hex_cr.hex_center(political_index.shape)
    crop_size = hex_cr.hex_center((0, political_index.shape[1]))
    canvas_size = giga_canvas_size[0] - crop_size[0], giga_canvas_size[1]
    hex_cr.offset = (round(-crop_size[0] / 2), 0)
    hex_cr_m.offset = (round(-crop_size[0] / 2), 0)

    hex_types_img = Image.new('RGBA', canvas_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(hex_types_img)

    for i in range(political_index.shape[0]):
        for j in range(political_index.shape[1]):
            doms = political_index[i, j]
            if doms['space'] != None:
                hexagon = hex_cr((i, j))
                color_tpl = doms['space'].color
                draw.polygon(hexagon, fill=color_tpl)
                hexagon_m = hex_cr_m((i, j))
                draw.polygon(hexagon_m, fill="#00000000")

            if doms['system'] != None:
                hexagon_m = hex_cr_m((i, j))
                color_tpl = doms['system'].color
                draw.polygon(hexagon_m, fill=color_tpl)

    # hex_types_img.show()
    hex_types_img.save(out_filepath)


def color_political_player(out_filepath, civ):
    hex_index = numpy.load("data/hex_types.npy", allow_pickle=True)
    all_civs = load_civs()

    political_index = political.generate_pol_index("data/hex_types.npy", all_civs)

    hex_cr = HexagonCreator(hex_outer_radius, pixel_offset_of_00_hex, border_size)
    hex_cr_m = political.MicroHexagonCreator(hex_outer_radius, pixel_offset_of_00_hex, border_size)

    giga_canvas_size = hex_cr.hex_center(political_index.shape)
    crop_size = hex_cr.hex_center((0, political_index.shape[1]))
    canvas_size = giga_canvas_size[0] - crop_size[0], giga_canvas_size[1]
    hex_cr.offset = (round(-crop_size[0] / 2), 0)
    hex_cr_m.offset = (round(-crop_size[0] / 2), 0)

    hex_types_img = Image.new('RGBA', canvas_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(hex_types_img)

    for i in range(political_index.shape[0]):
        for j in range(political_index.shape[1]):
            if civ.explored_space[i, j]:
                doms = political_index[i, j]
                if doms['space'] != None:
                    hexagon = hex_cr((i, j))
                    color_tpl = doms['space'].color
                    draw.polygon(hexagon, fill=color_tpl)
                    hexagon_m = hex_cr_m((i, j))
                    draw.polygon(hexagon_m, fill="#00000000")

                if doms['system'] != None:
                    hexagon_m = hex_cr_m((i, j))
                    color_tpl = doms['system'].color
                    draw.polygon(hexagon_m, fill=color_tpl)
            else:
                if hex_index[i, j] is not None:
                    hexagon = hex_cr((i, j))
                    color_tpl = (0, 0, 0, 125)
                    draw.polygon(hexagon, fill=color_tpl)

    # hex_types_img.show()
    hex_types_img.save(out_filepath)


def explore_and_print():
    explored_systems = {
        "101": [(18, -23),
                (18, -24),
                (20, -24),
                (20, -25),
                (19, -23),
                (19, -25),
                (17, -22), ],
        "102": [(-34, 29),
                (-32, 29),
                (-31, 28),
                (-33, 30),
                (-34, 30),
                (-33, 28),
                (-32, 28),
                (-31, 28),
                (-32, 27),
                (-33, 27),
                (-32, 27),
                (-33, 27), ],
        "103": [(-25, 9),
                (-25, 8),
                (-25, 7),
                (-24, 7),
                (-23, 7),
                (-24, 6), ],
        "104": [(31, -30),
                (32, -31),
                (32, -30),
                (32, -29),
                (33, -32),
                (33, -31),
                (33, -29),
                (34, -32),
                (34, -31),
                (34, -30),
                (34, -29),
                (35, -32),
                (35, -31),
                (35, -30), ],
        "105": [(-11, 29),
                (-10, 29),
                (-12, 31),
                (-10, 30),
                (-12, 30),
                (-11, 28),
                (-11, 27),
                (-12, 29),
                (-9, 29),
                (-9, 28), ],
        "106": [(10, 6),
                (11, 5),
                (12, 5),
                (12, 6),
                (11, 7),
                (10, 7),
                (11, 8), ],
        "107": [],
        "108": [(30, -2),
                (31, -3),
                (31, -4),
                (30, -4),
                (29, -3),
                (29, -2),
                (32, -3), ],
        "109": [],
        "110": [(9, -24),
                (10, -24),
                (11, -25), ],
        "111": [(20, 14),
                (19, 15),
                (18, 15),
                (18, 14),
                (19, 13),
                (20, 13), ],
        "112": [(-24, -13),
                (-23, -13),
                (-22, -14), ],
        "113": [(22, -15),
                (22, -14),
                (23, -14),
                (23, -16),
                (24, -16),
                (24, -15),
                (21, -15), ],
        "114": [(1, 20), ],
        "115": [(-39, 4),
                (-38, 3),
                (-39, 5),
                (-38, 5),
                (-37, 4),
                (-37, 3), ],
        "116": [(9, -7),
                (9, -5),
                (8, -6),
                (8, -5),
                (10, -6),
                (10, -7),
                (9, -8),
                (10, -8),
                (11, -8),
                (11, -7),
                (11, -6), ],
        "117": [(-6, -5),
                (-5, -5),
                (-5, -4),
                (-6, -3),
                (-7, -3),
                (-7, -4), ],
        "118": [(-7, -24),
                (-8, -23),
                (-6, -23),
                (-7, -22),
                (-8, -22),
                (-7, -24),
                (-6, -24), ],
        "119": [(-11, 17),
                (-11, 19),
                (-10, 18),
                (-12, 18),
                (-10, 17),
                (-12, 19),
                (-9, 18), ],

    }
    counter = 0
    for civ_id in explored_systems:
        counter += len(explored_systems[civ_id])
    print(counter)

    all_civs = load_civs()
    all_systems = load_systems()
    for civ in all_civs:
        if civ.player_id in explored_systems.keys():
            print(f"{'':_<40}\n{civ.player_id:<3} {civ.player_name}")
            for coords in explored_systems[civ.player_id]:
                civ.explore_star_system(coords)
                shifted_coords = coords[0] + 42, coords[1] + 42
                if all_systems[shifted_coords] is not None:
                    print(f"{coords[0]}\t{coords[1]}")
                    print(all_systems[shifted_coords].description)
                else:
                    print(f"Player {civ.player_id} explored {coords[0]}\t{coords[1]} but it is None")

                print(f"{'':_<20}")
    pass
    save_civs(all_civs)


def color_politicals(turn):
    if not os.path.exists("./maps/players"):
        os.makedirs("./maps/players")

    all_civs = load_civs()
    for civ in all_civs:
        if civ.player_name is not None:
            color_political_player(f"maps/players/hex_political_{turn}_{civ.player_id}_{civ.player_name}.png", civ)

    pass


def count():
    pass
    # hex_index = numpy.load('hex_types.npy', allow_pickle=True)
    # unique, counts = numpy.unique(hex_index, return_counts=True)
    # print((hex_index == "yellow").sum())

def main(turn):
    # pixel_colors = map_to_hex_index.extract_pixel_collors("rolltable.png")
    # hex_colors = map_to_hex_index.convert_to_hex_type_index(pixel_colors)
    # numpy.save('hex_types.npy', hex_colors)
    if not os.path.exists("./maps"):
        os.makedirs("./maps")

    # coordinate_hexes("data/hex_types.npy", "maps/hex_coords.png")
    # grid_hexes("data/hex_types.npy", "maps/hex_grid.png")
    #
    # color_hexes("data/hex_types.npy", "maps/hex_types.png")
    # color_hexes("data/hex_sectors.npy", "maps/hex_sectors.png")
    # color_hexes("data/precursors.npy", "maps/hex_precursors.png")

    color_political("data/hex_types.npy", "maps/hex_political.png")

    # explore_and_print()

    color_politicals(turn)


if __name__ == '__main__':
    main(1)
