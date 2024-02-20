<?php
// Check if the form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Check if email is set and not empty
    if (isset($_POST["email"]) && !empty($_POST["email"])) {
        // Validate and sanitize email
        $email = filter_var($_POST["email"], FILTER_SANITIZE_EMAIL);
        if (filter_var($email, FILTER_VALIDATE_EMAIL)) {
            // Email is valid, save it to JSON file
            $jsonData = json_encode(array("email" => $email));
            file_put_contents("email.json", $jsonData);
            
            // Redirect to main_page.html
            header("Location: main_page.html");
            exit; // Stop further execution
        } else {
            // Invalid email format
            echo "Error: Invalid email format";
        }
    } else {
        // Email is not set or empty
        echo "Error: Email is required";
    }
} else {
    // If the form is not submitted via POST method, redirect back to the form page
    header("Location: first_time.php");
    exit; // Stop further execution
}
?>
