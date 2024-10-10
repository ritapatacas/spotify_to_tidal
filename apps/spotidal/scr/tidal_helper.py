import os
import requests
import logging
import utils
import yaml
import json
import tidalapi
from auth import get_td_session

class TidalHelper:
    def __init__(self):
        self.td_session = get_td_session()
        logging.debug(f"tidal session {self.td_session}")
        logging.debug(f"session id {self.td_session.session_id}")
        logging.debug(f"user id {self.td_session.user.id}")

    def delete_playlist(self, playlist_name):
        user = self.td_session.user

        playlists = user.playlists()

        for p in playlists:
            if p.name == playlist_name:
                print(f"> deleting playlist: {p.name} (ID: {p.id})")
                p.delete()
                print("> playlist deleted successfully.")
    
    def get_playlist(self, playlist_id):
        playlist = tidalapi.Playlist(self.td_session, playlist_id)
        return playlist
    
    def new_playlist(self, name, description):
        search = self.find_playlist(name)
        if search is None:
            new_playlist = self.td_session.user.create_playlist(name, description)
            if new_playlist:
                print(new_playlist)
                return new_playlist.id
            else:
                return False
        else:
            return search
    
    def fetch_and_save_all_playlists(self):
        user = self.td_session.user
        playlists = user.playlists()
        playlist_data = [{'name': playlist.name, 'id': playlist.id} for playlist in playlists]

        utils.save_to_json(playlist_data, 'td_playlists')

        return playlist_data

    def find_playlist(self, name):
        playlists = utils.load_json('td_playlists.json')

        for playlist in playlists:
            if playlist['name'] == name:
                return playlist['id']
        return None

    def search_tidal(self, query, country_code='PT', types='tracks', limit=10):
        access_token = self.td_session.access_token
        search_url = 'https://api.tidal.com/v1/search'

        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        params = {
            'query': query,
            'countryCode': country_code,
            'types': types,
            'limit': limit
        }

        response = requests.get(search_url, headers=headers, params=params)
        tracks = response.json()['tracks']['items']

        for track in tracks:    
            print(
                track['title'], '\n',
                track['artists'][0]['name'], '\n',
                '   id:', track['id'], '\n',
                '   duration:', track['duration'], '\n',
                '   album:', track['album']['title'], '\n',
                '   track number:', track['trackNumber'], '\n',
                '   release date:', track['album']['releaseDate'], '\n'
            )
        
        return tracks
        

if __name__ == "__main__":
    #with open('./../usr/config.yml', 'r') as f:
    #    config = yaml.safe_load(f)
    app = TidalHelper()
