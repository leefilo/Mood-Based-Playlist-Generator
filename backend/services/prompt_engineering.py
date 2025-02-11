import subprocess

def generate_song_suggestions(mood: str) -> list:
    prompt = f"Based on the mood '{mood}', list 5 popular songs formatted as 'Song Title - Artist Name', each on a new line."
    
    # Call Ollama 
    result = subprocess.run(
    ["C:\\Users\\leefi\\AppData\\Local\\Programs\\Ollama\\ollama.exe", "run", "mistral", prompt],
    capture_output=True,
    text=True
)

    suggestions_text = result.stdout.strip()

    # Convert output into a list of songs
    suggestions = [line.strip() for line in suggestions_text.split("\n") if line.strip()]
    return suggestions
