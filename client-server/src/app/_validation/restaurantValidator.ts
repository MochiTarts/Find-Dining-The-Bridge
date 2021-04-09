import { formValidator } from "./formValidator"
import { formValidation } from "./forms"

export class restaurantValidator extends formValidator{

    constructor(){
        super();
        this.errors = {
            'name': '',
            'years': '',
            'address': '',
            'streetAddress2': '',
            'streetAddress3': '',
            'phone': '',
            'email': '',
            'pricepoint':'',
            'cuisines':'',
            'offer_options': '',
            'bio': '',
            'postalCode': '',
            'deliveryDetails': '',
            'locationNotes': '',
            'owner_first_name': '',
            'owner_last_name': '',
            'owner_preferred_name': '',
            'open_hours': '',
            'payment_methods': '',

            // for profanity filter
            'name_p': '',
            'owner_first_name_p': '',
            'owner_last_name_p': '',
            'owner_preferred_name_p': '',
            'address_p': '',
            'streetAddress2_p': '',
            'streetAddress3_p': '',
            'deliveryDetails_p': '',
            'dineinPickupDetails_p': '',
            'locationNotes_p': '',
            'bio_p': '',
            'open_hours_p': '',
        }
    }

    errors = {}

    linkerror: string = "link does not exist.";
    profaneError: string = "This field contains profane content.";

    errorStrings = {
        'name': 'Restaurant Name is required, and must be less than 255 characters.',
        'years': 'Invalid Years in Business, ensure it is a non-negative number.',
        'address': 'Invalid Address - ensure the address is in Scarborough.',
        'streetAddress2': 'Invalid Address, must be less than 100 characters.',
        'streetAddress3': 'Invalid Address, must be less than 100 characters.',
        'phone': 'Invalid Phone Number, ensure it contains exactly 10 digits.',
        'email': 'Invalid Email, ensure it follows the name@domain.name format.',
        'pricepoint':'Invalid Price Point, please select one.',
        'cuisines':'Invalid Cuisine, please choose at least one cuisine.',
        'bio': 'Restaurant Story is required, and must be less than 2000 characters.',
        'postalCode': "Invalid postal code - ensure A#A #A# format, and is in Scarborough.",
        'offer_options': "Invalid general serives.",
        'deliveryDetails': "Delivery Details must be less than 2000 characters.",
        'dineinPickupDetails': "Dine-in / Pick-up Details must be less than 2000 characters.",
        'locationNotes': "Location Notes must be less than 2000 characters.",
        'owner_first_name': "Owner First Name cannot be empty and cannot contain numbers or symbols.",
        'owner_last_name': "Owner Last Name cannot be empty and cannot contain numbers or symbols.",
        'owner_preferred_name': "Owner Preferred Name cannot be empty.",
        'open_hours': 'Open Hours is required.',
        'payment_methods': 'Invalid Payment Method, please select at least one method.',

        // for profanity filter
        'name_p': this.profaneError,
        'owner_first_name_p': this.profaneError,
        'owner_last_name_p': this.profaneError,
        'owner_preferred_name_p': this.profaneError,
        'address_p': this.profaneError,
        'streetAddress2_p': this.profaneError,
        'streetAddress3_p': this.profaneError,
        'deliveryDetails_p': this.profaneError,
        'dineinPickupDetails_p': this.profaneError,
        'locationNotes_p': this.profaneError,
        'bio_p': this.profaneError,
        'open_hours_p': this.profaneError,
    }

    validationFuncs = formValidator.replaceDefaults({
        'name': (name) => formValidation.isShorterThan(255, name, true),
        'years': (years) => formValidation.isYearsValid(years),
        'address': (address) => formValidation.isShorterThan(100, address, true),
        'streetAddress2': (address) => formValidation.isShorterThan(100, address, false),
        'streetAddress3': (address) => formValidation.isShorterThan(100, address, false),
        'phone': (phone) => formValidation.isPhoneValid(phone),
        'email': (email) => formValidation.isEmailValid(email),
        'pricepoint': (pricepoint) => formValidation.isPricepointValid(pricepoint),
        'cuisines': (cuisines) => formValidation.isListNonEmpty(cuisines),
        'bio': (bio) => formValidation.isShorterThan(2000, bio, true),
        'postalCode': (postalCode)=> formValidation.isPostalValid(postalCode),
        'deliveryDetails': (deliveryDetails) => formValidation.isShorterThan(2000, deliveryDetails, false),
        'dineinPickupDetails': (dineinPickupDetails) => formValidation.isShorterThan(2000, dineinPickupDetails, false),
        'locationNotes': (locationNotes) => formValidation.isShorterThan(2000, locationNotes, false),
        'owner_first_name': (owner_first_name) => formValidation.isOwnerNamesNonEmpty(owner_first_name),
        'owner_last_name': (owner_last_name) => formValidation.isOwnerNamesNonEmpty(owner_last_name),
        'open_hours': '',
        'payment_methods': (payment_methods) => formValidation.isListNonEmpty(payment_methods),

        // for profanity filter
        'name_p': (name_p) => formValidation.isNotProfane(name_p),
        'owner_first_name_p': (owner_first_name_p) => formValidation.isNotProfane(owner_first_name_p),
        'owner_last_name_p': (owner_last_name_p) => formValidation.isNotProfane(owner_last_name_p),
        'owner_preferred_name_p': (owner_preferred_name_p) => formValidation.isNotProfane(owner_preferred_name_p),
        'address_p': (address_p) => formValidation.isNotProfane(address_p),
        'streetAddress2_p': (streetAddress2_p) => formValidation.isNotProfane(streetAddress2_p),
        'streetAddress3_p': (streetAddress3_p) => formValidation.isNotProfane(streetAddress3_p),
        'deliveryDetails_p': (deliveryDetails_p) => formValidation.isNotProfane(deliveryDetails_p),
        'dineinPickupDetails_p': (dineinPickupDetails_p) => formValidation.isNotProfane(dineinPickupDetails_p),
        'locationNotes_p': (locationNotes_p) => formValidation.isNotProfane(locationNotes_p),
        'bio_p': (bio_p) => formValidation.isNotProfane(bio_p),
        'open_hours_p': (open_hours_p) => formValidation.isNotProfane(open_hours_p),
    })

}
