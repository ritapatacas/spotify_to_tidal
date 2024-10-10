from InquirerPy import prompt
from spotidal2u import Spotidal2U 
import json
import sys


print('\n\nSpotidal2u\n')
spotidal = Spotidal2U()

playlists = spotidal.fetch.sp_playlists()
playlist_names = sorted([playlist['name'] for playlist in playlists])

# we have to clean this or think, maybe i want to sync one and download other? or after sync i would ask if i wanted to download it? or maybe add this option: sync and download
selection = []
selected_playlist_names = []

def playlist_selection_mode():
    q_sync = [
        {
            "type": "list",
            "message": "Which playlists?",
            "choices": ["search", "select from list", "by id", "load previous selection"],
        }
    ]
    return prompt(q_sync)[0]
    
def select_from_list(action):
    keybindings_select_list = {
        "toggle-all-true": [
            {"key": "a"},
        ],
        "toggle-all-false": [
            {"key": "n"},
        ],
    }

    while True:
        q_select_playlists = [
            {
                "type": "checkbox",
                "message": "Select playlists (all = a, none = n)",
                "name": "selected_playlists",
                "choices": playlist_names
            }
        ]

        a_selected_playlists = prompt(
            q_select_playlists, keybindings=keybindings_select_list)

        if a_selected_playlists["selected_playlists"]:
            for p in a_selected_playlists["selected_playlists"]:
                action(p)
            return a_selected_playlists
        else:
            print("\n> No playlists selected. Please select at least one playlist.")

def select_by_id(action):
    def select_by_id_handler():
        print("> Syncing playlist by ID...")
        q_playlist_id = [
        {
            "type": "input",
            "name": "playlist_id",
            "message": "Spotify playlist ID to sync",
        }
        ]
        playlist_id = prompt(q_playlist_id)["playlist_id"]

        selection.append(playlist_id)
        selected_playlist_names.append(spotidal.get_playlist_name_by_sp_id(playlist_id))

        print("> Playlists selected: ", selected_playlist_names)
        print("> Playlist ID: ", selection)
    select_by_id_handler()
    while True:
        if confirm("Add another playlist?"):
            select_by_id_handler()
        else:
            for p_sp_id in selection:
                action(p_sp_id)
            break

def search_playlists(action):
    def search_playlists_handler():
        print("> Searching playlists...")
        q_search_playlist = [
        {
            "type": "fuzzy",
            "message": "Search playlist",
            "name": "search_playlist",
            "choices": playlist_names,
            "max_height": "70%",
            "default": None,
        }
        ]

        a_searched_playlist = prompt(q_search_playlist)    
        print(a_searched_playlist["search_playlist"])
        selection.append(a_searched_playlist["search_playlist"])

    search_playlists_handler()
    print("> Playlists selected: ", selection)
    
    while True:
        if confirm("Add another playlist?"):
            search_playlists_handler()
        else:
            for p in selection:
                action(p)
            break

def save_selection(selected_playlists):
    a_save_selection = confirm("Save selection?")

    td_playlists_ids = []
    if a_save_selection:
        for p in selected_playlists["selected_playlists"]:
            spotidal.get_playlist_by_name(p)
            td_playlists_ids.append(spotidal.get_playlist_by_name(p))

        # should be make in app
        with open('./jsons/selected_playlists.json', 'w') as f:
            json.dump(td_playlists_ids, f, indent=4)
        print("> Selection saved")

def settings_menu():
    q_settings_menu = [
            {
                "type": "list",
                "message": "Settings",
                "choices": ["Reset download settings", "Download troubleshooting", "Back"],
            }
    ]
    return prompt(q_settings_menu)[0]


def confirm(message):
    q_confirm = [
        {
            "type": "confirm",
            "message": message,
            "name": "confirm",
            "default": True,
        }
    ]
    a_confirm = prompt(q_confirm)
    return a_confirm["confirm"]

def main_menu():
    print("\n")
    menu = [
        {
            "type": "list",
            "message": "What do you want to do?",
            "choices": ["Sync playlists", "Download playlist", "Settings", "Quit"],
        }
    ]

    return prompt(menu)[0]

while True:
    try:
        action = main_menu()

        if action == "Sync playlists":
            a_sync = playlist_selection_mode()

            if a_sync == "search":
                search_playlists(spotidal.sync.by_playlist_name)

            if a_sync == "by id":
                select_by_id(spotidal.sync.by_playlist_id)

            if a_sync == "from previous selection":
                spotidal.sync.selected_playlists()

            if a_sync == "select from list":
                a_selected_playlists = select_from_list(spotidal.sync.by_playlist_name)
                save_selection(a_selected_playlists)

        if action == "Download playlist":
            a_download = playlist_selection_mode()

            if a_download == "search":
                search_playlists(spotidal.download.playlist_by_name)

            if a_download == "by id":
                select_by_id(spotidal.download.playlist_by_sp_id)

            if a_download == "from previous selection":
                spotidal.download.selected_playlists()

            if a_download == "select from list":
                a_selected_playlists = select_from_list(spotidal.download.playlist_by_name)
                save_selection(a_selected_playlists)

        if action == "Settings":
            action_settings = settings_menu()
            
            if action_settings == "Reset download settings":
                if confirm("Reset settings?"):
                    spotidal.settings.reset_settings()

            if action_settings == "Download troubleshooting":
                spotidal.settings.check_tidal_login()


        if action == "Quit":
            print("\n> Quitting!")
            sys.exit()

    except KeyboardInterrupt:
        print("\n> Quitting!")
        sys.exit()