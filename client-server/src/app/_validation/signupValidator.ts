import { formValidator } from "./formValidator"
import { formValidation } from "./forms"

export class signupValidator extends formValidator{
  constructor() {
    super();
    //all errors start off empty
    this.errors = {
        'city': '',
        'profile_created': '',
        'restaurant_name': '',
        'restaurant_phone': '',
        'street_number': '',
        'street_name': '',
        'postalCode': '',
        'province': '',
        'signup_first_name': '',
        'signup_last_name': '',
        'phone': '',
        'email': '',
        'signup_user_role': '',
        'motivation': '',
        'food_type': '',
        'signature_dish': '',
        'popular_dish': '',
        'unique_facts': '',
        'why_scarborough': '',
        'date_opened': '',
        'date_opened_future': '',
        'open_hours': '',
        'offer_options': '',
        'website': '',
        'pronouns': '',
    }
  }

  errors = {}

  errorStrings = {
      'city': 'This field is required',
      'profile_created': 'This field is required',
      'restaurant_name': 'This field is required',
      'restaurant_phone': 'Invalid phone number - ensure exactly 10 digits',
      'street_number': 'Invalid Street Number - ensure your address is in Scarborough',
      'street_name': 'Invalid Street Name - ensure your address is in Scarborough',
      'postalCode': 'Invalid postal code - ensure A#A #A# format and that the postal code entered is in Scarborough',
      'province': 'This field is required - Scarborough is in Ontario',
      'signup_first_name': 'Invalid first name - Name must not contain numbers or symbols',
      'signup_last_name': 'Invalid last name - Name must not contain numbers or symbols',
      'phone': 'Invalid phone number - ensure exactly 10 digits',
      'email': 'Invalid email',
      'signup_user_role': 'Please select at least one job position. If "Other" is checked, please specify the role',
      'motivation': 'This field is required',
      'food_type': 'This field is required',
      'signature_dish': 'This field is required',
      'popular_dish': 'This field is required',
      'unique_facts': 'This field is required',
      'why_scarborough': 'This field is required',
      'date_opened': 'Invalid date - Please enter date in YYYY-MM-DD or YYYY',
      'date_opened_future': 'Invalid date - Please ensure entered date is not a future date',
      'open_hours': 'This field is required',
      'offer_options': 'Please select at least one option. If "Other" is checked, please specify',
      'website': 'Invalid url',
      'pronouns': 'Please select at least one pronoun. If "Other" is checked, please specify'
  }

  validationFuncs = formValidator.replaceDefaults({
      'city': '',
      'profile_created': (profile_created) => formValidation.isBoolean(profile_created),
      'restaurant_name': '',
      'restaurant_phone': (restaurant_phone) => formValidation.isPhoneValid(restaurant_phone),
      'street_number': (street_number) => formValidation.isStreetNumValid(street_number),
      'street_name': '',
      'postalCode': (postalCode) => formValidation.isPostalCodeValid(postalCode),
      'province': '',
      'signup_first_name': (signup_first_name) => formValidation.isNameValid(signup_first_name),
      'signup_last_name': (signup_last_name) => formValidation.isNameValid(signup_last_name),
      'phone': (phone) => formValidation.isOptionalPhoneValid(phone),
      'email': (email) => formValidation.isEmailValid(email),
      'signup_user_role': (signup_user_role) => formValidation.isListValid(signup_user_role),
      'motivation': '',
      'food_type': '',
      'signature_dish': '',
      'popular_dish': (popular_dish) => formValidation.isListNonEmpty(popular_dish),
      'unique_facts': '',
      'why_scarborough': '',
      'date_opened': (date_opened) => formValidation.isBirthdayValid(date_opened),
      'date_opened_future': (date_opened) => formValidation.isOlderThanAge(date_opened, 0),
      'open_hours': '',
      'offer_options': (offer_options) => formValidation.isListValid(offer_options),
      'pronouns': (pronouns) => formValidation.isListValid(pronouns),
  })
}
