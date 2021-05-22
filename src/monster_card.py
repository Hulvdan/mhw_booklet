import os
from typing import List, Optional, Tuple, Union

from PIL import Image, ImageDraw, ImageEnhance, ImageFont

from .ailment_stack import AilmentStack
from .colors import BLACK, BRACES_COLOR
from .config import (
    ATTACK_ICON_WIDTH, ATTACK_ICONS_SPACING_FROM_ICON, ATTACK_SPACING,
    DEBUG_POLYGON, FONT_FOLDER, ICON_BOTTOM_POS, MONSTER_ICON_SIZE,
    MONSTER_ICONS_FOLDER, MONSTER_IMAGE_ENHANCE_COEFFICIENT,
    MONSTER_NAME_FONT_SIZE, SMALL_SCALE, WEAKNESS_COLUMN_PADDING, WEAKNESS_TOP,
    logger)
from .element_weakness_stack import ElementType, ElementWeaknessStack
from .helper import alpha_paster
from .images import Images

ElementWeakness = Union[Tuple[int, int], int]


class MonsterCard:
    """Monster's card with icon, name, attack types and weaknesses."""

    def __init__(self,
                 library: dict,
                 width: int,
                 height: int):
        """Initialization.

        Args:
            library: Monster's data (name, attack_type, weaknesses...).
            width: Card's width.
            height: Card's height.
        """
        self._library = library
        self._name = self._library['name']
        self._color = self._get_name_color()

        self._attack_types = self._library['attack']

        # Element weaknesses
        element_weaknesses: List[ElementWeakness] = self._library['weakness']
        self._fire_res: ElementWeakness = element_weaknesses[0]
        self._water_res: ElementWeakness = element_weaknesses[1]
        self._thunder_res: ElementWeakness = element_weaknesses[2]
        self._ice_res: ElementWeakness = element_weaknesses[3]
        self._dragon_res: ElementWeakness = element_weaknesses[4]

        # Ailment weaknesses
        ail: List[int] = self._library['ailments']
        self._poison_ail = ail[0]
        self._sleep_ail = ail[1]
        self._paralysis_ail = ail[2]
        self._blast_ail = ail[3]
        self._stun_ail = ail[4]

        # Values of element weaknesses
        fire_weakness_value: int = self._fire_res[0] if isinstance(
            self._fire_res, list) else self._fire_res
        water_weakness_value: int = self._water_res[0] if isinstance(
            self._water_res, list) else self._water_res
        thunder_weakness_value: int = self._thunder_res[0] if isinstance(
            self._thunder_res, list) else self._thunder_res
        ice_weakness_value: int = self._ice_res[0] if isinstance(
            self._ice_res, list) else self._ice_res
        dragon_weakness_value: int = self._dragon_res[0] if isinstance(
            self._dragon_res, list) else self._dragon_res

        # Max weakness value of first monster's stage.
        # NOTE: Mb it should be changed to max total value if there are addition
        # of weakness vulnerability in the second monster's form.
        max_elem_weakness = max((fire_weakness_value,
                                 water_weakness_value,
                                 thunder_weakness_value,
                                 ice_weakness_value,
                                 dragon_weakness_value))
        fire_weakness_stack = ElementWeaknessStack(
            ElementType.fire,
            fire_weakness_value != max_elem_weakness,
            self._primary_elem_res(self._fire_res),
            self._secondary_elem_res(self._fire_res))
        water_weakness_stack = ElementWeaknessStack(
            ElementType.water,
            water_weakness_value != max_elem_weakness,
            self._primary_elem_res(self._water_res),
            self._secondary_elem_res(self._water_res))
        thunder_weakness_stack = ElementWeaknessStack(
            ElementType.thunder,
            thunder_weakness_value != max_elem_weakness,
            self._primary_elem_res(self._thunder_res),
            self._secondary_elem_res(self._thunder_res))
        ice_weakness_stack = ElementWeaknessStack(
            ElementType.ice,
            ice_weakness_value != max_elem_weakness,
            self._primary_elem_res(self._ice_res),
            self._secondary_elem_res(self._ice_res))
        dragon_weakness_stack = ElementWeaknessStack(
            ElementType.dragon,
            dragon_weakness_value != max_elem_weakness,
            self._primary_elem_res(self._dragon_res),
            self._secondary_elem_res(self._dragon_res))

        ailment_stack = AilmentStack(ail)
        self._big_stack: Tuple[ElementWeaknessStack] = (
            fire_weakness_stack,
            water_weakness_stack,
            thunder_weakness_stack,
            ice_weakness_stack,
            dragon_weakness_stack,
            ailment_stack)

        self._width = width
        self._height = height
        self._size = (width, height)

        extensions = ['png', 'webp', 'jpg']
        icon_image_path: Optional[str] = None
        for extension in extensions:
            path = MONSTER_ICONS_FOLDER / f'{self._name}.{extension}'
            if os.path.exists(path):
                icon_image_path = path
                break
            logger.debug('No such file "%s", checking other extensions' % path)

        if icon_image_path is None:
            logger.error('Did not find image for "%s"' % self._name)
            raise ValueError('Did not find image for "%s"' % self._name)

        logger.debug('Loading image "%s"' % icon_image_path)
        monster_image: Image.Image = Image.open(icon_image_path)
        if monster_image.mode != 'RGBA':
            logger.debug('Converting image mode "%s" to "RGBA"' %
                         icon_image_path)
            monster_image = monster_image.convert('RGBA')
        self._icon_image = ImageEnhance.Color(
            monster_image).enhance(MONSTER_IMAGE_ENHANCE_COEFFICIENT)
        self._icon_image.thumbnail(
            (MONSTER_ICON_SIZE, MONSTER_ICON_SIZE * 2), Image.ANTIALIAS)

        logger.debug('Created monster card of "%s"' % self._name)

    def __str__(self):
        """String representation of monster's card."""
        return '{}\t[{}{}{}{}{}]\t[{}{}{}{}{}]'.format(
            self._name, *self._library['weakness'], *self._library['ailments'])

    def get_card_image(self) -> Image.Image:
        """Monster's card with icon, name, attack types and weaknesses.

        Returns:
            Image.
        """
        image = Image.new('RGBA', (self._width, self._height))
        drawer = ImageDraw.Draw(image)

        monster_name_font = ImageFont.truetype(
            str(FONT_FOLDER / 'gabriola.ttf'), MONSTER_NAME_FONT_SIZE)

        # Drawing debug polygon
        if DEBUG_POLYGON:
            p1 = (0, 0)
            p2 = (self._width - 1, 0)
            p3 = (self._width - 1, self._height - 1)
            p4 = (0, self._height - 1)
            debug_color = (255, 0, 0, 100)
            drawer.line((p1, p2), fill=debug_color)
            drawer.line((p2, p3), fill=debug_color)
            drawer.line((p3, p4), fill=debug_color)
            drawer.line((p4, p1), fill=debug_color)

        # Drawing monster's icon
        height = self._icon_image.size[1]
        alpha_paster(image, self._icon_image,
                     (0, self._height - ICON_BOTTOM_POS - height))

        # Drawing monster's weaknesses to element types
        x_left = self._width
        for stack in reversed(self._big_stack):
            x_left -= stack.width
            alpha_paster(image,
                         stack.get_image(),
                         (x_left, WEAKNESS_TOP))
            x_left -= WEAKNESS_COLUMN_PADDING

        # Drawing monster's name
        text_size = drawer.textsize(self._name, font=monster_name_font)
        drawer.text(
            ((self._width - text_size[0]) / 2, 0),
            self._name,
            font=monster_name_font,
            fill=self._color)

        # Drawing monster's attack type
        image_y = (self._height - ICON_BOTTOM_POS +
                   ATTACK_ICONS_SPACING_FROM_ICON)
        alpha_paster(image, self._get_monster_attack_image(), (0, image_y))

        logger.info('Created image-card of "%s"' % self._name)
        return image

    @ classmethod
    def _primary_elem_res(cls, elem_res: ElementWeakness) -> int:
        """Get monster's primary element weakness.

        If monster's weaknesses vary through battle (like Kulve Taroth's thunder
        weakness: 3 at the start, 5 at the end), then this function will return
        3.
        Otherwise, it will return monster's weakness.

        Args:
            elem_res: Monster's weakness to the element.

        Returns:
            Primary value.
        """
        if isinstance(elem_res, list):
            return elem_res[0]
        return elem_res

    @ classmethod
    def _secondary_elem_res(cls, elem_res: ElementWeakness) -> Optional[int]:
        """Get monster's secondary element weakness.

        If monster's weaknesses vary through battle (like Kulve Taroth's thunder
        weakness: 3 at the start, 5 at the end), then this function will return
        5.
        Otherwise, it will return None.

        Args:
            elem_res: Monster's weakness to the element.

        Returns:
            Secondary value.
        """
        if isinstance(elem_res, list):
            return elem_res[1]
        return None

    @ classmethod
    def _get_image_by_attack_type(cls, attack_type: str) -> Image.Image:
        """Get image of monster's attack type.

        Args:
            attack_type: Monster's attack type.

        Raises:
            ValueError: Wrong attack type passed from library.

        Returns:
            Image of monster's attack type.
        """
        images_instance = Images.get_instance()

        width = ATTACK_ICON_WIDTH
        size = (width, width)

        img: Optional[Image.Image] = None
        if attack_type == 'waterblight':  # noqa: WPS223
            img = images_instance.waterblight.resize(size)
        elif attack_type == 'dragonblight':  # noqa: WPS223
            img = images_instance.dragonblight.resize(size)
        elif attack_type == 'mud_brackets':
            img_brackets = cls._draw_brackets(icon_size=width, margin=False)
            res_mud = images_instance.mud.resize(size)
            alpha_paster(res_mud, img_brackets, (0, 0))
            img = res_mud
        elif attack_type == 'poison':
            img = images_instance.ail_poison.resize(size)
        elif attack_type == 'water':
            img = images_instance.elem_water.resize(size)
        elif attack_type == 'thunder':
            img = images_instance.elem_thunder.resize(size)
        elif attack_type == 'thunderblight':
            img = images_instance.thunderblight.resize(size)
        elif attack_type == 'fire':
            img = images_instance.elem_fire.resize(size)
        elif attack_type == 'fireblight':
            img = images_instance.fireblight.resize(size)
        elif attack_type == 'stun':
            img = images_instance.ail_stun.resize(size)
        elif attack_type == 'ice':
            img = images_instance.elem_ice.resize(size)
        elif attack_type == 'iceblight':
            img = images_instance.iceblight.resize(size)
        elif attack_type == 'bleeding':
            img = images_instance.ail_bleeding.resize(size)
        elif attack_type == 'blast':
            img = images_instance.ail_blast.resize(size)
        elif attack_type == 'diamond_brackets':
            img_brackets = cls._draw_brackets(icon_size=width, margin=False)
            res_diamond = images_instance.diamond.resize(size)
            alpha_paster(res_diamond, img_brackets, (0, 0))
            img = res_diamond
        elif attack_type == 'sleep':
            img = images_instance.ail_sleep.resize(size)
        elif attack_type == 'dragon':
            img = images_instance.elem_dragon.resize(size)
        elif attack_type == 'effluvial':
            img = images_instance.ail_effluvial.resize(size)
        elif attack_type == 'noxious_poison':
            img = images_instance.noxious_poison.resize(size)
        elif attack_type == 'blastscourge':
            img = images_instance.blastscourge.resize(size)
        elif attack_type == 'defense_down':
            img = images_instance.defense_down.resize(size)

        if img is None:
            raise ValueError(f'Wrong attack_type "{attack_type}"')
        return img

    @ classmethod
    def _draw_brackets(cls, icon_size: int, margin=True) -> Image.Image:
        """Brackets for some of monster's attack types.

        Args:
            icon_size: Size that brackets should occupy.
            margin: Enable spacing around brackets. Defaults to True.

        Returns:
            Image of brackets. Will be layered on image of attack type.
        """
        size = (int(icon_size), int(icon_size))
        image = Image.new('RGBA', size, (0, 0, 0, 0))
        drawer = ImageDraw.ImageDraw(image)
        line_width = 6

        offset = 3 if margin else 0
        if margin:
            p1 = (offset + line_width * 2 - 3, 3)
            p2 = (offset, 3)
            p3 = (offset, icon_size * SMALL_SCALE - 3)
            p4 = (offset + line_width * 2 - 3,
                  icon_size * SMALL_SCALE - 3)

            p5 = (-offset + size[0] - 2 * line_width, 1)
            p6 = (-offset + size[0] - line_width, 1)
            p7 = (-offset + size[0] - line_width, icon_size * SMALL_SCALE)
            p8 = (-offset + size[0] - 2 * line_width,
                  icon_size * SMALL_SCALE)
        else:
            p1 = (offset + line_width * 2, 2)
            p2 = (offset + 1, 2)
            p3 = (offset + 1, icon_size - 6)
            p4 = (offset + line_width * 2, icon_size - 6)

            p5 = (-offset + size[0] - 2 * line_width, 1)
            p6 = (-offset + size[0] - line_width + 2, 1)
            p7 = (-offset + size[0] - line_width + 2,
                  icon_size - 2)
            p8 = (-offset + size[0] - 2 * line_width,
                  icon_size - 2)

        drawer.line((p1, p2), fill=BRACES_COLOR, width=line_width)
        drawer.line((p2, p3), fill=BRACES_COLOR, width=line_width)
        drawer.line((p3, p4), fill=BRACES_COLOR, width=line_width)
        drawer.line((p5, p6), fill=BRACES_COLOR, width=line_width)
        drawer.line((p6, p7), fill=BRACES_COLOR, width=line_width)
        drawer.line((p7, p8), fill=BRACES_COLOR, width=line_width)

        return image

    def _get_name_color(self) -> str:
        if self._library['color'] == '#':
            logger.warning(f'Monster "{self._name}" has undefined name color')
            return BLACK
        return self._library['color']

    def _get_monster_attack_image(self) -> Image.Image:
        """Image of monster's attack type's under monster's icon."""
        image = Image.new('RGBA', (int(MONSTER_ICON_SIZE),
                                   int(ATTACK_ICON_WIDTH)))

        spacing = ATTACK_SPACING
        width = ATTACK_ICON_WIDTH
        count = len(self._attack_types)

        # Drawing each monster's attack type in row w/ calculated spacing
        for im_index in range(count):
            attack_type = self._attack_types[im_index]

            posy = 0
            # Centered!
            posx = (MONSTER_ICON_SIZE / 2 -
                    (count - 1) / 2 * spacing -
                    count / 2 * width +
                    im_index * (spacing + width))

            alpha_paster(image,
                         self._get_image_by_attack_type(attack_type),
                         (int(posx), int(posy)))

        return image
