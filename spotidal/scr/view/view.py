import sys
from InquirerPy import prompt
from spotidal.scr.controller.controller import Controller
from spotidal.scr.model.helpers.text import Text as t

print("\n\nSpotidal2u\n")

app = Controller()

SYNC_PLAYLISTS = "sync"
DOWNLOAD_PLAYLIST = "download"
SETTINGS = "settings"
QUIT = "quit!"

MAIN_MENU = [DOWNLOAD_PLAYLIST, SYNC_PLAYLISTS, SETTINGS, QUIT]
SELECTION_MODE = ["search", "select from list", "by id", "load saved selection"]


def main_menu():
    menu = [
        {
            "type": "list",
            "message": "What do you want to do?",
            "choices": MAIN_MENU,
        }
    ]
    return prompt(menu)[0]


def playlist_selection_mode():
    q_sync = [
        {
            "type": "list",
            "message": "Which playlists?",
            "choices": SELECTION_MODE,
        }
    ]
    return prompt(q_sync)[0]


def confirm(message):
    q_confirm = [
        {
            "type": "confirm",
            "message": message,
            "name": "confirm",
            "default": True,
            "keybindings": {
                "confirm": [
                    {"key": "y"},
                    {"key": "Y"},
                    {"key": "1"},
                ],  # confirm the prompt
                "reject": [
                    {"key": "n"},
                    {"key": "N"},
                    {"key": "0"},
                ],  # reject the prompt
            },
        }
    ]
    return prompt(q_confirm)["confirm"]


def save_selection(selected_playlists):
    if confirm("Save selection?"):
        td_playlists_ids = [
            app.get_playlist_by_name(p)
            for p in selected_playlists["selected_playlists"]
        ]
        app.save_current_selection(td_playlists_ids)
        print(t.log("selection saved"))


def handle_playlist_selection(action):
    selection = playlist_selection_mode()

    if selection == "search":
        search_playlists(action)
    elif selection == "by id":
        select_by_id(action)
    elif selection == "select from list":
        selected_playlists = select_from_list(action)
        save_selection(selected_playlists)
    elif selection == "load previous selection":
        app._sync.saved_selection()


def search_playlists(action):
    playlists = app.get_playlist_names()
    while True:
        q_search = [
            {
                "type": "fuzzy",
                "message": "Search playlist",
                "name": "search_playlists",
                "choices": playlists,
                "max_height": "70%",
            }
        ]
        selected_playlist = prompt(q_search)["search_playlists"]
        app.add_to_current_selection(selected_playlist)
        print(t.display_selection(app.get_current_selection()))

        if confirm("Add more or proceed with selection?"):
            for p in app.get_current_selection():
                action(p)
            app.clear_current_selection()
            break


def select_from_list(action):
    playlists = app.get_playlist_names()
    keybindings_select_list = {
        "toggle-all-true": [{"key": "a"}],
        "toggle-all-false": [{"key": "n"}],
    }
    while True:
        q_select = [
            {
                "type": "checkbox",
                "message": "Select playlists (all = a, none = n)",
                "name": "selected_playlists",
                "choices": playlists,
            }
        ]
        selected = prompt(q_select, keybindings=keybindings_select_list)
        if selected["selected_playlists"]:
            for p in selected["selected_playlists"]:
                action(p)
            print(t.display_selection(app.get_current_selection()))
            return selected
        print(t.error("select at least one playlist"))


def select_by_id(action):
    playlist_selection = []
    while True:
        q_id = [
            {
                "type": "input",
                "name": "playlist_id",
                "message": "Spotify playlist ID to sync",
            }
        ]
        playlist_id = prompt(q_id)["playlist_id"]
        app.add_to_current_selection(playlist_id)

        print(t.display_selection(app.get_current_selection()))

        if confirm("Add more or proceed with selection?"):
            for p_id in playlist_selection:
                action(p_id)
            break


def settings_menu():
    q_settings_menu = [
        {
            "type": "list",
            "message": "Settings",
            "choices": ["Reset download settings", "Back"],
        }
    ]
    return prompt(q_settings_menu)[0]

def init():
    while True:
        try:
            action = main_menu()

            if action == SETTINGS:
                if settings_menu() == "Reset download settings" and confirm(
                    "Reset settings?"
                ):
                    app.reset_settings()

            elif action == QUIT:
                print(t.log("quitting!"))
                sys.exit()

            elif action == SYNC_PLAYLISTS:
                handle_playlist_selection(app.sync)

            elif action == DOWNLOAD_PLAYLIST:
                handle_playlist_selection(app.download)

        except KeyboardInterrupt:
            print(t.log("quitting!"))
            sys.exit()



def main():
    init()