import os
import shutil

from src.booklet import Booklet
from src.config import CLEAR_DIST_FOLDER_ON_START, DIST_FOLDER, logger


def main():
    if CLEAR_DIST_FOLDER_ON_START and os.path.exists(DIST_FOLDER):
        logger.info(f'Removing "{DIST_FOLDER}"')
        shutil.rmtree(DIST_FOLDER)

    booklet_landscape_horizontal = Booklet(6, 6, 0)
    booklet_landscape_horizontal.export_as_png(
        'mhw-booklet-landscape-left-to-right')

    booklet_landscape_vertical = Booklet(6, 6, 1)
    booklet_landscape_vertical.export_as_png(
        'mhw-booklet-landscape-top-to-bottom')

    booklet_portrait_horizontal = Booklet(4, 9, 0)
    booklet_portrait_horizontal.export_as_png(
        'mhw-booklet-portrait-left-to-right')

    booklet_portrait_vertical = Booklet(4, 9, 1)
    booklet_portrait_vertical.export_as_png(
        'mhw-booklet-portrait-top-to-bottom')


if __name__ == '__main__':
    main()
