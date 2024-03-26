<?php
// Get the device name and IP address from the request body
$requestBody = file_get_contents('php://input');
$requestData = json_decode($requestBody, true);
$deviceMAC = isset($requestData['MAC']) ? $requestData['MAC'] : '';
$deviceIP = isset($requestData['IP']) ? $requestData['IP'] : '';
$output = shell_exec("sudo python ../Backend_Scripts/passwordReset.py $deviceIP $deviceMAC");

?>
