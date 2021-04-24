// Materaiize Initializations

document.addEventListener('DOMContentLoaded', function () {
    var elems = document.querySelectorAll('.sidenav');
    var instances = M.Sidenav.init(elems, { edge: "right" });
});

document.addEventListener('DOMContentLoaded', function () {
    var elems = document.querySelectorAll('select');
    var instances = M.FormSelect.init(elems);
});

document.addEventListener('DOMContentLoaded', function () {
    var elems = document.querySelectorAll('.tooltipped');
    var instances = M.Tooltip.init(elems);
});

document.addEventListener('DOMContentLoaded', function () {
    var elems = document.querySelectorAll('.collapsible');
    var instances = M.Collapsible.init(elems);
});

document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.modal');
    var instances = M.Modal.init(elems);
  });

function setPageReload() {
    let msgtxt = document.getElementById("msgtxt")

    // Get the value from the localStorage if there is a value
    let storeText = localStorage.getItem("msgtxt");
    if (storeText !== "") {
        msgtxt.textContent = storeText;
    }
    let timer = setTimeout(function () {
        // Update the localStorage anytime the is a pull
        localStorage.setItem("msgtxt", msgtxt.value);
        location.reload();
    }, 10000);

    // Set the focus
    msgtxt.focus();

    // Move the cursor to the end of the input text
    const len = msgtxt.value.length;
    msgtxt.setSelectionRange(len, len);

    // Get the form element and add a event handler to capture the submit
    // event and clear the input text after submitting the message.
    const chatForm = document.getElementById('chat');
    chatForm.addEventListener("submit", () => {
        localStorage.setItem("msgtxt", "");
    });
}