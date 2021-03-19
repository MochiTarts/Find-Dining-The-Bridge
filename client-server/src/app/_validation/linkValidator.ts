import { formValidator } from "./formValidator"
import { formValidation } from "./forms"

export class linkValidator extends formValidator{

    constructor(){
        super();
        this.errors = {
            'link': '',
            'full_menu_url': '',
        }
    }

    errors = {}

    errorStrings = {
        'link': 'The provided YouTube link is invalid',
        'full_menu_url': 'The provided link is invalid',
    }

    validationFuncs = formValidator.replaceDefaults({
        'link': (link) => formValidation.isYoutubeLinkValid(link),
    })

}