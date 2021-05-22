from src.booklet import Booklet
from src.config import DIST_FOLDER


def main():
    booklet_landscape_horizontal = Booklet(12, 6, 0)
    booklet_landscape_horizontal.export_as_png(
        DIST_FOLDER / 'MHW_Booklet_Landscape_Horizontal.png')

    booklet_landscape_vertical = Booklet(6, 6, 1)
    booklet_landscape_vertical.export_as_png(
        DIST_FOLDER / 'MHW_Booklet_Landscape_Vertical.png')

    booklet_portrait_horizontal = Booklet(4, 9, 0)
    booklet_portrait_horizontal.export_as_png(
        DIST_FOLDER / 'MHW_Booklet_Portrait_Horizontal.png')

    booklet_portrait_vertical = Booklet(4, 9, 1)
    booklet_portrait_vertical.export_as_png(
        DIST_FOLDER / 'MHW_Booklet_Portrait_Vertical.png')


if __name__ == '__main__':
    main()
