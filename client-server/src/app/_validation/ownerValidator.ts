import { formValidator } from "./formValidator"
import { formValidation } from "./forms"

export class ownerValidator extends formValidator{

    constructor(){
        super();
        this.errors = {
            'owner_name': '',
            'owner_story': ''
        }
    }

    errors = {}

    errorStrings = {
        'owner_name': 'Invalid Owner Name',
        'owner_story': 'Invalid Owner Story'
    }

    validationFuncs = formValidator.replaceDefaults({
        'owner_name': (owner_name) => formValidation.isShorterThan(255, owner_name, true),
        'owner_story': (owner_story) => formValidation.isShorterThan(2000, owner_story, true),
    })

}
