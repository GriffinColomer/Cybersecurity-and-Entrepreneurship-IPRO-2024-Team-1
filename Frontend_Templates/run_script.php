<?php
$output = shell_exec('python ..\Backend_Scripts\netScan.py');
echo $output;

// Source file path
$sourceFile = 'localIP.json';

// Destination file path
$destinationFile = '../Backend_Scripts/localIP.json';

// Check if the source file exists
if (file_exists($sourceFile)) {
    // Check if the destination file already exists
    if (file_exists($destinationFile)) {
        // Delete the existing destination file before moving the source file
        unlink($destinationFile);
    }

    // Move the source file to the destination location
    if (rename($sourceFile, $destinationFile)) {
        echo 'File moved successfully.';
    } else {
        echo 'Error moving file.';
    }
} else {
    echo 'Source file does not exist.';
}
?>
