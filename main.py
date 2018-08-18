
# Depends on Pillow 5.2.0
from Booklet import *


def main():
    Images.load()
    data_filename = "data.json"

    booklet_lh = Booklet(data_filename, 6, 6, 0)
    booklet_lh.exportIntoFileAsPNG("MHW_Booklet_Landscape_Horizontal.png")

    booklet_lv = Booklet(data_filename, 6, 6, 1)
    booklet_lv.exportIntoFileAsPNG("MHW_Booklet_Landscape_Vertical.png")

    booklet_ph = Booklet(data_filename, 4, 9, 0)
    booklet_ph.exportIntoFileAsPNG("MHW_Booklet_Portrait_Horizontal.png")

    booklet_pv = Booklet(data_filename, 4, 9, 1)
    booklet_pv.exportIntoFileAsPNG("MHW_Booklet_Portrait_Vertical.png")


if __name__ == "__main__":
    main()
