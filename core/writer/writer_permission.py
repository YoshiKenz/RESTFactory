from core import utils_path
from core.writer.writer_class import WriterClass


class WriterPermission(WriterClass):
    """Class for writing a django Permission class on python file,

               create a python class file named {app}Permission.py

               Attributes:
                    filename: Filename of file
                    filepath: Filepath of file
                    content: Content of file to print
                    auths:
                """

    def __init__(self, data: dict, **kwargs):
        super().__init__('permissions', utils_path.path_permissions(data['name']), data['name'], **kwargs)
        self.permissions = dict((k, data[k]) for k in ("read", "write"))

    def write(self):
        self.content = f"""from rest_framework import permissions

        
class {self.name.capitalize()}Permission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            app_roles = request.user.app_role.split(', ')
        
        read_actions = {'list', 'retrieve'}
        read_roles = {self.get_read_roles()}
        
{self.read_permissions()}      
        
        write_actions = {'create', 'update', 'partial_update', 'destroy'}
        write_roles = {self.get_write_roles()}
        
{self.write_permissions()}   

        return False
        """
        self.print()

    def get_read_roles(self) -> str:
        read_roles = self.permissions['read']
        return [f"{x}_{self.name}" for x in read_roles if x != 'public']

    def get_write_roles(self) -> str:
        write_roles = self.permissions['write']
        return [f"{x}_{self.name}" for x in write_roles if x != 'public']

    def read_permissions(self) -> str:
        read_permission = self.permissions['read']
        result = []

        for group in read_permission:
            if group == 'public':
                result.append(f"""        if not request.user.is_authenticated or not read_roles:
            if view.action in read_actions:
                return True""")
            else:
                result.append(f"""        if request.user.is_authenticated:
            if any(role in app_roles for role in read_roles):
                if view.action in read_actions:
                    return True""")

        return '\n'.join(result)

    def write_permissions(self) -> str:
        write_permission = self.permissions['write']
        result = []

        for group in write_permission:
            if group == 'public':
                result.append(f"""        if not request.user.is_authenticated or not write_roles:
            if view.action in write_actions:
                return True""")
            else:
                result.append(f"""        if request.user.is_authenticated:
            if any(role in app_roles for role in write_roles):
                if view.action in write_actions:
                    return True""")

        return '\n'.join(result)
