
from hlp import *
from SConfig import *
from PIL import Image, ImageDraw, ImageFont


class WeaknessStack:
    def __init__(self, kind, is_faded, power, power_secondary=-1):
        self._kind = kind
        self._power = power
        self._power_secondary = power_secondary
        self._is_faded = is_faded

    def getImage(self) -> Image.Image:
        size = self.getWidth(), self.getHeight()
        image = Image.new("RGBA", size, Colors.transparent)
        if self._kind == 0:
            alphaPaster(image, Images.image_elem_fire if not self._is_faded else Images.image_elem_fire_faded)
        elif self._kind == 1:
            alphaPaster(image, Images.image_elem_water if not self._is_faded else Images.image_elem_water_faded)
        elif self._kind == 2:
            alphaPaster(image, Images.image_elem_thunder if not self._is_faded else Images.image_elem_thunder_faded)
        elif self._kind == 3:
            alphaPaster(image, Images.image_elem_ice if not self._is_faded else Images.image_elem_ice_faded)
        elif self._kind == 4:
            alphaPaster(image, Images.image_elem_dragon if not self._is_faded else Images.image_elem_dragon_faded)
        alphaPaster(image, self._getPowerValueImage(), (0, SConfig.weakness_column_width + SConfig.weakness_row_padding))
        return image
    
    def _getPowerValueImage(self) -> Image.Image:
        image = Image.new("RGBA", (SConfig.weakness_column_width, SConfig.weakness_column_width * 3 + SConfig.weakness_row_padding * 2))
        if self._power_secondary == -1:
            if self._power == 0:
                alphaPaster(image, Images.image_cross if not self._is_faded else Images.image_cross_faded, (0,0))
            for i in range(self._power):
                alphaPaster(image, Images.image_star_faded if self._is_faded else Images.image_star, (0,SConfig.weakness_column_width * i + SConfig.weakness_row_padding * i))
        else:
            new_size = (int(SConfig.weakness_column_width * SConfig.small_scale), int(SConfig.weakness_column_width * SConfig.small_scale))
            little_star = Images.image_star.resize(new_size)
            little_star_faded = Images.image_star_faded.resize(new_size)
            little_cross = Images.image_cross.resize(new_size)
            little_cross_faded = Images.image_cross_faded.resize(new_size)
            little_image_left_pos = int((SConfig.weakness_column_width - new_size[0]) / 2)
            last_y = 0

            if self._power == 0:
                alphaPaster(image, little_cross_faded if not self._is_faded else little_cross, (little_image_left_pos, 0))

            for i in range(self._power):
                little_star_y = int(i * SConfig.small_scale * SConfig.weakness_row_padding + i * SConfig.small_scale * SConfig.weakness_column_width)
                alphaPaster(image, little_star_faded if not self._is_faded else little_star, (little_image_left_pos, little_star_y))

            for i in range(self._power_secondary + 1 if self._power_secondary == 0 else self._power_secondary):
                if self._power_secondary == 0:
                    if SConfig.drawCrossAtBottom:
                        alphaPaster(image, little_cross_faded if not self._is_faded else little_cross, (little_image_left_pos, image.size[1] - new_size[1]))
                    else:
                        last_y = int((self._power if self._power > 0 else 1) * new_size[1] + (self._power if self._power > 0 else 1) * SConfig.small_scale * SConfig.weakness_row_padding)
                        alphaPaster(image, little_cross_faded if not self._is_faded else little_cross, (little_image_left_pos, last_y))

            for k in range(self._power_secondary):
                last_y = int((self._power if self._power > 0 else 1) * new_size[1] + (self._power if self._power > 0 else 1) * SConfig.small_scale * SConfig.weakness_row_padding)
                little_star_y = int(k * SConfig.small_scale * SConfig.weakness_row_padding + k * SConfig.small_scale * SConfig.weakness_column_width + last_y)
                alphaPaster(image, little_star_faded if not self._is_faded else little_star, (little_image_left_pos, little_star_y))

            alphaPaster(image, self._drawBrackets(1 if self._power_secondary == 0 else self._power_secondary, self._is_faded, SConfig.weakness_column_width, SConfig.weakness_row_padding * SConfig.small_scale), (0, last_y))

        return image

    @staticmethod
    def _drawBrackets(images_count, is_not_faded, icon_size, padding, margin=True) -> Image.Image:
        size = (int(icon_size), int(icon_size * images_count + padding * (images_count - 1)))
        image = Image.new("RGBA", size, (0,0,0,0))
        drawer = ImageDraw.ImageDraw(image)
        line_width = 2

        offset = 3 if margin else 0
        if margin:
            p1 = (offset+line_width*2-1, 1)
            p2 = (offset+0, 1)
            p3 = (offset+0,              icon_size * images_count * SConfig.small_scale + padding * (images_count - 1) * SConfig.small_scale-1)
            p4 = (offset+line_width*2-1, icon_size * images_count * SConfig.small_scale + padding * (images_count - 1) * SConfig.small_scale-1)

            p5 = (-offset+size[0] - 2*line_width, 0)
            p6 = (-offset+size[0] - line_width, 0)
            p7 = (-offset+size[0] - line_width,   icon_size * images_count * SConfig.small_scale + padding * (images_count - 1) * SConfig.small_scale)
            p8 = (-offset+size[0] - 2*line_width, icon_size * images_count * SConfig.small_scale + padding * (images_count - 1) * SConfig.small_scale)
        else:
            p1 = (offset+line_width*2-1, 1)
            p2 = (offset+0, 1)
            p3 = (offset+0,              icon_size * images_count + padding * (images_count - 1) - 2)
            p4 = (offset+line_width*2-1, icon_size * images_count + padding * (images_count - 1) - 2)

            p5 = (-offset+size[0] - 2*line_width, 0)
            p6 = (-offset+size[0] - line_width, 0)
            p7 = (-offset+size[0] - line_width,   icon_size * images_count + padding * (images_count - 1) - 1)
            p8 = (-offset+size[0] - 2*line_width, icon_size * images_count + padding * (images_count - 1) - 1)

        clr = SConfig.braces_color_faded if not is_not_faded else SConfig.braces_color
        drawer.line((p1, p2), fill=clr, width=line_width)
        drawer.line((p2, p3), fill=clr, width=line_width)
        drawer.line((p3, p4), fill=clr, width=line_width)
        drawer.line((p5, p6), fill=clr, width=line_width)
        drawer.line((p6, p7), fill=clr, width=line_width)
        drawer.line((p7, p8), fill=clr, width=line_width)

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
