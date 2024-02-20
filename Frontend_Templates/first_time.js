document.getElementById("emailForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent form submission

    var email = document.getElementById("emailInput").value;

    // Create a FormData object and append the email to it
    var formData = new FormData();
    formData.append('email', email);

    // Send form data to the server using AJAX
    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'save_email.php', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            console.log("Email saved successfully");
            // You can add further handling here (e.g., redirect)
        } else {
            console.error("Error saving email");
        }
    };
    xhr.send(formData);
});

document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent form submission
    window.location.href = "main_page.html";
});
