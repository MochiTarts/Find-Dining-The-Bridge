import { formValidator } from "./formValidator"
import { formValidation } from "./forms"

export class newsletterValidator extends formValidator{
  constructor() {
    super();
    //all errors start off empty
    this.errors = {
        'first_name': '',
        'last_name': '',
        'email': ''
    }
  }

  errors = {}

  errorStrings = {
      'first_name': 'Invalid first name - name should not contain numbers or symbols',
      'last_name': 'Invalid last name - name should not contain numbers or symbols',
      'email': 'Invalid email'
  }

  validationFuncs = formValidator.replaceDefaults({
      'first_name': '',
      'last_name': '',
      'email': (email) => formValidation.isEmailValid(email)
  })
}
