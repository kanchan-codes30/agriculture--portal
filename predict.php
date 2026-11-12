<?php

$N = $_POST['N'];
$P = $_POST['P'];
$K = $_POST['K'];
$temp = $_POST['temp'];
$humidity = $_POST['humidity'];
$ph = $_POST['ph'];
$rainfall = $_POST['rainfall'];

$command = "python predict.py $N $P $K $temp $humidity $ph $rainfall";

$output = shell_exec($command);

echo "<h2>Predicted Crop: $output</h2>";

?>