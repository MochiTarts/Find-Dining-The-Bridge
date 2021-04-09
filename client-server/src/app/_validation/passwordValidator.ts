import { formValidator } from "./formValidator"
import { formValidation } from "./forms"

export class passwordValidator extends formValidator{

    constructor(){
        super();
        this.errors = {
            'oldPassword': '',
            'newPassword': '',
            'confirmPassword': '',
        }
    }

    errors = {}

    errorStrings = {
        'oldPassword': 'Invalid Passowrd',
        'newPassword': 'Invalid Passowrd',
        'confirmPassword': 'Invalid Passowrd',
    }

    

    validationFuncs = formValidator.replaceDefaults({
        'oldPassword': (oldPassword) => formValidation.isShorterThan(255, oldPassword, true),
        'newPassword': (newPassword) => formValidation.isShorterThan(255, newPassword, true),
        'confirmPassword': (confirmPassword) => formValidation.isShorterThan(255, confirmPassword, true),
    })

}
