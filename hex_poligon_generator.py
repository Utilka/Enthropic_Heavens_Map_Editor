import math

from PIL import Image, ImageDraw


class HexagonCreator(object):

    def __init__(self, size: int, offset: (int, int), border: int):
        """
        pointy top hexes,
        in all coordinates width is first, height is second
        :type border: distance between hexes
        :type size: radius of the outer circle of hexagon
        :type offset: (height, width) of offset for hex grid
        """
        self.border = border
        self.size = size
        self.offset = offset

    @property
    def col_width(self):
        return round(math.floor(math.sqrt(3) * (self.size + self.border)))

    @property
    def row_height(self):
        return round((self.size + self.border) * 2)

    @property
    def q(self):
        return self.col_width, 0

    @property
    def r(self):
        return round(self.col_width / 2), round(self.row_height * 0.75)

    def __call__(self, coord):
        # jij = [angle_deg for angle_deg in range(30, 390, 60)]
        p_center = self.hex_center(coord)

        hexus = []
        for angle_deg in range(30, 390, 60):
            angle_rad = math.radians(angle_deg)
            p_x = p_center[0] + round(math.cos(angle_rad) * self.size)
            p_y = p_center[1] + round(math.sin(angle_rad) * self.size)
            hexus.append((p_x, p_y))

        return hexus

    def hex_center(self, coord):
        return (coord[0] * self.q[0] + coord[1] * self.r[0] + self.offset[0],
                coord[0] * self.q[1] + coord[1] * self.r[1] + self.offset[1])


def main():
    image = Image.new('RGBA', (200, 200), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    hex_cr = HexagonCreator(20, (20, 20), 2)
    for i in range(3):
        for j in range(3):
            hexagon = hex_cr((i, j))
            draw.polygon(hexagon, fill='red')
    image.show()


if __name__ == '__main__':
    main()
