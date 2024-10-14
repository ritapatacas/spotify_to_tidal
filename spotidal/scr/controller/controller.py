from spotidal.scr.model.model import Model
from spotidal.scr.model.helpers.type.playlist_ref import PlaylistReference as playlist
from spotidal.scr.model.helpers.actions.settings import Settings
from spotidal.scr.model.helpers.actions.sync import Sync
from spotidal.scr.model.helpers.actions.download import Download


class Controller:
    def __init__(self):
        self._model = Model()
        self.sessions = self._model.sessions
        self._settings = Settings()
        self._sync = Sync(self.sessions)
        self._download = Download(self.sessions)

    def get_playlist_names(self):
        return self._model.get_playlist_names()

    def get_current_selection(self):
        return self._model.get_current_selection()

    def clear_current_selection(self):
        self._model.current_selection = []

    def add_to_current_selection(self, e):
        self._model.add_to_current_selection(e)

    def load_saved_selection(self):
        return self._model.get_saved_selection()

    def save_current_selection(self, selected_playlists):
        self._model.save_selection(selected_playlists)

    def sync(self, e):
        if isinstance(e, list):
            for p in e:
                self._sync.by_sp_id(playlist.get_info(p)["sp_id"])
        else:
            self._sync.by_sp_id(playlist.get_info(e)["sp_id"])

    def download(self, e, sync=True):
        if isinstance(e, list):
            for p in e:
                self._download.by_td_id(playlist.get_info(p)["td_id"])
        else:
            self._download.by_td_id(playlist.get_info(e)["td_id"])

    def reset_settings(self):
        self._settings.reset_settings()
        self._settings.check_tidal_login()


if __name__ == "__main__":
    controller = Controller()
