import os
import shutil

from src.booklet import Booklet, FillingMode
from src.config import (
    CLEAR_DIST_FOLDER_ON_START, DIST_FOLDER, PROJECT_VERSION, logger)


def main():
    if CLEAR_DIST_FOLDER_ON_START and os.path.exists(DIST_FOLDER):
        logger.info(f'Removing "{DIST_FOLDER}"')
        shutil.rmtree(DIST_FOLDER)

    booklet_landscape_left_to_right = Booklet(6, 6, FillingMode.left_to_right)
    booklet_landscape_left_to_right.export_as_png(
        f'mhw-booklet-{PROJECT_VERSION}-landscape-left-to-right')

    booklet_landscape_top_to_bottom = Booklet(6, 6, FillingMode.top_to_bottom)
    booklet_landscape_top_to_bottom.export_as_png(
        f'mhw-booklet-{PROJECT_VERSION}-landscape-top-to-bottom')

    booklet_portrait_left_to_right = Booklet(4, 9, FillingMode.left_to_right)
    booklet_portrait_left_to_right.export_as_png(
        f'mhw-booklet-{PROJECT_VERSION}-portrait-left-to-right')

    booklet_portrait_top_to_bottom = Booklet(4, 9, FillingMode.top_to_bottom)
    booklet_portrait_top_to_bottom.export_as_png(
        f'mhw-booklet-{PROJECT_VERSION}-portrait-top-to-bottom')


if __name__ == '__main__':
    main()
