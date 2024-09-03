const registrationForm = document.getElementById('registrationForm');
const guessForm = document.getElementById('guessForm');
const guessResponse = document.getElementById('guessResponse');

window.addEventListener('load', () => {
    const username = getCookie('username');
    if (username) {
        registrationForm.style.display = 'none';
        guessForm.style.display = 'block';
    }
});

// Helper function to get a cookie by name
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return false;
}


registrationForm.addEventListener('submit', (event) => {
    event.preventDefault();

    const username = document.getElementById('username').value;

    const formData = new FormData();
    formData.append('username', username);

    fetch('/register', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            alert('Username registered successfully!');
            document.cookie = `username=${username}`;
            registrationForm.style.display = 'none';
            guessForm.style.display = 'block';
        } else {
            alert('Error registering username. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again later.');
    });
});

guessForm.addEventListener('submit', (event) => {
    event.preventDefault();

    const guess = document.getElementById('guess').value;

    fetch(`/guess/${guess}`)
        .then(response => response.json()) // Assuming the server returns JSON
        .then(data => {
            if (data.success) {
                guessResponse.textContent = `Correct! You guessed it in ${data.attempts} attempts.`;
            } else {
                guessResponse.textContent = `Incorrect. You've had ${data.attempts} attempts.`;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            guessResponse.textContent = 'An error occurred. Please try again later.';
        });
});

const tabLinks = document.querySelectorAll('.tab-link');
const tabPanes = document.querySelectorAll('.tab-pane');

tabLinks.forEach(tabLink => {
    tabLink.addEventListener('click', () => {
        // Remove 'active' class from all tabs and panes
        tabLinks.forEach(link => link.classList.remove('active'));
        tabPanes.forEach(pane => pane.classList.remove('active'));

        // Add 'active' class to the clicked tab and its corresponding pane
        tabLink.classList.add('active');
        const tabPaneId = tabLink.dataset.tab;
        document.getElementById(tabPaneId).classList.add('active');
    });
});

