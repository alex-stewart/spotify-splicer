import json
import os

import spotipy
from flask import Flask, request, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'

auth_manager = spotipy.oauth2.SpotifyOAuth(cache_path='.cache')
sp = spotipy.Spotify(auth_manager=auth_manager)
print(auth_manager.get_authorize_url())


@app.route('/')
def index():
    if request.args.get('code'):
        code = request.args['code']
        auth_manager.get_access_token(code)
        return redirect('/')

    return f'{sp.me()["display_name"]}'


def get_track_from_playlist_item(item):
    return item['track']['id']


def extract_track_ids_from_playlist(playlist):
    playlist = sp.playlist(playlist)
    playlist_items = playlist['tracks']['items']
    return list(map(get_track_from_playlist_item, playlist_items))


@app.route('/splice', methods=['POST'])
def playlists():
    record = json.loads(request.data)
    playlist_ids = record['playlists']
    print('Splicing playlists {}'.format(playlist_ids))

    playlist_tracks = map(extract_track_ids_from_playlist, playlist_ids)
    print(playlist_tracks)

    return '200'


if __name__ == '__main__':
    app.run(port=8080)
