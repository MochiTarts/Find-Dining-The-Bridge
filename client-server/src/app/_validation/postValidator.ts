import { formValidator } from "./formValidator"
import { formValidation } from "./forms"

export class postValidator extends formValidator{

    constructor(){
        super();
        this.errors = {
            'content': '',
            'is_profane': '',
        }
    }

    errors = {}

    errorStrings = {
        'content': 'The post should not be empty and must be less than 4096 characters',
        'is_profane': 'The post contains profane content'
    }

    validationFuncs = formValidator.replaceDefaults({
        'content': (content) => formValidation.isShorterThan(4096, content, true),
        'is_profane': (is_profane) => formValidation.isNotProfane(is_profane),
    })

}
