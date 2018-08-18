
from hlp import *
from SConfig import *
from PIL import Image, ImageDraw, ImageFont


class AilmentStack:
    def __init__(self, powers, draw_numbers):
        self._powers = powers

        self._is_faded = not any(x > 1 for x in powers)
        self._poison_ail    = powers[0]
        self._sleep_ail     = powers[1]
        self._paralysis_ail = powers[2]
        self._blast_ail     = powers[3]
        self._stun_ail      = powers[4]
        self._max_power = max(self._powers)

        self._draw_numbers = draw_numbers

    def getImage(self) -> Image.Image:
        size = self.getWidth(), self.getHeight()
        small_size = tuple([int(SConfig.weakness_column_width * SConfig.small_scale)] * 2)
        image = Image.new("RGBA", size, Colors.transparent)
        image_numbers = Image.new("RGBA", size, Colors.transparent)

        alphaPaster(image, Images.image_ail_ailment if not self._is_faded else Images.image_ail_ailment_faded)
        ailments_x = int(0 if self._draw_numbers else (SConfig.weakness_column_width - small_size[0]) / 2)
        last_y = SConfig.weakness_row_padding + SConfig.weakness_column_width
        images_by_powers = (Images.image_ail_poison,
                            Images.image_ail_sleep,
                            Images.image_ail_paralysis,
                            Images.image_ail_blast,
                            Images.image_ail_stun)
        images_by_powers_faded = (Images.image_ail_poison_faded,
                                  Images.image_ail_sleep_faded,
                                  Images.image_ail_paralysis_faded,
                                  Images.image_ail_blast_faded,
                                  Images.image_ail_stun_faded)
        colors_by_powers = (Colors.font_poison,
                            Colors.font_sleep,
                            Colors.font_paralysis,
                            Colors.font_blast,
                            Colors.font_stun)

        for i in range(5):
            if self._powers[i] == 0 and (not SConfig.zero_ailment_space):
                continue

            elif self._powers[i] == 1:
                if self._draw_numbers:
                    alphaPaster(image, images_by_powers[i].resize(small_size), (ailments_x, int(last_y)))
                else:
                    alphaPaster(image, images_by_powers_faded[i].resize(small_size), (ailments_x, int(last_y)))

            elif self._powers[i] == 2:
                if self._draw_numbers:
                    alphaPaster(image, images_by_powers[i].resize(small_size), (ailments_x, int(last_y)))
                else:
                    alphaPaster(image, Images.image_back_small_faded, (ailments_x, int(last_y)))
                    alphaPaster(image, images_by_powers_faded[i].resize(small_size), (ailments_x, int(last_y)))

            elif self._powers[i] == 3:
                if not self._draw_numbers:
                    alphaPaster(image, Images.image_back_small, (ailments_x, int(last_y)))
                alphaPaster(image, images_by_powers[i].resize(small_size), (ailments_x, int(last_y)))
            last_y += (SConfig.weakness_column_width + SConfig.weakness_row_padding) * SConfig.small_scale


        drawer = ImageDraw.Draw(image)
        font = ImageFont.truetype("11988.otf", 28)
        last_y = SConfig.weakness_row_padding + SConfig.weakness_column_width
        if self._draw_numbers:
            for i in range(5):
                if not SConfig.zero_ailment_space:
                    continue
                if self._powers[i] != 0:
                    drawer.text((small_size[0] + (1 if self._powers[i] == 1 else 0), last_y-8), str(self._powers[i]), font=font, fill=colors_by_powers[i])
                last_y += (SConfig.weakness_column_width + SConfig.weakness_row_padding) * SConfig.small_scale


        # Image.alpha_composite(image, image_numbers)
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
