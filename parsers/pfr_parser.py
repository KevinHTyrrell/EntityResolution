import os
from bs4 import BeautifulSoup
from misc.file_fns import write_to_file
from parsers.base_parser import BaseParser


class PFRParser(BaseParser):
    def extract_basic_info(
            self,
            to_parse: list = None
    ):
        file_list = os.listdir(self._raw_player_dir)
        file_list.sort()

        if to_parse is not None:
            file_list = [filename for filename in file_list if filename in to_parse]

        for filename in file_list:
            print(filename, end='', flush=True)
            filepath = os.path.join(self._raw_player_dir, filename)
            with open(filepath, 'r') as file_reader:
                raw_data = file_reader.read()
            parser = BeautifulSoup(raw_data, parser='lxml')
            player_list_raw = parser.find('div', {'class': 'section_content'})
            player_list = player_list_raw.findAll('p')

            parsed_player_dict = {}
            for selected_player in player_list:
                player_link = selected_player.find('a')
                player_info = selected_player.text.replace(player_link.text, '')
                player_id = player_link['href'].replace('.', '/').split('/')[-2]

                player_info_dict = {
                    'name_pfr':     player_link.text,
                    'id_pfr':       player_id,
                    'url_pfr':      player_link['href'],
                    'info_pfr':     player_info.split()
                }
                parsed_player_dict[player_id] = player_info_dict
            outpath = os.path.join(self._parsed_player_dir, filename)
            write_to_file(parsed_player_dict, filepath=outpath)
