from typing import Tuple

from PIL import Image

from .config import (
    ELEMENTS_FOLDER, WEAKNESS_COLUMN_WIDTH, WEAKNESS_COLUMN_WIDTH_SMALL, logger)

_default_img_size = (WEAKNESS_COLUMN_WIDTH, WEAKNESS_COLUMN_WIDTH)


def small_image_of_element_weakness(image: Image.Image):
    """Get small version of an image."""
    width = WEAKNESS_COLUMN_WIDTH_SMALL
    return image.resize((width, width))


def fade_image(image: Image.Image):
    """Get faded version of an image."""
    # TODO: Implement fading here & rewrite code!
    return image


def load_image(
        image_path: str,
        image_size: Tuple[int, int] = _default_img_size) -> Image.Image:
    """Getting thumbnailed antialiased image with configured size."""
    logger.debug('Loading image "%s" and resizing it to (%d, %d)' %
                 (image_path, image_size[0], image_size[1]))
    img: Image.Image = Image.open(image_path)
    img.thumbnail(image_size, Image.ANTIALIAS)
    return img


class Images:  # noqa: WPS230
    """Loading all images except monsters."""

    __instance__ = None

    def __init__(self):
        """Loading images from filesystem."""
        logger.info('Loading all images except monsters...')
        weakness_column_width = WEAKNESS_COLUMN_WIDTH
        self.size = [weakness_column_width, weakness_column_width]
        # Image scaling needed to put 5 little stars into height of 3 normal
        # stars. Spacing calculated too
        self.small_scale = 0.59

        self.elem_fire = load_image(ELEMENTS_FOLDER / 'fire.png')
        self.elem_water = load_image(ELEMENTS_FOLDER / 'water.png')
        self.elem_thunder = load_image(ELEMENTS_FOLDER / 'thunder.png')
        self.elem_ice = load_image(ELEMENTS_FOLDER / 'ice.png')
        self.elem_dragon = load_image(ELEMENTS_FOLDER / 'dragon.png')

        self.elem_fire_faded = load_image(ELEMENTS_FOLDER / 'fire_faded.png')
        self.elem_water_faded = load_image(ELEMENTS_FOLDER / 'water_faded.png')
        self.elem_thunder_faded = load_image(
            ELEMENTS_FOLDER / 'thunder_faded.png')
        self.elem_ice_faded = load_image(ELEMENTS_FOLDER / 'ice_faded.png')
        self.elem_dragon_faded = load_image(
            ELEMENTS_FOLDER / 'dragon_faded.png')

        self.fireblight = load_image(ELEMENTS_FOLDER / 'fireblight.png')
        self.waterblight = load_image(ELEMENTS_FOLDER / 'waterblight.png')
        self.iceblight = load_image(ELEMENTS_FOLDER / 'iceblight.png')
        self.thunderblight = load_image(ELEMENTS_FOLDER / 'thunderblight.png')
        self.dragonblight = load_image(ELEMENTS_FOLDER / 'dragonblight.webp')
        self.diamond = load_image(ELEMENTS_FOLDER / 'diamond.png')
        self.mud = load_image(ELEMENTS_FOLDER / 'mud.png')
        self.noxious_poison = load_image(ELEMENTS_FOLDER / 'noxious_poison.png')
        self.blastscourge = load_image(ELEMENTS_FOLDER / 'blastscourge.png')
        self.defense_down = load_image(ELEMENTS_FOLDER / 'defense_down.png')
        self.blastblight = load_image(ELEMENTS_FOLDER / 'blastblight.webp')

        self.ail_poison = load_image(ELEMENTS_FOLDER / 'poison.png')
        self.ail_sleep = load_image(ELEMENTS_FOLDER / 'sleep.png')
        self.ail_paralysis = load_image(ELEMENTS_FOLDER / 'paralysis.png')
        self.ail_blast = load_image(ELEMENTS_FOLDER / 'blast.png')
        self.ail_stun = load_image(ELEMENTS_FOLDER / 'stun.png')

        self.ail_poison_faded = load_image(ELEMENTS_FOLDER / 'poison_faded.png')
        self.ail_sleep_faded = load_image(ELEMENTS_FOLDER / 'sleep_faded.png')
        self.ail_paralysis_faded = load_image(
            ELEMENTS_FOLDER / 'paralysis_faded.png')
        self.ail_blast_faded = load_image(ELEMENTS_FOLDER / 'blast_faded.png')
        self.ail_stun_faded = load_image(ELEMENTS_FOLDER / 'stun_faded.png')


        self.ail_bleeding = load_image(ELEMENTS_FOLDER / 'bleeding.png')
        self.ail_effluvial = load_image(ELEMENTS_FOLDER / 'effluvial.png')

        self._ail_ailment = load_image(ELEMENTS_FOLDER / 'ailment.png')
        self._ail_ailment_faded = load_image(
            ELEMENTS_FOLDER / 'ailment_faded.png')

        self._star = load_image(ELEMENTS_FOLDER / 'star.png')
        self._star_faded = load_image(ELEMENTS_FOLDER / 'star_faded.png')
        self._cross = load_image(ELEMENTS_FOLDER / 'cross.png')
        self._cross_faded = load_image(ELEMENTS_FOLDER / 'cross_faded.png')

        small_size = (self.size[0] * self.small_scale,
                      self.size[1] * self.small_scale)
        self.back_small = load_image(ELEMENTS_FOLDER / 'back.png', small_size)
        self.back_small_faded = load_image(
            ELEMENTS_FOLDER / 'back_faded.png', small_size)
        logger.debug('Images loaded!')

    def ail_ailment(self, faded: bool) -> Image.Image:
        if faded:
            return self._ail_ailment_faded
        return self._ail_ailment

    def cross(self, faded: bool) -> Image.Image:
        if faded:
            return self._cross_faded
        return self._cross

    def star(self, faded: bool) -> Image.Image:
        if faded:
            return self._star_faded
        return self._star

    @classmethod
    def get_instance(cls) -> 'Images':
        """Singleton pattern."""
        if cls.__instance__ is None:
            cls.__instance__ = Images()
        return cls.__instance__
