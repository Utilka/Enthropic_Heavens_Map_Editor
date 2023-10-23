import os

import numpy

import numpy as numpy
from PIL import Image, ImageDraw, ImageFont
from hex_poligon_generator import HexagonCreator
import map_to_hex_index
import political
from Civ import *
from System_DB_handler import *

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


def color_explored(out_filepath):
    hex_index = numpy.load("data/hex_types.npy", allow_pickle=True)
    all_civs = load_civs()

    exploration_index = numpy.full(hex_index.shape, False)

    for i in range(hex_index.shape[0]):
        for j in range(hex_index.shape[1]):
            for civ in all_civs:
                exploration_index[i, j] = civ.explored_space[i, j] or exploration_index[i, j]

    hex_cr = HexagonCreator(hex_outer_radius, pixel_offset_of_00_hex, border_size)

    giga_canvas_size = hex_cr.hex_center(exploration_index.shape)
    crop_size = hex_cr.hex_center((0, exploration_index.shape[1]))
    canvas_size = giga_canvas_size[0] - crop_size[0], giga_canvas_size[1]
    hex_cr.offset = (round(-crop_size[0] / 2), 0)

    hex_types_img = Image.new('RGBA', canvas_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(hex_types_img)

    for i in range(exploration_index.shape[0]):
        for j in range(exploration_index.shape[1]):
            if exploration_index[i, j]:
                hexagon = hex_cr((i, j))
                draw.polygon(hexagon, fill="#00000000")
            else:
                if hex_index[i, j] is not None:
                    hexagon = hex_cr((i, j))
                    color_tpl = (0, 0, 0, 125)
                    draw.polygon(hexagon, fill=color_tpl)

    # hex_types_img.show()
    hex_types_img.save(out_filepath)


def color_politicals(turn):
    if not os.path.exists("./maps/players"):
        os.makedirs("./maps/players")

    all_civs = load_civs()
    for civ in all_civs:
        if civ.player_name is not None:
            color_political_player(f"maps/players/hex_political_{turn}_{civ.player_id}_{civ.player_name}.png", civ)

    pass
