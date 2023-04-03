import os
import subprocess

from django.apps import apps
from django.core import management

from core import utils, utils_path
from core.logger_package import logger


def call_startapp(app_new: str):
    os.chdir(utils_path.PROJECT_PATH)
    utils.say_to_bash(f'mkdir custom_apps/{app_new}')
    management.call_command('startapp', app_new, utils_path.path(app_new))


def call_migrate_db(app_new: str):
    logger.info("app config %s", app_new)
    result = subprocess.run(f'python manage.py makemigrations {app_new}', shell=True, stdout=subprocess.PIPE)
    logger.info("makemigrations -> %s", result)
    result = subprocess.run(f'python manage.py migrate', shell=True, stdout=subprocess.PIPE)
    logger.info("migrate -> %s", result)
