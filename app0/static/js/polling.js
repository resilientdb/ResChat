const receiver = JSON.parse(document.getElementById('json-receiver').textContent);

// Periodically call the update function
setInterval(update, 5000);
// Fetch new messages every 5 seconds (adjust the interval as needed)
function update() {
// Make an HTTP request to fetch new messages
    fetch('/' + receiver + '/')
}