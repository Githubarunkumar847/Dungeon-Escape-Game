// Move the player based on the input direction
function movePlayer(direction) {
    fetch('/move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ move: direction }),
    })
    .then(response => response.json())
    .then(data => {
        // Display the game status (notification)
        document.getElementById('notification').innerText = data.comment;

        // Handle game over or level-up conditions
        if (data.status === 'game_over') {
            alert('Game Over! Try Again');
            restartLevel();
        } else if (data.status === 'level_up') {
            alert('Level up! Proceeding to the next level.');
            location.reload(); // Reload to the next level
        } else {
            renderMaze(data.maze); // Dynamically update the maze
            document.getElementById('health').innerText = `Health: ${data.health}`;
        }
    });
}

// Render the maze grid dynamically
function renderMaze(maze) {
    const mazeContainer = document.getElementById('maze');
    mazeContainer.innerHTML = '';  // Clear the previous maze
    maze.forEach(row => {
        row.forEach(cell => {
            const cellDiv = document.createElement('div');
            cellDiv.className = `cell ${cell}`;
            cellDiv.textContent = cell !== '.' ? cell : '';
            mazeContainer.appendChild(cellDiv);
        });
    });
}

// Restart the current level
function restartLevel() {
    fetch('/restart', {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'restarted') {
            alert('Level restarted!');
            location.reload(); // Reload the page to restart
        }
    });
}

// Toggle the visibility of the contact developer section
function toggleContact() {
    const contactInfo = document.getElementById('contact-info');
    contactInfo.style.display = contactInfo.style.display === 'none' ? 'block' : 'none';
}

// Close the contact developer section
function closeContact() {
    const contactInfo = document.getElementById('contact-info');
    contactInfo.style.display = 'none';
}

// Send email via 'mailto'
function sendEmail() {
    const message = document.getElementById('contact-message').value;
    const subject = "Dungeon Escape - Contact Message";
    const body = encodeURIComponent(message);
    const mailtoLink = `mailto:arunjkumar847@gmail.com?subject=${subject}&body=${body}`;
    window.location.href = mailtoLink;  // Open the email client
}

// Send WhatsApp message via URL
function sendWhatsApp() {
    const message = document.getElementById('contact-message').value;
    const encodedMessage = encodeURIComponent(message);
    const whatsappLink = `https://wa.me/6301677200?text=${encodedMessage}`;
    window.open(whatsappLink, '_blank');  // Open WhatsApp
}

const musicToggle = document.getElementById("music-toggle");
const backgroundMusic = document.getElementById("background-music");

let isMusicPlaying = false;

// Toggle music on/off
musicToggle.addEventListener("click", () => {
    if (isMusicPlaying) {
        backgroundMusic.pause();
        musicToggle.textContent = "🔇";
    } else {
        backgroundMusic.play();
        musicToggle.textContent = "🔊";
    }
    isMusicPlaying = !isMusicPlaying;
});

