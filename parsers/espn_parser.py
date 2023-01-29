import os
from bs4 import BeautifulSoup
from misc.file_fns import write_to_file
from parsers.base_parser import BaseParser


class ESPNParser(BaseParser):
    def extract_basic_info(
            self,
            to_parse: list = None
    ):
        file_list = os.listdir(self._raw_player_dir)
        file_list.sort()

        if to_parse is not None:
            file_list = [filename for filename in file_list if filename in to_parse]

        for filename in file_list:
            print(filename, end=' ', flush=True)
            filepath = os.path.join(self._raw_player_dir, filename)
            with open(filepath, 'r') as file_reader:
                raw_data = file_reader.read()
            parser = BeautifulSoup(raw_data, parser='lxml')
            player_rows = parser.find_all('tr')
            player_list_raw = [x.find('a') for x in player_rows if x.find('a') is not None]

            parsed_player_dict = {}
            for selected_player in player_list_raw:
                player_name_raw = selected_player.text
                player_name_list = [x.strip() for x in player_name_raw.split(',')[::-1]]
                player_name = ' '.join(player_name_list)
                player_link = selected_player['href']
                player_id = player_link.split('/')[-2]

                player_info_dict = {
                    'name_espn': player_name,
                    'id_espn': player_id,
                    'url_espn': player_link
                }
                parsed_player_dict['-'.join(player_link.split('/')[-2:])] = player_info_dict
            outpath = os.path.join(self._parsed_player_dir, filename)
            write_to_file(parsed_player_dict, filepath=outpath)
