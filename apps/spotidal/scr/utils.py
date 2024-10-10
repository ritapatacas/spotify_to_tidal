import os
import json
import subprocess
import logging
import yaml


logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


usr_path = './../usr/'
sp_session = './../usr/config.yml'
td_session_yml = './../usr/session.yml'
downloader_settings_path = '~/.config/tidal_dl_ng/settings.json'

def json_path(filename):
    return usr_path + filename + '.json'



def save_to_json(data, file_name):
    save(json_path(file_name), data)
    print("> ", file_name, "saved")

def save_downloader_settings(data):
    path = os.path.expanduser(downloader_settings_path)
    os.makedirs(os.path.dirname(path), exist_ok=True)

    save(path, data)
    print("> settings saved to", path)

def load_json(file_name):
    return load(json_path(file_name))

def save_session(session_data):
    session_yml = save(td_session_yml, session_data, 'yaml')
    print("> session saved")

    return session_yml

def load_session():
    session_yml = load(td_session_yml, 'yaml')
    return session_yml

def load_credentials(credentials = 'all'):
    config_yml = load(sp_session, 'yaml')
    print(f"> {credentials} credentials loaded")

    if credentials == 'all':
        return config_yml
    elif credentials == 'sp':
        return config_yml['spotify']
    elif credentials == 'td':
        return config_yml['tidal']
    
def save(file_path, data, file_type='json'):
    try:
        with open(file_path, 'w') as f:
            if file_type == 'json':
                json.dump(data, f, indent=4)
            elif file_type == 'yaml':
                yaml.dump(data, f)
    except IOError as e:
        logging.error(f"> error saving {file_path}: {e}")

def load(file_path, file_type='json'):
    try:
        with open(file_path, 'r') as f:
            if file_type == 'json':
                data = json.load(f)
            elif file_type == 'yaml':
                data = yaml.safe_load(f)
    except FileNotFoundError:
        logging.error(f"> not found: {file_path}")
        data = {}
    except json.JSONDecodeError:
        logging.error(f"> error decoding {file_path}")
        data = {}
    return data



def parse_and_merge_playlists():
    sp_playlists = load_json('sp_playlists')
    td_playlists = load_json('td_playlists')

    print(f"Spotify playlists: {len(sp_playlists)}")
    print(f"Tidal playlists: {len(td_playlists)}")

    playlist_dict = {}

    for sp_playlist in sp_playlists:
        name = sp_playlist['name']
        playlist_dict[name] = {
            'sp_name': name,
            'sp_id': sp_playlist['id'],
            'td_name': None,
            'td_id': None
        }

    for td_playlist in td_playlists:
        name = td_playlist['name']
        if name in playlist_dict:
            playlist_dict[name]['td_name'] = name
            playlist_dict[name]['td_id'] = td_playlist['id']
        else:
            playlist_dict[name] = {
                'sp_name': None,
                'sp_id': None,
                'td_name': name,
                'td_id': td_playlist['id']
            }

    merged_playlists = list(playlist_dict.values())
    save_to_json(merged_playlists, 'parsed_playlists')
    return merged_playlists


def sync_playlist(sp_playlist_id):
    base_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'apps', 'spotify_to_tidal', 'src'))
    env = os.environ.copy()
    env['PYTHONPATH'] = base_dir
    subprocess.run(
        ["python", "-m", "spotify_to_tidal", "--uri", sp_playlist_id],
        env=env
    )
