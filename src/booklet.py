import json
import os
from typing import List

from PIL import Image

from . import colors
from .config import (
    CARDS_HORIZONTAL_PADDING, CARDS_VERTICAL_PADDING, DIST_FOLDER)
from .helper import alpha_paster
from .monster_card import MonsterCard


class FillingMode:
    horizontal = 0
    vertical = 1


class Booklet:
    """Image filled with monsters."""

    card_size = (1035, 636)
    filling_color = colors.WHITE

    def __init__(self,
                 data_filename: str,
                 columns: int,
                 rows: int,
                 filling_mode: FillingMode):
        self._data_filename = data_filename

        self._columns = columns
        self._rows = rows

        self._filling_mode = filling_mode

        with open(self._data_filename) as data_file:
            library = json.load(data_file)

        self._cards: List[MonsterCard] = []
        for lib in library:
            card = MonsterCard(lib,
                               __class__.card_size[0],
                               __class__.card_size[1])
            self._cards.append(card)

    def export_as_png(self, export_filename):
        sheet_width = (__class__.card_size[0] * self._columns +
                       CARDS_HORIZONTAL_PADDING * (self._columns - 1))
        sheet_height = (__class__.card_size[1] * self._rows +
                        CARDS_VERTICAL_PADDING * (self._rows - 1))
        sheet_size = (sheet_width, sheet_height)
        sheet = Image.new('RGBA', sheet_size, __class__.filling_color)

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
                card_image = current_card.get_card_image()
                alpha_paster(sheet, card_image, card_position)

        if not os.path.exists(str(DIST_FOLDER)):
            os.mkdir(str(DIST_FOLDER))
        sheet.save(export_filename)

    def _card_index(self, col_index, row_index) -> int:
        if self._filling_mode == FillingMode.horizontal:
            return row_index * self._columns + col_index
        elif self._filling_mode == FillingMode.vertical:
            return col_index * self._rows + row_index
        else:
            ValueError(f'Wrong filling mode "{self._filling_mode}"!')
