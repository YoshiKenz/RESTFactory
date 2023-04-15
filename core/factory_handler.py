import argparse
import os

import django
import json

import jsonschema

from core import utils, utils_path, config, manage_helper
from core.logger_package import logger
from core.writer import utils as writer_utils, writer_urls_class

from core.writer.writer import Writer
from core.writer.writer_model_class import WriterModel
from core.writer.writer_permission import WriterPermission
from core.writer.writer_serializers_class import WriterSerializers
from core.writer.writer_urls_class import WriterUrls
from core.writer.writer_views_class import WriterViewsClass


def install(config_path : str):

    # Read the content of configuration file
    with open(config_path, 'r') as f:
        # with open(sys.argv[1], 'r') as f:
        config_string = f.read()

    with open(config.SCHEMA_FILE, 'r') as f:
        schema_str = f.read()

    try:
        schema = json.loads(schema_str)
    except json.JSONDecodeError:
        logger.info('Il file schema.json non contiene un JSON valido')
        exit(1)

    # convert config file in json
    config_json = json.loads(config_string)

    logger.info("Config read: %s", str(config_json))

    jsonschema.validate(config_json, schema)

    # set base url
    config.base_url = config_json['baseUrl']

    # reset custom_apps old version
    if utils.apps_installed():
        reset()

    # list of new custom_apps to install
    apps_new = utils.find_new_apps_from(config_json)
    models = config_json['models']

    logger.info("new custom_apps to install: %s", str(apps_new))
    logger.info("new models to install: %s", str(models))

    for app in apps_new:
        _install(app)
        _install_model(app, models[app])
        _configure(app, models[app], utils.get_client_data(app, config_json['endpoints']))

    _create_permissions(config_json['endpoints'])

    apps_installed = utils.apps_installed()
    _install_url(apps_installed)


# .: STEP 1 :.
def _install(app_new):
    """Install the new app.

        Do this steps:
            - run command startapp
            - refactor config name in apps.py of each new app
            - add new app name in ADDITIONAL_SETTINGS

        Args:
            app_new: A string that represent the name of new app to install
        """
    from restfactory.additional_settings import ADDITIONAL_APPS
    logger.info("START TO INSTALL %s", app_new)
    django.setup()
    # write additional_settings.py
    manage_helper.call_startapp(app_new)
    logger.info("step 01: created %s", app_new)
    new_additional_apps = ADDITIONAL_APPS
    file_name_app = utils.get_config_filename(app_new)

    writer_utils.replace_config_name(utils_path.path_apps_config(app_new), app_new)
    logger.info("step 02: refactored config name in apps.py for %s", app_new)
    new_additional_apps.append(file_name_app)

    with open(utils_path.ADD_SETTINGS_FILE_PATH, 'w') as file_add_settings:
        tmp = writer_utils.write_list(new_additional_apps, config.ADDITIONAL_APPS)
        file_add_settings.write(tmp)

    logger.info("step 03: added in ADDITIONAL_APPS. END TO INSTALL %s", app_new)


# .: STEP 2 :. CHARGE MODELS
def _install_model(app_new: str, attributes: dict):
    """Install model from config file

            Do this steps:
                - write models.py file for each new app to install
                - for each new apps add in file admin.py the entry for new model
                - run bash command for migration of new model
                    python ./manage.py makemigrations
                    python ./manage.py migrate

            Args:
                app_new: A string that represent the name of new app to install
                attributes: A dict that describes the attributes of new models
            """
    logger.info("START TO SET MODELS FOR %s", app_new)
    model_class = WriterModel(app_new, attributes)
    model_class.write()
    logger.info("step 01: written model file")
    writer_instance = Writer(config.APP_ADMIN_FILE, utils_path.path_admin(app_new))
    writer_instance.write_model_admin_register(app_new)
    logger.info("step 02: app registered in admin.py")
    manage_helper.call_migrate_db(app_new)
    logger.info("step 03 : migration of model done. END TO SET MODELS FOR %s", app_new)


def _configure(app_new: str, attributes: dict, client_data: dict):
    """Do other step to configure new apps

            Do this steps:
                - write the serializers for each new app to install
                - write views.py for each new app to install
                - write urls.py for each new app to install
                - add new path urls in ADDITIONAL_URLS


            Args:
                app_new: A string that represent the name of new app to install
                attributes: A dict that describes the attributes of new models
            """
    logger.info("START FINAL STEPS FOR %s", app_new)
    serializers_class = WriterSerializers(str(app_new), list(attributes.keys()))
    serializers_class.write()
    logger.info("step 01: written serializers file")
    views_class = WriterViewsClass(app_new, client_data['client_id'], client_data['client_secret'])
    views_class.write()
    logger.info("step 02: written views file")
    urls_file = WriterUrls(app_new)
    urls_file.write()
    logger.info("step 03: written urls file")

    logger.info("step 03: added in ADDITIONAL_URLS. END TO INSTALL %s", app_new)


def _install_url(apps_installed: list):
    # new_additional_url_patterns = []
    # for app in apps_installed:
    #    new_additional_url_patterns.append(util.get_url_pattern(app))

    new_additional_url_patterns = list(map(utils.get_login_url_pattern, apps_installed))
    new_additional_url_patterns += list(map(utils.get_callback_url_pattern, apps_installed))
    new_additional_url_patterns += list(map(utils.get_app_url_pattern, apps_installed))

    with open(utils_path.ADD_URLS_PATTERN_PATH, 'w+') as file_add_urls:
        # backup_additional_urls = file_add_urls.read()
        import_tmp = f"""from django.urls import path, include
{writer_urls_class.get_import_getter_url(apps_installed)}

"""
        tmp = writer_utils.write_list_no_string(new_additional_url_patterns, config.ADDITIONAL_URL_PATTERN)
        file_add_urls.write(import_tmp + tmp)


def _create_permissions(endpoints: list):
    for endpoint in endpoints:
        permissions_class = WriterPermission(endpoint)
        permissions_class.write()


def reset():
    """Reset project during development."""

    with open(f'{utils_path.ADD_SETTINGS_FILE_PATH}', 'w') as file_add_settings:
        file_add_settings.write(writer_utils.write_list([], config.ADDITIONAL_APPS))
    with open(f'{utils_path.ADD_URLS_PATTERN_PATH}', 'w') as file_urls_settings:
        file_urls_settings.write(
            f"from django.urls import path, include\n{writer_utils.write_list([], 'additionalurlpattern')}")

    apps_installed = utils.apps_installed()
    if apps_installed:
        for app in apps_installed:
            logger.info("Deleted: %s", app)
            utils.delete(f'{utils_path.path(app)}')
    logger.info("End of reset")



