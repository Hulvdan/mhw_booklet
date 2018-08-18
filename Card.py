
import os
from hlp import *
from SConfig import *
from PIL import Image, ImageDraw, ImageFont, ImageEnhance


class Card:
    def __init__(self, _library:dict, _w, _h):
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

        self._width, self._height = _w, _h

        self._color = '#ffff00' if self._library['color'] == "#" else self._library['color']

        self._icon_image = ImageEnhance.Color(Image.open("images\\"+self._name+'.png')).enhance(1.5)
        self._icon_image.thumbnail((SConfig.icon_size, SConfig.icon_size*2), Image.ANTIALIAS)

    debug_polygon = False
    def getCardImage(self):
        image = Image.new("RGBA", (self._width, self._height))
        drawer = ImageDraw.Draw(image)

        font = ImageFont.truetype("Gabriola.ttf", 60)
        height = self._icon_image.size[1]
        alphaPaster(image, self._icon_image, (0, self._height - SConfig.icon_bottom_pos - height))

        if Card.debug_polygon:
            p1 = (0, 0)
            p2 = (self._width - 1, 0)
            p3 = (self._width - 1, self._height - 1)
            p4 = (0, self._height - 1)
            debug_color = (255,0,0,100)
            drawer.line((p1, p2), fill=debug_color)
            drawer.line((p2, p3), fill=debug_color)
            drawer.line((p3, p4), fill=debug_color)
            drawer.line((p4, p1), fill=debug_color)

        # - drawing ailments
        w = SConfig.weakness_column_width
        sw = self._width
        p = SConfig.weakness_column_padding
        t = SConfig.weakness_top

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
        alphaPaster(image, Images.image_ail_ailment  if any_ailment_power_bigger_than_1 else Images.image_ail_ailment_faded, (sw - w, t))
        alphaPaster(image, Images.image_elem_dragon  if faded_res[-1] else Images.image_elem_dragon_faded,   (sw - 2 * w - 1 * p, t))
        alphaPaster(image, Images.image_elem_ice     if faded_res[-2] else Images.image_elem_ice_faded,      (sw - 3 * w - 2 * p, t))
        alphaPaster(image, Images.image_elem_thunder if faded_res[-3] else Images.image_elem_thunder_faded,  (sw - 4 * w - 3 * p, t))
        alphaPaster(image, Images.image_elem_water   if faded_res[-4] else Images.image_elem_water_faded,    (sw - 5 * w - 4 * p, t))
        alphaPaster(image, Images.image_elem_fire    if faded_res[-5] else Images.image_elem_fire_faded,     (sw - 6 * w - 5 * p, t))

        t += SConfig.weakness_row_padding + SConfig.weakness_column_width
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
        alphaPaster(image, self.getAttackImage(), (0, self._height - SConfig.icon_bottom_pos + SConfig.attack_icons_spacing_from_icon))
        # - drawing ailments - end

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

    drawCrossAtBottom = False
    def getWeaknessImage(self, initial, second, is_faded) -> Image.Image:
        image = Image.new("RGBA", (SConfig.weakness_column_width, SConfig.weakness_column_width * 3 + SConfig.weakness_row_padding * 2))
        if second == -1:
            if initial == 0:
                alphaPaster(image, Images.image_cross if is_faded else Images.image_cross_faded, (0,0))
            for i in range(initial):
                alphaPaster(image, Images.image_star_faded if not is_faded else Images.image_star, (0,SConfig.weakness_column_width * i + SConfig.weakness_row_padding * i))
        else:
            new_size = (int(SConfig.weakness_column_width * SConfig.small_scale), int(SConfig.weakness_column_width * SConfig.small_scale))
            little_star = Images.image_star.resize(new_size)
            little_star_faded = Images.image_star_faded.resize(new_size)
            little_cross = Images.image_cross.resize(new_size)
            little_cross_faded = Images.image_cross_faded.resize(new_size)
            little_image_left_pos = int((SConfig.weakness_column_width - new_size[0]) / 2)
            last_y = 0

            if initial == 0:
                alphaPaster(image, little_cross_faded if not is_faded else little_cross, (little_image_left_pos, 0))

            for i in range(initial):
                little_star_y = int(i * SConfig.small_scale * SConfig.weakness_row_padding + i * SConfig.small_scale * SConfig.weakness_column_width)
                alphaPaster(image, little_star_faded if not is_faded else little_star, (little_image_left_pos, little_star_y))

            for i in range(second + 1 if second == 0 else second):
                if second == 0:
                    if Card.drawCrossAtBottom:
                        alphaPaster(image, little_cross_faded if not is_faded else little_cross, (little_image_left_pos, image.size[1] - new_size[1]))
                    else:
                        last_y = int((initial if initial > 0 else 1) * new_size[1] + (initial if initial > 0 else 1) * SConfig.small_scale * SConfig.weakness_row_padding)
                        alphaPaster(image, little_cross_faded if not is_faded else little_cross, (little_image_left_pos, last_y))

            for k in range(second):
                last_y = int((initial if initial > 0 else 1) * new_size[1] + (initial if initial > 0 else 1) * SConfig.small_scale * SConfig.weakness_row_padding)
                little_star_y = int(k * SConfig.small_scale * SConfig.weakness_row_padding + k * SConfig.small_scale * SConfig.weakness_column_width + last_y)
                alphaPaster(image, little_star_faded if not is_faded else little_star, (little_image_left_pos, little_star_y))

            alphaPaster(image, self.drawBrackets(1 if second == 0 else second, is_faded, SConfig.weakness_column_width, SConfig.weakness_row_padding * SConfig.small_scale), (0, last_y))

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

        # new_size = (int(Card.weakness_column_width * Card.small_scale), int(Card.weakness_column_width * Card.small_scale))
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
