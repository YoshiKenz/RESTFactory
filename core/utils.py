import re
import shutil
import subprocess


def get_config_filename(app_new: str) -> str:
    """Generate trusted python path of new app Config file"""
    return f'custom_apps.{app_new}'


def get_app_url_pattern(app_new: str) -> str:
    """Generate trusted path of new app to add in project urls.py"""
    return f"path('api/{app_new}/', include('{get_config_filename(app_new)}.urls'))"


def get_login_url_pattern(app_new: str) -> str:
    """Generate trusted path of login of new app in project urls.py"""
    return f"path('api/{app_new}/login/', {app_new.capitalize()}GoogleLogin.as_view(), name='{app_new}_login')"


def get_callback_url_pattern(app_new: str) -> str:
    """Generate trusted path of login of new app in project urls.py"""
    return f"path('api/{app_new}/callback/', {app_new.capitalize()}GoogleCallback.as_view(), name='{app_new}call_back')"


def say_to_bash(command: str) -> str:
    # either if I validate input, is not secure use shell=true???
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')


def find_new_apps_from(config_json: dict) -> list:
    """Return list of name of new custom_apps to install"""
    endpoints = config_json['endpoints']
    apps_new = [endpoint['name'].lower() for endpoint in endpoints]
    return apps_new


def delete(app: str):
    shutil.rmtree(f"{app}")


def apps_installed() -> list:
    """ Give a list of custom_apps name installed"""
    apps_result = say_to_bash("find ./custom_apps -name 'apps.py' -printf '%h\n' | sort -u")
    apps_text = str(apps_result)
    apps_list = list(apps_text.split("\n"))
    apps_list.pop()
    apps_list = __format_files_name(apps_list)
    return apps_list


def get_client_data(app: str, endpoints: list):
    client_data = None
    for endpoint in endpoints:
        if endpoint['name'] == app:
            client_data = {
                'client_id': endpoint['client_id'],
                'client_secret': endpoint['client_secret']
            }
            break
    return client_data


def __format_files_name(list_filenames: list) -> list:
    """ Format string name file after filter bash command"""
    list_filenames = [re.sub('^./custom_apps/', '', item) for item in list_filenames]

    return list_filenames
