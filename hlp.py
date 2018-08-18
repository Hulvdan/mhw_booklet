
from PIL import Image
from SConfig import *
import time


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' % \
                  (method.__name__, (te - ts) * 1000))
        return result
    return timed

class Colors:
    transparent = (0,0,0,0)
    black = (0,0,0,255)
    white = (255,255,255,255)
    font_poison = "#81007F"
    font_sleep = "#05006C"
    font_paralysis = "#666500"
    font_blast = "#431900"
    font_stun = "#666500"

class Images:
    s = None
    image_elem_fire = None
    image_elem_water = None
    image_elem_thunder = None
    image_elem_ice = None
    image_elem_dragon = None
    image_elem_fire_faded = None
    image_elem_water_faded = None
    image_elem_thunder_faded = None
    image_elem_ice_faded = None
    image_elem_dragon_faded = None
    image_fireblight = None
    image_waterblight = None
    image_iceblight = None
    image_thunderblight = None
    image_diamond = None
    image_mud = None
    image_ail_poison = None
    image_ail_sleep = None
    image_ail_paralysis = None
    image_ail_blast = None
    image_ail_stun = None
    image_ail_poison_faded = None
    image_ail_sleep_faded = None
    image_ail_paralysis_faded = None
    image_ail_blast_faded = None
    image_ail_stun_faded = None
    image_ail_bleed = None
    image_ail_effluvial = None
    image_ail_ailment = None
    image_ail_ailment_faded = None
    image_star = None
    image_star_faded = None
    image_cross = None
    image_cross_faded = None
    image_back_small = None
    image_back_small_faded = None
    small_scale = .59 # image scaling needed to put 5 little stars into height of 3 normal stars. Spacing calculated too

    @staticmethod
    def load():
        weakness_column_width = SConfig.weakness_column_width
        Images.s = list([weakness_column_width] * 2)
        s = Images.s
        Images.image_elem_fire           = Image.open(r"images\element\fire.png")
        Images.image_elem_water          = Image.open(r"images\element\water.png")
        Images.image_elem_thunder        = Image.open(r"images\element\thunder.png")
        Images.image_elem_ice            = Image.open(r"images\element\ice.png")
        Images.image_elem_dragon         = Image.open(r"images\element\dragon.png")

        Images.image_elem_fire_faded     = Image.open(r"images\element\fire_faded.png")
        Images.image_elem_water_faded    = Image.open(r"images\element\water_faded.png")
        Images.image_elem_thunder_faded  = Image.open(r"images\element\thunder_faded.png")
        Images.image_elem_ice_faded      = Image.open(r"images\element\ice_faded.png")
        Images.image_elem_dragon_faded   = Image.open(r"images\element\dragon_faded.png")

        Images.image_fireblight          = Image.open(r"images\element\fireblight.png")
        Images.image_waterblight         = Image.open(r"images\element\waterblight.png")
        Images.image_iceblight           = Image.open(r"images\element\iceblight.png")
        Images.image_thunderblight       = Image.open(r"images\element\thunderblight.png")
        Images.image_diamond             = Image.open(r"images\element\diamond.png")
        Images.image_mud                 = Image.open(r"images\element\mud.png")

        Images.image_ail_poison          = Image.open(r"images\element\poison.png")
        Images.image_ail_sleep           = Image.open(r"images\element\sleep.png")
        Images.image_ail_paralysis       = Image.open(r"images\element\paralysis.png")
        Images.image_ail_blast           = Image.open(r"images\element\blast.png")
        Images.image_ail_stun            = Image.open(r"images\element\stun.png")

        Images.image_ail_poison_faded    = Image.open(r"images\element\poison_faded.png")
        Images.image_ail_sleep_faded     = Image.open(r"images\element\sleep_faded.png")
        Images.image_ail_paralysis_faded = Image.open(r"images\element\paralysis_faded.png")
        Images.image_ail_blast_faded     = Image.open(r"images\element\blast_faded.png")
        Images.image_ail_stun_faded      = Image.open(r"images\element\stun_faded.png")

        Images.image_ail_bleed           = Image.open(r"images\element\bleed.png")
        Images.image_ail_effluvial       = Image.open(r"images\element\effluvial.png")
        Images.image_ail_ailment         = Image.open(r"images\element\ailment.png").resize(s)
        Images.image_ail_ailment_faded   = Image.open(r"images\element\ailment_faded.png").resize(s)

        Images.image_star                = Image.open(r"images\element\star.png")
        Images.image_star_faded          = Image.open(r"images\element\star_faded.png")
        Images.image_cross               = Image.open(r"images\element\cross.png")
        Images.image_cross_faded         = Image.open(r"images\element\cross_faded.png")
        Images.image_back_small          = Image.open(r"images\element\back.png")
        Images.image_back_small_faded    = Image.open(r"images\element\back_faded.png")

        Images.image_elem_fire          .thumbnail(s, Image.ANTIALIAS)
        Images.image_elem_water         .thumbnail(s, Image.ANTIALIAS)
        Images.image_elem_thunder       .thumbnail(s, Image.ANTIALIAS)
        Images.image_elem_ice           .thumbnail(s, Image.ANTIALIAS)
        Images.image_elem_dragon        .thumbnail(s, Image.ANTIALIAS)
        Images.image_elem_fire_faded    .thumbnail(s, Image.ANTIALIAS)
        Images.image_elem_water_faded   .thumbnail(s, Image.ANTIALIAS)
        Images.image_elem_thunder_faded .thumbnail(s, Image.ANTIALIAS)
        Images.image_elem_ice_faded     .thumbnail(s, Image.ANTIALIAS)
        Images.image_elem_dragon_faded  .thumbnail(s, Image.ANTIALIAS)
        Images.image_ail_poison         .thumbnail(s, Image.ANTIALIAS)
        Images.image_ail_poison_faded   .thumbnail(s, Image.ANTIALIAS)
        Images.image_ail_sleep          .thumbnail(s, Image.ANTIALIAS)
        Images.image_ail_sleep_faded    .thumbnail(s, Image.ANTIALIAS)
        Images.image_ail_paralysis      .thumbnail(s, Image.ANTIALIAS)
        Images.image_ail_paralysis_faded.thumbnail(s, Image.ANTIALIAS)
        Images.image_ail_blast          .thumbnail(s, Image.ANTIALIAS)
        Images.image_ail_blast_faded    .thumbnail(s, Image.ANTIALIAS)
        Images.image_ail_stun           .thumbnail(s, Image.ANTIALIAS)
        Images.image_ail_stun_faded     .thumbnail(s, Image.ANTIALIAS)
        Images.image_ail_bleed          .thumbnail(s, Image.ANTIALIAS)
        Images.image_ail_effluvial      .thumbnail(s, Image.ANTIALIAS)
        Images.image_star               .thumbnail(s, Image.ANTIALIAS)
        Images.image_star_faded         .thumbnail(s, Image.ANTIALIAS)
        Images.image_cross              .thumbnail(s, Image.ANTIALIAS)
        Images.image_cross_faded        .thumbnail(s, Image.ANTIALIAS)
        Images.image_back_small         .thumbnail((s[0] * Images.small_scale, s[1] * Images.small_scale), Image.ANTIALIAS)
        Images.image_back_small_faded   .thumbnail((s[0] * Images.small_scale, s[1] * Images.small_scale), Image.ANTIALIAS)

def alphaPaster(img_destination:Image.Image, img_source:Image.Image, pos=(0,0)):
    """Pastes img_source into img_destination with alpha_composing"""
    intermediate_image = Image.new("RGBA", img_destination.size, Colors.transparent)
    intermediate_image.paste(img_source, pos)
    img_destination.alpha_composite(intermediate_image)

