async function generatePlaylist() {
    const moodInput = document.getElementById("moodInput");
    const mood = moodInput.value;

    if (!mood) {
        alert("Please enter how you're feeling!");
        return;
    }

    
    localStorage.setItem("savedMood", mood);

    try {
        const response = await fetch("http://127.0.0.1:5000/api/generate_playlist", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ mood: mood })
        });

        const data = await response.json();
        displayPlaylist(data.playlist);

    } catch (error) {
        console.error("Error fetching playlist:", error);
        alert("Failed to generate playlist. Check the console for errors.");
    }
}


function displayPlaylist(playlist) {
    const container = document.getElementById("playlistContainer");
    container.innerHTML = "";  // Clear previous results

    if (playlist.length === 0) {
        container.innerHTML = "<p>No songs found. Try a different mood!</p>";
        return;
    }

    playlist.forEach(track => {
        const songElement = document.createElement("p");
        songElement.innerHTML = `<a href="${track.spotify_url}" target="_blank">${track.name} - ${track.artists.join(", ")}</a>`;
        container.appendChild(songElement);
    });
}

document.addEventListener("DOMContentLoaded", () => {
    const moodInput = document.getElementById("moodInput");

    // Clear the input field on page refresh
    moodInput.value = ""; 
});


window.addEventListener("beforeunload", () => {
    localStorage.removeItem("savedMood");
});

