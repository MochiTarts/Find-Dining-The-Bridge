import { formValidator } from "./formValidator"
import { formValidation } from "./forms"
export class userValidator extends formValidator{

    constructor() {
        super();
        //all errors start off empty
        this.errors = {
            'first_name': '',
            'last_name': '',
            'postalCode': '',
            'phone': '',
        }
    }

    errors = {}

    errorStrings = {
        'first_name': 'Invalid First Name - name should not contain numbers or symbols',
        'last_name': 'Invalid Last Name - name should not contain numbers or symbols',
        'postalCode': 'Invalid Postal Code - ensure A#A #A# format',
        'phone': 'Invalid phone number - ensure exactly 10 digits',
    }
    // age checks if the date is invalid, then don't throw an error, because birthday will throw an error
    validationFuncs = formValidator.replaceDefaults({
        'first_name': '',
        'last_name': '',
        'postalCode': (postalCode) => formValidation.isPostalCodeValid(postalCode),
        'phone': (phone) => formValidation.isPhoneValid(phone),
    })
}
