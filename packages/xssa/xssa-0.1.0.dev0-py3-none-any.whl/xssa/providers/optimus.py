#  -*- coding: utf-8 -*-
"""
Author: Rafael R. L. Benevides
"""

from __future__ import annotations

import os

import json

import requests
from requests.auth import HTTPBasicAuth

from dotenv import load_dotenv
from pathlib import Path

from numbers import Number



class OptimusSession:

    # ========== ========== ========== ========== ========== class attributes
    URL_BASE = 'https://api.optimus-space.com'

    # ========== ========== ========== ========== ========== special methods
    def __init__(self, *args, **kwargs) -> None:

        if args:

            match len(args):

                case 1:
                    load_dotenv(dotenv_path=Path(args[0]), override=True)

                    username = os.getenv('OPTIMUS_USERNAME')
                    password = os.getenv('OPTIMUS_PASSWORD')

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
            load_dotenv()

            username = os.getenv('OPTIMUS_USERNAME')
            password = os.getenv('OPTIMUS_PASSWORD')

        self._auth = HTTPBasicAuth(username, password)

    def __enter__(self) -> OptimusSession:

        self._session = requests.session().__enter__()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._session.__exit__(exc_type, exc_val, exc_tb)

    # ========== ========== ========== ========== ========== private methods
    ...

    # ========== ========== ========== ========== ========== protected methods
    ...

    # ========== ========== ========== ========== ========== public methods
    def get(self, schema: str, params: dict[str, str|Number|None]|None = None) -> requests.Response:

        params = {} if params is None else params

        response = self._session.get(f'{self.URL_BASE}/{schema}', params=params, auth=self._auth)

        if response.status_code != 200:
            response = self._session.get(response.url, auth=self._auth)

            if response.status_code != 200:
                print(response.url)
                print(response.status_code)
                print(response.json())
                raise ConnectionError(response.text)

        return response

    def post(self, schema: str, data: dict[str, str|Number|None]|None = None) -> requests.Response:

        if not schema.endswith('/'):
            schema += '/'

        response = self._session.post(f'{self.URL_BASE}/{schema}', json=data, auth=self._auth)

        if response.status_code != 200:
            print(response.url)
            raise ConnectionError(response.text)

        return response

    def delete(self, schema: str) -> requests.Response:
        response = self._session.delete(f'{self.URL_BASE}/{schema}', auth=self._auth)

        if response.status_code != 200:
            print(response.url)
            print(response.status_code)
            print(response.json())
            raise ConnectionError(response.text)



    def download(self,
                 path: Path | str,
                 schema: str,
                 params: dict[str, str | Number | None] | None = None
                 ) -> None:

        response = self.get(schema, params=params)

        with Path(path).with_suffix('.json').open('w') as file:
            json.dump(response.json(), file, indent=4)

        return response
