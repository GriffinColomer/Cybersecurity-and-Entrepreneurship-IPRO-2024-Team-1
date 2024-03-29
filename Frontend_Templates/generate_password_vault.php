<?php

// Define the path to the localIP.json file and password vault JSON file
$localIPFile =  "../Backend_Scripts/localIP.json";
$passwordVaultFile = "password_vault.json";
$DatabaseFile = "login_data.json";
$passwordFile = "../../passwords";

// Function to read MAC addresses and passwords from a file
function readPasswordsFromFile($filename) {
    $macPasswords = [];
    $file = fopen($filename, "r");
    if ($file) {
        while (($line = fgets($file)) !== false) {
            $parts = explode(",", $line);
            if (count($parts) == 2) {
                $macPassword = explode(",", $line);
                $macAddress = trim($macPassword[0]);
                $password = trim($macPassword[1]);
                $macPasswords[$macAddress] = $password;
            }
        }
        fclose($file);
    } else {
        echo "Error reading file.";
    }
    return $macPasswords;
}

// Function to load data from the localIP.json file
function loadLocalIPData() {
    global $localIPFile;
    if (file_exists($localIPFile)) {
        $jsonContent = file_get_contents($localIPFile);
        return json_decode($jsonContent, true);
    } else {
        echo "localIP.json file not found.";
        return array();
    }
}

// Function to load the login data from the JSON file
function loadLoginData() {
    global $DatabaseFile;
    if (file_exists($DatabaseFile)) {
        $jsonContent = file_get_contents($DatabaseFile);
        return json_decode($jsonContent, true);
    } else {
        echo "login_data.json file not found.";
        return array();
    }
}

// Function to load the password vault data from the JSON file
function loadPasswordVault() {
    global $passwordVaultFile;
    if (file_exists($passwordVaultFile)) {
        $jsonContent = file_get_contents($passwordVaultFile);
        return json_decode($jsonContent, true);
    } else {
        echo "password_vault.json file not found. Creating a new one.";
        file_put_contents($passwordVaultFile, '[]');
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

// Load data from the login_data.json file
$loginData = loadLoginData();

// Initialize an empty password vault
$passwordVault = array();


//Get MAC address's and passwords
$macPasswords = readPasswordsFromFile($passwordFile);
print_r($macPasswords);
// Populate the password vault based on data from localIP.json
foreach ($localIPData as $deviceName => $deviceInfo) {
    // Check if the device company exists in the login data
    $companyName = $deviceInfo['Company'];
    $IP = $deviceInfo['IP'];
    foreach ($loginData as $login) {
        if ($login['company'] === $companyName) {
            $username = $login['username'];
            $defaultPassword = $login['password'];
            break;
        }
    }
    
    // If username is not found, use "admin" as default
    if (!isset($username) || $username == "") {
        $username = 'No Username';
    }

    // Check if the password has been changed
    $passwordChanged = isset($deviceInfo['passwordChanged']) ? $deviceInfo['passwordChanged'] : false;
    
    // Check if the MAC address exists in the password file
    if (array_key_exists($deviceInfo['MAC'], $macPasswords)) {
        $password = $macPasswords[$deviceInfo['MAC']];
    }else{
        $password = "";
    }
    
    // Add the device to the password vault with retrieved username
    $passwordVault[$deviceName] = array(
        'Company' => $deviceInfo['Company'],
        'MAC' => $deviceInfo['MAC'],
        'defaultPassword' => $defaultPassword,
        'Username' => $username,
        'Password' => $password,
        'IP' => $IP, 
        'PasswordChanged' => $passwordChanged,
        'flagged' => $deviceInfo['flagged']
    );
}

// Save the password vault data
savePasswordVault($passwordVault);

echo "Password vault populated successfully.";
?>
