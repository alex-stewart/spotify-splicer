import json
import os
import random

import spotipy
from flask import Flask, request, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'

auth_manager = spotipy.oauth2.SpotifyOAuth(cache_path='.cache', scope='playlist-modify-public')
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


def extract_track_ids_from_playlist(playlist_config):
    playlist = sp.playlist(playlist_config['id'])
    playlist_items = playlist['tracks']['items']
    playlist_tracks = list(map(get_track_from_playlist_item, playlist_items))
    if playlist_config['shuffle']:
        random.shuffle(playlist_tracks)
    return playlist_tracks


def merge_tracks(tracks_by_source_playlist):
    tracks_by_source_playlist.sort(key=len)
    tracks = []
    shortest_playlist = len(tracks_by_source_playlist[0])
    for i in range(shortest_playlist):
        for playlist in tracks_by_source_playlist:
            tracks.append(playlist[i])
    return tracks


def add_tracks_to_playlist(username, playlist_id, track_list):
    while track_list:
        sp.user_playlist_add_tracks(username, playlist_id, track_list[:100])
        del track_list[:100]


def create_playlist_with_tracks(track_list, playlist_name):
    username = sp.current_user()['id']
    print('Creating playlist with name {} for user {}'.format(playlist_name, username))

    new_playlist_id = sp.user_playlist_create(username, 'test')['id']
    print('Created new playlist with id {}.'.format(new_playlist_id))

    add_tracks_to_playlist(username, new_playlist_id, track_list)


@app.route('/splice', methods=['POST'])
def playlists():
    record = json.loads(request.data)
    playlist_configs = record['playlists']
    print('Splice playlists {}.'.format(playlist_configs))

    source_playlist_track_ids = list(map(extract_track_ids_from_playlist, playlist_configs))
    new_playlist_track_ids = merge_tracks(source_playlist_track_ids)
    print('Creating new playlist with {} tracks.'.format(len(new_playlist_track_ids)))

    create_playlist_with_tracks(new_playlist_track_ids, record['name'])
    print('Playlist splice complete.')
    return '200'


if __name__ == '__main__':
    app.run(port=8080)
