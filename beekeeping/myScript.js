document.addEventListener('DOMContentLoaded', () => {
    // Placeholder: Load hive data from server
    const hiveData = document.getElementById('hiveData');
    hiveData.innerHTML = '<p>Loading data...</p>';
    
    // Fetch data from the server
    fetch('php/getHiveData.php')
        .then(response => response.json())
        .then(data => {
            // Display data
            hiveData.innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
        })
        .catch(error => {
            hiveData.innerHTML = '<p>Error loading data.</p>';
            console.error('Error fetching hive data:', error);
        });
});
