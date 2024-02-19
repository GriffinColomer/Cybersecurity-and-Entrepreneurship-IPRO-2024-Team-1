<?php
// Define the path to the localIP.json file and password vault JSON file
$localIPFile = '..\Backend_Scripts\localIP.json';
$passwordVaultFile = 'password_vault.json';

// Function to load data from the localIP.json file
function loadLocalIPData() {
    global $localIPFile;
    if (file_exists($localIPFile)) {
        $jsonContent = file_get_contents($localIPFile);
        return json_decode($jsonContent, true);
    } else {
        return array(); // Return an empty array if the file doesn't exist yet
    }
}

// Function to load the password vault data from the JSON file
function loadPasswordVault() {
    global $passwordVaultFile;
    if (file_exists($passwordVaultFile)) {
        $jsonContent = file_get_contents($passwordVaultFile);
        return json_decode($jsonContent, true);
    } else {
        return array(); // Return an empty array if the file doesn't exist yet
    }
}

// Function to save the password vault data to the JSON file
function savePasswordVault($passwordVaultData) {
    global $passwordVaultFile;
    $jsonContent = json_encode($passwordVaultData, JSON_PRETTY_PRINT);
    file_put_contents($passwordVaultFile, $jsonContent);
}

// Load data from the localIP.json file
$localIPData = loadLocalIPData();

// Initialize an empty password vault
$passwordVault = array();

// Populate the password vault based on data from localIP.json
foreach ($localIPData as $deviceName => $deviceInfo) {
    // Check if the password has been changed
    $passwordChanged = isset($deviceInfo['passwordChanged']) ? $deviceInfo['passwordChanged'] : false;

    // Set the password to blank if it hasn't been changed
    $password = $passwordChanged ? $deviceInfo['password'] : '';

    // Add the device to the password vault with username as "admin"
    $passwordVault[$deviceName] = array(
        'Company' => $deviceInfo['Company'],
        'Username' => 'admin',
        'Password' => $password,
        'PasswordChanged' => $passwordChanged,
        'flagged' => $deviceInfo['flagged']
    );
}

// Save the password vault data
savePasswordVault($passwordVault);
?>