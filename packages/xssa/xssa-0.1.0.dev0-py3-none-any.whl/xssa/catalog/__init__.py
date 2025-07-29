#  -*- coding: utf-8 -*-
"""
Author: Rafael R. L. Benevides
"""

import pandas

from pathlib import Path

from xssa.providers import SpaceTrackSession


satcat_filepath = Path(__file__).parent / 'satcat.json'


def update_catalog_file() -> None:
    SpaceTrackSession.download_catalog(satcat_filepath)


def satcat() -> pandas.DataFrame:
    return pandas.read_json(satcat_filepath)


def get_info(norad: int|str) -> pandas.Series:

    frame = satcat()
    return frame.loc[frame['NORAD_CAT_ID'] == int(norad)].iloc[0]
