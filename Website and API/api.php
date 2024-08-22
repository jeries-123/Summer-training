<?php
header("Content-Type: application/json");

// File to store the sensor data
$data_file = 'data.json';

// Check for a POST request
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Get the JSON data from the request body
    $input = json_decode(file_get_contents('php://input'), true);

    // Validate and process the data
    if (isset($input['temperature_humidity']) && isset($input['distance']) && isset($input['bees_alive']) && isset($input['hive_open'])) {
        // Save the data to a file
        file_put_contents($data_file, json_encode($input, JSON_PRETTY_PRINT));

        $response = array(
            'status' => 'success',
            'message' => 'Data received and stored'
        );
    } else {
        $response = array(
            'status' => 'error',
            'message' => 'Invalid data'
        );
    }
} else {
    // Handle GET request to fetch data
    if (file_exists($data_file)) {
        $data = json_decode(file_get_contents($data_file), true);
        $response = array(
            'status' => 'success',
            'data' => $data
        );
    } else {
        $response = array(
            'status' => 'error',
            'message' => 'No data available'
        );
    }
}

echo json_encode($response);
?>
