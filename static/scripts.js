document.getElementById('login-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const response = await fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    });
    if (response.ok) {
        document.getElementById('login-form').style.display = 'none';
        document.getElementById('generate-form').style.display = 'block';
    } else {
        alert('Login failed');
    }
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