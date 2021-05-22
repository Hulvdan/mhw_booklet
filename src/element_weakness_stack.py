from typing import Optional

from PIL import Image, ImageDraw

from . import colors
from .config import (
    DRAW_CROSS_AT_THE_BOTTOM, SMALL_SCALE, WEAKNESS_COLUMN_WIDTH,
    WEAKNESS_COLUMN_WIDTH_SMALL, WEAKNESS_ROW_PADDING,
    WEAKNESS_ROW_PADDING_SMALL, logger)
from .helper import alpha_paster
from .images import Images, small_image_of_element_weakness


class ElementType:
    fire = 0
    water = 1
    thunder = 2
    ice = 3
    dragon = 4


class ElementWeaknessStack:
    """Instance of monster's weakness to element."""

    def __init__(self,
                 element_type: ElementType,
                 is_faded: bool,
                 power: int,
                 power_secondary: Optional[int] = None):
        """Initialization.

        Args:
            element_type: Type of the element.
            is_faded: Should image be faded. Means that this is not the best
                choice. There are better options.
            power: How much is monster vulnerable to that element.
            power_secondary: If monster has different
                coefficient vulnerability to that element (mb in another stage).
        """
        self._element_type = element_type
        self._power = power
        self._power_secondary = power_secondary
        self._is_faded = is_faded

    def get_image(self) -> Image.Image:
        """Get element type's image with stars (or cross).

        Indicates how much is monster vulnerable to the element type.
        """
        size = self.width, self.height
        image = Image.new('RGBA', size, colors.TRANSPARENT)

        alpha_paster(image, self._get_element_image(
            self._element_type, self._is_faded))

        pos = (0, WEAKNESS_COLUMN_WIDTH + WEAKNESS_ROW_PADDING)
        alpha_paster(image, self._get_power_value_image(), pos)

        logger.debug('Created Element Weakness Stack image')
        return image

    @classmethod
    def _get_element_image(cls, element_type: ElementType, faded: bool):
        """Get image of the element."""
        images_instance = Images.get_instance()

        if element_type == ElementType.fire:
            if faded:
                return images_instance.elem_fire_faded
            return images_instance.elem_fire

        elif element_type == ElementType.water:
            if faded:
                return images_instance.elem_water_faded
            return images_instance.elem_water

        elif element_type == ElementType.thunder:
            if faded:
                return images_instance.elem_thunder_faded
            return images_instance.elem_thunder

        elif element_type == ElementType.ice:
            if faded:
                return images_instance.elem_ice_faded
            return images_instance.elem_ice

        elif element_type == ElementType.dragon:
            if faded:
                return images_instance.elem_dragon_faded
            return images_instance.elem_dragon

        raise ValueError(f'Wrong ElementType "{element_type}"!')

    def _get_power_value_image(self) -> Image.Image:
        """Returns image with element type and stars (or cross).

        Stars indicate how much monster is vulnerable to the element.
        Cross is drawn if monster is not vulnerable to the element type.

        Also, supports 2 stages. Stars (and cross) will be smaller, captured in
        brackets.
        """
        images_instance: Images = Images.get_instance()

        height = (WEAKNESS_COLUMN_WIDTH * 3 + WEAKNESS_ROW_PADDING * 2)

        placeholder_img = Image.new(
            'RGBA', (WEAKNESS_COLUMN_WIDTH, height))

        if self._power_secondary is None:
            if self._power == 0:
                img_cross = images_instance.cross(self._is_faded)
                alpha_paster(placeholder_img, img_cross, (0, 0))

            for row in range(self._power):
                star_y = (WEAKNESS_COLUMN_WIDTH * row +
                          WEAKNESS_ROW_PADDING * row)
                img_star = images_instance.star(self._is_faded)
                alpha_paster(placeholder_img, img_star, (0, star_y))
        else:
            new_size = (WEAKNESS_COLUMN_WIDTH_SMALL,
                        WEAKNESS_COLUMN_WIDTH_SMALL)
            little_star = small_image_of_element_weakness(
                images_instance.star(self._is_faded))
            little_cross = small_image_of_element_weakness(
                images_instance.cross(self._is_faded))
            little_image_left_pos = (
                WEAKNESS_COLUMN_WIDTH - new_size[0]) // 2

            # Drawing cross if no power
            if self._power == 0:
                alpha_paster(placeholder_img, little_cross,
                             (little_image_left_pos, 0))

            # Drawing little stars
            for row in range(self._power):
                little_star_y = int(row * WEAKNESS_ROW_PADDING_SMALL +
                                    row * WEAKNESS_COLUMN_WIDTH_SMALL)
                alpha_paster(placeholder_img, little_star,
                             (little_image_left_pos, little_star_y))

            # Drawing cross if no power_secondary
            if self._power_secondary == 0:
                if DRAW_CROSS_AT_THE_BOTTOM:
                    alpha_paster(
                        placeholder_img,
                        little_cross,
                        (little_image_left_pos,
                            placeholder_img.size[1] - new_size[1])
                    )
                else:
                    last_y = (
                        max(1, self._power) * new_size[1] +
                        max(self._power, 1) * WEAKNESS_ROW_PADDING_SMALL)
                    alpha_paster(placeholder_img,
                                 little_cross,
                                 (little_image_left_pos, last_y))

            # Drawing secondary stars
            for row in range(self._power_secondary):
                power_c = max(1, self._power)
                last_y = (
                    power_c * new_size[1] +
                    power_c * WEAKNESS_ROW_PADDING_SMALL)
                little_star_y = (
                    row * WEAKNESS_ROW_PADDING_SMALL +
                    row * WEAKNESS_COLUMN_WIDTH_SMALL + last_y)
                alpha_paster(placeholder_img, little_star,
                             (little_image_left_pos, little_star_y))

            # Drawing brackets on secondary stars (or cross)
            alpha_paster(
                placeholder_img,
                self._get_brackets_img(
                    max(1, self._power_secondary),
                    self._is_faded,
                    WEAKNESS_COLUMN_WIDTH,
                    WEAKNESS_ROW_PADDING_SMALL),
                (0, last_y))

        return placeholder_img

    @classmethod
    def _get_brackets_img(cls,
                          images_count: int,
                          is_faded: bool,
                          icon_size: int,
                          top_padding: int,
                          draw_margin=True) -> Image.Image:
        """Get image of brackets.

        It will be layered on placeholder image later, capturing small stars (or
        cross).
        """
        size = (int(icon_size), int(
            icon_size * images_count + top_padding * (images_count - 1)))
        image = Image.new('RGBA', size, (0, 0, 0, 0))
        drawer = ImageDraw.ImageDraw(image)
        line_width = 6

        offset = 3 if draw_margin else 0
        if draw_margin:
            p1 = (offset + line_width * 2 - 3, 3)
            p2 = (offset, 3)
            p3 = (offset, icon_size * images_count * SMALL_SCALE +
                  top_padding * (images_count - 1) * SMALL_SCALE - 3)
            p4 = (offset + line_width * 2 - 3,
                  icon_size * images_count * SMALL_SCALE +
                  top_padding * (images_count - 1) * SMALL_SCALE - 3)

            p5 = (-offset + size[0] - 2 * line_width, 1)
            p6 = (-offset + size[0] - line_width, 1)
            p7 = (-offset + size[0] - line_width,
                  icon_size * images_count * SMALL_SCALE +
                  top_padding * (images_count - 1) * SMALL_SCALE)
            p8 = (-offset + size[0] - 2 * line_width,
                  icon_size * images_count * SMALL_SCALE +
                  top_padding * (images_count - 1) * SMALL_SCALE)
        else:
            p1 = (offset + line_width * 2 - 3, 1)
            p2 = (offset, 1)
            p3 = (offset, icon_size *
                  images_count + top_padding * (images_count - 1) - 6)
            p4 = (offset + line_width * 2 - 3, icon_size *
                  images_count + top_padding * (images_count - 1) - 6)

            p5 = (-offset + size[0] - 2 * line_width, 0)
            p6 = (-offset + size[0] - line_width, 0)
            p7 = (-offset + size[0] - line_width, icon_size *
                  images_count + top_padding * (images_count - 1) - 2)
            p8 = (-offset + size[0] - 2 * line_width, icon_size *
                  images_count + top_padding * (images_count - 1) - 2)

        clr = colors.BRACES_COLOR_FADED if is_faded else colors.BRACES_COLOR
        drawer.line((p1, p2), fill=clr, width=line_width)
        drawer.line((p2, p3), fill=clr, width=line_width)
        drawer.line((p3, p4), fill=clr, width=line_width)
        drawer.line((p5, p6), fill=clr, width=line_width)
        drawer.line((p6, p7), fill=clr, width=line_width)
        drawer.line((p7, p8), fill=clr, width=line_width)

        return image

    @property
    def width(self):
        """Width of weakness image."""
        return WEAKNESS_COLUMN_WIDTH

    @property
    def height(self):
        """Height of weakness image. Includes element image."""
        icons_sum = WEAKNESS_COLUMN_WIDTH * 4
        paddings_sum = WEAKNESS_ROW_PADDING * 3
        return icons_sum + paddings_sum
