import os
from itertools import count
from math import ceil
from typing import List

from PIL import Image
from progress.bar import IncrementalBar
from src.images import Images

from . import colors
from .config import (
    BAR_MESSAGE_LENGTH, CARDS_HORIZONTAL_PADDING, CARDS_VERTICAL_PADDING,
    DIST_FOLDER, logger)
from .helper import alpha_paster
from .library import Library
from .monster_card import MonsterCard


class FillingMode:
    left_to_right = 0
    top_to_bottom = 1


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

        # Caching images...
        Images.get_instance()

        sheet_width = (__class__.card_size[0] * self._columns +
                       CARDS_HORIZONTAL_PADDING * (self._columns - 1))
        sheet_height = (__class__.card_size[1] * self._rows +
                        CARDS_VERTICAL_PADDING * (self._rows - 1))
        sheet_size = (sheet_width, sheet_height)

        # Progress bar with len(monsters) + sheets_count steps
        bar_message = 'Loading "{}"'
        pogress_bar = IncrementalBar(
            bar_message.format(self._cards[0].name).ljust(
                BAR_MESSAGE_LENGTH, ' '),
            max=len(self._cards) + self._sheets_count,
            suffix='%(index)d/%(max)d, elapsed: %(elapsed)d sec.')

        export_filename_generator = self._gen_export_path(export_filename)
        for sheet_index in range(self._sheets_count):
            sheet = Image.new('RGBA', sheet_size, __class__.filling_color)

            for row_index in range(self._rows):
                for col_index in range(self._columns):
                    card_x = col_index * (__class__.card_size[0] +
                                          CARDS_HORIZONTAL_PADDING)
                    card_y = row_index * (__class__.card_size[1] +
                                          CARDS_VERTICAL_PADDING)
                    card_position = (card_x, card_y)

                    card_index = self._card_index(
                        col_index, row_index, sheet_index)
                    if card_index >= len(self._cards):
                        break

                    current_card = self._cards[card_index]
                    pogress_bar.message = bar_message.format(
                        current_card.name).ljust(BAR_MESSAGE_LENGTH, ' ')
                    card_image = current_card.get_card_image()
                    alpha_paster(sheet, card_image, card_position)
                    pogress_bar.next(1)  # noqa: B305

            if not os.path.exists(str(DIST_FOLDER)):
                os.mkdir(str(DIST_FOLDER))

            export_file_path = next(export_filename_generator)
            pogress_bar.message = 'Exporting booklet to "{}"'.format(
                export_file_path)
            pogress_bar.next(1)  # noqa: B305
            sheet.save(export_file_path)

        pogress_bar.finish()
        logger.info('Exported booklets!')

    def _gen_export_path(self, export_filename_wo_ext: str) -> str:
        if self._sheets_count == 1:
            yield DIST_FOLDER / f'{export_filename_wo_ext}.png'
        for sheet_number in count(1):
            yield DIST_FOLDER / f'{export_filename_wo_ext}-{sheet_number}.png'

    @property
    def _count_monsters_in_sheet(self):
        return self._rows * self._columns

    @property
    def _sheets_count(self):
        return ceil(len(self._cards) / self._count_monsters_in_sheet)

    def _card_index(self,
                    col_index: int,
                    row_index: int,
                    sheet_index: int) -> int:
        if self._filling_mode == FillingMode.left_to_right:
            return (row_index * self._columns +
                    col_index +
                    self._count_monsters_in_sheet * sheet_index)
        elif self._filling_mode == FillingMode.top_to_bottom:
            return (col_index * self._rows +
                    row_index +
                    self._count_monsters_in_sheet * sheet_index)
        raise ValueError(f'Wrong filling mode "{self._filling_mode}"!')
