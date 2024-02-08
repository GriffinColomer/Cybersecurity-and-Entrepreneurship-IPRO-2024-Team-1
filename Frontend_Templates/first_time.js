// Define a function to handle first-time setup form submission
function handleFirstTimeSetup() {
    document.getElementById('emailForm').addEventListener('submit', function(event) {
        event.preventDefault(); 
        const email = document.getElementById('emailInput').value;
        console.log('Email submitted:', email); 
        window.location.href = 'main_page.html';
    });
}

// Call the function to handle first-time setup on DOMContentLoaded event
document.addEventListener('DOMContentLoaded', function() {
    handleFirstTimeSetup();
});
