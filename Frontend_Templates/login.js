document.addEventListener("DOMContentLoaded", function() {
    document.getElementById('loginForm').addEventListener('submit', async function(event) {
        event.preventDefault();
        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value.trim();
        if (!username || !password) {
            alert("Please fill in all fields.");
            return;
        }

        try {
            const authenticationResult = await authenticateUser(username, password);
            if (authenticationResult === true) {
                alert("Authentication successful. Redirecting...");
                const emailExists = await checkEmailExists();
                if (emailExists) {
                    window.location.href = 'main_page.html'; // Redirect to main page
                } else {
                    window.location.href = 'first_time.html'; // Redirect to first time setup
                }
            } else {
                alert("Invalid username or password.");
            }
        } catch (error) {
            console.error('Error during authentication:', error);
            alert("An error occurred during authentication. Please try again later.");
        }
    });
});

async function authenticateUser(username, password) {
    try {
        // Fetch user data from users.json
        const userResponse = await fetch('user.json');
        const userData = await userResponse.json();

        // Check if the provided username and password match any entry
        const user = userData.users.find(user => user.username === username && user.password === password);
        if (!user) {
            throw new Error('Invalid username or password.');
        }

        return true; // Authentication successful
    } catch (error) {
        console.error('Error during authentication:', error);
        return false; // Authentication failed
    }
}

async function checkEmailExists() {
    try {
        // Fetch email data from email.json
        const emailResponse = await fetch('email.json');
        const emailData = await emailResponse.json();

        // Check if email exists
        return !!emailData.email;
    } catch (error) {
        console.error('Error checking email:', error);
        return false;
    }
}
