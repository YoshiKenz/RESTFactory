import os

from core import config

# CURRENT_PATH = os.getcwd()
# PROJECT_PATH = os.path.abspath(os.path.join(CURRENT_PATH, os.pardir))
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_PATH = os.path.abspath(os.path.join(CURRENT_PATH, os.pardir))
PROJECT_MAIN_FOLDER_PATH = f'{PROJECT_PATH}/{config.PROJECT_NAME}'
APPS_PATH = f'{PROJECT_PATH}/{config.APPS_FOLDER}'
SETTINGS_FILE_PATH = f'{PROJECT_MAIN_FOLDER_PATH}/{config.SETTINGS_FILE}'
ADD_SETTINGS_FILE_PATH = f'{PROJECT_MAIN_FOLDER_PATH}/{config.ADDITIONAL_SETTINGS_FILE}'
ADD_URLS_PATTERN_PATH = f'{PROJECT_MAIN_FOLDER_PATH}/{config.ADDITIONAL_URLS_FILE}'
CONFIG_INPUT_FILE_PATH = f'{PROJECT_PATH}/{config.INPUT_FILE}'
SCHEMA_FILE_PATH = f'{PROJECT_PATH}/{config.INPUT_FILE}'


def path(app: str) -> str:
    return f'{APPS_PATH}/{app}'


def path_models(app: str) -> str:
    return f'{path(app)}/{config.APP_MODELS_FILE}'


def path_serializers(app: str) -> str:
    return f'{path(app)}/{config.APP_SERIALIZERS_FILE}'


def path_admin(app: str) -> str:
    return f'{path(app)}/{config.APP_ADMIN_FILE}'


def path_apps_config(app: str) -> str:
    return f'{path(app)}/{config.APPS_CONFIG_FILE}'


def path_views(app: str) -> str:
    return f'{path(app)}/{config.APP_VIEWS_FILE}'


def path_urls(app: str) -> str:
    return f'{path(app)}/{config.APP_URLS_FILE}'


def path_permissions(app: str) -> str:
    return f'{path(app)}/{config.APP_PERMISSIONS_FILE}'
