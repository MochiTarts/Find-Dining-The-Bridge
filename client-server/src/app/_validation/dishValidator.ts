import { formValidator } from "./formValidator"
import { formValidation } from "./forms"
export class dishValidator extends formValidator{
    
    constructor(){
        super();
        this.errors = {
            'name': '',
            'description': '',
            'price': '',
            'cuisine': '',
            'allergy': '',
            'menuCategory': ''
        }
    }

    errors = {}

    errorStrings = {
        'name': 'Invalid Name',
        'description': 'Invalid Description, make sure it is less than 200 characters',
        'price':"Invalid Price, make sure it is a positve number",
        'cuisine': 'Invalid Cuisine',
        'allergy': 'Invalid Allergy',
        'menuCategory': 'Invalid Menu Category'
    }

    validationFuncs = formValidator.replaceDefaults({
        'name': '',
        'description': (description) => formValidation.isShorterThan(200, description, true),
        'price': (price) => formValidation.isNumberValid(price) && Number(price) > 0,
        'cuisine': '',
        'allergy': '',
        'menuCategory': ''
    });

}