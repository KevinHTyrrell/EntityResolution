from misc.file_fns import read_file
from downloaders.downloader import Downloader
from parsers.espn_parser import ESPNParser
from parsers.pfr_parser import PFRParser


if __name__ == '__main__':
    downloader_config_filepath = 'ref/config_download.yml'
    parser_config_filepath = 'ref/config_parser.yml'

    downloader_config = read_file(downloader_config_filepath)
    parser_config = read_file(parser_config_filepath)

    downloader_config_espn = downloader_config['ESPN']
    downloader_config_pfr = downloader_config['PFR']
    parser_config_espn = parser_config['ESPN']
    parser_config_pfr = parser_config['PFR']

    downloader_espn = Downloader(**downloader_config_espn)
    downloader_pfr = Downloader(**downloader_config_pfr)
    downloader_espn.download_all_players()
    downloader_pfr.download_all_players()

    parser_espn = ESPNParser(**parser_config_espn)
    parser_pfr = PFRParser(**parser_config_pfr)
    parser_espn.extract_basic_info()
    parser_pfr.extract_basic_info()