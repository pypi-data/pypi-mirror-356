#  -*- coding: utf-8 -*-
"""
Author: Rafael R. L. Benevides
"""

from __future__ import annotations

import os
import json
import requests

from pathlib import Path

from dotenv import load_dotenv


# ========== ========== ========== ========== ========== ==========
class SpaceTrackSession:

    URL_BASE = "https://www.space-track.org"
    REQ_LOGIN = "/ajaxauth/login"
    REQ_LOGOUT = '/ajaxauth/logout'

    def __init__(self, *args, **kwargs) -> None:

        if args:

            match len(args):

                case 1:
                    load_dotenv(dotenv_path=Path(args[0]), override=True)

                    username = os.getenv('SPACETRACK_USERNAME')
                    password = os.getenv('SPACETRACK_PASSWORD')

                case 2:
                    username, password = args

                case _:
                    raise TypeError(f"__init__() takes 1 or 2 positional arguments but {len(args)} were given")

        elif kwargs:
            username = kwargs.pop('username')
            password = kwargs.pop('password')

            if kwargs:
                raise TypeError(f"__init__() got an unexpected keyword argument '{next(iter(kwargs))}'")

        else:
            # load_dotenv('.env')

            username = os.getenv('SPACETRACK_USERNAME')
            password = os.getenv('SPACETRACK_PASSWORD')

        self.__credentials = {
            'identity': username,
            'password': password,
        }

    def __enter__(self) -> SpaceTrackSession:

        self._session = requests.session().__enter__()

        response = self._session.post(f"{self.URL_BASE}{self.REQ_LOGIN}", data=self.__credentials)
        response.raise_for_status()

        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:

        self._session.post(f"{self.URL_BASE}{self.REQ_LOGOUT}")

        self._session.__exit__(exc_type, exc_value, traceback)

    def get(self, link: str) -> requests.Response:

        response = self._session.get(f"{self.URL_BASE}{link}")
        if response.status_code != 200:
            raise ConnectionError('Could not retrieve data')

        return response

    def post(self, link: str, files: dict) -> requests.Response:

        response = self._session.post(f"{self.URL_BASE}{link}", files=files)
        if response.status_code != 200:
            raise ConnectionError('Could not send data')

        return response

    @classmethod
    def download_catalog(cls, filepath: Path|str) -> None:

        with cls() as session:

            response = session.get('/basicspacedata/query/class/satcat/orderby/NORAD_CAT_ID%20asc/emptyresult/show')

            filepath = Path(filepath).with_suffix('.json')

            with filepath.open('w') as file:
                json.dump(response.json(), file, indent=4)


