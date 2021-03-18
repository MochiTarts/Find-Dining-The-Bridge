import { formValidation } from './forms'
export abstract class formValidator{

    // holds the state of the errors
    abstract errors: Object;
    // constant for the error strings
    abstract errorStrings: Object;
    // constant for the functions which validate each form field
    abstract validationFuncs: Object;

    clearAllErrors(){
        Object.keys(this.errors).forEach(
            key => this.clearError(key)
        );
    }

    // replaces all empty strings in a formValidator's validationFuncs object
    // with a function checking if a string is non-empty, for convenience
    static replaceDefaults(validationFuncs: Object){
        Object.keys(validationFuncs).forEach(
            key => {
                if(validationFuncs[key] == ''){
                    validationFuncs[key] =  function(input){ return formValidation.nonEmpty(input)};
                }
        })
        return validationFuncs;
    }

    /** Validates all of the form fields using their functions,
     *  Any time a validation fails, failureCallback runs with 
     *  the argument being the key for which the validation failed
     *  returns false if all of the validations pass, true if one or more fail
     * **/
    validateAll(data: Object, failureCallback: Function): Boolean
    {
        let failFlag = false;
        Object.keys(data).forEach(key => {
            // gets the corresponding validation function from the object in formError and calls it on key
            // if it fails, then it causes the field to error and set the failureFlag
            if(this.validationFuncs.hasOwnProperty(key) && ! this.validationFuncs[key](data[key])){
                failureCallback(key);
                failFlag = true;
            } 
        })
        return failFlag;
    }

    setError(fieldName: string, errorName = fieldName){
        this.errors[fieldName] = this.errorStrings[fieldName];
    }
    clearError(fieldName: string){
        this.errors[fieldName] = '';
    }
}