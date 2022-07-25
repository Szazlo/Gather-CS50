function clipBoard() {
    var copyText = document.getElementById('linker1');
    copyText.select();
    navigator.clipboard.writeText(copyText.value);
}

var OtherOption = document.getElementById('meeting_type');
OtherOption.addEventListener('change', OtherTypeDisplay);
var dateType = document.getElementById('meeting_dateType');
dateType.addEventListener("change", meetingDateTypeDisplay);
var meetingPublic = document.getElementById('meeting_public');
meetingPublic.addEventListener("change", meetingPassword);
// Reset to the default option upon loading up.
if (OtherOption.value != "Select Type") {
    OtherOption.value = "Select Type";
}


if (dateType.value == "Set by me") {
    document.getElementById("meetingSetDate").classList.add("show");
}

if (meetingPublic.value == "y") {
    document.getElementById("meetingPassword").classList.add("show");
}

function OtherTypeDisplay() {
    // If user selects "Other" option, display input box
    let x = document.getElementById("OtherType");
    if (OtherOption.value === "Other") {
        x.classList.add("show");
    }
    else {
        x.classList.remove("show");
        document.getElementById("meeting_typeOther").value = "";
        OtherTypeCounter.innerHTML = "Characters left: 20";
        OtherTypeCounter.style.color = "green";
    }
}


function OtherTypeInput() {
    // If user enters text in input box, display counter
    let text = document.getElementById("meeting_typeOther").value;
 
    OtherTypeCounter.innerHTML = "Characters left: " + (20 - text.length);
    
    if (text.length > 19) {
        // If character limit has been reached, change to red.
        OtherTypeCounter.style.color = "red";
    }
    else {
        OtherTypeCounter.style.color = "green";
    }
}

// Function to hide and show meeting date types etc.
function meetingDateTypeDisplay() {
    let y = document.getElementById("meetingSetDate");
    let z = document.getElementById("meetingAllowDate");

    if (dateType.value == "Set by me") {
        y.classList.add("show");
        z.classList.remove("show");
    }
    else {
        y.classList.remove("show");
        z.classList.add("show");

    }
}

function meetingPassword() {
    let x = document.getElementById("meetingPassword");
    if (meetingPublic.checked == false) {
        x.classList.add("show");
    }
    else {
        x.classList.remove("show");
        document.getElementById("meeting_password").value = "";
    }
}

window.addEventListener("load", function(){
    var toggle  = document.getElementById('togglePassword');
    var x = document.getElementById('{{form.password.id}}');
    var con = document.getElementById('{{form.confirmPassword.id}}');
    toggle.addEventListener('click', function() {
        if (toggle.className === 'far fa-eye') {
            toggle.className = 'fa-eye-slash';
        } else {
            toggle.className = 'far fa-eye';
        }
        if(x.type === 'password') {
            x.type = 'text'; 
            con.type = 'text';
        } else {
            x.type = 'password';
            con.type = 'password';
        }
    });
});