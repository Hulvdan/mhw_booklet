
# Depends on Pillow
import json
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import os


class Booklet:
    card_size = (345, 212)
    # cards_x = 6
    # cards_y = 6
    # cards_x = 6
    # cards_y = 6

    white = (255,255,255,255)
    black = (0,0,0,255)
    transparent = (0,0,0,0)
    filling_color = white

    # filling_mode = 1

    cards_vertical_padding = 20
    cards_horizontal_padding = 20

    def __init__(self, data_filename, grid_x, grid_y, filling_mode):
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
            card = Card(i)
            self._cards.append(card)

    def exportIntoFileAsPNG(self, export_filename):
        sheet_size = (Booklet.card_size[0] * self._grid_x + Booklet.cards_horizontal_padding * (self._grid_x - 1),
                      Booklet.card_size[1] * self._grid_y + Booklet.cards_vertical_padding * (self._grid_y - 1))
        sheet = Image.new("RGBA", sheet_size, Booklet.filling_color)

        for y in range(self._grid_y):
            for x in range(self._grid_x):
                card_position = (x * Booklet.card_size[0] + Booklet.cards_horizontal_padding * x,
                                 y * Booklet.card_size[1] + Booklet.cards_vertical_padding * y)

                card_index = y * self._grid_x + x if self._filling_mode == 0 else x * self._grid_y + y
                if card_index > len(self._cards) - 1:
                    break

                current_card = self._cards[card_index]
                card_image = current_card.getCardImage()
                alphaPaster(sheet, card_image, card_position)

        sheet.save(export_filename)


