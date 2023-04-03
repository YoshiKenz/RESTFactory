from core import config
import core.writer.constant


class Writer:
    """Class for writing a  python file

       create a python class file from filename, and filepath
       there is other attributes to set for adding different plug-in(ex. define some attributes, extends some classes..)

       Attributes:
           filename: Filename of file
           filepath: Filepath of file
           content: Content of file to print
       """

    def __init__(self, filename: str, filepath: str, **kwargs):
        self.filename = f"{filename}.py"
        self.filepath = filepath
        # util.path_models(name)
        self.content = ''

    def append(self, to_append: str) -> str:
        self.content = ''.join([self.content, to_append])

    def write_row(self, row: str):
        self.append(f'{row}\n')

    def write_new_line(self):
        self.write_row('')

    def write_row_with_tab(self, n_tab: int, row: str):
        for i in range(0, n_tab):
            self.append(core.writer.constant.TAB)
        self.write_row(f'{row}')

    def write_import(self, from_str: str, class_str: str):
        self.write_row(f'from {from_str} import {class_str}')

    def print(self):
        try:
            with open(self.filepath, 'w') as filepath:
                filepath.write(self.content)
        except Exception as err:
            pass
            # handle exception

    def write_model_admin_register(self, app: str) -> str:
        app_capitalized = app.capitalize()
        self.write_import('django.contrib', 'admin')
        self.write_new_line()
        self.write_import(f'{config.APPS_FOLDER}.{app}.models', f'{app_capitalized}')
        self.write_new_line()
        self.write_new_line()
        self.write_row(f'admin.site.register({app_capitalized})')
        self.print()
