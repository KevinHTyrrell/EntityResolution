import os
import requests
import string
import time
import warnings
from typing import List
from misc.file_fns import write_to_file
from typing import Union


class Downloader:
    def __init__(
            self,
            url_base: str,
            raw_dir_base: str,
            player_dir: str,
            page_timeout: int,
            iterate_list: Union[list, str]
    ):
        self._iterate_list      = iterate_list
        self._url_base          = url_base
        self._raw_dir_base      = raw_dir_base
        self._raw_player_dir    = os.path.join(self._raw_dir_base, player_dir)
        self._page_timeout      = page_timeout

    def download_raw_player_page(
            self,
            to_download: str,
            overwrite: bool = False,
            verbose: bool = False
    ):
        filepath = os.path.join(self._raw_player_dir, to_download.upper())
        url = os.path.join(self._url_base, f'players/{to_download.upper()}/')
        if verbose:
            print(url)
        page_response = requests.get(url)
        response_code = page_response.status_code
        if response_code == 200:
            write_to_file(page_response.text, filepath, overwrite=overwrite)
        else:
            warnings.warn(f'WARNING: RECEIVED RESPONSE CODE {response_code}')
        return page_response.status_code

    def download_all_players(self, iterate_list: List[str] = None, verbose: bool = False):
        missed = []
        iterate_list = self._iterate_list if iterate_list is None else iterate_list
        for i in iterate_list:
            print(i, end=' ', flush=True)
            page_response = self.download_raw_player_page(i, verbose=verbose)
            if page_response != 200:
                missed.append(i)
            time.sleep(self._page_timeout)
        return missed