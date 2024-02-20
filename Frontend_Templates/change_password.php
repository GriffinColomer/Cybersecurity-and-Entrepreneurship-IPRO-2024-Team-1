<?php
// Define the path to the localIP.json file and password vault JSON file
$localIPFile = '..\Backend_Scripts\localIP.json';
$passwordVaultFile = 'password_vault.json';

// Function to load data from a JSON file
function loadJSONData($filePath) {
    if (file_exists($filePath)) {
        $jsonContent = file_get_contents($filePath);
        return json_decode($jsonContent, true);
    } else {
        return array(); // Return an empty array if the file doesn't exist yet
    }
}

// Function to save data to a JSON file
function saveJSONData($filePath, $data) {
    $jsonContent = json_encode($data, JSON_PRETTY_PRINT);
    file_put_contents($filePath, $jsonContent);
}

// Load data from the localIP.json file
$localIPData = loadJSONData($localIPFile);

// Load data from the password vault JSON file
$passwordVaultData = loadJSONData($passwordVaultFile);

// Get the device name from the request body
$requestBody = file_get_contents('php://input');
$requestData = json_decode($requestBody, true);
$deviceName = isset($requestData['deviceName']) ? $requestData['deviceName'] : '';

// Check if the device is flagged
if (isset($localIPData[$deviceName]) && $localIPData[$deviceName]['flagged']) {
    // Generate a random password for the flagged device
    $randomPassword = generateRandomPassword();
    
    // Update localIP.json with the new password information
    $localIPData[$deviceName]['password'] = $randomPassword;
    $localIPData[$deviceName]['passwordChanged'] = true;
    $localIPData[$deviceName]['lastPasswordChange'] = date("Y-m-d H:i:s");
    $localIPData[$deviceName]['flagged'] = false;
    saveJSONData($localIPFile, $localIPData);

    // Update password_vault.json with the new password information
    if (isset($passwordVaultData[$deviceName])) {
        $passwordVaultData[$deviceName]['Password'] = $randomPassword;
        $passwordVaultData[$deviceName]['PasswordChanged'] = true;
    } else {
        $passwordVaultData[$deviceName] = array(
            'DeviceName' => $deviceName,
            'Company' => $localIPData[$deviceName]['Company'],
            'Username' => 'admin',
            'Password' => $randomPassword,
            'PasswordChanged' => true,
            'flagged' => false
        );
    }
    saveJSONData($passwordVaultFile, $passwordVaultData);

    // Respond with success message
    http_response_code(200);
    echo json_encode(array('message' => 'Password changed successfully'));
} else {
    // Respond with error message if the device is not flagged or does not exist
    http_response_code(400);
    echo json_encode(array('error' => 'Device not flagged or does not exist'));
}

// Function to generate a random password
function generateRandomPassword($length = 12) {
    return substr(str_replace(['+', '/', '='], '', base64_encode(random_bytes($length))), 0, $length);
}
?>
