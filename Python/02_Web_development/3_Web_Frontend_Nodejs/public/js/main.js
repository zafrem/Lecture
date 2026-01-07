// Main JavaScript file for frontend functionality

document.addEventListener('DOMContentLoaded', () => {
    console.log('Frontend JavaScript loaded successfully');
    
    // Get reference to the button and result container
    const fetchButton = document.getElementById('fetchButton');
    const apiResult = document.getElementById('apiResult');
    
    // Add event listener for the button
    fetchButton.addEventListener('click', async () => {
        try {
            apiResult.textContent = 'Loading...';
            
            // Fetch data from our API endpoint
            const response = await fetch('/api/hello');
            const data = await response.json();
            
            // Display the result
            apiResult.textContent = `API Response: ${data.message}`;
        } catch (error) {
            console.error('Error fetching API data:', error);
            apiResult.textContent = 'Error: Could not fetch data from the API';
        }
    });
});
