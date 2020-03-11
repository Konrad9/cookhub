var usernameField = document.getElementById("id_username");
var passwordField = document.getElementById("id_password");
var passwordRepeatField = document.getElementById("id_password2");
var usernameFine = true;
var passwordFine = false;
var passwordRepFine = false;
var passwordWarnings = {"lower":"<li>At least one lowercase letter<li/>",
             "upper": "<li>At least one uppercase letter<li/>",
             "numbers": "<li>At least one number<li/>",
             "length": "<li>At least 8 characters<li/>"}
             

setInterval(registerFine, 10);

usernameField.onkeyup = function () {
    }

function checkPasswordRepetition() {
    if(passwordField.value==passwordRepeatField.value) {
        document.getElementById("password_repetition").textContent = "";
        passwordRepFine = true;
    }
    else {
        document.getElementById("password_repetition").textContent = "Does not match with password\n";
        passwordRepFine = false;
    }
}

function registerFine() {
    if (usernameFine && passwordFine && passwordRepFine) {
        document.getElementById("password_validate").disabled = false;
    }
    else {
        document.getElementById("password_validate").disabled = true;
    }
}


var letter = document.getElementById("letter");
var capital = document.getElementById("capital");
var number = document.getElementById("number");
var length = document.getElementById("length");

// When the user clicks on the password field, show the message box
passwordField.onfocus = function() {
  document.getElementById("message").style.display = "block";
}

// When the user clicks outside of the password field, hide the message box
passwordField.onblur = function() {
  document.getElementById("message").style.display = "none";
}

// When the user starts to type something inside the password field
passwordField.onkeyup = function() {
  // Validate lowercase letters
  var lowerCaseLetters = /[a-z]/g;
  if(passwordField.value.match(lowerCaseLetters)) {  
    letter.classList.remove("invalid");
    letter.classList.add("valid");
    passwordFine = true;
  } else {
    letter.classList.remove("valid");
    letter.classList.add("invalid");
    passwordFine = false;
  }
  
  // Validate capital letters
  var upperCaseLetters = /[A-Z]/g;
  if(passwordField.value.match(upperCaseLetters)) {  
    capital.classList.remove("invalid");
    capital.classList.add("valid");
    passwordFine = true;
  } else {
    capital.classList.remove("valid");
    capital.classList.add("invalid");
    passwordFine = false;
  }

  // Validate numbers
  var numbers = /[0-9]/g;
  if(passwordField.value.match(numbers)) {  
    number.classList.remove("invalid");
    number.classList.add("valid");
    passwordFine = true;
  } else {
    number.classList.remove("valid");
    number.classList.add("invalid");
  }
  
  // Validate length
  if(passwordField.value.length >= 8) {
    length.classList.remove("invalid");
    length.classList.add("valid");
    passwordFine = true;
  } else {
    length.classList.remove("valid");
    length.classList.add("invalid");
    passwordFine = false;
  }
}