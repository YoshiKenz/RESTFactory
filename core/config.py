from typing import Type

# value to set in config.json
base_url: Type[str]

CONFIG_DIR = "./config"
LOG_DIR = "./logs"
LOG_CONFIG_INI = "logging.ini"
PROJECT_NAME = "restfactory"
APPS_FOLDER = "custom_apps"
APP_MODELS_FILE = "models.py"
APP_SERIALIZERS_FILE = "serializers.py"
APP_PERMISSIONS_FILE = "permissions.py"
APP_ADMIN_FILE = "admin.py"
SETTINGS_FILE = "settings.py"
ADDITIONAL_SETTINGS_FILE = "additional_settings.py"
ADDITIONAL_URLS_FILE = "additional_urls.py"
INPUT_FILE = "config.json"
APPS_CONFIG_FILE = "apps.py"
APP_VIEWS_FILE = "views.py"
APP_URLS_FILE = "urls.py"
ADDITIONAL_URL_PATTERN = "additionalurlpattern"
ADDITIONAL_APPS = "ADDITIONAL_APPS"
SCOPES = ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']


