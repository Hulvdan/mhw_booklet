from typing import Tuple

from PIL import Image

from .config import ELEMENTS_FOLDER, WEAKNESS_COLUMN_WIDTH, WEAKNESS_COLUMN_WIDTH_SMALL

_default_img_size = (WEAKNESS_COLUMN_WIDTH, WEAKNESS_COLUMN_WIDTH)


def small_image(image: Image.Image):
    """Get small version of an image."""
    width = WEAKNESS_COLUMN_WIDTH_SMALL
    return image.resize((width, width))


def fade_image(image: Image.Image):
    """Get faded version of an image."""
    # TODO: Implement fading here & rewrite code!
    return image


def load_image(
        image_path: str,
        image_size: Tuple[float, float] = _default_img_size) -> Image.Image:
    """Getting thumbnailed antialiased image with configured size."""
    img: Image.Image = Image.open(image_path)
    img.thumbnail(image_size, Image.ANTIALIAS)
    return img


class Images:  # noqa: WPS230
    """Loading images of everything, but not monster thumbnails."""

    __instance__ = None

    def __init__(self):
        """Loading images from filesystem."""
        weakness_column_width = WEAKNESS_COLUMN_WIDTH
        self.size = [weakness_column_width, weakness_column_width]
        # Image scaling needed to put 5 little stars into height of 3 normal
        # stars. Spacing calculated too
        self.small_scale = 0.59

        self.image_elem_fire = load_image(ELEMENTS_FOLDER / 'fire.png')
        self.image_elem_water = load_image(ELEMENTS_FOLDER / 'water.png')
        self.image_elem_thunder = load_image(ELEMENTS_FOLDER / 'thunder.png')
        self.image_elem_ice = load_image(ELEMENTS_FOLDER / 'ice.png')
        self.image_elem_dragon = load_image(ELEMENTS_FOLDER / 'dragon.png')

        self.image_elem_fire_faded = load_image(
            ELEMENTS_FOLDER / 'fire_faded.png')
        self.image_elem_water_faded = load_image(
            ELEMENTS_FOLDER / 'water_faded.png')
        self.image_elem_thunder_faded = load_image(
            ELEMENTS_FOLDER / 'thunder_faded.png')
        self.image_elem_ice_faded = load_image(
            ELEMENTS_FOLDER / 'ice_faded.png')
        self.image_elem_dragon_faded = load_image(
            ELEMENTS_FOLDER / 'dragon_faded.png')

        self.image_fireblight = load_image(ELEMENTS_FOLDER / 'fireblight.png')
        self.image_waterblight = load_image(ELEMENTS_FOLDER / 'waterblight.png')
        self.image_iceblight = load_image(ELEMENTS_FOLDER / 'iceblight.png')
        self.image_thunderblight = load_image(
            ELEMENTS_FOLDER / 'thunderblight.png')
        self.image_diamond = load_image(ELEMENTS_FOLDER / 'diamond.png')
        self.image_mud = load_image(ELEMENTS_FOLDER / 'mud.png')

        self.image_ail_poison = load_image(ELEMENTS_FOLDER / 'poison.png')
        self.image_ail_sleep = load_image(ELEMENTS_FOLDER / 'sleep.png')
        self.image_ail_paralysis = load_image(ELEMENTS_FOLDER / 'paralysis.png')
        self.image_ail_blast = load_image(ELEMENTS_FOLDER / 'blast.png')
        self.image_ail_stun = load_image(ELEMENTS_FOLDER / 'stun.png')

        self.image_ail_poison_faded = load_image(
            ELEMENTS_FOLDER / 'poison_faded.png')
        self.image_ail_sleep_faded = load_image(
            ELEMENTS_FOLDER / 'sleep_faded.png')
        self.image_ail_paralysis_faded = load_image(
            ELEMENTS_FOLDER / 'paralysis_faded.png')
        self.image_ail_blast_faded = load_image(
            ELEMENTS_FOLDER / 'blast_faded.png')
        self.image_ail_stun_faded = load_image(
            ELEMENTS_FOLDER / 'stun_faded.png')

        self.image_ail_bleed = load_image(ELEMENTS_FOLDER / 'bleed.png')
        self.image_ail_effluvial = load_image(ELEMENTS_FOLDER / 'effluvial.png')

        self._image_ail_ailment = load_image(ELEMENTS_FOLDER / 'ailment.png')
        self._image_ail_ailment_faded = load_image(
            ELEMENTS_FOLDER / 'ailment_faded.png')

        self._image_star = load_image(ELEMENTS_FOLDER / 'star.png')
        self._image_star_faded = load_image(ELEMENTS_FOLDER / 'star_faded.png')
        self._image_cross = load_image(ELEMENTS_FOLDER / 'cross.png')
        self._image_cross_faded = load_image(
            ELEMENTS_FOLDER / 'cross_faded.png')

        small_size = (self.size[0] * self.small_scale,
                      self.size[1] * self.small_scale)
        self.image_back_small = load_image(
            ELEMENTS_FOLDER / 'back.png', small_size)
        self.image_back_small_faded = load_image(
            ELEMENTS_FOLDER / 'back_faded.png', small_size)

    def image_ail_ailment(self, faded: bool) -> Image.Image:
        if faded:
            return self._image_ail_ailment_faded
        return self._image_ail_ailment

    def image_cross(self, faded: bool) -> Image.Image:
        if faded:
            return self._image_cross_faded
        return self._image_cross

    def image_star(self, faded: bool) -> Image.Image:
        if faded:
            return self._image_star_faded
        return self._image_star

    @classmethod
    def get_instance(cls) -> 'Images':
        """Singleton pattern."""
        if cls.__instance__ is None:
            cls.__instance__ = Images()
        return cls.__instance__
