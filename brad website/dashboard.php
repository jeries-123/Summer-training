

 <div class="btn">
<a href="logout.php" class="button">Logout</a>
</div>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Beekeeping Dashboard</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.3/css/bootstrap.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
     <link rel="stylesheet" type="text/css" href="style.css">
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f4f4f9;
            margin: 0;
            padding: 0;
            color: #333;
        }
        .navbar {
            margin-bottom: 20px;
        }
        header {
            background: #6f2036;
            color: #fff;
            padding: 0.5rem;
            text-align: center;
        }
        header nav a {
            color: #fff;
            margin: 0 1rem;
            text-decoration: none;
        }
        .sensor-data {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 20px;
        }
        .sensor-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            background-color: #fff;
            border: 2px solid #ddd;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            width: 450px;
            height: 300px; /* Adjusted height */
        }
        .sensor-display {
            font-size: 1.5em;
            margin-bottom: 10px;
            text-align: center;
        }
        .chart-container {
            width: 100%;
            height: 400px;
        }
        .status-container{
            display: flex;
            justify-content: space-around;
            padding: 20px;
        }
        .status{
            background-color: #fff;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 20px;
            margin: 20px;
            width: 100%;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }    
        .weightstatus{
            background-color: #fff;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 20px;
            margin: 20px;
            width: 400px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
    </style>
</head>
<body>
    <header>
        <nav>
            <h2>Smart Beekeeping Dashboard</h2>
            <a href="index.html">Home</a>
            <a href="web.html">live</a>
            
        </nav>
    </header>
    <div class="container">
        <div class="sensor-data" id="stats">
            <div class="sensor-container">
                <div class="sensor-display" id="temperatureDisplay">Temperature: -- °C</div>
                <div class="chart-container">
                    <canvas id="temperatureChart"></canvas>
                </div>
            </div>
            <div class="sensor-container">
                <div class="sensor-display" id="humidityDisplay">Humidity: -- %</div>
                <div class="chart-container">
                    <canvas id="humidityChart"></canvas>
                </div>
            </div>
        </div>    
    </div>
    <div class= "status-container">
        <div class="status" id ="stats">
            <div id="bee-status">
                <h2>Bee Status</h2>
                <p id="soundDisplay">Status: --</p>
            </div>
        </div>
        <div class="status" id ="stats">
            <div id="hive-status">
                <h2>Hive Status</h2>
                <p id="lightDisplay">Status: --</p>
            </div>
        </div>
        <div class="status" id ="stats">
            <div id="distance">
                <h2>Distance Detection</h2>
                <p id="distanceDisplay">Object Distance: --</p>
            </div>
        </div>
    </div>
    
     <div class="status-container">
   
    <div class="weightstatus" id="stats">
         <h3>Hive Weight Measurements</h3>
        <div id="currentWeight">
            <h4>Current Weight</h4>
            <p id="currentWeightDisplay">Weight: --</p>
        </div>
        <div id="boxWeight">
            <h4>Box Weight</h4>
            <p id="boxWeightDisplay">Weight: --</p>
        </div>
        <div id="honeyWeight">
            <h4>Honey Weight</h4>
            <p id="honeyWeightDisplay">Weight: --</p>
        </div>
    </div>
</div>

    <script>
        const knownBoxWeight = 6.35; //weight of beehive with raspberry pi
        
        async function fetchData() {
            try {
                const response = await fetch('api.php');
                const result = await response.json();
                if (result.status === 'success') {
                    const data = result.data;

                    if (data.temperature_humidity.temperature !== undefined) {
                                            document.getElementById('temperatureDisplay').textContent = `Temperature: ${data.temperature_humidity.temperature} °C`;
                    }
                    if (data.temperature_humidity.humidity !== undefined) {
                                            document.getElementById('humidityDisplay').textContent = `Humidity: ${data.temperature_humidity.humidity} %`;
                    }
                    
                    document.getElementById('lightDisplay').textContent = `Status: ${data.hive_open ? 'Open' : 'Closed'}`;
                    
                    document.getElementById('soundDisplay').textContent = `Status: ${data.bees_alive ? 'Alive' : 'Check Hive'}`;
                    
                     // Update Weight Measurements
                     
                     // Update Box Weight
                    document.getElementById('boxWeightDisplay').textContent = `Weight: ${knownBoxWeight.toFixed(2)} kg`;
                    
                    document.getElementById('currentWeightDisplay').textContent = `Weight: ${data.weight.toFixed(2)} kg`;
                    
                    const currentWeight = data.weight;
                    const honey = currentWeight - knownBoxWeight;
                    if (honey < 0){
                        honeyWeight = 0;
                    }
                    else{
                        honeyWeight = honey;
                    }
                    
                    document.getElementById('honeyWeightDisplay').textContent = `Weight: ${honeyWeight.toFixed(2)} kg`;
                     
                     // Update distance display
                    if (data.distance < 150) {
                        document.getElementById('distanceDisplay').textContent = `Distance: Object detected at ${data.distance} cm`;
                    } else {
                        document.getElementById('distanceDisplay').textContent = `Distance: No object detected`;
                    }
                                       
                 // Update charts
                    updateChart(temperatureChart, data.temperature_humidity.temperature);
                    updateChart(humidityChart, data.temperature_humidity.humidity);

                } else {
                    console.error('Error fetching data:', result.message);
                }
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        }


        function updateChart(chart, value) {
            chart.data.datasets[0].data.push(value);
            if (chart.data.datasets[0].data.length > 20) {
                chart.data.datasets[0].data.shift(); // Maintain a maximum of 20 data points
            }
            chart.update();
        }

        // Initialize charts
        const temperatureCtx = document.getElementById('temperatureChart').getContext('2d');
        const humidityCtx = document.getElementById('humidityChart').getContext('2d');

        const temperatureChart = new Chart(temperatureCtx, {
            type: 'line',
            data: {
                labels: Array(20).fill(''),
                datasets: [{
                    label: 'Temperature (°C)',
                    data: [],
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });

        const humidityChart = new Chart(humidityCtx, {
            type: 'line',
            data: {
                labels: Array(20).fill(''),
                datasets: [{
                    label: 'Humidity (%)',
                    data: [],
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });

        // Fetch initial data and start periodic updates
        window.onload = fetchData;
        setInterval(fetchData, 0.0005); // Fetch data every 0.05 seconds
    </script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.3/js/bootstrap.bundle.min.js"></script>
</body>
</html>
