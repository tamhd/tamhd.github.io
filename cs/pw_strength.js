// alert("Hello");
/** This is the main function to check if a password is strong or weak 
 * It implement a vanilla version of password security check on a standalone 
 * piece of string. 
 * 2021.05.31: Implement https://m.workplace.com/help/work/229045974183406
*/

/**
 * The list of all strength levels
 */
const PasswordStrengthLevel = {
    WEAK: "weak",
    STRONG: "strong",
}

/**
 * This function is called from the main page
 * @returns an alert showing the result
 */
function showLog() {
    var pw = document.getElementById("your_pw").value;
    let pm = new PasswordManager(pw);
    alert("Your password, " + pw + ", is " + pm.evaluate());
    return;  
}

class PasswordManager {
    constructor(pw_value) {
        this.password = pw_value;
    }

    /**
     * evaluate the security of the password
     * @returns PasswordStrengthLevel
     */
    evaluate() {
        if (!this.isLongEnough()) {
            return PasswordStrengthLevel.WEAK;   
        } 
        if (!this.hasCaseSensitiveAndDigit()) {
            return PasswordStrengthLevel.WEAK; 
        }
        if (!this.hasSpecialCharacter()) {
            return PasswordStrengthLevel.WEAK;
        }
        return PasswordStrengthLevel.STRONG;    
    }

    /**
     * If the password is longer than 8 characters
     * @returns true, otherwise false
     */
    isLongEnough(){
        if (this.password.length >= 8) {
            return true;
        }
        return false;
    }

    /**
     * If the password contains
     * 1. at least 1 lower case
     * 2. at least 1 upper case
     * 3. at least 1 digit
     * @returns true, otherwise false
     */
    hasCaseSensitiveAndDigit() {
        const regex = /^(?=.*[A-Za-z])(?=.*[0-9]).{1,}$/;
        return regex.test(this.password);
    }
    /**
     * If the password contains at least 1 special character
     * @returns true, otherwise false
     */
    hasSpecialCharacter() {
        const regex = /^(?=.*?[#?!@$%^&*-]).{1,}$/;
        return regex.test(this.password);
    }

}