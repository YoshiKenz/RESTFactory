from core.writer import utils_field
from core.writer.writer import Writer


class WriterClass(Writer):
    """Class for writing a class on python file,

           create a python class file from filename, name and filepath
           there is other attributes to set for adding different plug-in(ex. define some attributes, extends some classes..)


           Attributes:
            filename: Filename of file
            filepath: Filepath of file
            content: Content of file to print
            name: Name of class
            extends: If extends some class, init None
            attributes: attributes of class, init None

    """

    def __init__(self, filename: str, filepath: str, name: str, **kwargs):
        super().__init__(filename, filepath, **kwargs)
        self.name = name
        self.extends = None
        self.attributes = None


