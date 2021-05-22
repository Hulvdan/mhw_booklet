import logging
from pathlib import Path

import structlog

LOG_LEVEL = logging.DEBUG
logger: structlog.PrintLogger = structlog.get_logger()


MONSTER_NAME_FONT_SIZE = 180
AILMENT_FONT_SIZE = 84

DIST_FOLDER = Path('dist')
ASSETS_FOLDER = Path('assets')
FONT_FOLDER = ASSETS_FOLDER / 'fonts'
IMAGES_FOLDER = ASSETS_FOLDER / 'images'
ELEMENTS_FOLDER = IMAGES_FOLDER / 'elements'
MONSTER_ICONS_FOLDER = IMAGES_FOLDER / 'monster_icons'
LIBRARY_DATA_PATH = ASSETS_FOLDER / 'data.json'

# Should the numbers be drawn to the right of ailments.
DRAW_AILMENT_NUMBERS = True

# Padding between cards
CARDS_VERTICAL_PADDING = 60
CARDS_HORIZONTAL_PADDING = 60

MONSTER_ICON_SIZE = 360

ICON_WEAK_PADDING = 30

WEAK_PADDING = 12

ATTACK_ICON_WIDTH = 84
ATTACK_SPACING = 3
ATTACK_ICONS_SPACING_FROM_ICON = 15

SMALL_SCALE = 0.59

WEAKNESS_COLUMN_WIDTH = 102
WEAKNESS_COLUMN_WIDTH_SMALL = int(WEAKNESS_COLUMN_WIDTH * SMALL_SCALE)
WEAKNESS_COLUMN_PADDING = 9
WEAKNESS_COLUMN_PADDING_SMALL = int(WEAKNESS_COLUMN_PADDING * SMALL_SCALE)
WEAKNESS_ROW_PADDING = 15
WEAKNESS_ROW_PADDING_SMALL = int(WEAKNESS_ROW_PADDING * SMALL_SCALE)
WEAKNESS_TOP = 180

ICON_BOTTOM_POS = 120

# Coefficient that enhances monster's icon. Without it monster's icon will be
# more dull.
MONSTER_IMAGE_ENHANCE_COEFFICIENT = 1.5

# When monster's weakness to the element type is "0", then cross will be drawn
# on the bottom. If True - on the top.
DRAW_CROSS_AT_THE_BOTTOM = False

# Should be space drawn if ailment's power is 0.
# True - blank. False - continue with the next ailment.
ZERO_AILMENT_SPACE = True

DEBUG_POLYGON = False
