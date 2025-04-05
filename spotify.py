from langchain_core.tools import tool
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from pydantic import BaseModel, Field
from typing import List
import re, random


scope = ["user-top-read", "user-read-recently-played", "playlist-modify-public", "playlist-modify-private"]
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

print(f"Spotify User ID: {sp.me()["id"]}")

@tool
def get_user_top_tracks(limit: int, time_range: str):
    """
    Tool for retrieving users top tracks.
    
    Args:
        limit (int): Number of top tracks to retrieve.
            - Minimum: 1
            - Maximum: 50
        time_range(str): Time period for top tracks.
            - Allowed values:
                * 'short_term': Last 4 weeks
                * 'medium_term': Last 6 months
                * 'long_term': Several years of data
    
    Returns:
        List of top tracks IDs

    Example usage:
        get_user_top_tracks(limit=10, time_range='medium_term') 

    """
    try:
        top_tracks = sp.current_user_top_tracks(
            limit=limit,
            time_range=time_range
        )
        track_ids = [track["id"] for track in top_tracks["items"]]

        return f"Top tracks: {track_ids}"
    except Exception as e:
        return f"Error getting top tracks: {str(e)}"


@tool
def create_spotify_playlist(name: str, description: str):
    """
    Tool for creating a Spotify playlist.

    Args:
        name (str): The name for the new playlist.
        description (str): The description for the new playlist.
    
    Returns:
        The URL of the created playlist.
    
    Example usage:
        create_spotify_playlist(name='My Coolest Playlist', description='My coolest tracks playlist')
    """
    try:
        user_id = sp.me()["id"]
        new_playlist = sp.user_playlist_create(
            user=user_id,
            name=name,
            description=description or '',
            public=True
        )
        return f"Playlist created successfully: {new_playlist["external_urls"]["spotify"]}"
    except Exception as e:
        return f"Error creating new playlist: {str(e)}"


@tool
def add_tracks_to_playlist(playlist_id: str, track_uris: list[str]):
    """
    Tool for adding tracks to a Spotify playlist.

    Args:
        playlist_id (str): A valid Spotify playlist ID.
        track_uris (list[str]): A list containg valid Spotify track IDs.
    
    Example usage:
        add_tracks_to_playlist(playlist_id='4sUYetgbYvsBU4e7Im5GQC', track_uris=['1WMImncoIZZ7Bz0Y6cZGVp', '2lz3zjQ5QCVXiyOzIk02vW', '0RD3NWnHlyBCRwgNZy8QAn', '3cfzDDUaIydvRN0txCJQ3f', '3QzAOrNlsabgbMwlZt7TAY'])
    """
    try:
        sp.playlist_add_items(
            playlist_id=playlist_id,
            items=track_uris,
            position=0
        )
        return f"Successfully added {len(track_uris)} tracks to the playlist."
    except Exception as e:
        return f"Error adding tracks: {str(e)}"


@tool
def get_recommendation(size: int, seeds: List[str]):
    """
    Tool for getting recommedations based on top tracks ids

    Args:
        size (int): Total number of tracks to return
            - Minimum: 1
            - Maximum: 100
        seed (list[str]): List of Track's Spotify ID.
            - Minimum: 1
            - Maximum: 5
    
    Returns:
        List of recommended Spotify track IDs
    
    Example usage:
        get_recommendation(size=10, seeds=['1WMImncoIZZ7Bz0Y6cZGVp', '2lz3zjQ5QCVXiyOzIk02vW', '0RD3NWnHlyBCRwgNZy8QAn'])
    """

    url = "https://api.reccobeats.com/v1/track/recommendation"
    payload = {}
    headers = {
        'Accept': 'application/json'
    }

    # randomly choosing any 5 seeds
    if len(seeds) >= 5:
        track_ids = random.sample(seeds, 5)

    params = {
        'size': size,
        'seeds': ",".join(track_ids)
    }
    
    try:
        response = requests.get(
            url=url,
            params=params,
            headers=headers,
            data=payload
        )
        if response.status_code == 200:
            data = response.json()
            tracks = data.get("content", [])
            tracks_urls = [track["href"] for track in tracks]
            
            pattern = r"(?<=track/)[a-zA-Z0-9]+"
            track_ids = []

            for url in tracks_urls:
                match = re.search(pattern, url)
                if match:
                    track_ids.append(match.group())

            return f"Your recommended track IDs: {track_ids}"
        else:
            return f"Request failed: {response}"
    except Exception as e:
        return f"Error getting recommendations: {str(e)}"
