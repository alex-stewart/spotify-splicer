import spotipy
from argparse import ArgumentParser
from spotipy.oauth2 import SpotifyOAuth

# Parse Input
parser = ArgumentParser(description='Splice the contents of a playlist with songs from a selected genre.')
parser.add_argument('input_playlist', type=str, help='A Spotify playlist.')
parser.add_argument('genre', type=str, help='A Spotify genre.')
args = parser.parse_args()

# Create Spotify Client
scope = "user-library-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# Print Saved Tracks
results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])
