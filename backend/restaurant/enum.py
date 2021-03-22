from enum import Enum


class Prices(Enum):
    """ The Price Points a restaurant can have """
    #Low = "$"
    #Medium = "$$"
    #High = "$$$"
    LOW = '$ (under $10)'
    MID =  '$$ ($11 - $30)'
    HIGH = '$$$ ($31 - $60)'
    EXHIGH =  '$$$$ (over $61)'

    @classmethod
    def choices(cls):
        """
        Gets the choices in tuple form
        :return: prices' name and value in tuple form usable to models
        """
        return tuple((role.name, role.value) for role in cls)

    @classmethod
    def has_key(cls, name):
        return name in cls.__members__


class Categories(Enum):
    """ The Tag Categories a tag can have """
    PR = "Promotion"
    FR = "Food Restriction"
    CU = "Cuisine"
    DI = "Dish"

    @classmethod
    def choices(cls):
        """
        Gets the choices in tuple form
        :return: categories' name and value in tuple form usable to models
        """
        return tuple((role.name, role.value) for role in cls)

class Status(Enum):
    """ The Status Value a restaurant can have """
    Rejected = "Rejected"
    Pending = "Pending"
    Approved = "Approved"
    In_Progress = "In_Progress"

    @classmethod
    def choices(cls):
        """
        Gets the choices in tuple forms
        :return: categories' name and value in tuple form usable to models
        """
        return tuple((role.name, role.value) for role in cls)

class Options(Enum):
    """ The options a restaurant can offer """
    PICKUP = 'Pick-up'
    DELIVERY = 'Delivery'
    DINE = 'Dine-in'
    PATIO = 'Patio'
    MEAL = 'Meal kits'
    CATER = 'Catering'
    MUSIC = 'Live music'
    WIFI = 'Wifi'
    PARK = 'Parking'
    ACC = 'Accessible Access (ramps, one floor etc.)'
    LLBO = 'LLBO'
    CASH = 'Cash only'
    VEG = 'Vegetarian Options'
    VE = 'Vegan Options'
    GF = 'Gluten-free Options'
    HALAL = 'Halal Options'

    @classmethod
    def names(cls):
        """
        Gets the offer options in tuple forms
        :return: options' value in tuple form
        """
        return tuple(option.name for option in cls)

    @classmethod
    def values(cls):
        """
        Get the offer options values in tuple form
        :return: options' value in tuple form
        """
        return tuple(option.value for option in cls)

class Payment(Enum):
    """ The types of payment a restaurant can have """
    CR = 'Credit'
    DB = 'Debit'
    CA = 'Cash'

    @classmethod
    def names(cls):
        """
        Gets the payment methods names in tuple form
        :return: payment methods' names in tuple form
        """
        return tuple(payment.name for payment in cls)

    @classmethod
    def values(cls):
        """
        Gets the payment methods values in tuple form
        :return: payment methods' values in tuple form
        """
        return tuple(payment.value for payment in cls)
