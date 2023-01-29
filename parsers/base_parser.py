from abc import ABC


class BaseParser(ABC):
    def __init__(
            self,
            raw_player_dir: str,
            parsed_player_dir: str
    ):
        self._raw_player_dir        = raw_player_dir
        self._parsed_player_dir     = parsed_player_dir

    def extract_basic_info(self, to_parse: list = None):
        NotImplementedError('NOT IMPLEMENTED')

