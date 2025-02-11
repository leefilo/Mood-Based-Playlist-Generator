import requests
import base64
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET


def get_spotify_access_token():
    """
    Retrieves a Spotify access token using Client Credentials Flow
    """
    url = "https://accounts.spotify.com/api/token"

    # Encode client ID and secret for authentication
    headers = {
        "Authorization": "Basic " + base64.b64encode(
            f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}".encode()
        ).decode(),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {"grant_type": "client_credentials"}

    # Request access token
    response = requests.post(url, headers=headers, data=data)
    response_data = response.json()

    return response_data.get("access_token")  # Return token if successful, None otherwise


def search_spotify_track(query: str, access_token: str) -> dict:
    """
    Searches for a track on Spotify using a query string.
    """
    url = "https://api.spotify.com/v1/search"
    
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "q": query,
        "type": "track",
        "limit": 1,  # Only fetch the top result
        "market": "US"  # Restrict search to the US market
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        tracks = data.get("tracks", {}).get("items", [])

        if tracks:
            track = tracks[0]
            return {
                "name": track["name"],
                "artists": [artist["name"] for artist in track["artists"]],
                "spotify_url": track["external_urls"]["spotify"]
            }
    
    return {}  # No track found or request failed
