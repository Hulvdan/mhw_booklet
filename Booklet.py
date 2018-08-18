
import json
from Card import *
from SConfig import *


class Booklet:
    card_size = (345, 212)
    filling_color = Colors.white

    def __init__(self, data_filename, grid_x, grid_y, filling_mode, draw_numbers=False):
        self._data_filename = data_filename

        self._grid_x = grid_x
        self._grid_y = grid_y

        # 0 - Horizontal filling
        # 1 - Vertical filling
        self._filling_mode = filling_mode

        with open(self._data_filename) as data_file:
            library = json.load(data_file)

        self._cards = []
        for i in library:
            card = Card(i, Booklet.card_size[0], Booklet.card_size[1], draw_numbers)
            self._cards.append(card)

    def exportIntoFileAsPNG(self, export_filename):
        sheet_size = (Booklet.card_size[0] * self._grid_x + SConfig.cards_horizontal_padding * (self._grid_x - 1),
                      Booklet.card_size[1] * self._grid_y + SConfig.cards_vertical_padding * (self._grid_y - 1))
        sheet = Image.new("RGBA", sheet_size, Booklet.filling_color)

        for y in range(self._grid_y):
            for x in range(self._grid_x):
                card_position = (x * Booklet.card_size[0] + SConfig.cards_horizontal_padding * x,
                                 y * Booklet.card_size[1] + SConfig.cards_vertical_padding * y)

                card_index = y * self._grid_x + x if self._filling_mode == 0 else x * self._grid_y + y
                if card_index > len(self._cards) - 1:
                    break

                current_card = self._cards[card_index]
                card_image = current_card.getCardImage()
                alphaPaster(sheet, card_image, card_position)

        sheet.save(export_filename)
