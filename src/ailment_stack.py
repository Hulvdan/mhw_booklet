from typing import Tuple

from PIL import Image, ImageDraw, ImageFont  # noqa: WPS102

from . import colors
from .config import (
    AILMENT_FONT_SIZE, DRAW_AILMENT_NUMBERS, FONT_FOLDER, WEAKNESS_COLUMN_WIDTH,
    WEAKNESS_COLUMN_WIDTH_SMALL, WEAKNESS_ROW_PADDING,
    WEAKNESS_ROW_PADDING_SMALL, ZERO_AILMENT_SPACE)
from .helper import alpha_paster
from .images import Images


class AilmentType:
    poison = 0
    sleep = 1
    paralysis = 2
    blast = 3
    stun = 4


class AilmentStack:
    def __init__(self, powers: Tuple[int, int, int, int, int]):
        self._powers = powers

        self._is_faded = not any(power > 1 for power in powers)
        self._poison_ail = powers[0]
        self._sleep_ail = powers[1]
        self._paralysis_ail = powers[2]
        self._blast_ail = powers[3]
        self._stun_ail = powers[4]
        self._max_power = max(self._powers)

    def get_image(self) -> Image.Image:
        """Image of ailments with their powers stacked in column.

        Returns:
            Image of ailments.
        """
        images_instance = Images.get_instance()
        size = (self.width, self.height)
        small_size = (WEAKNESS_COLUMN_WIDTH_SMALL, WEAKNESS_COLUMN_WIDTH_SMALL)
        image = Image.new('RGBA', size, colors.TRANSPARENT)

        alpha_paster(
            image,
            images_instance.ail_ailment(self._is_faded).resize(
                (self.width, self.width)))
        ailments_x = int(0 if DRAW_AILMENT_NUMBERS else (
            WEAKNESS_COLUMN_WIDTH - small_size[0]) / 2)
        last_y = WEAKNESS_ROW_PADDING + WEAKNESS_COLUMN_WIDTH
        images_by_powers = (images_instance.ail_poison,
                            images_instance.ail_sleep,
                            images_instance.ail_paralysis,
                            images_instance.ail_blast,
                            images_instance.ail_stun)
        images_by_powers_faded = (images_instance.ail_poison_faded,
                                  images_instance.ail_sleep_faded,
                                  images_instance.ail_paralysis_faded,
                                  images_instance.ail_blast_faded,
                                  images_instance.ail_stun_faded)
        colors_by_powers = (colors.FONT_POISON,
                            colors.FONT_SLEEP,
                            colors.FONT_PARALYSIS,
                            colors.FONT_BLAST,
                            colors.FONT_STUN)

        for i in range(5):
            if self._powers[i] == 0 and (not ZERO_AILMENT_SPACE):
                continue

            elif self._powers[i] == 1:
                if DRAW_AILMENT_NUMBERS:
                    alpha_paster(image, images_by_powers[i].resize(
                        small_size), (ailments_x, int(last_y)))
                else:
                    alpha_paster(image, images_by_powers_faded[i].resize(
                        small_size), (ailments_x, int(last_y)))

            elif self._powers[i] == 2:
                if DRAW_AILMENT_NUMBERS:
                    alpha_paster(image, images_by_powers[i].resize(
                        small_size), (ailments_x, int(last_y)))
                else:
                    alpha_paster(image, Images.back_small_faded,
                                 (ailments_x, int(last_y)))
                    alpha_paster(image, images_by_powers_faded[i].resize(
                        small_size), (ailments_x, int(last_y)))

            elif self._powers[i] == 3:
                if not DRAW_AILMENT_NUMBERS:
                    alpha_paster(image, Images.back_small,
                                 (ailments_x, int(last_y)))
                alpha_paster(image, images_by_powers[i].resize(
                    small_size), (ailments_x, int(last_y)))
            last_y += WEAKNESS_COLUMN_WIDTH_SMALL + WEAKNESS_ROW_PADDING_SMALL

        drawer = ImageDraw.Draw(image)
        font = ImageFont.truetype(
            str(FONT_FOLDER / '11988.otf'), AILMENT_FONT_SIZE)
        last_y = WEAKNESS_ROW_PADDING + WEAKNESS_COLUMN_WIDTH
        if DRAW_AILMENT_NUMBERS:
            for i in range(5):
                if not ZERO_AILMENT_SPACE:
                    continue
                if self._powers[i] != 0:
                    # Drawing power of ailment.
                    # Spacing "1" by 3 pixels to the right for perfectionism.
                    number_pos = [small_size[0], last_y - 24]
                    if self._powers[i] == 1:
                        number_pos[0] += 3

                    drawer.text(number_pos,
                                str(self._powers[i]),
                                font=font,
                                fill=colors_by_powers[i])
                last_y += (WEAKNESS_COLUMN_WIDTH_SMALL +
                           WEAKNESS_ROW_PADDING_SMALL)

        return image

    @property
    def width(self):
        return WEAKNESS_COLUMN_WIDTH

    @property
    def height(self):
        icons_sum = WEAKNESS_COLUMN_WIDTH * 4
        paddings_sum = WEAKNESS_ROW_PADDING * 3
        return int(icons_sum + paddings_sum)
