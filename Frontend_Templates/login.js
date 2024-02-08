document.addEventListener("DOMContentLoaded", function() {
    // Attach event listener to the login form submission
    document.getElementById('loginForm').addEventListener('submit', function(event) {
        event.preventDefault();
        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value.trim();
        if (!username || !password) {
            alert("Please fill in all fields.");
            return;
        }
        const isFirstLogin = true; 
        if (isFirstLogin) {
            window.location.href = 'first_time.html';
        } else {
            window.location.href = 'main_page.html';
        }
    });
});
