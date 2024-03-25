<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $data = json_decode(file_get_contents("php://input"), true);
    $ip = $data["ip"];

    // Log the received IP address
    error_log("Received IP address: " . $ip);

    // Execute the Python script with the IP address as an argument
    $command = "sudo python ../Backend_Scripts/passwordReset.py " . escapeshellarg($ip);
    $output = shell_exec($command);

    // Log the output from the Python script
    error_log("Python script output: " . $output);

    // Decode the JSON output from the Python script
    $result = json_decode($output, true);

    // Store the new password in a JSON file
    $passwords = [];
    if (file_exists('passwords.json')) {
        $passwords = json_decode(file_get_contents('auto_saved_passwords.json'), true);
    }
    $passwords[$ip] = $result['new_password'];
    file_put_contents('passwords.json', json_encode($passwords, JSON_PRETTY_PRINT));

    // Log the stored password
    error_log("Stored password for IP " . $ip . ": " . $result['new_password']);

    // Return the result as JSON response
    header('Content-Type: application/json');
    echo json_encode($result);
}
?>