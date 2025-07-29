#  -*- coding: utf-8 -*-
"""
Author: Rafael R. L. Benevides
"""

from pathlib import Path
from dotenv import load_dotenv


def load_credentials(credentials_dotenv_filepath: Path|str|None=None) -> None:
    if credentials_dotenv_filepath is None:
        load_dotenv('.env')
    else:
        load_dotenv(dotenv_path=credentials_dotenv_filepath)