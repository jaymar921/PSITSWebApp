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

if(document.getElementById("Date") != null){
    document.getElementById("Date").valueAsDate = new Date()
}


function search_student(){
    var input = document.getElementById("search_student")
    if(input != null)
        location.href="/PSITS@Students/"+input.value+"";
}

function edit_studentInfo(uid){
    if(document.getElementById(uid+"idno").disabled == true){
        document.getElementById(uid+"rfid").disabled=false;
        document.getElementById(uid+"lastname").disabled=false;
        document.getElementById(uid+"firstname").disabled=false;
        document.getElementById(uid+"course").disabled=false;
        document.getElementById(uid+"year").disabled=false;
        document.getElementById(uid+"edit").style.display='none';
        document.getElementById(uid+"button").hidden=false;
    }else{
        document.getElementById(uid+"rfid").disabled=true;
        document.getElementById(uid+"lastname").disabled=true;
        document.getElementById(uid+"firstname").disabled=true;
        document.getElementById(uid+"course").disabled=true;
        document.getElementById(uid+"year").disabled=true;
        document.getElementById(uid+"edit").style.display='block';
    }

}

function deleteStudent(uid){
    if(confirm("Are you sure you want to delete id["+uid+"]?") === true){
        location.href="/PSITS@StudentRemove/"+uid;
    }
}

function showEvents(){
    location.href="/PSITS@Events"
}