class Card:
    icon_size = 120
    icon_weak_padding = 10
    weak_padding = 4
    attack_icon_width = 28 #* 0.59
    attack_spacing = 1
    attack_icons_spacing_from_icon = 5
    weakness_column_width = 34
    weakness_column_padding = 3
    weakness_row_padding = 5
    weakness_top = 60
    icon_bottom_pos = 40
    faded_opacity = 100
    small_scale = 0.59
    braces_color = (100,100,100,255)
    braces_color_faded = (200,200,200,255)

    def __init__(self, _library:dict):
        self._library = _library
        self._name        = self._library["name"]

        self._attack_types = self._library["attack"]

        self._fire_res    = self._library["weakness"][0]
        self._water_res   = self._library["weakness"][1]
        self._thunder_res = self._library["weakness"][2]
        self._ice_res     = self._library["weakness"][3]
        self._dragon_res  = self._library["weakness"][4]

        self._poison_ail    = self._library["ailments"][0]
        self._sleep_ail     = self._library["ailments"][1]
        self._paralysis_ail = self._library["ailments"][2]
        self._blast_ail     = self._library["ailments"][3]
        self._stun_ail      = self._library["ailments"][4]

        self._width, self._height = Booklet.card_size

        self._color = '#ffff00' if self._library['color'] == "#" else self._library['color']

        self._icon_image = ImageEnhance.Color(Image.open("images\\"+self._name+'.png')).enhance(1.5)
        self._icon_image.thumbnail((Card.icon_size, Card.icon_size*2), Image.ANTIALIAS)

    debug_polygon = False
    def getCardImage(self):
        image = Image.new("RGBA", Booklet.card_size)
        drawer = ImageDraw.Draw(image)

        # new_size = (int(Card.weakness_column_width * Card.small_scale), int(Card.weakness_column_width * Card.small_scale))
        # little_faded_poison = image_ail_poison_faded.resize(new_size)
        # little_faded_sleep = image_ail_sleep_faded.resize(new_size)
        # little_faded_paralysis = image_ail_paralysis_faded.resize(new_size)
        # little_faded_blast = image_ail_blast_faded.resize(new_size)
        # little_faded_stun = image_ail_stun_faded.resize(new_size)

        font = ImageFont.truetype("Gabriola.ttf", 60)
        height = self._icon_image.size[1]
        alphaPaster(image, self._icon_image, (0, self._height - Card.icon_bottom_pos - height))

        if Card.debug_polygon:
            p1 = (0, 0)
            p2 = (Booklet.card_size[0]-1, 0)
            p3 = (Booklet.card_size[0]-1, Booklet.card_size[1]-1)
            p4 = (0, Booklet.card_size[1]-1)
            debug_color = (255,0,0,100)
            drawer.line((p1, p2), fill=debug_color)
            drawer.line((p2, p3), fill=debug_color)
            drawer.line((p3, p4), fill=debug_color)
            drawer.line((p4, p1), fill=debug_color)

        # - drawing ailments
        w = Card.weakness_column_width
        sw = self._width
        p = Card.weakness_column_padding
        t = Card.weakness_top

        max_level = max(self._fire_res[0]    if isinstance(self._fire_res, list)    else self._fire_res,
                        self._water_res[0]   if isinstance(self._water_res, list)   else self._water_res,
                        self._thunder_res[0] if isinstance(self._thunder_res, list) else self._thunder_res,
                        self._ice_res[0]     if isinstance(self._ice_res, list)     else self._ice_res,
                        self._dragon_res[0]  if isinstance(self._dragon_res, list)  else self._dragon_res)
        faded_res = [self._fire_res    == max_level if not isinstance(self._fire_res, list)    else self._fire_res[0] == max_level,
                     self._water_res   == max_level if not isinstance(self._water_res, list)   else self._water_res[0] == max_level,
                     self._thunder_res == max_level if not isinstance(self._thunder_res, list) else self._thunder_res[0] == max_level,
                     self._ice_res     == max_level if not isinstance(self._ice_res, list)     else self._ice_res[0] == max_level,
                     self._dragon_res  == max_level if not isinstance(self._dragon_res, list)  else self._dragon_res[0] == max_level,]

        any_ailment_power_bigger_than_1 = any(x > 1 for x in self._library["ailments"])
        alphaPaster(image, image_ail_ailment  if any_ailment_power_bigger_than_1 else image_ail_ailment_faded, (sw - w, t))
        alphaPaster(image, image_elem_dragon  if faded_res[-1] else image_elem_dragon_faded,   (sw - 2 * w - 1 * p, t))
        alphaPaster(image, image_elem_ice     if faded_res[-2] else image_elem_ice_faded,      (sw - 3 * w - 2 * p, t))
        alphaPaster(image, image_elem_thunder if faded_res[-3] else image_elem_thunder_faded,  (sw - 4 * w - 3 * p, t))
        alphaPaster(image, image_elem_water   if faded_res[-4] else image_elem_water_faded,    (sw - 5 * w - 4 * p, t))
        alphaPaster(image, image_elem_fire    if faded_res[-5] else image_elem_fire_faded,     (sw - 6 * w - 5 * p, t))

        t += Card.weakness_row_padding + Card.weakness_column_width
        if isinstance(self._fire_res, list):
            alphaPaster(image, self.getWeaknessImage(self._fire_res[0], self._fire_res[1], faded_res[0]), (sw - 6 * w - 5 * p, t))
        else:
            alphaPaster(image, self.getWeaknessImage(self._fire_res, -1, faded_res[0]), (sw - 6 * w - 5 * p, t))

        if isinstance(self._water_res, list):
            alphaPaster(image, self.getWeaknessImage(self._water_res[0], self._water_res[1], faded_res[1]), (sw - 5 * w - 4 * p, t))
        else:
            alphaPaster(image, self.getWeaknessImage(self._water_res, -1, faded_res[1]), (sw - 5 * w - 4 * p, t))

        if isinstance(self._thunder_res, list):
            alphaPaster(image, self.getWeaknessImage(self._thunder_res[0], self._thunder_res[1], faded_res[2]), (sw - 4 * w - 3 * p, t))
        else:
            alphaPaster(image, self.getWeaknessImage(self._thunder_res, -1, faded_res[2]), (sw - 4 * w - 3 * p, t))

        if isinstance(self._ice_res, list):
            alphaPaster(image, self.getWeaknessImage(self._ice_res[0], self._ice_res[1], faded_res[3]), (sw - 3 * w - 2 * p, t))
        else:
            alphaPaster(image, self.getWeaknessImage(self._ice_res, -1, faded_res[3]), (sw - 3 * w - 2 * p, t))

        if isinstance(self._dragon_res, list):
            alphaPaster(image, self.getWeaknessImage(self._dragon_res[0], self._dragon_res[1], faded_res[4]), (sw - 2 * w - 1 * p, t))
        else:
            alphaPaster(image, self.getWeaknessImage(self._dragon_res, -1, faded_res[4]), (sw - 2 * w - 1 * p, t))

        alphaPaster(image, self.getAilmentsImage(self._poison_ail, self._sleep_ail, self._paralysis_ail, self._blast_ail, self._stun_ail), (sw - w, t))
        alphaPaster(image, self.getAttackImage(), (0, self._height - Card.icon_bottom_pos + Card.attack_icons_spacing_from_icon))
        # - drawing ailments - end

        text_size = drawer.textsize(self._name, font=font)
        drawer.text(((self._width - text_size[0]) / 2, 0), self._name, font=font, fill=self._color)

        return image

    def getAttackImage(self) -> Image.Image:
        image = Image.new("RGBA", (int(Card.icon_size), int(Card.attack_icon_width)))

        spacing = Card.attack_spacing
        width = Card.attack_icon_width
        count = len(self._attack_types)
        for i in range(count):
            attack_type = self._attack_types[i]
            _s = tuple([int(width)] * 2)
            posy = 0
            posx = Card.icon_size / 2 - (count - 1) / 2 * spacing - count / 2 * width + i * (spacing + width)

            if attack_type == 'waterblight':
                alphaPaster(image, image_waterblight.resize(_s), (int(posx), int(posy)))
            elif attack_type == 'mud_brackets':
                img_brackets = self.drawBrackets(1, True, width, spacing, False)
                res_mud = image_mud.resize(_s)
                alphaPaster(res_mud, img_brackets, (0,0))
                alphaPaster(image, res_mud, (int(posx), int(posy)))
            elif attack_type == 'poison':
                alphaPaster(image, image_ail_poison.resize(_s), (int(posx), int(posy)))
            elif attack_type == 'water':
                alphaPaster(image, image_elem_water.resize(_s), (int(posx), int(posy)))
            elif attack_type == 'thunder':
                alphaPaster(image, image_elem_thunder.resize(_s), (int(posx), int(posy)))
            elif attack_type == 'thunderblight':
                alphaPaster(image, image_thunderblight.resize(_s), (int(posx), int(posy)))
            elif attack_type == 'fire':
                alphaPaster(image, image_elem_fire.resize(_s), (int(posx), int(posy)))
            elif attack_type == 'fireblight':
                alphaPaster(image, image_fireblight.resize(_s), (int(posx), int(posy)))
            elif attack_type == 'stun':
                alphaPaster(image, image_ail_stun.resize(_s), (int(posx), int(posy)))
            elif attack_type == 'ice':
                alphaPaster(image, image_elem_ice.resize(_s), (int(posx), int(posy)))
            elif attack_type == 'iceblight':
                alphaPaster(image, image_iceblight.resize(_s), (int(posx), int(posy)))
            elif attack_type == 'bleed':
                alphaPaster(image, image_ail_bleed.resize(_s), (int(posx), int(posy)))
            elif attack_type == 'blast':
                alphaPaster(image, image_ail_blast.resize(_s), (int(posx), int(posy)))
            elif attack_type == 'diamond_brackets':
                img_brackets = self.drawBrackets(1, True, width, spacing, False)
                res_diamond = image_diamond.resize(_s)
                alphaPaster(res_diamond, img_brackets, (0,0))
                alphaPaster(image, res_diamond, (int(posx), int(posy)))
            elif attack_type == 'sleep':
                alphaPaster(image, image_ail_sleep.resize(_s), (int(posx), int(posy)))
            elif attack_type == 'dragon':
                alphaPaster(image, image_elem_dragon.resize(_s), (int(posx), int(posy)))
            elif attack_type == 'effluvial':
                alphaPaster(image, image_ail_effluvial.resize(_s), (int(posx), int(posy)))

        return image

    drawCrossAtBottom = False
    def getWeaknessImage(self, initial, second, is_faded) -> Image.Image:
        image = Image.new("RGBA", (Card.weakness_column_width, Card.weakness_column_width * 3 + Card.weakness_row_padding * 2))
        if second == -1:
            if initial == 0:
                alphaPaster(image, image_cross if is_faded else image_cross_faded, (0,0))
            for i in range(initial):
                alphaPaster(image, image_star_faded if not is_faded else image_star, (0,Card.weakness_column_width * i + Card.weakness_row_padding * i))
        else:
            new_size = (int(Card.weakness_column_width * Card.small_scale), int(Card.weakness_column_width * Card.small_scale))
            little_star = image_star.resize(new_size)
            little_star_faded = image_star_faded.resize(new_size)
            little_cross = image_cross.resize(new_size)
            little_cross_faded = image_cross_faded.resize(new_size)
            little_image_left_pos = int((Card.weakness_column_width - new_size[0]) / 2)
            last_y = 0

            if initial == 0:
                alphaPaster(image, little_cross_faded if not is_faded else little_cross, (little_image_left_pos, 0))

            for i in range(initial):
                little_star_y = int(i * Card.small_scale * Card.weakness_row_padding + i * Card.small_scale * Card.weakness_column_width)
                alphaPaster(image, little_star_faded if not is_faded else little_star, (little_image_left_pos, little_star_y))

            for i in range(second + 1 if second == 0 else second):
                if second == 0:
                    if Card.drawCrossAtBottom:
                        alphaPaster(image, little_cross_faded if not is_faded else little_cross, (little_image_left_pos, image.size[1] - new_size[1]))
                    else:
                        last_y = int((initial if initial > 0 else 1) * new_size[1] + (initial if initial > 0 else 1) * Card.small_scale * Card.weakness_row_padding)
                        alphaPaster(image, little_cross_faded if not is_faded else little_cross, (little_image_left_pos, last_y))

            for k in range(second):
                last_y = int((initial if initial > 0 else 1) * new_size[1] + (initial if initial > 0 else 1) * Card.small_scale * Card.weakness_row_padding)
                little_star_y = int(k * Card.small_scale * Card.weakness_row_padding + k * Card.small_scale * Card.weakness_column_width + last_y)
                alphaPaster(image, little_star_faded if not is_faded else little_star, (little_image_left_pos, little_star_y))

            alphaPaster(image, self.drawBrackets(1 if second == 0 else second, is_faded, Card.weakness_column_width, Card.weakness_row_padding * Card.small_scale), (0, last_y))

        return image

    @staticmethod
    def getAilmentsImage(poison, sleep, paralysis, blast, stun) -> Image.Image:
        image = Image.new("RGBA", (Card.weakness_column_width, Card.weakness_column_width * 3 + Card.weakness_row_padding * 2))
        new_size = (int(Card.weakness_column_width * Card.small_scale), int(Card.weakness_column_width * Card.small_scale))
        # little_star = image_star.resize(new_size)
        little_image_left_pos = int((Card.weakness_column_width - new_size[0]) / 2)
        little_poison = image_ail_poison.resize(new_size)
        little_sleep = image_ail_sleep.resize(new_size)
        little_paralysis = image_ail_paralysis.resize(new_size)
        little_blast = image_ail_blast.resize(new_size)
        little_stun = image_ail_stun.resize(new_size)

        # _low_opacity = 50
        y = 0
        dy = new_size[1] + Card.small_scale * Card.weakness_row_padding
        if poison == 1:
            alphaPaster(image, little_poison, (little_image_left_pos, int(y)))
            y += dy
        elif poison == 2:
            alphaPaster(image, image_back_small_faded, (little_image_left_pos, int(y)))
            alphaPaster(image, little_poison, (little_image_left_pos, int(y)))
            y += dy
        elif poison == 3:
            alphaPaster(image, image_back_small, (little_image_left_pos, int(y)))
            alphaPaster(image, little_poison, (little_image_left_pos, int(y)))
            y += dy

        if sleep == 1:
            alphaPaster(image, little_sleep, (little_image_left_pos, int(y)))
            y += dy
        elif sleep == 2:
            alphaPaster(image, image_back_small_faded, (little_image_left_pos, int(y)))
            alphaPaster(image, little_sleep, (little_image_left_pos, int(y)))
            y += dy
        elif sleep == 3:
            alphaPaster(image, image_back_small, (little_image_left_pos, int(y)))
            alphaPaster(image, little_sleep, (little_image_left_pos, int(y)))
            y += dy

        if paralysis == 1:
            alphaPaster(image, little_paralysis, (little_image_left_pos, int(y)))
            y += dy
        elif paralysis == 2:
            alphaPaster(image, image_back_small_faded, (little_image_left_pos, int(y)))
            alphaPaster(image, little_paralysis, (little_image_left_pos, int(y)))
            y += dy
        elif paralysis == 3:
            alphaPaster(image, image_back_small, (little_image_left_pos, int(y)))
            alphaPaster(image, little_paralysis, (little_image_left_pos, int(y)))
            y += dy

        if blast == 1:
            alphaPaster(image, little_blast, (little_image_left_pos, int(y)))
            y += dy
        elif blast == 2:
            alphaPaster(image, image_back_small_faded, (little_image_left_pos, int(y)))
            alphaPaster(image, little_blast, (little_image_left_pos, int(y)))
            y += dy
        elif blast == 3:
            alphaPaster(image, image_back_small, (little_image_left_pos, int(y)))
            alphaPaster(image, little_blast, (little_image_left_pos, int(y)))
            y += dy

        if stun == 1:
            alphaPaster(image, little_stun, (little_image_left_pos, int(y)))
            y += dy
        elif stun == 2:
            alphaPaster(image, image_back_small_faded, (little_image_left_pos, int(y)))
            alphaPaster(image, little_stun, (little_image_left_pos, int(y)))
            y += dy
        elif stun == 3:
            alphaPaster(image, image_back_small, (little_image_left_pos, int(y)))
            alphaPaster(image, little_stun, (little_image_left_pos, int(y)))
            y += dy


        return image

    @staticmethod
    def drawBrackets(images_count, is_not_faded, icon_size, padding, margin=True) -> Image.Image:
        size = (int(icon_size), int(icon_size * images_count + padding * (images_count - 1)))
        image = Image.new("RGBA", size, (0,0,0,0))
        drawer = ImageDraw.ImageDraw(image)
        line_width = 2

        offset = 3 if margin else 0
        if margin:
            p1 = (offset+line_width*2-1, 1)
            p2 = (offset+0, 1)
            p3 = (offset+0,              icon_size * images_count * Card.small_scale + padding * (images_count - 1) * Card.small_scale-1)
            p4 = (offset+line_width*2-1, icon_size * images_count * Card.small_scale + padding * (images_count - 1) * Card.small_scale-1)

            p5 = (-offset+size[0] - 2*line_width, 0)
            p6 = (-offset+size[0] - line_width, 0)
            p7 = (-offset+size[0] - line_width,   icon_size * images_count * Card.small_scale + padding * (images_count - 1) * Card.small_scale)
            p8 = (-offset+size[0] - 2*line_width, icon_size * images_count * Card.small_scale + padding * (images_count - 1) * Card.small_scale)
        else:
            p1 = (offset+line_width*2-1, 1)
            p2 = (offset+0, 1)
            p3 = (offset+0,              icon_size * images_count + padding * (images_count - 1) - 2)
            p4 = (offset+line_width*2-1, icon_size * images_count + padding * (images_count - 1) - 2)

            p5 = (-offset+size[0] - 2*line_width, 0)
            p6 = (-offset+size[0] - line_width, 0)
            p7 = (-offset+size[0] - line_width,   icon_size * images_count + padding * (images_count - 1) - 1)
            p8 = (-offset+size[0] - 2*line_width, icon_size * images_count + padding * (images_count - 1) - 1)

        clr = Card.braces_color_faded if not is_not_faded else Card.braces_color
        drawer.line((p1, p2), fill=clr, width=line_width)
        drawer.line((p2, p3), fill=clr, width=line_width)
        drawer.line((p3, p4), fill=clr, width=line_width)
        drawer.line((p5, p6), fill=clr, width=line_width)
        drawer.line((p6, p7), fill=clr, width=line_width)
        drawer.line((p7, p8), fill=clr, width=line_width)

        return image


    def checkImage(self):
        if not os.path.exists("images\\"+self._name+".png"):
            print('Not Found Image: "{}"'.format(self._name))

    def __str__(self):
        return "{} \t[{}{}{}{}{}]\t[{}{}{}{}{}]".format(self._name, *self._library["weakness"], *self._library["ailments"])

