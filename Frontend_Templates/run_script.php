<?php
chdir("../Backend_Scripts");
$output = shell_exec('sudo python netScan.py');
echo $output;
?>
