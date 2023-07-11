import numpy
from PIL import Image

color = {
    (0, 0, 0, 0): None,
    (0, 74, 127, 128): "blue-ish",
    (76, 255, 0, 128): "green",
    (178, 0, 255, 128): "purple",
    (255, 0, 0, 128): "red",
    (255, 216, 0, 128): "yellow",
    (99, 111, 108, 0): None,
    (182, 255, 0, 255): "s-green",
    (0, 148, 255, 255): "s-blue",
    (255, 0, 0, 255): "s-red",
    (255, 216, 0, 255): "s-orange",
    (0, 38, 255, 48): None,
    (0, 38, 255, 255): "p-blue",
    (178, 0, 255, 255): "p-purple"

}

center = (1192, 1173)
hex_width = 23
hex_height = 25
hex_full_width = 24
hex_full_height = 28
hex_field_radius = 42

sidestep = (24, 0)
diagonstep = (12, 22)

leftmost_hex_coord = center[0] - sidestep[0] * 43, center[1]
starting_coord = leftmost_hex_coord[0] - diagonstep[0] * 41, leftmost_hex_coord[1] - diagonstep[1] * 41


def pixel_cord(hex_coord):
    return (starting_coord[0] + hex_coord[0] * sidestep[0] + hex_coord[1] * diagonstep[0],
            starting_coord[1] + hex_coord[0] * sidestep[1] + hex_coord[1] * diagonstep[1])


def extract_pixel_collors(filename):
    im = Image.open(filename)
    im = im.convert("RGBA")
    # Use a breakpoint in the code line below to debug your script.
    print(im.format, im.size, im.mode)

    width, height = im.size

    micro_jija = list(im.getdata())
    # jija = list(micro_jija)
    # uniq_jij = numpy.unique(micro_jija, axis=0)

    jija = [color[i] for i in micro_jija]

    pixel_values = numpy.array(jija).reshape((height, width))
    return pixel_values


def convert_to_hex_type_index(pixel_values):
    hex_index = numpy.empty([hex_field_radius * 2, hex_field_radius * 2], dtype=object)
    for i in range(hex_index.shape[0]):
        for j in range(hex_index.shape[1]):
            w, h = pixel_cord((i, j))
            if h < 0 or w < 0:
                hex_index[i][j] = None
            else:
                try:
                    hex_index[i][j] = pixel_values[h][w]
                except IndexError:
                    hex_index[i][j] = None

    return hex_index


def main():
    pixel_colors = extract_pixel_collors("rolltable.png")
    hex_types = convert_to_hex_type_index(pixel_colors)
    # numpy.save('data/hex_types.npy', hex_types)

    pixel_colors = extract_pixel_collors("sectors.png")
    hex_sectors = convert_to_hex_type_index(pixel_colors)
    # numpy.save('data/hex_sectors.npy', hex_sectors)

    pixel_colors = extract_pixel_collors("precursors.png")
    hex_precursors = convert_to_hex_type_index(pixel_colors)
    # numpy.save('data/precursors.npy', hex_precursors)

    pass


if __name__ == '__main__':
    main()
