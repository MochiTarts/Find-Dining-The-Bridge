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
    Credit = 'Credit'
    Debit = 'Debit'
    Cash = 'Cash'

    @classmethod
    def choices(cls):
        """ Get the payment methods in tuple form

        :return: payment methods' in tuple form
        :rtype: tuple
        """
        return tuple((method.name, method.value) for method in cls)

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

class MediaType(Enum):
    """ The types of media a restaurant can upload """
    IMAGE = 'image'
    VIDEO = 'video'

    @classmethod
    def choices(cls):
        """ Gets the choies in tuple form
        :return: Media type name and value in tuple form
        """
        return tuple((media_type.name, media_type.value) for media_type in cls)

class RestaurantSaveLocations(Enum):
    """ The valid locations a restaurant can upload/remove media to/from """
    cover_photo_url = "Cover Photo"
    logo_url = 'Logo'
    restaurant_video_url = 'Restaurant Video'
    restaurant_image_url = 'Restaurant Image'

    @classmethod
    def choices(cls):
        """ Gets the choices in tuple form
        :return: Location name and value in tuple form
        """
        return tuple((location.name, location.value) for location in cls)

class FoodSaveLocations(Enum):
    """ The valid locations a restaurant dish can upload/remove media to/from """
    picture = 'Food Picture'

    @classmethod
    def choices(cls):
        """ Gets the choices in tuple form
        :return: Location name and value in tuple for
        """
        return tuple((location.name, location.value) for location in cls)