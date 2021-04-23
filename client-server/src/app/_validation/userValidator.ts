import { formValidator } from "./formValidator"
import { formValidation } from "./forms"
export class userValidator extends formValidator {

  constructor() {
    super();
    //all errors start off empty
    this.errors = {
      'first_name': '',
      'last_name': '',
      'postalCode': '',
      'phone': '',
      'phone_ext': '',

      // for profanity filter
      'first_name_p': '',
      'last_name_p': '',
    }
  }

  errors = {}

  profaneError: string = "This field contains profane content.";

  errorStrings = {
    'first_name': 'Invalid First Name - name should not contain numbers or symbols',
    'last_name': 'Invalid Last Name - name should not contain numbers or symbols',
    'postalCode': 'Invalid Postal Code - ensure this postal code does exist and A#A #A# format',
    'phone': 'Invalid phone number - ensure exactly 10 digits',
    'phone_ext': 'Invalid phone extension',

    // for profanity filter
    'first_name_p': this.profaneError,
    'last_name_p': this.profaneError,
  }
  // age checks if the date is invalid, then don't throw an error, because birthday will throw an error
  validationFuncs = formValidator.replaceDefaults({
    'first_name': '',
    'last_name': '',
    'postalCode': (postalCode) => formValidation.isPostalCodeValid(postalCode),
    'phone': (phone) => formValidation.isPhoneValid(phone),
    'phone_ext': (phone_ext) => formValidation.isOptionalNumberNonNegative(phone_ext),

    // for profanity filter
    'first_name_p': (first_name_p) => formValidation.isNotProfane(first_name_p),
    'last_name_p': (last_name_p) => formValidation.isNotProfane(last_name_p),
  })
}
