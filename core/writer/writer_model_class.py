from core import utils_path
from core.writer import utils_field
from core.writer.writer_class import WriterClass


class WriterModel(WriterClass):
    """Class for writing a django Model class on python file,

           create a python class file from filename, name and filepath there is other attributes to set for adding
           different plug-in(ex. define some attributes, extends some classes..)

           Attributes:
                filename: Filename of file
                filepath: Filepath of file
                content: Content of file to print
                name: Name of class
                extends: If extends some class
                attributes: attributes of class
    """

    def __init__(self, name: str, attributes: dict, **kwargs):
        super().__init__('models', utils_path.path_models(name), name, **kwargs)
        self.extends = 'models.Model'
        self.attributes = attributes

    def __write_attributes(self):
        attributes = ""
        for name, type_field in self.attributes.items():
            attributes = "\n    ".join([attributes, f"{name} = models.{utils_field.generate_field(name, type_field)}"])
        return attributes

    def write(self):
        self.content = f"""from django.db import models


class {self.name.capitalize()}(models.Model):
    id = models.TextField(primary_key=True)
    {self.__write_attributes()}

    def __str__(self):
        field_values = []
        for field in self._meta.get_fields():
            field_values.append(str(getattr(self, field.name, '')))
        return ''.join(field_values)

        """
        self.print()
