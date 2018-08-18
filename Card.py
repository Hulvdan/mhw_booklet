
import os
from hlp import *
from SConfig import *
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from AilmentStack import *
from WeaknessStack import *


class Card:
    def __init__(self, _library:dict, _w, _h, draw_numbers):
        self._library = _library
        self._name        = self._library["name"]

        self._attack_types = self._library["attack"]

        weak = self._library["weakness"]
        self._fire_res    = weak[0]
        self._water_res   = weak[1]
        self._thunder_res = weak[2]
        self._ice_res     = weak[3]
        self._dragon_res  = weak[4]

        ail = self._library["ailments"]
        self._poison_ail    = ail[0]
        self._sleep_ail     = ail[1]
        self._paralysis_ail = ail[2]
        self._blast_ail     = ail[3]
        self._stun_ail      = ail[4]

        max_res = max(i[0] if isinstance(i, list) else i for i in weak)
        self._fire_stack    = WeaknessStack(0, self._fire_res != max_res,    weak[0][0] if isinstance(weak[0], list) else weak[0], weak[0][1] if isinstance(weak[0], list) else -1)
        self._water_stack   = WeaknessStack(1, self._water_res != max_res,   weak[1][0] if isinstance(weak[1], list) else weak[1], weak[1][1] if isinstance(weak[1], list) else -1)
        self._thunder_stack = WeaknessStack(2, self._thunder_res != max_res, weak[2][0] if isinstance(weak[2], list) else weak[2], weak[2][1] if isinstance(weak[2], list) else -1)
        self._ice_stack     = WeaknessStack(3, self._ice_res != max_res,     weak[3][0] if isinstance(weak[3], list) else weak[3], weak[3][1] if isinstance(weak[3], list) else -1)
        self._dragon_stack  = WeaknessStack(4, self._dragon_res != max_res,  weak[4][0] if isinstance(weak[4], list) else weak[4], weak[4][1] if isinstance(weak[4], list) else -1)
        self._ailment_stack = AilmentStack(ail, draw_numbers)
        self._big_stack = (self._fire_stack, self._water_stack, self._thunder_stack, self._ice_stack, self._dragon_stack, self._ailment_stack)

        self._width, self._height, self._size = _w, _h, (_w, _h)

        self._color = '#ffff00' if self._library['color'] == "#" else self._library['color']

        self._icon_image = ImageEnhance.Color(Image.open("images\\"+self._name+'.png')).enhance(1.5)
        self._icon_image.thumbnail((SConfig.icon_size, SConfig.icon_size*2), Image.ANTIALIAS)

    def getCardImage(self):
        image = Image.new("RGBA", (self._width, self._height))
        drawer = ImageDraw.Draw(image)

        font = ImageFont.truetype("Gabriola.ttf", 60)
        height = self._icon_image.size[1]
        alphaPaster(image, self._icon_image, (0, self._height - SConfig.icon_bottom_pos - height))

        if SConfig.debug_polygon:
            p1 = (0, 0)
            p2 = (self._width - 1, 0)
            p3 = (self._width - 1, self._height - 1)
            p4 = (0, self._height - 1)
            debug_color = (255,0,0,100)
            drawer.line((p1, p2), fill=debug_color)
            drawer.line((p2, p3), fill=debug_color)
            drawer.line((p3, p4), fill=debug_color)
            drawer.line((p4, p1), fill=debug_color)

        x_left = self._width
        for i in range(len(self._big_stack)):
            stack = self._big_stack[-i-1]
            x_left -= stack.getWidth()
            alphaPaster(image, stack.getImage(), (x_left, SConfig.weakness_top))
            x_left -= SConfig.weakness_column_padding

        text_size = drawer.textsize(self._name, font=font)
        drawer.text(((self._width - text_size[0]) / 2, 0), self._name, font=font, fill=self._color)

        return image

    def getAttackImage(self) -> Image.Image:
        image = Image.new("RGBA", (int(SConfig.icon_size), int(SConfig.attack_icon_width)))

        spacing = SConfig.attack_spacing
        width = SConfig.attack_icon_width
        count = len(self._attack_types)
        for i in range(count):
            attack_type = self._attack_types[i]
            _s = tuple([int(width)] * 2)
            posy = 0
            posx = SConfig.icon_size / 2 - (count - 1) / 2 * spacing - count / 2 * width + i * (spacing + width)

            if attack_type == 'waterblight':
                alphaPaster(image, Images.image_waterblight.resize(_s), (int(posx), int(posy)))
            elif attack_type == 'mud_brackets':
                img_brackets = self.drawBrackets(1, True, width, spacing, False)
                res_mud = Images.image_mud.resize(_s)
                alphaPaster(res_mud, img_brackets, (0,0))
                alphaPaster(image, res_mud, (int(posx), int(posy)))
            elif attack_type == 'poison':
                alphaPaster(image, Images.image_ail_poison.resize(_s), (int(posx), int(posy)))
            elif attack_type == 'water':
                alphaPaster(image, Images.image_elem_water.resize(_s), (int(posx), int(posy)))
            elif attack_type == 'thunder':
                alphaPaster(image, Images.image_elem_thunder.resize(_s), (int(posx), int(posy)))
            elif attack_type == 'thunderblight':
                alphaPaster(image, Images.image_thunderblight.resize(_s), (int(posx), int(posy)))
            elif attack_type == 'fire':
                alphaPaster(image, Images.image_elem_fire.resize(_s), (int(posx), int(posy)))
            elif attack_type == 'fireblight':
                alphaPaster(image, Images.image_fireblight.resize(_s), (int(posx), int(posy)))
            elif attack_type == 'stun':
                alphaPaster(image, Images.image_ail_stun.resize(_s), (int(posx), int(posy)))
            elif attack_type == 'ice':
                alphaPaster(image, Images.image_elem_ice.resize(_s), (int(posx), int(posy)))
            elif attack_type == 'iceblight':
                alphaPaster(image, Images.image_iceblight.resize(_s), (int(posx), int(posy)))
            elif attack_type == 'bleed':
                alphaPaster(image, Images.image_ail_bleed.resize(_s), (int(posx), int(posy)))
            elif attack_type == 'blast':
                alphaPaster(image, Images.image_ail_blast.resize(_s), (int(posx), int(posy)))
            elif attack_type == 'diamond_brackets':
                img_brackets = self.drawBrackets(1, True, width, spacing, False)
                res_diamond = Images.image_diamond.resize(_s)
                alphaPaster(res_diamond, img_brackets, (0,0))
                alphaPaster(image, res_diamond, (int(posx), int(posy)))
            elif attack_type == 'sleep':
                alphaPaster(image, Images.image_ail_sleep.resize(_s), (int(posx), int(posy)))
            elif attack_type == 'dragon':
                alphaPaster(image, Images.image_elem_dragon.resize(_s), (int(posx), int(posy)))
            elif attack_type == 'effluvial':
                alphaPaster(image, Images.image_ail_effluvial.resize(_s), (int(posx), int(posy)))

        return image

    @staticmethod
    def getAilmentsImage(poison, sleep, paralysis, blast, stun) -> Image.Image:
        image = Image.new("RGBA", (SConfig.weakness_column_width, SConfig.weakness_column_width * 3 + SConfig.weakness_row_padding * 2))
        new_size = (int(SConfig.weakness_column_width * SConfig.small_scale), int(SConfig.weakness_column_width * SConfig.small_scale))
        # little_star = image_star.resize(new_size)
        little_image_left_pos = int((SConfig.weakness_column_width - new_size[0]) / 2)
        little_poison = Images.image_ail_poison.resize(new_size)
        little_sleep = Images.image_ail_sleep.resize(new_size)
        little_paralysis = Images.image_ail_paralysis.resize(new_size)
        little_blast = Images.image_ail_blast.resize(new_size)
        little_stun =Images.image_ail_stun.resize(new_size)

        little_faded_poison = Images.image_ail_poison_faded.resize(new_size)
        little_faded_sleep = Images.image_ail_sleep_faded.resize(new_size)
        little_faded_paralysis = Images.image_ail_paralysis_faded.resize(new_size)
        little_faded_blast = Images.image_ail_blast_faded.resize(new_size)
        little_faded_stun = Images.image_ail_stun_faded.resize(new_size)

        # _low_opacity = 50
        y = 0
        dy = new_size[1] + SConfig.small_scale * SConfig.weakness_row_padding
        if poison == 1:
            alphaPaster(image, little_faded_poison, (little_image_left_pos, int(y)))
            # alphaPaster(image, little_poison, (little_image_left_pos, int(y)))
            y += dy
        elif poison == 2:
            alphaPaster(image, Images.image_back_small_faded, (little_image_left_pos, int(y)))
            alphaPaster(image, little_faded_poison, (little_image_left_pos, int(y)))
            # alphaPaster(image, little_poison, (little_image_left_pos, int(y)))
            y += dy
        elif poison == 3:
            alphaPaster(image, Images.image_back_small, (little_image_left_pos, int(y)))
            alphaPaster(image, little_poison, (little_image_left_pos, int(y)))
            y += dy

        if sleep == 1:
            alphaPaster(image, little_faded_sleep, (little_image_left_pos, int(y)))
            # alphaPaster(image, little_sleep, (little_image_left_pos, int(y)))
            y += dy
        elif sleep == 2:
            alphaPaster(image, Images.image_back_small_faded, (little_image_left_pos, int(y)))
            alphaPaster(image, little_faded_sleep, (little_image_left_pos, int(y)))
            # alphaPaster(image, little_sleep, (little_image_left_pos, int(y)))
            y += dy
        elif sleep == 3:
            alphaPaster(image, Images.image_back_small, (little_image_left_pos, int(y)))
            alphaPaster(image, little_sleep, (little_image_left_pos, int(y)))
            y += dy

        if paralysis == 1:
            alphaPaster(image, little_faded_paralysis, (little_image_left_pos, int(y)))
            # alphaPaster(image, little_paralysis, (little_image_left_pos, int(y)))
            y += dy
        elif paralysis == 2:
            alphaPaster(image, Images.image_back_small_faded, (little_image_left_pos, int(y)))
            alphaPaster(image, little_faded_paralysis, (little_image_left_pos, int(y)))
            # alphaPaster(image, little_paralysis, (little_image_left_pos, int(y)))
            y += dy
        elif paralysis == 3:
            alphaPaster(image, Images.image_back_small, (little_image_left_pos, int(y)))
            alphaPaster(image, little_paralysis, (little_image_left_pos, int(y)))
            y += dy

        if blast == 1:
            alphaPaster(image, little_faded_blast, (little_image_left_pos, int(y)))
            # alphaPaster(image, little_blast, (little_image_left_pos, int(y)))
            y += dy
        elif blast == 2:
            alphaPaster(image, Images.image_back_small_faded, (little_image_left_pos, int(y)))
            alphaPaster(image, little_faded_blast, (little_image_left_pos, int(y)))
            # alphaPaster(image, little_blast, (little_image_left_pos, int(y)))
            y += dy
        elif blast == 3:
            alphaPaster(image, Images.image_back_small, (little_image_left_pos, int(y)))
            alphaPaster(image, little_blast, (little_image_left_pos, int(y)))
            y += dy

        if stun == 1:
            alphaPaster(image, little_faded_stun, (little_image_left_pos, int(y)))
            # alphaPaster(image, little_stun, (little_image_left_pos, int(y)))
            y += dy
        elif stun == 2:
            alphaPaster(image, Images.image_back_small_faded, (little_image_left_pos, int(y)))
            alphaPaster(image, little_faded_stun, (little_image_left_pos, int(y)))
            # alphaPaster(image, little_stun, (little_image_left_pos, int(y)))
            y += dy
        elif stun == 3:
            alphaPaster(image, Images.image_back_small, (little_image_left_pos, int(y)))
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
            p3 = (offset+0,              icon_size * images_count * SConfig.small_scale + padding * (images_count - 1) * SConfig.small_scale-1)
            p4 = (offset+line_width*2-1, icon_size * images_count * SConfig.small_scale + padding * (images_count - 1) * SConfig.small_scale-1)

            p5 = (-offset+size[0] - 2*line_width, 0)
            p6 = (-offset+size[0] - line_width, 0)
            p7 = (-offset+size[0] - line_width,   icon_size * images_count * SConfig.small_scale + padding * (images_count - 1) * SConfig.small_scale)
            p8 = (-offset+size[0] - 2*line_width, icon_size * images_count * SConfig.small_scale + padding * (images_count - 1) * SConfig.small_scale)
        else:
            p1 = (offset+line_width*2-1, 1)
            p2 = (offset+0, 1)
            p3 = (offset+0,              icon_size * images_count + padding * (images_count - 1) - 2)
            p4 = (offset+line_width*2-1, icon_size * images_count + padding * (images_count - 1) - 2)

            p5 = (-offset+size[0] - 2*line_width, 0)
            p6 = (-offset+size[0] - line_width, 0)
            p7 = (-offset+size[0] - line_width,   icon_size * images_count + padding * (images_count - 1) - 1)
            p8 = (-offset+size[0] - 2*line_width, icon_size * images_count + padding * (images_count - 1) - 1)

        clr = SConfig.braces_color_faded if not is_not_faded else SConfig.braces_color
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
