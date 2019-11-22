function validNum() {
    var number = document.getElementById('num').value;
    var check = /^[0-9]+$/;
    if (number.match(check) || number.length == 0) {
        document.getElementById('num').style.borderColor = "black";
        document.getElementById('numError').innerHTML = "";
        document.getElementById('numError').style.display = none;
    }
    else {
        document.getElementById('num').style.borderColor = "red";
        document.getElementById('numError').innerHTML = "Please enter a number. If no requirements, leave it blank.";
        document.getElementById('numError').style.visibility = "visible";
    }
}