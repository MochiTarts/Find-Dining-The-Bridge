export class formValidation {

  static RESPONSE_INVALID: string = "Invalid"
  static MS_PER_DAY = 1000 * 60 * 60 * 24;
  static DAYS_PER_YEAR = 365.2422;
  static YOUNGEST_VALID_AGE = 18;

  static VALID_PRICE_POINTS: Set<string> = new Set<string>(['LOW', 'MID', 'HIGH', 'EXHIGH'])

  static EMAIL_VALIDATION_REGEX = /^(([^<>()\[\]\.,;:\s@\"]+(\.[^<>()\[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
  static YYYYMMDD_REGEX = '^\\d{4}-\\d{2}-\\d{2}$';
  static POSTAL_CODE_REGEX = new RegExp(/^[A-Z]\d[A-Z][ ]\d[A-Z]\d$/);
  static ADDRESS_REGEX = new RegExp(/^([0-9]+[ ])[a-zA-Z .'-]+(, Unit [0-9]+)?$/);
  static YOUTUBE_LINK_REGEX = new RegExp(/^(?:https?:\/\/)?(?:m\.|www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))((\w|-){11})(?:\S+)?$/);
  static NAME_REGEX = new RegExp(/^[^±!@£$%^&*_+§¡€#¢§¶•ªº«\\/<>?:;|=.,0-9]{1,40}$/);

  static isBirthdayValid(birthday: string) {
    return birthday != null && birthday.match(formValidation.YYYYMMDD_REGEX);
  }
  // gives the difference calculated as abs(Date1-Date2) in years
  static ageDifference(Date1: string, Date2: string) {
    let First = new Date(Date1);
    let Second = new Date(Date2);
    let diffMs = First.getTime() - Second.getTime();
    return diffMs / (formValidation.MS_PER_DAY * formValidation.DAYS_PER_YEAR);
  }
  // current date in YYYY-MM-DD format
  static currentDate() {
    let today = new Date();
    let currentDate = (today.getFullYear()).toString().padStart(4, '0') + "-" +
      (today.getMonth() + 1).toString().padStart(2, '0') + "-" +
      today.getDate().toString().padStart(2, '0');
    return currentDate;
  }

  static isOlderThanAge(birthday: string, age: number) {
    // debugging print
    let currentAge = formValidation.ageDifference(formValidation.currentDate(), birthday);
    return currentAge >= age;
  }

  static isPricepointValid(pricepoint: string) {
    return formValidation.VALID_PRICE_POINTS.has(pricepoint);
  }

  static isEmailValid(email: string) {
    // credit: found at https://stackoverflow.com/questions/46155/how-to-validate-an-email-address-in-javascript
    return email != null && email != '' && formValidation.EMAIL_VALIDATION_REGEX.test(email.toLowerCase());
  }

  static isAddressValid(address: string) {
    return address != null && address != '' && formValidation.ADDRESS_REGEX.test(address);
  }

  static isOptionalAddressValid(address: string) {
    if (address == '') {
      return true;
    } else {
      return this.isAddressValid(address);
    }
  }

  static isPhoneValid(phone: string) {
    return phone != null && phone.length == 10 && !isNaN(Number(phone));
  }

  static isOptionalPhoneValid(phone: string) {
    if (phone == '') {
      return true;
    } else {
      return this.isPhoneValid(phone);
    }
  }

  static isPostalCodeValid(postalcode: string) {
    return postalcode != null && postalcode != '' && formValidation.POSTAL_CODE_REGEX.test(postalcode);
  }

  static isCityValid(city: string) {
    return city == 'Scarborough';
  }

  static isStreetNumValid(num: string) {
    return num != null && num.length > 0 && !isNaN(Number(num));
  }

  static isInvalidResponse(data: JSON) {
    return data.hasOwnProperty(formValidation.RESPONSE_INVALID);
  }

  static HandleInvalid(data: JSON, errorFunc: Function) {
    data[formValidation.RESPONSE_INVALID].forEach(element => {
      errorFunc(element);
    });
  }

  static isNumberValid(num: string) {
    return formValidation.nonEmpty(num) && !isNaN(Number(num));
  }

  static isNumerNonNegative(num: string) {
    return this.isNumberValid(num) && Number(num) >= 0;
  }

  static isOptionalNumerNonNegative(num: string) {
    return num ? this.isNumerNonNegative(num) : true;
  }

  static isPostalValid(postal: string) {
    return postal != null && postal != '' && formValidation.POSTAL_CODE_REGEX.test(postal);
  }

  static isShorterThan(length: number, value: string, empty_check: boolean) {
    if (empty_check) {
      return formValidation.nonEmpty(value) && value.length <= length;
    } else {
      return value.length <= length;
    }
  }

  static isListNonEmpty(l: Array<String>) {
    return l.length > 0;
  }

  static isListValid(roles: Array<String>) {
    return this.isListNonEmpty(roles) && !roles.includes('');
  }

  static isOwnerNamesNonEmpty(list: Array<String>) {
    return list.indexOf('') < 0;
  }

  static isYearsValid(years: any) {
    return years != '' && years >= 0;
  }

  static nonEmpty(s: string) {
    return s != '';
  }
  static isDefined(obj: any) {
    return obj != undefined;
  }

  static isYoutubeLinkValid(link: string) {
    return link != null && link != '' && formValidation.YOUTUBE_LINK_REGEX.test(link);
  }

  static isBoolean(bool: any) {
    return typeof (bool) === "boolean";
  }

  static isNameValid(name: string) {
    return name != null && name != '' && formValidation.NAME_REGEX.test(name);
  }

  static isNotProfane(content: string) {
    var Filter = require('bad-words'), filter = new Filter();
    return !filter.isProfane(content);
  }
}
