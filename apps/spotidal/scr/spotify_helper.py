import logging
import spotipy
from utils import save_to_json, load_json
from auth import open_spotify_session

class Spotify:
    def __init__(self, discover_weekly_id=None):
        self.playlists = None
        self.playlists_list = None
        self.sp_session = open_spotify_session()
        self.username = self.sp_session.me()['id']
        self._client_id = self.sp_session.auth_manager.client_id
        self._client_secret = self.sp_session.auth_manager.client_secret
        self._client_redirect_uri = self.sp_session.auth_manager.redirect_uri
        
    def fetch_playlists(self):
        self.current_user = self.sp_session.current_user()
        assert self.current_user is not None
        self.user_id = self.current_user["id"]

        print(f"> fetching spotify playlists from user {self.user_id}")
        playlists = self.sp_session.user_playlists(self.user_id)
        self.playlists = playlists
        self.playlists_list = [{"name": item["name"], "id": item["id"]} for item in playlists['items']]
        return [ self.playlists, self.playlists_list]       

    def fetch_and_save_playlists(self):
        playlists = self.fetch_playlists()
        save_to_json(playlists[0], 'user_playlists')
        save_to_json(playlists[1], 'sp_playlists')
        return playlists[1]

    @property
    def own_playlists(self):
        """All playlists of the user.

        This does not include things like 'Discover Weekly', since these are
        technically owned by Spotify, not the user.
        """
        try:
            result = self.sp_session.current_user_playlists()
            playlists = result["items"]

            while result["next"]:
                result = self.sp_session.next(result)
                playlists.extend(result["items"])
        except spotipy.client.SpotifyException:
            logging.getLogger(__name__).error("Failed to fetch playlists")
            return []

        return playlists

    @property
    def saved_artists(self):
        """List with all saved artists."""
        try:
            result = self.sp_session.current_user_followed_artists()["artists"]
            artists = result["items"]

            while result["next"]:
                result = self.sp_session.next(result)["artists"]
                artists.extend(result["items"])
        except spotipy.client.SpotifyException:
            logging.getLogger(__name__).error("Failed to fetch saved artists")
            return []

        return artists

    @property
    def saved_albums(self):
        """List with all saved albums."""
        try:
            result = self.sp_session.current_user_saved_albums()
            albums = result["items"]

            while result["next"]:
                result = self.sp_session.next(result)
                albums.extend(result["items"])
        except spotipy.client.SpotifyException:
            logging.getLogger(__name__).error("Failed to fetch saved albums")
            return []

        return albums

    @property
    def saved_tracks(self):
        """List with all saved tracks."""
        try:
            result = self.sp_session.current_user_saved_tracks()
            tracks = result["items"]

            while result["next"]:
                result = self.sp_session.next(result)
                tracks.extend(result["items"])
        except spotipy.client.SpotifyException:
            logging.getLogger(__name__).error("Failed to fetch saved tracks")
            return []

        return tracks

    @property
    def discover_weekly_playlist(self):
        """Playlist object of the 'Discover Weekly" playlist.

        Since the discover weekly is special in the sense that it isn't actually
        owned by the user, its ID has to be manually provided beforehand.
        """
        if not self._discover_weekly_id:
            raise ValueError("No discover weekly ID set")

        try:
            return self.sp_session.user_playlist(
                self.username, self._discover_weekly_id
            )
        except spotipy.client.SpotifyException:
            logging.getLogger(__name__).error("> failed to fetch Discover Weekly playlist")
            return None

    def get_selected_playlists(self):
        try:
            playlist_ids = load_json('selected_playlists.json')
            self.selected_playlists = [self.get_playlist(id) for id in playlist_ids]
            return self.selected_playlists
        except Exception as e:
            logging.getLogger(__name__).error(f"> failed to fetch selected_playlists: {e}")
            return []

    def get_playlist(self, playlist_id):
        try:
            return self.sp_session.playlist(playlist_id)
        except spotipy.client.SpotifyException:
            logging.getLogger(__name__).error("> failed to fetch playlist")

    def tracks_from_playlist(self, playlist):
        try:
            result = self.sp_session.user_playlist(
                user=playlist["owner"]["id"],
                playlist_id=playlist["id"],
                fields="tracks,next",
            )["tracks"]

            tracks = result["items"]

            while result["next"]:
                result = self.sp_session.next(result)
                tracks.extend(result["items"])
        except spotipy.client.SpotifyException:
            logging.getLogger(__name__).error("> failed to fetch tracks from playlist")
            return []

        return tracks
    
if __name__ == "__main__":
    app = Spotify()
    selected_playlist = app.get_selected_playlists()
    tracks = app.tracks_from_playlist(selected_playlist[0])
    print(tracks)