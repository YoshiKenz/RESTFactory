import fileinput
import sys

from core import utils
from core.writer import constant


def list_to_string(list_to_print: list) -> str:
    """Convert a list to string for printing to file python"""
    return ''.join([f"\n\t\"{item}\"," for item in list_to_print])


def list_to_string_tab(list_to_print: list, n_tab: int) -> str:
    """Convert a list to string for printing to file python"""
    return ''.join([f"\n{n_tab * constant.TAB}\"{item}\"," for item in list_to_print])


def write_list(list_to_print: list, name_list: str) -> str:
    """Return a string that contain a list to print in file python"""
    # return name_list + " = [" + list_to_string(list_to_print) + " \n]\n"
    return f"{name_list} = [{list_to_string(list_to_print)} \n]\n"


def write_list_tab(list_to_print: list, name_list: str, n_tab: int) -> str:
    """Return a string that contain a list to print in file python with n tab"""
    return f"{name_list} = [{list_to_string_tab(list_to_print, n_tab)} \n{constant.TAB * (n_tab -1)}]\n"


def write_list_no_string(list_to_print: list, name_list: str) -> str:
    return f"{name_list} = [{list_print_no_string(list_to_print)} \n]\n"


def list_print_no_string(list_to_print: list) -> str:
    """Convert a list to string for printing to file python addtional_urls"""
    return ''.join([f"\n\t{item}," for item in list_to_print])


def replace_config_name(file, app):
    """ Replace config name because we use a sub folder for custom apps. See in getter.additional_settings.py
    'custom_apps.app' either 'app' """
    search_exp = f"name = '{app}'"
    replace_exp = f"name = '{utils.get_config_filename(app)}'"
    for line in fileinput.input(file, inplace=1):
        line = line.replace(search_exp, replace_exp)
        sys.stdout.write(line)