def alphaPaster(img_destination:Image.Image, img_source:Image.Image, pos):
    """Pastes img_source into img_destination with alpha_composing"""
    intermediate_image = Image.new("RGBA", img_destination.size, Booklet.transparent)
    intermediate_image.paste(img_source, pos)
    img_destination.alpha_composite(intermediate_image)


def main():
    booklet_lh = Booklet("data.json", 6, 6, 0)
    booklet_lh.exportIntoFileAsPNG("MHW_Booklet_Landscape_Horizontal.png")
    booklet_lv = Booklet("data.json", 6, 6, 1)
    booklet_lv.exportIntoFileAsPNG("MHW_Booklet_Landscape_Vertical.png")
    booklet_ph = Booklet("data.json", 4, 9, 0)
    booklet_ph.exportIntoFileAsPNG("MHW_Booklet_Portrait_Horizontal.png")
    booklet_pv = Booklet("data.json", 4, 9, 1)
    booklet_pv.exportIntoFileAsPNG("MHW_Booklet_Portrait_Vertical.png")


if __name__ == "__main__":
    ail_icon_size = (Card.weakness_column_width, Card.weakness_column_width)
    image_elem_fire           = Image.open(r"images\element\fire.png")
    image_elem_water          = Image.open(r"images\element\water.png")
    image_elem_thunder        = Image.open(r"images\element\thunder.png")
    image_elem_ice            = Image.open(r"images\element\ice.png")
    image_elem_dragon         = Image.open(r"images\element\dragon.png")

    image_elem_fire_faded     = Image.open(r"images\element\fire_faded.png")
    image_elem_water_faded    = Image.open(r"images\element\water_faded.png")
    image_elem_thunder_faded  = Image.open(r"images\element\thunder_faded.png")
    image_elem_ice_faded      = Image.open(r"images\element\ice_faded.png")
    image_elem_dragon_faded   = Image.open(r"images\element\dragon_faded.png")

    image_fireblight          = Image.open(r"images\element\fireblight.png")
    image_waterblight         = Image.open(r"images\element\waterblight.png")
    image_iceblight           = Image.open(r"images\element\iceblight.png")
    image_thunderblight       = Image.open(r"images\element\thunderblight.png")
    image_diamond             = Image.open(r"images\element\diamond.png")
    image_mud                 = Image.open(r"images\element\mud.png")

    image_ail_poison          = Image.open(r"images\element\poison.png")
    image_ail_sleep           = Image.open(r"images\element\sleep.png")
    image_ail_paralysis       = Image.open(r"images\element\paralysis.png")
    image_ail_blast           = Image.open(r"images\element\blast.png")
    image_ail_stun            = Image.open(r"images\element\stun.png")

    image_ail_poison_faded    = Image.open(r"images\element\poison_faded.png")
    image_ail_sleep_faded     = Image.open(r"images\element\sleep_faded.png")
    image_ail_paralysis_faded = Image.open(r"images\element\paralysis_faded.png")
    image_ail_blast_faded     = Image.open(r"images\element\blast_faded.png")
    image_ail_stun_faded      = Image.open(r"images\element\stun_faded.png")

    image_ail_bleed           = Image.open(r"images\element\bleed.png")
    image_ail_effluvial       = Image.open(r"images\element\effluvial.png")
    image_ail_ailment         = Image.open(r"images\element\ailment.png")
    image_ail_ailment_faded   = Image.open(r"images\element\ailment_faded.png")

    image_star                = Image.open(r"images\element\star.png")
    image_star_faded          = Image.open(r"images\element\star_faded.png")
    image_cross               = Image.open(r"images\element\cross.png")
    image_cross_faded         = Image.open(r"images\element\cross_faded.png")
    image_back_small          = Image.open(r"images\element\back.png")
    image_back_small_faded    = Image.open(r"images\element\back_faded.png")

    s = (Card.weakness_column_width, Card.weakness_column_width)
    image_elem_fire          .thumbnail(s, Image.ANTIALIAS)
    image_elem_water         .thumbnail(s, Image.ANTIALIAS)
    image_elem_thunder       .thumbnail(s, Image.ANTIALIAS)
    image_elem_ice           .thumbnail(s, Image.ANTIALIAS)
    image_elem_dragon        .thumbnail(s, Image.ANTIALIAS)
    image_elem_fire_faded    .thumbnail(s, Image.ANTIALIAS)
    image_elem_water_faded   .thumbnail(s, Image.ANTIALIAS)
    image_elem_thunder_faded .thumbnail(s, Image.ANTIALIAS)
    image_elem_ice_faded     .thumbnail(s, Image.ANTIALIAS)
    image_elem_dragon_faded  .thumbnail(s, Image.ANTIALIAS)
    image_ail_poison         .thumbnail(s, Image.ANTIALIAS)
    image_ail_poison_faded   .thumbnail(s, Image.ANTIALIAS)
    image_ail_sleep          .thumbnail(s, Image.ANTIALIAS)
    image_ail_sleep_faded    .thumbnail(s, Image.ANTIALIAS)
    image_ail_paralysis      .thumbnail(s, Image.ANTIALIAS)
    image_ail_paralysis_faded.thumbnail(s, Image.ANTIALIAS)
    image_ail_blast          .thumbnail(s, Image.ANTIALIAS)
    image_ail_blast_faded    .thumbnail(s, Image.ANTIALIAS)
    image_ail_stun           .thumbnail(s, Image.ANTIALIAS)
    image_ail_stun_faded     .thumbnail(s, Image.ANTIALIAS)
    image_ail_bleed          .thumbnail(s, Image.ANTIALIAS)
    image_ail_effluvial      .thumbnail(s, Image.ANTIALIAS)
    image_ail_ailment        .thumbnail(s, Image.ANTIALIAS)
    image_ail_ailment_faded  .thumbnail(s, Image.ANTIALIAS)
    image_star               .thumbnail(s, Image.ANTIALIAS)
    image_star_faded         .thumbnail(s, Image.ANTIALIAS)
    image_cross              .thumbnail(s, Image.ANTIALIAS)
    image_cross_faded        .thumbnail(s, Image.ANTIALIAS)
    image_back_small         .thumbnail((s[0] * Card.small_scale, s[1] * Card.small_scale), Image.ANTIALIAS)
    image_back_small_faded   .thumbnail((s[0] * Card.small_scale, s[1] * Card.small_scale), Image.ANTIALIAS)

    main()
