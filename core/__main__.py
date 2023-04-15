import argparse
import os

from core import utils_path, factory_handler

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='RESTFactory argument parser')
    parser.add_argument('--reset', '-r', dest='reset', help='Reset installed apps', required=False, action='store_true')
    parser.add_argument('config_file', nargs='?', help='JSON configuration file')
    args = parser.parse_args()
    os.chdir(utils_path.PROJECT_PATH)
    if args.reset:
        factory_handler.reset()
    elif args.config_file:
        factory_handler.install(args.config_file)
