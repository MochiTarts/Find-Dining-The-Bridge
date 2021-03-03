from enum import Enum

class Roles(Enum):
    """ The Roles a user can have """
    RO = "Restaurant Owner"
    BU = "Basic User"

    @classmethod
    def choices(cls):
        """
        Gets the choices in tuple form
        :return: roles' name and value in tuple form usable to models
        """
        return tuple((role.name, role.value) for role in cls)