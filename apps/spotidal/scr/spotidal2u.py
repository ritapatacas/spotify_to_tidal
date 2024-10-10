from spotify_helper import Spotify
from tidal_helper import TidalHelper
import tidal_downloader
import utils

class Spotidal2U:
    def __init__(self):
        self.spotify = Spotify()
        self.tidal = TidalHelper()
        self.settings = self.Settings(self)
        self.download = self.Download(self)
        self.fetch = self.Fetch(self)
        self.sync = self.Sync(self)

    class Settings:
        def __init__(self, parent):
            self.parent = parent

        def reset_settings(self):
            tidal_downloader.default_Settings()
            pass

        def check_tidal_login(self):
            tidal_downloader.check_login()


    class Download:
        def __init__(self, parent):
            self.parent = parent

        def check_if_playlist_exists(self, playlist_name):
            pass

        def playlist_by_sp_id(self, playlist_sp_id):
            playlist_name = self.parent.get_playlist_name_by_sp_id(playlist_sp_id)
            self.playlist_by_name(playlist_name)

        def playlist_by_name(self, playlist_name):
            playlist_td_id = self.parent.get_td_playlist_id_by_name(playlist_name)
            tidal_downloader.download_playlist(playlist_td_id)

        def playlists_by_name(self, playlist_names):
            for p in playlist_names:
                self.playlist_by_name(p)

        def selected_playlists(self):
            selected_playlists = utils.load_json('selected_playlists')
            for p in selected_playlists:
                self.playlist_by_name(p['td_id'])




    class Fetch:
        def __init__(self, parent):
            self.parent = parent

        def sp_playlists(self):
            playlists = self.parent.spotify.fetch_and_save_playlists()
            return playlists

        def td_playlists(self):
            playlists = self.parent.tidal.fetch_and_save_all_playlists()
            return playlists

        def parsed_playlists(self):
            parsed_playlists = utils.parse_and_merge_playlists()
            return parsed_playlists
        
        def all(self):
            self.sp_playlists()
            self.td_playlists()
            self.parsed_playlists()

    class Sync:
        def __init__(self, parent):
            self.parent = parent

        def by_playlist_id(self, sp_playlist_id):
            utils.sync_playlist(sp_playlist_id)

        def by_playlist_ids(self, sp_playlists_id_list):
            for p in sp_playlists_id_list:
                self.by_playlist_id(p)

        def by_playlist_name(self, playlist_name):
            sp_playlists = utils.load_json('sp_playlists')
            for p in sp_playlists:
                if p['name'] == playlist_name:
                    self.by_playlist_id(p['id'])
                    break

        def selected_playlists(self):
            selected_playlists = utils.load_json('selected_playlists')
            for p in selected_playlists:
                self.by_playlist_id(p['sp_id'])

    # Utility Methods
    def delete_tidal_playlist_by_name(self, playlist_name):
        self.tidal.delete_playlist(playlist_name)

    def save_selected_playlists(self, selected_playlists):
        utils.save_to_json('selected_playlists', selected_playlists);
    
    def get_playlist_by_name(self, playlist_name):
        playlists = utils.load_json('parsed_playlists')
        playlist = next((playlist for playlist in playlists if playlist['sp_name'] == playlist_name or playlist['td_name'] == playlist_name), None)
        return playlist

    def get_playlist_name_by_sp_id(self, playlist_sp_id):
        playlists = utils.load_json('parsed_playlists')
        playlist = next((playlist for playlist in playlists if playlist['sp_id'] == playlist_sp_id), None)
        return playlist['sp_name'] if playlist else None

    def get_td_playlist_id_by_name(self, playlist_name):
        playlists = self.fetch.parsed_playlists()
        playlist = next((playlist for playlist in playlists if playlist['td_name'] == playlist_name), None)
        return playlist['td_id'] if playlist else None

if __name__ == "__main__":
    app = Spotidal2U()
