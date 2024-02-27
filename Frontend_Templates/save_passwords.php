<?php
// Define the path to the localIP.json file and password vault JSON file
$localIPFile = '../Backend_Scripts/localIP.json';
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

// Load updated device data from the request body
$updatedDeviceData = json_decode(file_get_contents('php://input'), true);

// Load data from the localIP.json file
$localIPData = loadJSONData($localIPFile);

// Update the localIP.json file with the updated password information
foreach ($updatedDeviceData as $deviceName => $deviceInfo) {
    if (isset($localIPData[$deviceName])) {
        $localIPData[$deviceName]['password'] = $deviceInfo['password'];
        $localIPData[$deviceName]['passwordChanged'] = true; // Set passwordChanged to true
        $localIPData[$deviceName]['lastPasswordChange'] = date("Y-m-d H:i:s");
    }
}

// Save the updated localIP data
saveJSONData($localIPFile, $localIPData);

// Load data from the password vault JSON file
$passwordVaultData = loadJSONData($passwordVaultFile);

// Update the password for each device in the password vault
foreach ($updatedDeviceData as $deviceName => $deviceInfo) {
    if (isset($passwordVaultData[$deviceName])) {
        $passwordVaultData[$deviceName]['Password'] = $deviceInfo['password'];
        $passwordVaultData[$deviceName]['PasswordChanged'] = true; // Set passwordChanged to true
    }
}

// Save the updated password vault data
saveJSONData($passwordVaultFile, $passwordVaultData);

// Respond with success message
http_response_code(200);
echo json_encode(array('message' => 'Device data updated successfully'));
?>
