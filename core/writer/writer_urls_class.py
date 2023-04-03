from core import utils_path
from core.writer.writer import Writer


class WriterUrls(Writer):
    """Class for writing a python urls file for django apps,

                   create a python file named urls.py


                   Attributes:
                    app: Name of app
    """

    def __init__(self, app: str, **kwargs):
        super().__init__('urls', utils_path.path_urls(app), **kwargs)
        self.name = app

    def write(self):
        self.content = f"""from rest_framework.routers import SimpleRouter
from custom_apps.{self.name}.views import {self.name.capitalize()}ViewSet


router = SimpleRouter()
router.register('', {self.name.capitalize()}ViewSet, basename='{self.name}')

urlpatterns = router.urls
        """
        self.print()


def get_import_getter_url(apps_installed: list) -> str:
    views_strings = [
        f"from custom_apps.{app}.views import GoogleLogin as {app.capitalize()}GoogleLogin\n"
        f"from custom_apps.{app}.views import GoogleCallback as {app.capitalize()}GoogleCallback"
        for app in apps_installed
    ]
    return "\n".join(views_strings)




