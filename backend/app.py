import os
from flask import Flask, request, jsonify, render_template
from services.spotify_api import search_spotify_track, get_spotify_access_token
from services.prompt_engineering import generate_song_suggestions

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")  # Serve the frontend

@app.route('/api/generate_playlist', methods=['POST'])
def generate_playlist():
    data = request.get_json()
    mood = data.get('mood')

    if not mood:
        return jsonify({"error": "No mood provided"}), 400

    # Get song suggestions from the LLM
    song_suggestions = generate_song_suggestions(mood)

    # Get a fresh Spotify access token 
    access_token = get_spotify_access_token()

    # Search Spotify for each song
    playlist = []
    for song in song_suggestions:
        track_info = search_spotify_track(song, access_token)
        if track_info:
            playlist.append(track_info)

    return jsonify({"mood": mood, "playlist": playlist})

@app.route('/routes', methods=['GET'])
def list_routes():
    routes = {rule.rule: list(rule.methods) for rule in app.url_map.iter_rules()}
    return jsonify(routes)



if __name__ == '__main__':
    app.run(debug=True)
