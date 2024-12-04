document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('login-form').style.display = 'none';
    document.getElementById('dashboard').style.display = 'block';
    document.getElementById('generate-form').style.display = 'block';
});

document.getElementById('generate-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    const prompt = document.getElementById('prompt').value;
    const response = await fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prompt })
    });
    const data = await response.json();
    document.getElementById('result').innerText = data.text;
});