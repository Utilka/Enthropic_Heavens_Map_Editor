import math

import numpy as numpy
from PIL import Image, ImageDraw, ImageFont

import map_to_hex_index
from hex_poligon_generator import HexagonCreator

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

def main():
    # pixel_colors = map_to_hex_index.extract_pixel_collors("rolltable.png")
    # hex_colors = map_to_hex_index.convert_to_hex_type_index(pixel_colors)
    # numpy.save('hex_types.npy', hex_colors)
    coordinate_hexes("hex_types.npy", "hex_coords.png")
    grid_hexes("hex_types.npy", "hex_grid.png")

    color_hexes("hex_types.npy", "hex_types.png")
    color_hexes("hex_sectors.npy", "hex_sectors.png")
    color_hexes("precursors.npy", "hex_precursors.png")
    pass


def count():
    pass
    # hex_index = numpy.load('hex_types.npy', allow_pickle=True)
    # unique, counts = numpy.unique(hex_index, return_counts=True)
    # print((hex_index == "yellow").sum())


if __name__ == '__main__':
    main()
    # main()