<?php
chdir("..\Backend_Scripts");
$output = exec('sudo python netScan.py');
echo $output;
?>
