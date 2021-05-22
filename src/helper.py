from PIL import Image

from . import colors


def alpha_paster(img_destination: Image.Image,
                 img_source: Image.Image, pos=(0, 0)):
    """Pastes img_source into img_destination with alpha_composing."""
    intermediate_image = Image.new(
        'RGBA', img_destination.size, colors.TRANSPARENT)
    intermediate_image.paste(img_source, pos)
    img_destination.alpha_composite(intermediate_image)
