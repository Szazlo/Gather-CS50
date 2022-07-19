function clipBoard() {
    var copyText = document.getElementById('linker1');
    copyText.select();
    navigator.clipboard.writeText(copyText.value);
}

var OtherOption = document.getElementById("meeting_type");
OtherOption.addEventListener("change", OtherTypeDisplay);

// Reset to the default option upon loading up.
if (OtherOption.value != "Select Type") {
    OtherOption.value = "Select Type";
}

var OtherTypeCounter = document.getElementById("OtherTypeCounter");
// Reset to the default option upon loading up.

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