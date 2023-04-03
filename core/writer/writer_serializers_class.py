import core.writer.utils
from core import utils_path, utils
from core.writer.writer_class import WriterClass


class WriterSerializers(WriterClass):
    """Class for writing a django Serializers class on python file,

           create a python class file named serialers.py from a name (of custom app and new model)
           and fields(attributes of model)

           Attributes:
                filename: Filename of file
                filepath: Filepath of file
                content: Content of file to print
                name: Name of class
                extends: If extends some class
                attributes: attributes of class
                inside_class: If main class contains some internal class """

    def __init__(self, name: str, fields: list, **kwargs):
        super().__init__('serializers', utils_path.path_serializers(name), name, **kwargs)
        self.extends = 'serializers.ModelSerializer'
        self.attributes = fields
        self.inside_class = 'Meta'

    def write(self):
        self.content = f"""from rest_framework import serializers
from custom_apps.{self.name}.models import {self.name.capitalize()}


class {self.name.capitalize()}Serializer(serializers.ModelSerializer):
    class Meta:
        model = {self.name.capitalize()}
        fields = '__all__'       
        """
        self.print()

# {core.writer.util.write_list_tab(self.attributes, 'fields', 3)}
