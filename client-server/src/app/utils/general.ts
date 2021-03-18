export class generalUtils {
    static shortenID(objectID: string): string {
        return objectID.slice(-6);
    }
    static generatePassword(email) {
        const upperChar: Array<string> = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'];
        const lowerChar: Array<string> = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'];
        const symbol: Array<string> = ['#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=', '|', '}', ']', '{', '[', '~', ':', ';', '?', '/', '>', '.', '<', '!', '@'];
        const digit: Array<string> = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];

        var getRand = function (array: Array<string>) {
            return array[Math.floor(Math.random() * array.length)];
        }
        // randomly take one char from the username of the email
        var password:string = email.split("@")[0];
        password = password[Math.floor(Math.random() * password.length)]
        // length range from 8 to 12
        var passwordLen:number = 8 + Math.floor(Math.random() * 4);

        // have at least one from each category
        password = password.concat(getRand(upperChar));
        password = password.concat(getRand(lowerChar));
        password = password.concat(getRand(symbol));
        password = password.concat(getRand(digit));

        var r:number;
        // rangomly fill up the password
        for (var i = 1; i < passwordLen - 5; i++) {
            r = Math.floor(Math.random() * 4);
            switch (r) {
                case 0:
                    password = password.concat(getRand(upperChar)); 
                    break;
                case 1:
                    password = password.concat(getRand(lowerChar));
                    break;
                case 2:
                    password = password.concat(getRand(symbol));
                    break;
                case 3:
                default:
                    password = password.concat(getRand(digit));
            }
        }

        // return the password (shaffled)
        return password.split('').sort(function () {
            return 0.5 - Math.random()
        }).join('');
    }
}
