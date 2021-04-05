from enum import Enum


class Visibility(Enum):
    """ The Tag Categories a tag can have """
    RO = "Restaurant Owners Only"
    BU = "Consumers Only"
    ALL = "All"

    @classmethod
    def choices(cls):
        """
        Gets the choices in tuple form
        :return: visibility's name and value in tuple form usable to models
        """
        return tuple((visibility.name, visibility.value) for visibility in cls)
