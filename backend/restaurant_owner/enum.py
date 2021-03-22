from enum import Enum

class ConsentStatus(Enum):
    """ The consent status a user can have """
    EXPRESSED = 'Expressed Consent'
    IMPLIED = 'Implied Enquiry'
    EXPIRED = 'Expired'
    UNSUBSCRIBED = 'Unsubscribed'

    @classmethod
    def choices(cls):
        """
        Gets the choices in tuple form
        :return: consent status' name and value in tuple form usable to models
        """
        return tuple((consentStatus.name, consentStatus.value) for consentStatus in cls)
