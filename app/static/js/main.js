document.addEventListener("DOMContentLoaded", function () {
    console.log("hello");
})

function validFName() {
    var fn = document.getElementById('fname').value;
    var check = /^[a-zA-Z ]+$/;
    if (fn.match(check)) {
        document.getElementById('fname').style.borderColor = "black";
        document.getElementById('fnameError').innerHTML = "";
        document.getElementById('fnameError').style.display = none;
    }
    else if (fn.length == 0) {
        document.getElementById('fname').style.borderColor = "red";
        document.getElementById('fnameError').innerHTML = "Please type in your first name.";
        document.getElementById('fnameError').style.visibility = "visible";
    }
    else {
        document.getElementById('fname').style.borderColor = "red";
        document.getElementById('fnameError').innerHTML = "First Name can only contain letters.";
        document.getElementById('fnameError').style.visibility = "visible";
    }
}

function validLName() {
    var ln = document.getElementById('lname').value;
    var check = /^[a-zA-Z ]+$/;
    if (ln.match(check)) {
        document.getElementById('lname').style.borderColor = "black";
        document.getElementById('lnameError').innerHTML = "";
        document.getElementById('lnameError').style.display = none;
    }
    else if (ln.length == 0) {
        document.getElementById('lname').style.borderColor = "red";
        document.getElementById('lnameError').innerHTML = "Please type in your last name.";
        document.getElementById('lnameError').style.visibility = "visible";
    }
    else {
        document.getElementById('lname').style.borderColor = "red";
        document.getElementById('lnameError').innerHTML = "Last Name can only contain letters.";
        document.getElementById('lnameError').style.visibility = "visible";
    }
}

function validUser() {
    var un = document.getElementById('user').value;
    var check = /^[0-9a-zA-Z_ ]+$/;
    if (un.match(check)) {
        document.getElementById('user').style.borderColor = "black";
        document.getElementById('userError').innerHTML = "";
        document.getElementById('userError').style.display = none;
    }
    else if (un.length == 0) {
        document.getElementById('user').style.borderColor = "red";
        document.getElementById('userError').innerHTML = "Please type in your username.";
        document.getElementById('userError').style.visibility = "visible";
    }
    else {
        document.getElementById('user').style.borderColor = "red";
        document.getElementById('userError').innerHTML = "Username can only contain letters, numbers, and/or underscores ( _ ).";
        document.getElementById('userError').style.visibility = "visible";
    }
}

function validEmail() {
    var mail = document.getElementById('email').value;
    var check = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    if (mail.match(check)) {
        document.getElementById('email').style.borderColor = "black";
        document.getElementById('emailError').innerHTML = "";
        document.getElementById('emailError').style.display = none;
    }
    else if (mail.length == 0) {
        document.getElementById('email').style.borderColor = "red";
        document.getElementById('emailError').innerHTML = "Please type in your email.";
        document.getElementById('emailError').style.visibility = "visible";
    }
    else {
        document.getElementById('email').style.borderColor = "red";
        document.getElementById('emailError').innerHTML = "Incorrect email format.";
        document.getElementById('emailError').style.visibility = "visible";
    }
}

function validPass() {
    var pass = document.getElementById('password').value;
    var check = /^[0-9a-zA-Z!@#$%^&*()]+$/;
    if (pass.length >= 8 && pass.match(check)) {
        document.getElementById('password').style.borderColor = "black";
        document.getElementById('passError').innerHTML = "";
        document.getElementById('passError').style.display = none;
    }
    else if (pass.length == 0) {
        document.getElementById('password').style.borderColor = "red";
        document.getElementById('passError').innerHTML = "Please type in your password.";
        document.getElementById('passError').style.visibility = "visible";
    }
    else if (pass.length < 8 && !pass.match(check)) {
        document.getElementById('password').style.borderColor = "red";
        document.getElementById('passError').innerHTML = "Password must contain at least 8 characters and can only have these symbols: !@#$%^&*( )";
        document.getElementById('passError').style.visibility = "visible";
    }
    else if (pass.length < 8) {
        document.getElementById('password').style.borderColor = "red";
        document.getElementById('passError').innerHTML = "Password must contain at least 8 characters.";
        document.getElementById('passError').style.visibility = "visible";
    }
    else {
        document.getElementById('password').style.borderColor = "red";
        document.getElementById('passError').innerHTML = "Password can only have these symbols: !@#$%^&*( )";
        document.getElementById('passError').style.visibility = "visible";
    }
}

function validConfirmPass() {
    var confirmPass = document.getElementById('confirmPassword').value;
    var pass = document.getElementById('password').value;
    if (confirmPass == pass) {
        document.getElementById('confirmPassword').style.borderColor = "black";
        document.getElementById('confirmError').innerHTML = "";
        document.getElementById('confirmError').style.display = none;
    }
    else {
        document.getElementById('confirmPassword').style.borderColor = "red";
        document.getElementById('confirmError').innerHTML = "Password do not match.";
        document.getElementById('confirmError').style.visibility = "visible";
    }
}