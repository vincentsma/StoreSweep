document.getElementById('inputForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const budget = document.getElementById('budget').value;
    const categories = document.getElementById('categories').value.split(',');

    fetch('/api/solve_knapsack', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ budget: budget, categories: categories })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('results').innerHTML = JSON.stringify(data);
    })
    .catch(error => console.error('Error:', error));
});
