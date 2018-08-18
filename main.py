
# Depends on Pillow 5.2.0
from Booklet import *


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
    Images.load()
    main()
