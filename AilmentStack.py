
from hlp import *
from SConfig import *
from PIL import Image, ImageDraw, ImageFont


class AilmentStack:
    def __init__(self, powers):
        self._powers = powers

        self._poison_ail    = powers[0]
        self._sleep_ail     = powers[1]
        self._paralysis_ail = powers[2]
        self._blast_ail     = powers[3]
        self._stun_ail      = powers[4]

    def getImage(self) -> Image.Image:
        size = self.getWidth(), self.getHeight()
        image = Image.new("RGBA", size, Colors.transparent)
        return image

    def getWidth(self):
        return int(SConfig.weakness_column_width)

    def getHeight(self):
        ## Same Things :D Calculated
        # icons_sum = SConfig.weakness_column_width + SConfig.weakness_column_width * 5 * SConfig.small_scale
        # paddings_sum = SConfig.weakness_row_padding * 4 * SConfig.small_scale
        icons_sum = SConfig.weakness_column_width * 4
        paddings_sum = SConfig.weakness_row_padding * 3
        return int(icons_sum + paddings_sum)
