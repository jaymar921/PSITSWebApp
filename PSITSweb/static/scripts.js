function home(){
   location.href="/PSITS";
}

function createNewEvent(){
    location.href="/PSITS@NewEvent"
}

function studentsInfo(){
    location.href="/PSITS@Students"
}

// PSITS@Event
function requiredPayment(checkbox){
    document.getElementById('item_field').style.display = checkbox.checked ? 'block':'none';
    document.getElementById('amount_field').style.display = checkbox.checked ? 'block':'none';
}

function register(){
    location.href="/PSITS@Register"
}

function onChange() {
  const password = document.querySelector('input[name=password]');
  const confirm = document.querySelector('input[name=confirm]');
  if (confirm.value === password.value) {
    confirm.setCustomValidity('');
  } else {
    confirm.setCustomValidity('Passwords do not match');
  }
}

document.getElementById("Date").valueAsDate = new Date()