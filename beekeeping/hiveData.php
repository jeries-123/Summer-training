<?php
// Placeholder: Return some dummy data
$data = [
    "temperature" => "35°C",
    "humidity" => "70%",
    "activity" => "Normal"
];

header('Content-Type: application/json');
echo json_encode($data);
?>
