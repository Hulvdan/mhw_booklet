import os
from typing import List

from PIL import Image
from progress.bar import IncrementalBar
from src import library
from src.images import Images

from . import colors
from .config import (
    BAR_MESSAGE_LENGTH, CARDS_HORIZONTAL_PADDING, CARDS_VERTICAL_PADDING,
    DIST_FOLDER, logger)
from .helper import alpha_paster
from .library import Library
from .monster_card import MonsterCard


class FillingMode:
    horizontal = 0
    vertical = 1


class Booklet:
    """Image filled with monsters."""

    card_size = (1035, 636)
    filling_color = colors.WHITE

    def __init__(self,
                 columns: int,
                 rows: int,
                 filling_mode: FillingMode):
        self._columns = columns
        self._rows = rows

        self._filling_mode = filling_mode

        logger.info('Creating monster cards...')

        monsters_library = Library.get_instance()
        if columns * rows < len(monsters_library):
            logger.warning(
                "We won't be able to place all monsters on the page.\n"
                'There are %d monsters and only %d cells'
                % (len(monsters_library), columns * rows))

        self._cards: List[MonsterCard] = []
        for monster_data in monsters_library:
            card = MonsterCard(
                monster_data, __class__.card_size[0], __class__.card_size[1])
            self._cards.append(card)

    def export_as_png(self, export_filename: str) -> None:
        logger.info('Exporting booklet as png...')
        sheet_width = (__class__.card_size[0] * self._columns +
                       CARDS_HORIZONTAL_PADDING * (self._columns - 1))
        sheet_height = (__class__.card_size[1] * self._rows +
                        CARDS_VERTICAL_PADDING * (self._rows - 1))
        sheet_size = (sheet_width, sheet_height)
        sheet = Image.new('RGBA', sheet_size, __class__.filling_color)

        # Caching images...
        Images.get_instance()

        bar_message = 'Loading "{}"'
        bar = IncrementalBar(
            bar_message.format(self._cards[0].name).ljust(
                BAR_MESSAGE_LENGTH, ' '), max=len(self._cards))
        for row_index in range(self._rows):
            for col_index in range(self._columns):
                card_x = col_index * (__class__.card_size[0] +
                                      CARDS_HORIZONTAL_PADDING)
                card_y = row_index * (__class__.card_size[1] +
                                      CARDS_VERTICAL_PADDING)
                card_position = (card_x, card_y)

                card_index = self._card_index(col_index, row_index)
                if card_index > len(self._cards) - 1:
                    break

                current_card = self._cards[card_index]
                bar.message = bar_message.format(
                    current_card.name).ljust(BAR_MESSAGE_LENGTH, ' ')
                card_image = current_card.get_card_image()
                alpha_paster(sheet, card_image, card_position)
                bar.next(1)
        bar.finish()

        if not os.path.exists(str(DIST_FOLDER)):
            os.mkdir(str(DIST_FOLDER))
        sheet.save(export_filename)
        logger.info('Exported booklet!')

    def _card_index(self, col_index: int, row_index: int) -> int:
        if self._filling_mode == FillingMode.horizontal:
            return row_index * self._columns + col_index
        elif self._filling_mode == FillingMode.vertical:
            return col_index * self._rows + row_index
        raise ValueError(f'Wrong filling mode "{self._filling_mode}"!')
